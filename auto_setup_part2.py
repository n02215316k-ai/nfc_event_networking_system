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
# CONFIG FILES
# ============================================================================

CONFIG_INIT = """
# Config package initialization
"""

DATABASE_PY = """
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    '''Database connection manager with connection pooling'''
    
    def __init__(self):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="nfc_social_pool",
                pool_size=10,
                pool_reset_session=True,
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'nfc_event_social_network'),
                autocommit=False
            )
            print("✓ Database connection pool created")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False, fetchone=False, return_lastrowid=False):
        '''Execute a database query'''
        conn = None
        cursor = None
        
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchone() if fetchone else cursor.fetchall()
                return result
            
            conn.commit()
            
            if return_lastrowid:
                return cursor.lastrowid
            
            return True
            
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            print(f"Database Error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_many(self, query, params_list):
        '''Execute multiple queries with different parameters'''
        conn = None
        cursor = None
        
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            
            cursor.executemany(query, params_list)
            conn.commit()
            
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Database Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Create global database instance
db = Database()
"""

# ============================================================================
# MAIN APPLICATION
# ============================================================================

MAIN_PY = """
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from config.database import db
import os
from datetime import datetime

# Import all blueprints
from controllers.auth_controller import auth_bp
from controllers.event_controller import events_bp
from controllers.nfc_controller import nfc_bp
from controllers.profile_controller import profile_bp
from controllers.messaging_controller import messaging_bp
from controllers.forum_controller import forum_bp
from controllers.system_manager_controller import system_manager_bp

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'nfc-social-network-secret-change-in-production')

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
app.config['ALLOWED_EXTENSIONS'] = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,pdf,doc,docx').split(','))

# Create upload directories if they don't exist
UPLOAD_FOLDERS = [
    'static/uploads/profiles',
    'static/uploads/qualifications',
    'static/uploads/events',
    'static/uploads/forums'
]

for folder in UPLOAD_FOLDERS:
    os.makedirs(folder, exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(nfc_bp, url_prefix='/nfc')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(messaging_bp, url_prefix='/messaging')
app.register_blueprint(forum_bp, url_prefix='/forum')
app.register_blueprint(system_manager_bp, url_prefix='/system-manager')

# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    '''Format datetime objects'''
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    return value.strftime(format)

@app.template_filter('timeago')
def timeago(value):
    '''Convert datetime to "X time ago" format'''
    if not value:
        return ""
    
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    
    now = datetime.now()
    diff = now - value
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"

@app.template_filter('truncate_words')
def truncate_words(text, length=20):
    '''Truncate text to specified word count'''
    if not text:
        return ""
    words = text.split()
    if len(words) <= length:
        return text
    return ' '.join(words[:length]) + '...'

# ============================================================================
# CONTEXT PROCESSORS
# ============================================================================

@app.context_processor
def inject_user():
    '''Inject current user into all templates'''
    if 'user_id' in session:
        user = db.execute_query(
            "SELECT * FROM users WHERE id = %s",
            (session['user_id'],),
            fetch=True,
            fetchone=True
        )
        
        if user:
            # Get unread message count
            unread_count = db.execute_query(
                "SELECT COUNT(*) as count FROM messages WHERE recipient_id = %s AND is_read = FALSE",
                (session['user_id'],),
                fetch=True,
                fetchone=True
            )
            
            # Get unread notification count
            notification_count = db.execute_query(
                "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = FALSE",
                (session['user_id'],),
                fetch=True,
                fetchone=True
            )
            
            return {
                'current_user': user,
                'unread_messages': unread_count['count'] if unread_count else 0,
                'unread_notifications': notification_count['count'] if notification_count else 0
            }
    
    return {'current_user': None, 'unread_messages': 0, 'unread_notifications': 0}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def allowed_file(filename):
    '''Check if file extension is allowed'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def create_notification(user_id, notification_type, title, message, link=None):
    '''Create a notification for a user'''
    try:
        db.execute_query('''
            INSERT INTO notifications (user_id, type, title, message, link)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, notification_type, title, message, link))
        return True
    except:
        return False

# Make helper functions available to blueprints
app.allowed_file = allowed_file
app.create_notification = create_notification

# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    '''Home page'''
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (session['user_id'],),
        fetch=True,
        fetchone=True
    )
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Get upcoming events
    upcoming_events = db.execute_query('''
        SELECT e.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id AND status != 'cancelled') as registration_count
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.status = 'published' AND e.start_date > NOW()
        ORDER BY e.start_date ASC
        LIMIT 6
    ''', fetch=True) or []
    
    # Get user's registered events
    my_events = db.execute_query('''
        SELECT e.*, a.status as attendance_status, u.full_name as creator_name,
               a.check_in_time, a.check_out_time
        FROM events e
        JOIN attendance a ON e.id = a.event_id
        JOIN users u ON e.creator_id = u.id
        WHERE a.user_id = %s AND e.start_date > NOW()
        ORDER BY e.start_date ASC
        LIMIT 4
    ''', (session['user_id'],), fetch=True) or []
    
    # Get active forums
    active_forums = db.execute_query('''
        SELECT f.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count,
               (SELECT COUNT(*) FROM forum_posts WHERE forum_id = f.id) as post_count
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.is_public = TRUE
        ORDER BY f.updated_at DESC
        LIMIT 6
    ''', fetch=True) or []
    
    # Get recent notifications
    notifications = db.execute_query('''
        SELECT * FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    ''', (session['user_id'],), fetch=True) or []
    
    # Get stats for dashboard
    stats = {
        'total_events': db.execute_query(
            "SELECT COUNT(*) as count FROM events WHERE status = 'published'",
            fetch=True, fetchone=True
        )['count'],
        'my_registrations': db.execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE user_id = %s",
            (session['user_id'],), fetch=True, fetchone=True
        )['count'],
        'my_forums': db.execute_query(
            "SELECT COUNT(*) as count FROM forum_members WHERE user_id = %s",
            (session['user_id'],), fetch=True, fetchone=True
        )['count'],
        'followers': db.execute_query(
            "SELECT COUNT(*) as count FROM followers WHERE following_id = %s",
            (session['user_id'],), fetch=True, fetchone=True
        )['count'],
        'following': db.execute_query(
            "SELECT COUNT(*) as count FROM followers WHERE follower_id = %s",
            (session['user_id'],), fetch=True, fetchone=True
        )['count']
    }
    
    return render_template('home.html',
                         user=user,
                         upcoming_events=upcoming_events,
                         my_events=my_events,
                         active_forums=active_forums,
                         notifications=notifications,
                         stats=stats)

@app.route('/search')
def search():
    '''Global search functionality'''
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')
    
    results = {
        'events': [],
        'forums': [],
        'users': []
    }
    
    if query:
        search_term = f'%{query}%'
        
        # Search events
        if search_type in ['all', 'events']:
            results['events'] = db.execute_query('''
                SELECT e.*, u.full_name as creator_name,
                       (SELECT COUNT(*) FROM attendance WHERE event_id = e.id) as registration_count
                FROM events e
                JOIN users u ON e.creator_id = u.id
                WHERE (e.title LIKE %s OR e.description LIKE %s OR e.category LIKE %s OR e.location LIKE %s)
                  AND e.status = 'published'
                ORDER BY e.start_date DESC
                LIMIT 20
            ''', (search_term, search_term, search_term, search_term), fetch=True) or []
        
        # Search forums
        if search_type in ['all', 'forums']:
            results['forums'] = db.execute_query('''
                SELECT f.*, u.full_name as creator_name,
                       (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count
                FROM forums f
                JOIN users u ON f.creator_id = u.id
                WHERE (f.title LIKE %s OR f.description LIKE %s)
                  AND f.is_public = TRUE
                ORDER BY f.updated_at DESC
                LIMIT 20
            ''', (search_term, search_term), fetch=True) or []
        
        # Search users
        if search_type in ['all', 'users']:
            results['users'] = db.execute_query('''
                SELECT id, full_name, email, profile_picture, current_employment, 
                       current_research_area, role, is_verified
                FROM users
                WHERE full_name LIKE %s OR email LIKE %s OR current_employment LIKE %s 
                      OR current_research_area LIKE %s
                LIMIT 20
            ''', (search_term, search_term, search_term, search_term), fetch=True) or []
    
    return render_template('search_results.html',
                         query=query,
                         search_type=search_type,
                         results=results)

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
    
    # Mark all as read
    db.execute_query(
        "UPDATE notifications SET is_read = TRUE WHERE user_id = %s AND is_read = FALSE",
        (session['user_id'],)
    )
    
    return render_template('notifications.html', notifications=all_notifications)

@app.route('/notifications/mark-read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    '''Mark a single notification as read'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    db.execute_query(
        "UPDATE notifications SET is_read = TRUE WHERE id = %s AND user_id = %s",
        (notification_id, session['user_id'])
    )
    
    return jsonify({'success': True})

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    '''404 error handler'''
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    '''500 error handler'''
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(e):
    '''File too large error handler'''
    flash('File is too large. Maximum size is 10MB.', 'danger')
    return redirect(request.referrer or url_for('index'))

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 NFC Event & Social Network System")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

CONTROLLERS_INIT = """
# Controllers package initialization
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("📦 PART 2: Creating Source Code (Config & Main App)")
    
    print_section("Creating config files...")
    create_file('src/config/__init__.py', CONFIG_INIT)
    create_file('src/config/database.py', DATABASE_PY)
    
    print_section("Creating main application...")
    create_file('src/main.py', MAIN_PY)
    
    print_section("Creating controllers package...")
    create_file('src/controllers/__init__.py', CONTROLLERS_INIT)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 2 Complete - Config & Main App created!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 3 script to create controllers{Colors.END}")

if __name__ == '__main__':
    main()