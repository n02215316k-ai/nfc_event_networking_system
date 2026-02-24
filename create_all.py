"""
NFC EVENT MANAGEMENT SYSTEM - COMPLETE AUTO INSTALLER
Save this file and run: python create_all.py
Everything will be created automatically!
"""

import os
import sys

print("=" * 70)
print("  NFC EVENT MANAGEMENT SYSTEM - COMPLETE INSTALLER")
print("=" * 70)
print("\nCreating complete project structure with all files...")
print("This may take a minute...\n")

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {filepath}")

# ============================================================================
# STEP 1: CREATE FOLDER STRUCTURE
# ============================================================================
print("\n[STEP 1/5] Creating folder structure...")

folders = [
    'database',
    'src/config',
    'src/controllers',
    'src/models',
    'src/services',
    'src/middleware',
    'templates/auth',
    'templates/events',
    'templates/scan',
    'templates/forums',
    'templates/messages',
    'templates/groups',
    'templates/users',
    'templates/admin',
    'static/uploads/profiles',
    'static/uploads/documents',
    'static/qr_codes',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("✓ All folders created!")

# ============================================================================
# STEP 2: CREATE CONFIGURATION FILES
# ============================================================================
print("\n[STEP 2/5] Creating configuration files...")

# .env file
create_file('.env', '''# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=nfc_event_management

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
FLASK_ENV=development
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
''')

# requirements.txt
create_file('requirements.txt', '''Flask==3.0.0
Flask-JWT-Extended==4.6.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
bcrypt==4.1.2
qrcode==7.4.2
Pillow==10.1.0
Werkzeug==3.0.1
''')

# README.md
create_file('README.md', '''# NFC Event Management System

A comprehensive digital identity and event management system with NFC badge integration.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup database:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

3. **Configure environment:**
   - Edit `.env` file with your database password

4. **Run the application:**
   ```bash
   python src/main.py
   ```

5. **Access the system:**
   - URL: http://localhost:5000
   - Default admin: admin@system.com / admin123

## Features

- User registration with NFC badge and QR code
- Event creation and management
- NFC/QR code attendance tracking
- Discussion forums
- Direct messaging
- Groups and networking
- Document verification system
- Admin dashboard

## Project Structure

```
nfc/
├── database/          # Database schema
├── src/              # Python source code
├── templates/        # HTML templates
├── static/           # Static files and uploads
├── .env             # Environment configuration
└── requirements.txt  # Python dependencies
```

## Support

For issues, please check the documentation or contact support.
''')

# run.bat
create_file('run.bat', '''@echo off
echo Starting NFC Event Management System...
echo.
python src/main.py
pause
''')

# run.sh
create_file('run.sh', '''#!/bin/bash
echo "Starting NFC Event Management System..."
echo
python src/main.py
''')

# ============================================================================
# STEP 3: CREATE DATABASE FILES
# ============================================================================
print("\n[STEP 3/5] Creating database files...")

create_file('database/schema.sql', '''-- NFC Event Management System Database Schema

CREATE DATABASE IF NOT EXISTS nfc_event_management;
USE nfc_event_management;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin', 'system_manager') DEFAULT 'user',
    nfc_badge_id VARCHAR(50) UNIQUE,
    qr_code VARCHAR(255),
    profile_image VARCHAR(255),
    biography TEXT,
    qualifications TEXT,
    certificates TEXT,
    current_employment VARCHAR(255),
    research_area VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_nfc_badge (nfc_badge_id)
);

-- Events table
CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    creator_id INT NOT NULL,
    max_attendees INT,
    current_attendees INT DEFAULT 0,
    category VARCHAR(100),
    status ENUM('draft', 'published', 'ongoing', 'completed', 'cancelled') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_start_date (start_date)
);

-- Attendance table
CREATE TABLE attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    check_in_time DATETIME,
    check_out_time DATETIME,
    status ENUM('registered', 'checked_in', 'checked_out') DEFAULT 'registered',
    scan_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance (event_id, user_id),
    INDEX idx_event_status (event_id, status)
);

-- Forums table
CREATE TABLE forums (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creator_id INT NOT NULL,
    event_id INT,
    member_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_event (event_id)
);

-- Forum members table
CREATE TABLE forum_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('member', 'moderator') DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (forum_id) REFERENCES forums(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_membership (forum_id, user_id)
);

-- Forum posts table
CREATE TABLE forum_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT NOT NULL,
    user_id INT NOT NULL,
    title VARCHAR(255),
    content TEXT NOT NULL,
    parent_post_id INT,
    is_pinned BOOLEAN DEFAULT FALSE,
    reply_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (forum_id) REFERENCES forums(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_post_id) REFERENCES forum_posts(id) ON DELETE CASCADE,
    INDEX idx_forum (forum_id),
    INDEX idx_parent (parent_post_id)
);

-- Messages table
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    subject VARCHAR(255),
    content TEXT NOT NULL,
    parent_message_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_message_id) REFERENCES messages(id) ON DELETE CASCADE,
    INDEX idx_receiver (receiver_id),
    INDEX idx_sender (sender_id)
);

-- Groups table
CREATE TABLE groups (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    creator_id INT NOT NULL,
    is_private BOOLEAN DEFAULT FALSE,
    member_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Group members table
CREATE TABLE group_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('member', 'admin') DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_group_membership (group_id, user_id)
);

-- Followers table
CREATE TABLE followers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_follow (follower_id, following_id)
);

-- Documents table
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    document_type ENUM('qualification', 'certificate', 'employment', 'other') NOT NULL,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    verified_by INT,
    verification_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status)
);

-- NFC Scans table
CREATE TABLE nfc_scans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scanner_id INT NOT NULL,
    scanned_id INT NOT NULL,
    event_id INT,
    scan_type ENUM('event', 'networking') NOT NULL,
    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scanned_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_scanner (scanner_id),
    INDEX idx_event (event_id)
);

-- Notifications table
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    link VARCHAR(255),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_read (user_id, is_read)
);

-- Insert default admin user (password: admin123)
INSERT INTO users (full_name, email, password_hash, role, nfc_badge_id, qr_code) VALUES
('System Administrator', 'admin@system.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7LJRY7TE6u', 'system_manager', 'NFC-ADMIN-001', 'admin_qr.png');
''')

create_file('database/sample_data.sql', '''USE nfc_event_management;

-- Sample Events
INSERT INTO events (title, description, location, start_date, end_date, creator_id, max_attendees, category, status) VALUES
('Tech Conference 2026', 'Annual technology conference featuring the latest innovations', 'Convention Center Hall A', '2026-03-15 09:00:00', '2026-03-15 18:00:00', 1, 500, 'Technology', 'published'),
('Business Networking Mixer', 'Connect with industry professionals', 'Downtown Business Hub', '2026-03-20 18:00:00', '2026-03-20 21:00:00', 1, 100, 'Business', 'published');
''')

# ============================================================================
# STEP 4: CREATE PYTHON SOURCE FILES
# ============================================================================
print("\n[STEP 4/5] Creating Python source files...")

# Database config
create_file('src/config/database.py', '''import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'nfc_event_management')
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False, fetchone=False):
        connection = self.connect()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchone() if fetchone else cursor.fetchall()
                cursor.close()
                self.disconnect()
                return result
            else:
                connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                self.disconnect()
                return last_id
        except Error as e:
            print(f"Database error: {e}")
            self.disconnect()
            return None

db = Database()
''')

# Main application
create_file('src/main.py', '''from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

jwt = JWTManager(app)

# Create upload directories
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
os.makedirs('static/qr_codes', exist_ok=True)

# Import controllers
try:
    from controllers import auth_controller, event_controller, user_controller
    from controllers import attendance_controller, forum_controller, message_controller
    from controllers import group_controller, admin_controller
    
    # Register blueprints
    app.register_blueprint(auth_controller.auth_bp, url_prefix='/auth')
    app.register_blueprint(event_controller.event_bp, url_prefix='/events')
    app.register_blueprint(user_controller.user_bp, url_prefix='/users')
    app.register_blueprint(attendance_controller.attendance_bp, url_prefix='/attendance')
    app.register_blueprint(forum_controller.forum_bp, url_prefix='/forums')
    app.register_blueprint(message_controller.message_bp, url_prefix='/messages')
    app.register_blueprint(group_controller.group_bp, url_prefix='/groups')
    app.register_blueprint(admin_controller.admin_bp, url_prefix='/admin')
except ImportError as e:
    print(f"Warning: Could not import controllers: {e}")

@app.route('/')
def index():
    if 'user_id' in session:
        from config.database import db
        
        # Get upcoming events
        events = db.execute_query("""
            SELECT e.*, u.full_name as creator_name
            FROM events e
            JOIN users u ON e.creator_id = u.id
            WHERE e.status = 'published' AND e.start_date > NOW()
            ORDER BY e.start_date ASC
            LIMIT 6
        """, fetch=True) or []
        
        return render_template('index.html', events=events)
    return render_template('index_public.html')

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return dict(current_user=session)

@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """Format datetime for templates"""
    if value is None:
        return ""
    from datetime import datetime
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    return value.strftime(format)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    
    print("=" * 60)
    print(f"  NFC Event Management System")
    print("=" * 60)
    print(f"  Running on: http://{host}:{port}")
    print(f"  Debug mode: {debug}")
    print("=" * 60)
    print()
    
    app.run(host=host, port=port, debug=debug)
''')

# Auth Controller (simplified version due to length)
create_file('src/controllers/auth_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db
import bcrypt
import qrcode
import os
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,), fetch=True, fetchone=True
        )
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            session['user_role'] = user['role']
            session['nfc_badge_id'] = user['nfc_badge_id']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email exists
        existing = db.execute_query(
            "SELECT id FROM users WHERE email = %s",
            (email,), fetch=True, fetchone=True
        )
        
        if existing:
            flash('Email already registered', 'error')
            return render_template('auth/signup.html')
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Generate NFC badge ID
        nfc_badge_id = f"NFC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Insert user
        user_id = db.execute_query("""
            INSERT INTO users (full_name, email, password_hash, nfc_badge_id)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, password_hash, nfc_badge_id))
        
        if user_id:
            # Generate QR code
            qr_filename = f"user_{user_id}_qr.png"
            qr = qrcode.make(nfc_badge_id)
            qr.save(f"static/qr_codes/{qr_filename}")
            
            db.execute_query(
                "UPDATE users SET qr_code = %s WHERE id = %s",
                (qr_filename, user_id)
            )
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Registration failed', 'error')
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (session['user_id'],), fetch=True, fetchone=True
    )
    
    # Get user's documents
    documents = db.execute_query("""
        SELECT d.*, u.full_name as verifier_name
        FROM documents d
        LEFT JOIN users u ON d.verified_by = u.id
        WHERE d.user_id = %s
        ORDER BY d.submitted_at DESC
    """, (session['user_id'],), fetch=True) or []
    
    return render_template('auth/profile.html', user=user, documents=documents)
''')

# Event Controller
create_file('src/controllers/event_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

event_bp = Blueprint('event', __name__)

@event_bp.route('/')
def list_events():
    search = request.args.get('search', '')
    status = request.args.get('status', 'published')
    
    query = """
        SELECT e.*, u.full_name as creator_name
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.status = %s
    """
    params = [status]
    
    if search:
        query += " AND (e.title LIKE %s OR e.description LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += " ORDER BY e.start_date DESC"
    
    events = db.execute_query(query, tuple(params), fetch=True) or []
    
    return render_template('events/list.html', events=events, search=search)

@event_bp.route('/<int:event_id>')
def view_event(event_id):
    event = db.execute_query("""
        SELECT e.*, u.full_name as creator_name
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.id = %s
    """, (event_id,), fetch=True, fetchone=True)
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('event.list_events'))
    
    # Get stats
    stats = db.execute_query("""
        SELECT 
            COUNT(*) as total_registered,
            SUM(CASE WHEN status = 'checked_in' THEN 1 ELSE 0 END) as currently_present,
            SUM(CASE WHEN status = 'checked_out' THEN 1 ELSE 0 END) as checked_out
        FROM attendance
        WHERE event_id = %s
    """, (event_id,), fetch=True, fetchone=True) or {'total_registered': 0, 'currently_present': 0, 'checked_out': 0}
    
    is_registered = False
    if 'user_id' in session:
        attendance = db.execute_query(
            "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
            (event_id, session['user_id']), fetch=True, fetchone=True
        )
        is_registered = attendance is not None
    
    return render_template('events/view.html', event=event, stats=stats, is_registered=is_registered)

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        max_attendees = request.form.get('max_attendees')
        category = request.form.get('category')
        status = request.form.get('status', 'draft')
        
        event_id = db.execute_query("""
            INSERT INTO events (title, description, location, start_date, end_date, 
                              creator_id, max_attendees, category, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, location, start_date, end_date, 
              session['user_id'], max_attendees or None, category, status))
        
        if event_id:
            flash('Event created successfully!', 'success')
            return redirect(url_for('event.view_event', event_id=event_id))
        
        flash('Failed to create event', 'error')
    
    return render_template('events/create.html')
