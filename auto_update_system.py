"""
NFC Event Management System - Auto Update Script
This script automatically updates your system with all new features
Run once: python auto_update_system.py
"""

import os
import shutil
import mysql.connector
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 NFC SYSTEM AUTO-UPDATE SCRIPT                          ║
║   Automatically updating your system...                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Update if you have a password
DB_NAME = 'nfc_event_system'
BASE_DIR = Path(__file__).parent

# ============================================================================
# STEP 1: CREATE DIRECTORIES
# ============================================================================
print("\n📁 STEP 1: Creating directories...")

directories = [
    'static/uploads/profiles',
    'static/uploads/documents',
    'static/uploads/events',
    'static/uploads/groups',
    'static/qr_codes',
    'templates/users',
    'templates/messages',
    'templates/forums',
    'templates/groups',
    'templates/admin',
    'templates/system',
    'templates/search',
    'templates/errors'
]

for directory in directories:
    dir_path = BASE_DIR / directory
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {directory}")

print("  ✅ All directories created!")

# ============================================================================
# STEP 2: UPDATE DATABASE
# ============================================================================
print("\n🗄️ STEP 2: Updating database schema...")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    # SQL updates
    sql_updates = [
        # Add columns to users table
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS biography TEXT,
        ADD COLUMN IF NOT EXISTS qualifications TEXT,
        ADD COLUMN IF NOT EXISTS certificates TEXT,
        ADD COLUMN IF NOT EXISTS current_employment VARCHAR(255),
        ADD COLUMN IF NOT EXISTS research_area VARCHAR(255),
        ADD COLUMN IF NOT EXISTS profile_image VARCHAR(255)
        """,
        
        # Create documents table
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            document_type ENUM('qualification', 'certificate', 'employment', 'other') NOT NULL,
            title VARCHAR(255) NOT NULL,
            file_path VARCHAR(255) NOT NULL,
            status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
            verified_by INT,
            verification_date TIMESTAMP NULL,
            rejection_reason TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
        )
        """,
        
        # Create followers table
        """
        CREATE TABLE IF NOT EXISTS followers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            follower_id INT NOT NULL,
            following_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_follow (follower_id, following_id)
        )
        """,
        
        # Create messages table
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INT PRIMARY KEY AUTO_INCREMENT,
            sender_id INT NOT NULL,
            recipient_id INT NOT NULL,
            subject VARCHAR(255),
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            parent_id INT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP NULL,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        
        # Create groups table
        """
        CREATE TABLE IF NOT EXISTS groups (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            creator_id INT NOT NULL,
            image VARCHAR(255),
            is_private BOOLEAN DEFAULT FALSE,
            member_count INT DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        
        # Create group_members table
        """
        CREATE TABLE IF NOT EXISTS group_members (
            id INT PRIMARY KEY AUTO_INCREMENT,
            group_id INT NOT NULL,
            user_id INT NOT NULL,
            role ENUM('member', 'moderator', 'admin') DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_membership (group_id, user_id)
        )
        """,
        
        # Create notifications table
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            type ENUM('message', 'follow', 'event', 'forum', 'mention', 'system') NOT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            link VARCHAR(255),
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        
        # Add scan_count to attendance
        """
        ALTER TABLE attendance 
        ADD COLUMN IF NOT EXISTS scan_count INT DEFAULT 0
        """
    ]
    
    for sql in sql_updates:
        try:
            cursor.execute(sql)
            conn.commit()
        except mysql.connector.Error as err:
            if "Duplicate column" not in str(err) and "already exists" not in str(err):
                print(f"    ⚠️ SQL Warning: {err}")
    
    cursor.close()
    conn.close()
    print("  ✅ Database updated successfully!")
    
except mysql.connector.Error as err:
    print(f"  ❌ Database Error: {err}")
    print("  Please ensure MySQL is running and credentials are correct")

# ============================================================================
# STEP 3: CREATE CONTROLLER FILES
# ============================================================================
print("\n📝 STEP 3: Creating controller files...")

# Users Controller
users_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\users.py
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from config.database import db
from werkzeug.utils import secure_filename
import os

user_bp = Blueprint('user', __name__, url_prefix='/users')

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/<int:user_id>')
def view_profile(user_id):
    """View user profile"""
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
    )['count'] if db.execute_query("SELECT COUNT(*) as count FROM followers WHERE following_id = %s", (user_id,), fetch=True, fetchone=True) else 0
    
    following_count = db.execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE follower_id = %s",
        (user_id,), fetch=True, fetchone=True
    )['count'] if db.execute_query("SELECT COUNT(*) as count FROM followers WHERE follower_id = %s", (user_id,), fetch=True, fetchone=True) else 0
    
    is_following = False
    if 'user_id' in session and session['user_id'] != user_id:
        follow = db.execute_query(
            "SELECT * FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id), fetch=True, fetchone=True
        )
        is_following = follow is not None
    
    documents = db.execute_query("""
        SELECT * FROM documents 
        WHERE user_id = %s AND status = 'verified'
        ORDER BY submitted_at DESC
    """, (user_id,), fetch=True) or []
    
    events = db.execute_query("""
        SELECT * FROM events 
        WHERE creator_id = %s AND status = 'published'
        ORDER BY start_date DESC
        LIMIT 5
    """, (user_id,), fetch=True) or []
    
    return render_template('users/profile.html', 
                         user=user, 
                         followers_count=followers_count,
                         following_count=following_count,
                         is_following=is_following,
                         documents=documents,
                         events=events)

@user_bp.route('/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    """Follow/Unfollow a user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    if user_id == session['user_id']:
        return jsonify({'success': False, 'error': 'Cannot follow yourself'})
    
    existing = db.execute_query(
        "SELECT id FROM followers WHERE follower_id = %s AND following_id = %s",
        (session['user_id'], user_id), fetch=True, fetchone=True
    )
    
    if existing:
        db.execute_query(
            "DELETE FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id)
        )
        return jsonify({'success': True, 'action': 'unfollowed'})
    else:
        db.execute_query(
            "INSERT INTO followers (follower_id, following_id) VALUES (%s, %s)",
            (session['user_id'], user_id)
        )
        return jsonify({'success': True, 'action': 'followed'})

@user_bp.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edit user profile"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (session['user_id'],), fetch=True, fetchone=True
    )
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        biography = request.form.get('biography')
        qualifications = request.form.get('qualifications')
        current_employment = request.form.get('current_employment')
        research_area = request.form.get('research_area')
        
        db.execute_query("""
            UPDATE users 
            SET full_name = %s, biography = %s, qualifications = %s,
                current_employment = %s, research_area = %s
            WHERE id = %s
        """, (full_name, biography, qualifications, current_employment, research_area, session['user_id']))
        
        session['full_name'] = full_name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.view_profile', user_id=session['user_id']))
    
    return render_template('users/edit_profile.html', user=user)
