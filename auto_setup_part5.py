import os
import sys

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")

# ============================================================================
# MAIN APP.PY - COMPLETE APPLICATION
# ============================================================================

APP_PY = """
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
from config.database import db
from datetime import datetime, timedelta
import os

# Import all controllers
from src.controllers.auth_controller import auth_bp
from src.controllers.event_controller import events_bp
from src.controllers.profile_controller import profile_bp
from src.controllers.nfc_controller import nfc_bp
from src.controllers.messaging_controller import messaging_bp
from src.controllers.forum_controller import forum_bp
from src.controllers.system_manager_controller import system_manager_bp

# Import filters
from src.utils.filters import register_filters

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Ensure upload directories exist
os.makedirs('static/uploads/profiles', exist_ok=True)
os.makedirs('static/uploads/events', exist_ok=True)
os.makedirs('static/uploads/qualifications', exist_ok=True)
os.makedirs('static/uploads/forum', exist_ok=True)
os.makedirs('static/qrcodes', exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(nfc_bp, url_prefix='/nfc')
app.register_blueprint(messaging_bp, url_prefix='/messages')
app.register_blueprint(forum_bp, url_prefix='/forum')
app.register_blueprint(system_manager_bp, url_prefix='/system-manager')

# Register custom template filters
register_filters(app)

# Helper function to create notifications
def create_notification(user_id, notification_type, title, message, link=None):
    '''Create a notification for a user'''
    try:
        db.execute_query('''
            INSERT INTO notifications (user_id, notification_type, title, message, link)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, notification_type, title, message, link))
        return True
    except Exception as e:
        print(f"Error creating notification: {e}")
        return False

# Make create_notification available to the app context
app.create_notification = create_notification

# Context processor to inject common variables into all templates
@app.context_processor
def inject_common_data():
    '''Inject common data into all templates'''
    current_user = None
    unread_messages = 0
    unread_notifications = 0
    
    if 'user_id' in session:
        # Get current user data
        current_user = db.execute_query(
            "SELECT * FROM users WHERE id = %s",
            (session['user_id'],),
            fetch=True,
            fetchone=True
        )
        
        # Get unread messages count
        unread_messages_result = db.execute_query('''
            SELECT COUNT(*) as count FROM messages
            WHERE recipient_id = %s AND is_read = 0
        ''', (session['user_id'],), fetch=True, fetchone=True)
        
        unread_messages = unread_messages_result['count'] if unread_messages_result else 0
        
        # Get unread notifications count
        unread_notifications_result = db.execute_query('''
            SELECT COUNT(*) as count FROM notifications
            WHERE user_id = %s AND is_read = 0
        ''', (session['user_id'],), fetch=True, fetchone=True)
        
        unread_notifications = unread_notifications_result['count'] if unread_notifications_result else 0
    
    return dict(
        current_user=current_user,
        unread_messages=unread_messages,
        unread_notifications=unread_notifications
    )

# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    '''Home page'''
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get statistics
    stats = {
        'total_events': db.execute_query(
            "SELECT COUNT(*) as count FROM events WHERE status = 'published'",
            fetch=True, fetchone=True
        )['count'],
        
        'my_registrations': db.execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE user_id = %s",
            (session['user_id'],),
            fetch=True, fetchone=True
        )['count'],
        
        'my_forums': db.execute_query(
            "SELECT COUNT(*) as count FROM forum_members WHERE user_id = %s",
            (session['user_id'],),
            fetch=True, fetchone=True
        )['count'],
        
        'followers': db.execute_query(
            "SELECT COUNT(*) as count FROM followers WHERE following_id = %s",
            (session['user_id'],),
            fetch=True, fetchone=True
        )['count']
    }
    
    # Get user's registered events
    my_events = db.execute_query('''
        SELECT e.*, a.status as attendance_status
        FROM events e
        JOIN attendance a ON e.id = a.event_id
        WHERE a.user_id = %s AND e.end_date >= NOW()
        ORDER BY e.start_date ASC
        LIMIT 5
    ''', (session['user_id'],), fetch=True) or []
    
    # Get upcoming events (not registered)
    upcoming_events = db.execute_query('''
        SELECT e.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id) as registration_count
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.status = 'published' 
        AND e.start_date > NOW()
        AND e.id NOT IN (
            SELECT event_id FROM attendance WHERE user_id = %s
        )
        ORDER BY e.start_date ASC
        LIMIT 6
    ''', (session['user_id'],), fetch=True) or []
    
    # Get active forums
    active_forums = db.execute_query('''
        SELECT f.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count,
               (SELECT COUNT(*) FROM forum_posts WHERE forum_id = f.id) as post_count
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.is_public = 1
        ORDER BY post_count DESC
        LIMIT 5
    ''', fetch=True) or []
    
    # Get recent notifications
    notifications = db.execute_query('''
        SELECT * FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    ''', (session['user_id'],), fetch=True) or []
    
    return render_template('home.html',
                         stats=stats,
                         my_events=my_events,
                         upcoming_events=upcoming_events,
                         active_forums=active_forums,
                         notifications=notifications)

@app.route('/search')
def search():
    '''Search page'''
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    query = request.args.get('q', '').strip()
    
    results = {
        'events': [],
        'users': [],
        'forums': []
    }
    
    if query:
        # Search events
        results['events'] = db.execute_query('''
            SELECT e.*, u.full_name as creator_name
            FROM events e
            JOIN users u ON e.creator_id = u.id
            WHERE e.status = 'published' 
            AND (e.title LIKE %s OR e.description LIKE %s OR e.location LIKE %s)
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'), fetch=True) or []
        
        # Search users
        results['users'] = db.execute_query('''
            SELECT id, full_name, email, current_employment, profile_picture
            FROM users
            WHERE full_name LIKE %s OR email LIKE %s OR current_employment LIKE %s
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'), fetch=True) or []
        
        # Search forums
        results['forums'] = db.execute_query('''
            SELECT f.*, u.full_name as creator_name,
                   (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count
            FROM forums f
            JOIN users u ON f.creator_id = u.id
            WHERE f.is_public = 1 
            AND (f.title LIKE %s OR f.description LIKE %s)
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%'), fetch=True) or []
    
    return render_template('search.html', query=query, results=results)

@app.route('/notifications')
def notifications():
    '''View all notifications'''
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    all_notifications = db.execute_query('''
        SELECT * FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 50
    ''', (session['user_id'],), fetch=True) or []
    
    return render_template('notifications.html', notifications=all_notifications)

@app.route('/notifications/mark-read/<int:notif_id>', methods=['POST'])
def mark_notification_read(notif_id):
    '''Mark a notification as read'''
    if 'user_id' not in session:
        return jsonify({'success': False}), 401
    
    db.execute_query('''
        UPDATE notifications
        SET is_read = 1
        WHERE id = %s AND user_id = %s
    ''', (notif_id, session['user_id']))
    
    return jsonify({'success': True})

@app.route('/notifications/mark-all-read', methods=['POST'])
def mark_all_read():
    '''Mark all notifications as read'''
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('auth.login'))
    
    db.execute_query('''
        UPDATE notifications
        SET is_read = 1
        WHERE user_id = %s
    ''', (session['user_id'],))
    
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('notifications'))

@app.route('/about')
def about():
    '''About page'''
    return render_template('about.html')

@app.route('/help')
def help_page():
    '''Help page'''
    return render_template('help.html')

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    '''Handle 404 errors'''
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    '''Handle 500 errors'''
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    '''Handle 403 errors'''
    return render_template('errors/403.html'), 403

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename):
    '''Check if file extension is allowed'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Make allowed_file available to blueprints
app.allowed_file = allowed_file

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    # Create default system manager if not exists
    try:
        existing_admin = db.execute_query(
            "SELECT * FROM users WHERE role = 'system_manager' LIMIT 1",
            fetch=True,
            fetchone=True
        )
        
        if not existing_admin:
            from werkzeug.security import generate_password_hash
            
            db.execute_query('''
                INSERT INTO users (full_name, email, password_hash, role, is_verified)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                'System Manager',
                'admin@nfcevents.com',
                generate_password_hash('admin123'),
                'system_manager',
                1
            ))
            
            print("✅ Default system manager created!")
            print("   Email: admin@nfcevents.com")
            print("   Password: admin123")
    except Exception as e:
        print(f"Note: {e}")
    
    print("\\n" + "="*70)
    print("🚀 NFC Event & Social Network System")
    print("="*70)
    print("📱 Starting Flask application...")
    print("🌐 Access at: http://localhost:5000")
    print("="*70 + "\\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

# ============================================================================
# ERROR TEMPLATES
# ============================================================================

ERROR_404_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Page Not Found - 404{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <i class="fas fa-exclamation-triangle fa-5x text-warning mb-4"></i>
            <h1 class="display-1">404</h1>
            <h2 class="mb-4">Page Not Found</h2>
            <p class="text-muted mb-4">
                The page you are looking for doesn't exist or has been moved.
            </p>
            <a href="{{ url_for('index') }}" class="btn btn-primary">
                <i class="fas fa-home me-2"></i>Go Home
            </a>
        </div>
    </div>
</div>
{% endblock %}
"""