''')

# User Controller
create_file('src/controllers/user_controller.py', '''from flask import Blueprint, render_template, redirect, url_for, session, flash
from config.database import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>')
def view_profile(user_id):
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,), fetch=True, fetchone=True
    )
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    
    followers_count = db.execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE following_id = %s",
        (user_id,), fetch=True, fetchone=True
    )['count']
    
    following_count = db.execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE follower_id = %s",
        (user_id,), fetch=True, fetchone=True
    )['count']
    
    is_following = False
    if 'user_id' in session:
        follow = db.execute_query(
            "SELECT * FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id), fetch=True, fetchone=True
        )
        is_following = follow is not None
    
    return render_template('users/profile.html', 
                         user=user, 
                         followers_count=followers_count,
                         following_count=following_count,
                         is_following=is_following)
''')

# Attendance Controller
create_file('src/controllers/attendance_controller.py', '''from flask import Blueprint, render_template, request, jsonify, session
from config.database import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if request.method == 'POST':
        badge_id = request.form.get('badge_id')
        scan_type = request.form.get('scan_type', 'event')
        event_id = request.form.get('event_id')
        
        # Get user by badge ID
        scanned_user = db.execute_query(
            "SELECT * FROM users WHERE nfc_badge_id = %s",
            (badge_id,), fetch=True, fetchone=True
        )
        
        if not scanned_user:
            return jsonify({'success': False, 'error': 'Invalid badge ID'})
        
        if scan_type == 'event' and event_id:
            # Check if user is registered
            attendance = db.execute_query(
                "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
                (event_id, scanned_user['id']), fetch=True, fetchone=True
            )
            
            if not attendance:
                return jsonify({'success': False, 'error': 'User not registered for this event'})
            
            # Toggle check-in/out
            if attendance['status'] == 'registered' or attendance['status'] == 'checked_out':
                db.execute_query("""
                    UPDATE attendance 
                    SET status = 'checked_in', check_in_time = %s, scan_count = scan_count + 1
                    WHERE id = %s
                """, (datetime.now(), attendance['id']))
                message = f"{scanned_user['full_name']} checked in successfully!"
            else:
                db.execute_query("""
                    UPDATE attendance 
                    SET status = 'checked_out', check_out_time = %s, scan_count = scan_count + 1
                    WHERE id = %s
                """, (datetime.now(), attendance['id']))
                message = f"{scanned_user['full_name']} checked out successfully!"
            
            return jsonify({'success': True, 'message': message})
        
        return jsonify({'success': False, 'error': 'Invalid scan type'})
    
    return render_template('scan/scanner.html')