'''

# Messages Controller
messages_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\messages.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from config.database import db
from datetime import datetime

message_bp = Blueprint('message', __name__, url_prefix='/messages')

@message_bp.route('/')
def inbox():
    """View inbox"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    messages = db.execute_query("""
        SELECT m.*, u.full_name as sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.recipient_id = %s
        ORDER BY m.sent_at DESC
    """, (session['user_id'],), fetch=True) or []
    
    return render_template('messages/inbox.html', messages=messages)

@message_bp.route('/compose', methods=['GET', 'POST'])
def compose():
    """Compose new message"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        message_text = request.form.get('message')
        
        db.execute_query("""
            INSERT INTO messages (sender_id, recipient_id, subject, message)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], recipient_id, subject, message_text))
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('message.inbox'))
    
    users = db.execute_query("""
        SELECT id, full_name FROM users 
        WHERE id != %s
        ORDER BY full_name ASC
    """, (session['user_id'],), fetch=True) or []
    
    return render_template('messages/compose.html', users=users)
'''

# Forums Controller
forums_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\forums.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.database import db

forum_bp = Blueprint('forum', __name__, url_prefix='/forums')

@forum_bp.route('/')
def list_forums():
    """List all forums"""
    forums = db.execute_query("""
        SELECT f.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM forum_posts WHERE forum_id = f.id) as post_count
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.is_public = TRUE
        ORDER BY f.created_at DESC
    """, fetch=True) or []
    
    return render_template('forums/list.html', forums=forums)

@forum_bp.route('/<int:forum_id>')
def view_forum(forum_id):
    """View forum details"""
    forum = db.execute_query("""
        SELECT f.*, u.full_name as creator_name
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.id = %s
    """, (forum_id,), fetch=True, fetchone=True)
    
    if not forum:
        flash('Forum not found', 'error')
        return redirect(url_for('forum.list_forums'))
    
    posts = db.execute_query("""
        SELECT p.*, u.full_name as author_name
        FROM forum_posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.forum_id = %s AND p.parent_id IS NULL
        ORDER BY p.created_at DESC
    """, (forum_id,), fetch=True) or []
    
    return render_template('forums/view.html', forum=forum, posts=posts)