ERROR_500_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Server Error - 500{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <i class="fas fa-server fa-5x text-danger mb-4"></i>
            <h1 class="display-1">500</h1>
            <h2 class="mb-4">Server Error</h2>
            <p class="text-muted mb-4">
                Something went wrong on our end. Please try again later.
            </p>
            <a href="{{ url_for('index') }}" class="btn btn-primary">
                <i class="fas fa-home me-2"></i>Go Home
            </a>
        </div>
    </div>
</div>
{% endblock %}
"""

ERROR_403_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Access Denied - 403{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <i class="fas fa-ban fa-5x text-danger mb-4"></i>
            <h1 class="display-1">403</h1>
            <h2 class="mb-4">Access Denied</h2>
            <p class="text-muted mb-4">
                You don't have permission to access this resource.
            </p>
            <a href="{{ url_for('index') }}" class="btn btn-primary">
                <i class="fas fa-home me-2"></i>Go Home
            </a>
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# REQUIREMENTS.TXT
# ============================================================================

REQUIREMENTS_TXT = """
Flask==3.0.0
PyMySQL==1.1.0
python-dotenv==1.0.0
qrcode==7.4.2
Pillow==10.1.0
werkzeug==3.0.1
"""

# ============================================================================
# .ENV EXAMPLE
# ============================================================================

ENV_EXAMPLE = """
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=nfc_event_system

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=16777216

# Application Settings
APP_NAME=NFC Event & Social Network
"""

# ============================================================================
# README.MD
# ============================================================================

README_MD = """
# NFC Event & Social Network System

A comprehensive event management and social networking platform with NFC/QR code scanning capabilities.

## Features

✅ **User Authentication & Profiles**
- User registration and login
- Profile management with qualifications
- Document verification system
- Follow/unfollow users

✅ **Event Management**
- Create and manage events
- NFC/QR code check-in/check-out
- Event registration and attendance tracking
- Automatic forum creation for events

✅ **Social Networking**
- User profiles with biography
- Follow/unfollow system
- Direct messaging
- Discussion forums

✅ **Forum System**
- Create public/private forums
- Post and reply to discussions
- Forum moderators
- File attachments

✅ **NFC/QR Scanning**
- Event check-in/check-out
- Networking mode for profile viewing
- Real-time attendance tracking

✅ **System Management**
- Admin dashboard
- User management
- Event analytics
- Document verification
- System reports

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd nfc-event-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**
```bash
mysql -u root -p < config/schema.sql
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
```
http://localhost:5000
```

## Default Credentials

**System Manager:**
- Email: admin@nfcevents.com
- Password: admin123

## Project Structure

```
nfc-event-system/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   ├── database.py            # Database connection
│   └── schema.sql             # Database schema
├── src/
│   ├── controllers/           # Application controllers
│   └── utils/                 # Utility functions
├── templates/                 # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── events/
│   ├── profile/
│   ├── forum/
│   ├── messaging/
│   ├── nfc/
│   └── system_manager/
└── static/
    ├── uploads/               # User uploads
    └── qrcodes/              # Generated QR codes
```

## Technologies Used

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** Bootstrap 5, jQuery
- **Icons:** Font Awesome
- **QR Codes:** qrcode library

## License

MIT License

## Support

For support, email support@nfcevents.com
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("📦 PART 5: Creating Main Application Files")
    
    print_section("Creating app.py...")
    create_file('app.py', APP_PY)
    
    print_section("Creating error templates...")
    os.makedirs('templates/errors', exist_ok=True)
    create_file('templates/errors/404.html', ERROR_404_TEMPLATE)
    create_file('templates/errors/500.html', ERROR_500_TEMPLATE)
    create_file('templates/errors/403.html', ERROR_403_TEMPLATE)
    
    print_section("Creating requirements.txt...")
    create_file('requirements.txt', REQUIREMENTS_TXT)
    
    print_section("Creating .env.example...")
    create_file('.env.example', ENV_EXAMPLE)
    
    print_section("Creating README.md...")
    create_file('README.md', README_MD)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}🎉 PART 5 COMPLETE - APPLICATION READY!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.CYAN}📋 Files Created:{Colors.END}")
    print(f"  ✅ app.py - Main application file")
    print(f"  ✅ Error templates (404, 500, 403)")
    print(f"  ✅ requirements.txt")
    print(f"  ✅ .env.example")
    print(f"  ✅ README.md")
    
    print(f"\n{Colors.YELLOW}{'=' * 70}{Colors.END}")
    print(f"{Colors.YELLOW}📋 NEXT STEPS TO RUN THE APPLICATION:{Colors.END}")
    print(f"{Colors.YELLOW}{'=' * 70}{Colors.END}")
    print(f"\n{Colors.CYAN}1. Install dependencies:{Colors.END}")
    print(f"   pip install -r requirements.txt")
    
    print(f"\n{Colors.CYAN}2. Set up database:{Colors.END}")
    print(f"   mysql -u root -p < config/schema.sql")
    
    print(f"\n{Colors.CYAN}3. Configure environment:{Colors.END}")
    print(f"   Copy .env.example to .env and update with your database credentials")
    
    print(f"\n{Colors.CYAN}4. Run the application:{Colors.END}")
    print(f"   python app.py")
    
    print(f"\n{Colors.CYAN}5. Access the application:{Colors.END}")
    print(f"   http://localhost:5000")
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}🎉 COMPLETE PROJECT SUMMARY{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"\n✅ Database schema & configuration")
    print(f"✅ All 7 controllers (auth, events, profile, nfc, messaging, forum, system_manager)")
    print(f"✅ All templates with blue & white theme")
    print(f"✅ Main application file (app.py)")
    print(f"✅ Error handling")
    print(f"✅ Documentation (README.md)")
    
    print(f"\n{Colors.YELLOW}🚀 Your NFC Event & Social Network System is ready!{Colors.END}\n")

if __name__ == '__main__':
    main()