''')

# Forum Controller
create_file('src/controllers/forum_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/')
def list_forums():
    forums = db.execute_query("""
        SELECT f.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count,
               (SELECT COUNT(*) FROM forum_posts WHERE forum_id = f.id) as post_count
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        ORDER BY f.created_at DESC
    """, fetch=True) or []
    
    return render_template('forums/list.html', forums=forums)

@forum_bp.route('/<int:forum_id>')
def view_forum(forum_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    forum = db.execute_query("""
        SELECT f.*, u.full_name as creator_name
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.id = %s
    """, (forum_id,), fetch=True, fetchone=True)
    
    if not forum:
        flash('Forum not found', 'error')
        return redirect(url_for('forum.list_forums'))
    
    is_member = db.execute_query(
        "SELECT * FROM forum_members WHERE forum_id = %s AND user_id = %s",
        (forum_id, session['user_id']), fetch=True, fetchone=True
    ) is not None
    
    posts = []
    if is_member:
        posts = db.execute_query("""
            SELECT fp.*, u.full_name as author_name, u.profile_image,
                   (SELECT COUNT(*) FROM forum_posts WHERE parent_post_id = fp.id) as reply_count
            FROM forum_posts fp
            JOIN users u ON fp.user_id = u.id
            WHERE fp.forum_id = %s AND fp.parent_post_id IS NULL
            ORDER BY fp.is_pinned DESC, fp.created_at DESC
        """, (forum_id,), fetch=True) or []
    
    return render_template('forums/view.html', forum=forum, is_member=is_member, posts=posts)
''')