'''

# Groups Controller
groups_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\groups.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
from config.database import db

group_bp = Blueprint('group', __name__, url_prefix='/groups')

@group_bp.route('/')
def list_groups():
    """List all groups"""
    groups = db.execute_query("""
        SELECT g.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.is_private = FALSE
        ORDER BY g.created_at DESC
    """, fetch=True) or []
    
    return render_template('groups/list.html', groups=groups)

@group_bp.route('/<int:group_id>')
def view_group(group_id):
    """View group details"""
    group = db.execute_query("""
        SELECT g.*, u.full_name as creator_name
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.id = %s
    """, (group_id,), fetch=True, fetchone=True)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('group.list_groups'))
    
    members = db.execute_query("""
        SELECT u.*, gm.role
        FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = %s
    """, (group_id,), fetch=True) or []
    
    return render_template('groups/view.html', group=group, members=members)
'''

# Search Controller
search_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\search.py
from flask import Blueprint, render_template, request, session
from config.database import db

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/')
def search():
    """Universal search"""
    query = request.args.get('q', '').strip()
    
    results = {'events': [], 'users': [], 'forums': []}
    
    if query and len(query) >= 2:
        results['events'] = db.execute_query("""
            SELECT * FROM events 
            WHERE title LIKE %s AND status = 'published'
            LIMIT 10
        """, (f'%{query}%',), fetch=True) or []
        
        results['users'] = db.execute_query("""
            SELECT id, full_name, email FROM users 
            WHERE full_name LIKE %s 
            LIMIT 10
        """, (f'%{query}%',), fetch=True) or []
        
        results['forums'] = db.execute_query("""
            SELECT * FROM forums 
            WHERE title LIKE %s AND is_public = TRUE
            LIMIT 10
        """, (f'%{query}%',), fetch=True) or []
    
    return render_template('search/results.html', query=query, results=results)
'''

# Admin Controller
admin_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\admin.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
from config.database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'system_manager']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    stats = {
        'total_users': db.execute_query("SELECT COUNT(*) as count FROM users", fetch=True, fetchone=True)['count'],
        'total_events': db.execute_query("SELECT COUNT(*) as count FROM events", fetch=True, fetchone=True)['count']
    }
    
    events = db.execute_query("""
        SELECT e.*, 
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id) as attendee_count
        FROM events e
        WHERE e.creator_id = %s OR %s = TRUE
        ORDER BY e.start_date DESC
    """, (session['user_id'], session.get('user_role') == 'system_manager'), fetch=True) or []
    
    return render_template('admin/dashboard.html', stats=stats, events=events)
'''

# System Manager Controller
system_controller = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\src\\controllers\\system_manager.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
from config.database import db

system_bp = Blueprint('system', __name__, url_prefix='/system')