# Message Controller
create_file('src/controllers/message_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

message_bp = Blueprint('message', __name__)

@message_bp.route('/inbox')
def inbox():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    messages = db.execute_query("""
        SELECT m.*, u.full_name as sender_name, u.profile_image as sender_image
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.receiver_id = %s AND m.parent_message_id IS NULL
        ORDER BY m.created_at DESC
    """, (session['user_id'],), fetch=True) or []
    
    unread_count = db.execute_query(
        "SELECT COUNT(*) as count FROM messages WHERE receiver_id = %s AND is_read = 0",
        (session['user_id'],), fetch=True, fetchone=True
    )['count']
    
    return render_template('messages/inbox.html', messages=messages, unread_count=unread_count)

@message_bp.route('/compose', methods=['GET', 'POST'])
def compose():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        receiver_id = request.form.get('receiver_id')
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        message_id = db.execute_query("""
            INSERT INTO messages (sender_id, receiver_id, subject, content)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], receiver_id, subject, content))
        
        if message_id:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.inbox'))
        
        flash('Failed to send message', 'error')
    
    return render_template('messages/compose.html')
''')

# Group Controller
create_file('src/controllers/group_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

group_bp = Blueprint('group', __name__)

@group_bp.route('/')
def list_groups():
    groups = db.execute_query("""
        SELECT g.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        ORDER BY g.created_at DESC
    """, fetch=True) or []
    
    return render_template('groups/list.html', groups=groups)

@group_bp.route('/<int:group_id>')
def view_group(group_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    group = db.execute_query("""
        SELECT g.*, u.full_name as creator_name
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.id = %s
    """, (group_id,), fetch=True, fetchone=True)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('group.list_groups'))
    
    is_member = db.execute_query(
        "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
        (group_id, session['user_id']), fetch=True, fetchone=True
    ) is not None
    
    members = db.execute_query("""
        SELECT u.*, gm.role
        FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = %s
    """, (group_id,), fetch=True) or []
    
    return render_template('groups/view.html', group=group, is_member=is_member, members=members)
''')

# Admin Controller
create_file('src/controllers/admin_controller.py', '''from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

admin_bp = Blueprint('admin', __name__)

def require_admin():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'system_manager']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    return None

@admin_bp.route('/dashboard')
def system_dashboard():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    stats = {
        'total_users': db.execute_query("SELECT COUNT(*) as count FROM users", fetch=True, fetchone=True)['count'],
        'total_events': db.execute_query("SELECT COUNT(*) as count FROM events", fetch=True, fetchone=True)['count'],
        'pending_verifications': db.execute_query("SELECT COUNT(*) as count FROM documents WHERE status = 'pending'", fetch=True, fetchone=True)['count']
    }
    
    users = db.execute_query("SELECT * FROM users ORDER BY created_at DESC LIMIT 10", fetch=True) or []
    
    return render_template('admin/dashboard.html', stats=stats, users=users)

@admin_bp.route('/users')
def manage_users():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    users = db.execute_query("SELECT * FROM users ORDER BY created_at DESC", fetch=True) or []
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/documents')
def verify_documents():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    pending_docs = db.execute_query("""
        SELECT d.*, u.full_name as user_name, u.email
        FROM documents d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.submitted_at ASC
    """, fetch=True) or []
    
    verified_docs = db.execute_query("""
        SELECT d.*, u.full_name as user_name, v.full_name as verifier_name
        FROM documents d
        JOIN users u ON d.user_id = u.id
        LEFT JOIN users v ON d.verified_by = v.id
        WHERE d.status IN ('verified', 'rejected')
        ORDER BY d.verified_at DESC
        LIMIT 20
    """, fetch=True) or []
    
    return render_template('admin/documents.html', pending_docs=pending_docs, verified_docs=verified_docs)
''')

# Placeholder files for remaining modules
placeholders = {
    'src/models/user.py': '# User Model',
    'src/models/event.py': '# Event Model',
    'src/models/attendance.py': '# Attendance Model',
    'src/models/forum.py': '# Forum Model',
    'src/models/message.py': '# Message Model',
    'src/models/group.py': '# Group Model',
    'src/models/document.py': '# Document Model',
    'src/models/nfc_scan.py': '# NFC Scan Model',
    'src/services/nfc_service.py': '# NFC Service',
    'src/services/notification_service.py': '# Notification Service',
    'src/services/statistics_service.py': '# Statistics Service',
    'src/middleware/auth_middleware.py': '# Auth Middleware',
    'src/middleware/role_middleware.py': '# Role Middleware',
}

for filepath, content in placeholders.items():
    create_file(filepath, content)

# ============================================================================
# STEP 5: CREATE HTML TEMPLATES
# ============================================================================
print("\n[STEP 5/5] Creating HTML templates...")

# Base template
create_file('templates/base.html', '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NFC Event Management{% endblock %}</title>
    <style>
        :root {
            --primary-blue: #0066cc;
            --secondary-blue: #0052a3;
            --light-blue: #e6f2ff;
            --text-dark: #333333;
            --text-light: #666666;
            --success: #28a745;
            --danger: #dc3545;
            --warning: #ffc107;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f9ff;
            color: var(--text-dark);
            line-height: 1.6;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }
        
        .nav-links a:hover {
            opacity: 0.8;
        }
        
        main {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 1rem;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--secondary-blue);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-success {
            background: var(--success);
            color: white;
        }
        
        .btn-danger {
            background: var(--danger);
            color: white;
        }
        
        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .alert {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        .alert-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .alert-error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .alert-info {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        
        .grid {
            display: grid;
            gap: 1.5rem;
        }
        
        .grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .d-flex {
            display: flex;
        }
        
        .justify-between {
            justify-content: space-between;
        }
        
        .align-center {
            align-items: center;
        }
        
        .gap-1 { gap: 0.5rem; }
        .gap-2 { gap: 1rem; }
        
        .mt-2 { margin-top: 1rem; }
        .mt-3 { margin-top: 1.5rem; }
        
        .text-center { text-align: center; }
        .text-light { color: var(--text-light); }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        table th,
        table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        table th {
            background: var(--light-blue);
            font-weight: 600;
        }
        
        footer {
            background: var(--primary-blue);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }
        
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">🎫 NFC Event Manager</a>
            <ul class="nav-links">
                {% if current_user.user_id %}
                    <li><a href="/">Home</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/forums">Forums</a></li>
                    <li><a href="/groups">Groups</a></li>
                    <li><a href="/messages/inbox">Messages</a></li>
                    <li><a href="/attendance/scan">Scan</a></li>
                    {% if current_user.user_role in ['admin', 'system_manager'] %}
                        <li><a href="/admin/dashboard">Admin</a></li>
                    {% endif %}
                    <li><a href="/auth/profile">{{ current_user.full_name }}</a></li>
                    <li><a href="/auth/logout">Logout</a></li>
                {% else %}
                    <li><a href="/">Home</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/auth/login">Login</a></li>
                    <li><a href="/auth/signup">Sign Up</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>
    
    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2026 NFC Event Management System. All rights reserved.</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
''')

# Index templates
create_file('templates/index.html', '''{% extends "base.html" %}

{% block content %}
<div class="card">
    <h1>Welcome, {{ current_user.full_name }}! 👋</h1>
    <p>Your NFC Badge ID: <strong>{{ current_user.nfc_badge_id }}</strong></p>
</div>

<div class="card">
    <h2>Upcoming Events</h2>
    {% if events %}
        <div class="grid grid-2 mt-2">
            {% for event in events %}
            <div class="card" style="background: var(--light-blue);">
                <h3 style="color: var(--primary-blue);">{{ event.title }}</h3>
                <p><strong>📅</strong> {{ event.start_date|datetime_format('%B %d, %Y') }}</p>
                <p><strong>📍</strong> {{ event.location }}</p>
                <a href="/events/{{ event.id }}" class="btn btn-primary mt-2">View Event</a>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No upcoming events</p>
    {% endif %}
</div>

<div class="grid grid-3">
    <div class="card" style="background: linear-gradient(135deg, #0066cc, #0052a3); color: white;">
        <h3>Events</h3>
        <p>Browse and register for events</p>
        <a href="/events" class="btn" style="background: white; color: var(--primary-blue);">Browse Events</a>
    </div>
    
    <div class="card" style="background: linear-gradient(135deg, #28a745, #1e7e34); color: white;">
        <h3>Forums</h3>
        <p>Join discussions and connect</p>
        <a href="/forums" class="btn" style="background: white; color: #28a745;">View Forums</a>
    </div>
    
    <div class="card" style="background: linear-gradient(135deg, #ffc107, #e0a800); color: white;">
        <h3>Scan</h3>
        <p>Check-in to events</p>
        <a href="/attendance/scan" class="btn" style="background: white; color: #ffc107;">Open Scanner</a>
    </div>
</div>
{% endblock %}
''')

create_file('templates/index_public.html', '''{% extends "base.html" %}

{% block content %}
<div class="card" style="text-align: center; padding: 4rem 2rem;">
    <h1 style="font-size: 3rem; color: var(--primary-blue); margin-bottom: 1rem;">
        🎫 NFC Event Management System
    </h1>
    <p style="font-size: 1.3rem; margin-bottom: 2rem;">
        Your Digital Identity & Event Platform
    </p>
    <div class="d-flex gap-2" style="justify-content: center;">
        <a href="/auth/signup" class="btn btn-primary" style="font-size: 1.2rem; padding: 1rem 2rem;">
            Get Started
        </a>
        <a href="/auth/login" class="btn btn-secondary" style="font-size: 1.2rem; padding: 1rem 2rem;">
            Login
        </a>
    </div>
</div>

<div class="grid grid-3 mt-3">
    <div class="card" style="text-align: center;">
        <h2>📱 Digital Identity</h2>
        <p>Get your unique NFC badge and QR code upon registration</p>
    </div>
    
    <div class="card" style="text-align: center;">
        <h2>🎉 Event Management</h2>
        <p>Create, manage, and attend events with easy check-in</p>
    </div>
    
    <div class="card" style="text-align: center;">
        <h2>🤝 Networking</h2>
        <p>Connect with attendees and build your professional network</p>
    </div>
</div>
{% endblock %}
''')

# Auth templates
create_file('templates/auth/login.html', '''{% extends "base.html" %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 2rem auto;">
    <h2 style="text-align: center; color: var(--primary-blue);">Login</h2>
    
    <form method="POST" style="margin-top: 2rem;">
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" required>
        </div>
        
        <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
    </form>
    
    <p style="text-align: center; margin-top: 1rem;">
        Don't have an account? <a href="/auth/signup">Sign up</a>
    </p>
</div>
{% endblock %}
''')

create_file('templates/auth/signup.html', '''{% extends "base.html" %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 2rem auto;">
    <h2 style="text-align: center; color: var(--primary-blue);">Sign Up</h2>
    
    <form method="POST" style="margin-top: 2rem;">
        <div class="form-group">
            <label for="full_name">Full Name</label>
            <input type="text" class="form-control" id="full_name" name="full_name" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" required minlength="6">
        </div>
        
        <button type="submit" class="btn btn-primary" style="width: 100%;">Sign Up</button>
    </form>
    
    <p style="text-align: center; margin-top: 1rem;">
        Already have an account? <a href="/auth/login">Login</a>
    </p>
</div>
{% endblock %}
''')

create_file('templates/auth/profile.html', '''{% extends "base.html" %}

{% block content %}
<div class="card">
    <h2>My Profile</h2>
    
    <div class="grid grid-2 mt-3">
        <div>
            <p><strong>Name:</strong> {{ user.full_name }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Role:</strong> {{ user.role }}</p>
            <p><strong>NFC Badge ID:</strong> {{ user.nfc_badge_id }}</p>
        </div>
        
        <div style="text-align: center;">
            {% if user.qr_code %}
                <img src="{{ url_for('static', filename='qr_codes/' + user.qr_code) }}" 
                     alt="QR Code" style="max-width: 200px;">
                <p><small>Your QR Code</small></p>
            {% endif %}
        </div>
    </div>
</div>

<div class="card">
    <h3>My Documents</h3>
    {% if documents %}
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Submitted</th>
                </tr>
            </thead>
            <tbody>
                {% for doc in documents %}
                <tr>
                    <td>{{ doc.title }}</td>
                    <td>{{ doc.document_type }}</td>
                    <td>{{ doc.status }}</td>
                    <td>{{ doc.submitted_at|datetime_format }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No documents submitted yet</p>
    {% endif %}
</div>
{% endblock %}
''')

# Event templates (simplified versions)
create_file('templates/events/list.html', '''{% extends "base.html" %}

{% block content %}
<div class="card">
    <h2>All Events</h2>
</div>

<div class="grid grid-2">
    {% for event in events %}
    <div class="card">
        <h3 style="color: var(--primary-blue);">{{ event.title }}</h3>
        <p>{{ event.description[:150] }}...</p>
        <p><strong>📅</strong> {{ event.start_date|datetime_format }}</p>
        <p><strong>📍</strong> {{ event.location }}</p>
        <a href="/events/{{ event.id }}" class="btn btn-primary">View Event</a>
    </div>
    {% else %}
    <p>No events found</p>
    {% endfor %}
</div>
{% endblock %}
''')

create_file('templates/events/view.html', '''{% extends "base.html" %}

{% block content %}
<div class="card">
    <h1>{{ event.title }}</h1>
    <p>{{ event.description }}</p>
    
    <div class="mt-3">
        <p><strong>📍 Location:</strong> {{ event.location }}</p>
        <p><strong>📅 Start:</strong> {{ event.start_date|datetime_format }}</p>
        <p><strong>📅 End:</strong> {{ event.end_date|datetime_format }}</p>
        <p><strong>👤 Organizer:</strong> {{ event.creator_name }}</p>
    </div>
    
    <div class="card mt-3" style="background: var(--light-blue);">
        <h3>Statistics</h3>
        <p><strong>Registered:</strong> {{ stats.total_registered }}</p>
        <p><strong>Present:</strong> {{ stats.currently_present }}</p>
        <p><strong>Checked Out:</strong> {{ stats.checked_out }}</p>
    </div>
</div>
{% endblock %}
''')

create_file('templates/events/create.html', '''{% extends "base.html" %}

{% block content %}
<div class="card" style="max-width: 700px; margin: 0 auto;">
    <h2>Create Event</h2>
    
    <form method="POST">
        <div class="form-group">
            <label>Title</label>
            <input type="text" class="form-control" name="title" required>
        </div>
        
        <div class="form-group">
            <label>Description</label>
            <textarea class="form-control" name="description" rows="4" required></textarea>
        </div>
        
        <div class="form-group">
            <label>Location</label>
            <input type="text" class="form-control" name="location" required>
        </div>
        
        <div class="grid grid-2">
            <div class="form-group">
                <label>Start Date</label>
                <input type="datetime-local" class="form-control" name="start_date" required>
            </div>
            
            <div class="form-group">
                <label>End Date</label>
                <input type="datetime-local" class="form-control" name="end_date" required>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">Create Event</button>
    </form>
</div>
{% endblock %}
''')

# Scanner template
create_file('templates/scan/scanner.html', '''{% extends "base.html" %}

{% block content %}
<div class="card" style="max-width: 600px; margin: 0 auto;">
    <h2 style="text-align: center;">NFC/QR Scanner</h2>
    
    <div class="form-group mt-3">
        <label>Badge ID / QR Code</label>
        <input type="text" class="form-control" id="badge_input" 
               placeholder="Scan or enter badge ID" autofocus>
    </div>
    
    <div class="form-group">
        <label>Event (optional)</label>
        <select class="form-control" id="event_id">
            <option value="">Select event...</option>
        </select>
    </div>
    
    <button onclick="performScan()" class="btn btn-primary" style="width: 100%;">Scan</button>
    
    <div id="result" class="mt-3"></div>
</div>

<script>
function performScan() {
    const badge = document.getElementById('badge_input').value;
    const event = document.getElementById('event_id').value;
    
    if (!badge) {
        alert('Please enter a badge ID');
        return;
    }
    
    const formData = new FormData();
    formData.append('badge_id', badge);
    formData.append('scan_type', 'event');
    if (event) formData.append('event_id', event);
    
    fetch('/attendance/scan', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        const result = document.getElementById('result');
        if (data.success) {
            result.innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
            document.getElementById('badge_input').value = '';
        } else {
            result.innerHTML = '<div class="alert alert-error">' + data.error + '</div>';
        }
    });
}

document.getElementById('badge_input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') performScan();
});
</script>
{% endblock %}
''')

# Create remaining template files (simplified)
template_placeholders = {
    'templates/forums/list.html': '{% extends "base.html" %}\n{% block content %}<h1>Forums</h1>{% endblock %}',
    'templates/forums/view.html': '{% extends "base.html" %}\n{% block content %}<h1>Forum</h1>{% endblock %}',
    'templates/messages/inbox.html': '{% extends "base.html" %}\n{% block content %}<h1>Inbox</h1>{% endblock %}',
    'templates/messages/compose.html': '{% extends "base.html" %}\n{% block content %}<h1>Compose</h1>{% endblock %}',
    'templates/groups/list.html': '{% extends "base.html" %}\n{% block content %}<h1>Groups</h1>{% endblock %}',
    'templates/groups/view.html': '{% extends "base.html" %}\n{% block content %}<h1>Group</h1>{% endblock %}',
    'templates/users/profile.html': '{% extends "base.html" %}\n{% block content %}<h1>User Profile</h1>{% endblock %}',
    'templates/admin/dashboard.html': '{% extends "base.html" %}\n{% block content %}<h1>Admin Dashboard</h1>{% endblock %}',
    'templates/admin/users.html': '{% extends "base.html" %}\n{% block content %}<h1>Manage Users</h1>{% endblock %}',
    'templates/admin/documents.html': '{% extends "base.html" %}\n{% block content %}<h1>Verify Documents</h1>{% endblock %}',
}

for filepath, content in template_placeholders.items():
    create_file(filepath, content)

# ============================================================================
# COMPLETION
# ============================================================================
print("\n" + "=" * 70)
print("  ✅ INSTALLATION COMPLETE!")
print("=" * 70)
print("\n📋 NEXT STEPS:\n")
print("1. Install Python dependencies:")
print("   pip install -r requirements.txt")
print()
print("2. Setup MySQL database:")
print("   mysql -u root -p < database/schema.sql")
print()
print("3. Configure environment:")
print("   Edit .env file with your database password")
print()
print("4. Run the application:")
print("   python src/main.py")
print()
print("5. Access the system:")
print("   http://localhost:5000")
print()
print("📧 Default Admin Login:")
print("   Email: admin@system.com")
print("   Password: admin123")
print()
print("=" * 70)
print("  🎉 Happy Event Managing!")
print("=" * 70)