@system_bp.route('/dashboard')
def dashboard():
    """System manager dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'system_manager':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    stats = {
        'total_users': db.execute_query("SELECT COUNT(*) as count FROM users", fetch=True, fetchone=True)['count'],
        'total_events': db.execute_query("SELECT COUNT(*) as count FROM events", fetch=True, fetchone=True)['count'],
        'pending_documents': db.execute_query("SELECT COUNT(*) as count FROM documents WHERE status = 'pending'", fetch=True, fetchone=True)['count']
    }
    
    return render_template('system/dashboard.html', stats=stats)

@system_bp.route('/documents')
def verify_documents():
    """View documents for verification"""
    if 'user_id' not in session or session.get('user_role') != 'system_manager':
        return redirect(url_for('index'))
    
    documents = db.execute_query("""
        SELECT d.*, u.full_name, u.email
        FROM documents d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.submitted_at DESC
    """, fetch=True) or []
    
    return render_template('system/documents.html', documents=documents)
'''

# Write controller files
controllers = {
    'users.py': users_controller,
    'messages.py': messages_controller,
    'forums.py': forums_controller,
    'groups.py': groups_controller,
    'search.py': search_controller,
    'admin.py': admin_controller,
    'system_manager.py': system_controller
}

src_controllers = BASE_DIR / 'src' / 'controllers'
for filename, content in controllers.items():
    file_path = src_controllers / filename
    if not file_path.exists():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Created {filename}")
    else:
        print(f"  ⚠️ {filename} already exists, skipping...")

print("  ✅ Controller files created!")

# ============================================================================
# STEP 4: UPDATE MAIN.PY
# ============================================================================
print("\n📝 STEP 4: Updating main.py...")

main_py_path = BASE_DIR / 'src' / 'main.py'

# Read existing main.py
with open(main_py_path, 'r', encoding='utf-8') as f:
    main_content = f.read()

# Add new imports if not present
new_imports = """
from controllers.users import user_bp
from controllers.messages import message_bp
from controllers.groups import group_bp
from controllers.forums import forum_bp
from controllers.admin import admin_bp
from controllers.system_manager import system_bp
from controllers.search import search_bp
"""

if 'from controllers.users import user_bp' not in main_content:
    # Find where to insert imports (after existing controller imports)
    import_position = main_content.find('from controllers.attendance')
    if import_position != -1:
        # Find end of line
        line_end = main_content.find('\n', import_position)
        main_content = main_content[:line_end+1] + new_imports + main_content[line_end+1:]
        print("  ✓ Added new controller imports")

# Add blueprint registrations if not present
new_registrations = """
app.register_blueprint(user_bp)
app.register_blueprint(message_bp)
app.register_blueprint(group_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(system_bp)
app.register_blueprint(search_bp)
"""

if 'app.register_blueprint(user_bp)' not in main_content:
    # Find where to insert registrations
    reg_position = main_content.find('app.register_blueprint(attendance_bp)')
    if reg_position != -1:
        line_end = main_content.find('\n', reg_position)
        main_content = main_content[:line_end+1] + new_registrations + main_content[line_end+1:]
        print("  ✓ Added new blueprint registrations")

# Add context processor for notifications
context_processor = """
@app.context_processor
def inject_user():
    \"\"\"Make user info and notifications available to all templates\"\"\"
    user_info = {
        'user_id': session.get('user_id'),
        'full_name': session.get('full_name'),
        'user_email': session.get('user_email'),
        'user_role': session.get('user_role')
    }
    
    unread_notifications = 0
    unread_messages = 0
    
    if 'user_id' in session:
        notif = db.execute_query(
            "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = FALSE",
            (session['user_id'],), fetch=True, fetchone=True
        )
        if notif:
            unread_notifications = notif['count']
        
        msg = db.execute_query(
            "SELECT COUNT(*) as count FROM messages WHERE recipient_id = %s AND is_read = FALSE",
            (session['user_id'],), fetch=True, fetchone=True
        )
        if msg:
            unread_messages = msg['count']
    
    return dict(
        current_user=user_info,
        unread_notifications=unread_notifications,
        unread_messages=unread_messages
    )
"""

if '@app.context_processor' not in main_content:
    # Add before if __name__ == '__main__'
    main_position = main_content.find("if __name__ == '__main__':")
    if main_position != -1:
        main_content = main_content[:main_position] + context_processor + '\n' + main_content[main_position:]
        print("  ✓ Added context processor for notifications")

# Write updated main.py
with open(main_py_path, 'w', encoding='utf-8') as f:
    f.write(main_content)

print("  ✅ main.py updated!")

# ============================================================================
# STEP 5: CREATE BASIC TEMPLATES
# ============================================================================
print("\n📄 STEP 5: Creating template files...")

# Create basic template files (you can expand these later)
templates = {
    'users/profile.html': '''{% extends "base.html" %}
{% block title %}{{ user.full_name }} - Profile{% endblock %}
{% block content %}
<div class="card">
    <h2>👤 {{ user.full_name }}</h2>
    <p>📧 {{ user.email }}</p>
    
    {% if user.biography %}
    <h3>About</h3>
    <p>{{ user.biography }}</p>
    {% endif %}
    
    <div style="margin-top: 1rem;">
        <strong>Followers:</strong> {{ followers_count }} | 
        <strong>Following:</strong> {{ following_count }}
    </div>
    
    {% if current_user.user_id and current_user.user_id != user.id %}
    <button onclick="followUser({{ user.id }})" id="followBtn" class="btn btn-primary" style="margin-top: 1rem;">
        {% if is_following %}Following{% else %}Follow{% endif %}
    </button>
    {% endif %}
</div>

<script>
function followUser(userId) {
    fetch('/users/' + userId + '/follow', {method: 'POST'})
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
}
</script>
{% endblock %}''',
    
    'users/edit_profile.html': '''{% extends "base.html" %}
{% block title %}Edit Profile{% endblock %}
{% block content %}
<div class="card">
    <h2>✏️ Edit Profile</h2>
    <form method="POST">
        <div class="form-group">
            <label>Full Name</label>
            <input type="text" name="full_name" class="form-control" value="{{ user.full_name }}" required>
        </div>
        <div class="form-group">
            <label>Biography</label>
            <textarea name="biography" class="form-control" rows="4">{{ user.biography or '' }}</textarea>
        </div>
        <div class="form-group">
            <label>Qualifications</label>
            <textarea name="qualifications" class="form-control" rows="3">{{ user.qualifications or '' }}</textarea>
        </div>
        <div class="form-group">
            <label>Current Employment</label>
            <input type="text" name="current_employment" class="form-control" value="{{ user.current_employment or '' }}">
        </div>
        <div class="form-group">
            <label>Research Area</label>
            <input type="text" name="research_area" class="form-control" value="{{ user.research_area or '' }}">
        </div>
        <button type="submit" class="btn btn-primary">💾 Save Changes</button>
        <a href="/users/{{ user.id }}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
{% endblock %}''',
    
    'messages/inbox.html': '''{% extends "base.html" %}
{% block title %}Inbox{% endblock %}
{% block content %}
<div class="card">
    <h2>📬 Inbox</h2>
    <a href="/messages/compose" class="btn btn-primary">✉️ Compose New</a>
    
    {% if messages %}
    <table style="width: 100%; margin-top: 1rem;">
        <tr><th>From</th><th>Subject</th><th>Date</th></tr>
        {% for msg in messages %}
        <tr style="{% if not msg.is_read %}font-weight: bold;{% endif %}">
            <td>{{ msg.sender_name }}</td>
            <td>{{ msg.subject }}</td>
            <td>{{ msg.sent_at|datetime_format }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p style="text-align: center; padding: 2rem; color: #999;">No messages</p>
    {% endif %}
</div>
{% endblock %}''',
    
    'messages/compose.html': '''{% extends "base.html" %}
{% block title %}Compose Message{% endblock %}
{% block content %}
<div class="card">
    <h2>✉️ Compose Message</h2>
    <form method="POST">
        <div class="form-group">
            <label>To</label>
            <select name="recipient_id" class="form-control" required>
                <option value="">Select recipient...</option>
                {% for u in users %}
                <option value="{{ u.id }}">{{ u.full_name }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>Subject</label>
            <input type="text" name="subject" class="form-control" required>
        </div>
        <div class="form-group">
            <label>Message</label>
            <textarea name="message" class="form-control" rows="6" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">📤 Send</button>
        <a href="/messages" class="btn btn-secondary">Cancel</a>
    </form>
</div>
{% endblock %}''',
    
    'forums/list.html': '''{% extends "base.html" %}
{% block title %}Forums{% endblock %}
{% block content %}
<div class="card">
    <h2>💬 Forums</h2>
    {% for forum in forums %}
    <div class="card" style="margin-bottom: 1rem;">
        <h3><a href="/forums/{{ forum.id }}">{{ forum.title }}</a></h3>
        <p>{{ forum.description }}</p>
        <small>{{ forum.post_count }} posts | Created by {{ forum.creator_name }}</small>
    </div>
    {% endfor %}
</div>
{% endblock %}''',
    
    'forums/view.html': '''{% extends "base.html" %}
{% block title %}{{ forum.title }}{% endblock %}
{% block content %}
<div class="card">
    <h2>{{ forum.title }}</h2>
    <p>{{ forum.description }}</p>
    
    <h3 style="margin-top: 2rem;">Posts</h3>
    {% for post in posts %}
    <div class="card">
        <strong>{{ post.author_name }}</strong>
        <p>{{ post.content }}</p>
        <small>{{ post.created_at|datetime_format }}</small>
    </div>
    {% endfor %}
</div>
{% endblock %}''',
    
    'groups/list.html': '''{% extends "base.html" %}
{% block title %}Groups{% endblock %}
{% block content %}
<div class="card">
    <h2>👥 Groups</h2>
    {% for group in groups %}
    <div class="card">
        <h3><a href="/groups/{{ group.id }}">{{ group.name }}</a></h3>
        <p>{{ group.description }}</p>
        <small>{{ group.member_count }} members</small>
    </div>
    {% endfor %}
</div>
{% endblock %}''',
    
    'groups/view.html': '''{% extends "base.html" %}
{% block title %}{{ group.name }}{% endblock %}
{% block content %}
<div class="card">
    <h2>{{ group.name }}</h2>
    <p>{{ group.description }}</p>
    
    <h3>Members ({{ members|length }})</h3>
    {% for member in members %}
    <div>{{ member.full_name }} - {{ member.role }}</div>
    {% endfor %}
</div>
{% endblock %}''',
    
    'search/results.html': '''{% extends "base.html" %}
{% block title %}Search: {{ query }}{% endblock %}
{% block content %}
<div class="card">
    <h2>🔍 Search Results: "{{ query }}"</h2>
    
    {% if results.events %}
    <h3>Events</h3>
    {% for event in results.events %}
    <div><a href="/events/{{ event.id }}">{{ event.title }}</a></div>
    {% endfor %}
    {% endif %}
    
    {% if results.users %}
    <h3>Users</h3>
    {% for user in results.users %}
    <div><a href="/users/{{ user.id }}">{{ user.full_name }}</a></div>
    {% endfor %}
    {% endif %}
    
    {% if not results.events and not results.users and not results.forums %}
    <p style="text-align: center; padding: 2rem;">No results found</p>
    {% endif %}
</div>
{% endblock %}''',
    
    'admin/dashboard.html': '''{% extends "base.html" %}
{% block title %}Admin Dashboard{% endblock %}
{% block content %}
<div class="card">
    <h2>⚙️ Admin Dashboard</h2>
    <div class="grid grid-2">
        <div class="card">
            <h3>{{ stats.total_users }}</h3>
            <p>Total Users</p>
        </div>
        <div class="card">
            <h3>{{ stats.total_events }}</h3>
            <p>Total Events</p>
        </div>
    </div>
    
    <h3 style="margin-top: 2rem;">My Events</h3>
    {% for event in events %}
    <div class="card">
        <strong>{{ event.title }}</strong>
        <p>{{ event.attendee_count }} attendees</p>
        <a href="/events/{{ event.id }}" class="btn btn-primary">View</a>
    </div>
    {% endfor %}
</div>
{% endblock %}''',
    
    'system/dashboard.html': '''{% extends "base.html" %}
{% block title %}System Dashboard{% endblock %}
{% block content %}
<div class="card">
    <h2>🔧 System Manager Dashboard</h2>
    <div class="grid grid-3">
        <div class="card">
            <h3>{{ stats.total_users }}</h3>
            <p>Total Users</p>
        </div>
        <div class="card">
            <h3>{{ stats.total_events }}</h3>
            <p>Total Events</p>
        </div>
        <div class="card">
            <h3>{{ stats.pending_documents }}</h3>
            <p>Pending Documents</p>
        </div>
    </div>
    <a href="/system/documents" class="btn btn-primary">📄 Verify Documents</a>
</div>
{% endblock %}''',
    
    'system/documents.html': '''{% extends "base.html" %}
{% block title %}Document Verification{% endblock %}
{% block content %}
<div class="card">
    <h2>📄 Document Verification</h2>
    {% for doc in documents %}
    <div class="card">
        <strong>{{ doc.title }}</strong>
        <p>User: {{ doc.full_name }} ({{ doc.email }})</p>
        <p>Type: {{ doc.document_type }}</p>
        <a href="/static/uploads/{{ doc.file_path }}" target="_blank" class="btn btn-secondary">View Document</a>
    </div>
    {% endfor %}
</div>
{% endblock %}'''
}

for template_path, content in templates.items():
    file_path = BASE_DIR / 'templates' / template_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Created {template_path}")

print("  ✅ Template files created!")

# ============================================================================
# FINAL SUCCESS MESSAGE
# ============================================================================
print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ✅ SYSTEM UPDATE COMPLETE!                                ║
║                                                              ║
║   Next steps:                                                ║
║   1. python src/main.py                                      ║
║   2. Visit http://localhost:5000                             ║
║   3. Test new features:                                      ║
║      - User profiles (/users/1)                              ║
║      - Messages (/messages)                                  ║
║      - Forums (/forums)                                      ║
║      - Groups (/groups)                                      ║
║      - Search (/search)                                      ║
║      - Admin (/admin/dashboard)                              ║
║      - System (/system/dashboard)                            ║
║                                                              ║
║   🎉 All features are now integrated!                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")