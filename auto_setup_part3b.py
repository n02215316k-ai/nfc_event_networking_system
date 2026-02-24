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
# MESSAGING CONTROLLER
# ============================================================================

MESSAGING_CONTROLLER = """
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from config.database import db
from datetime import datetime

messaging_bp = Blueprint('messaging', __name__)

def require_login(f):
    '''Decorator to require login'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@messaging_bp.route('/')
@require_login
def inbox():
    '''View inbox messages'''
    # Get all conversations (group by sender/recipient)
    messages = db.execute_query('''
        SELECT m.*, 
               sender.full_name as sender_name,
               sender.profile_picture as sender_picture,
               recipient.full_name as recipient_name,
               recipient.profile_picture as recipient_picture
        FROM messages m
        JOIN users sender ON m.sender_id = sender.id
        JOIN users recipient ON m.recipient_id = recipient.id
        WHERE m.recipient_id = %s OR m.sender_id = %s
        ORDER BY m.created_at DESC
    ''', (session['user_id'], session['user_id']), fetch=True) or []
    
    # Group messages by conversation partner
    conversations = {}
    for msg in messages:
        partner_id = msg['sender_id'] if msg['recipient_id'] == session['user_id'] else msg['recipient_id']
        partner_name = msg['sender_name'] if msg['recipient_id'] == session['user_id'] else msg['recipient_name']
        partner_picture = msg['sender_picture'] if msg['recipient_id'] == session['user_id'] else msg['recipient_picture']
        
        if partner_id not in conversations:
            conversations[partner_id] = {
                'partner_id': partner_id,
                'partner_name': partner_name,
                'partner_picture': partner_picture,
                'last_message': msg['message'][:50] + '...' if len(msg['message']) > 50 else msg['message'],
                'last_message_time': msg['created_at'],
                'is_read': msg['is_read'] if msg['recipient_id'] == session['user_id'] else True,
                'unread_count': 0
            }
    
    # Count unread messages per conversation
    for partner_id in conversations:
        unread = db.execute_query('''
            SELECT COUNT(*) as count FROM messages
            WHERE sender_id = %s AND recipient_id = %s AND is_read = FALSE
        ''', (partner_id, session['user_id']), fetch=True, fetchone=True)
        
        conversations[partner_id]['unread_count'] = unread['count'] if unread else 0
    
    conversations_list = sorted(conversations.values(), 
                               key=lambda x: x['last_message_time'], 
                               reverse=True)
    
    return render_template('messaging/inbox.html', conversations=conversations_list)

@messaging_bp.route('/conversation/<int:user_id>')
@require_login
def conversation(user_id):
    '''View conversation with specific user'''
    # Get conversation partner details
    partner = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )
    
    if not partner:
        flash('User not found.', 'danger')
        return redirect(url_for('messaging.inbox'))
    
    # Get all messages between current user and partner
    messages = db.execute_query('''
        SELECT m.*, 
               sender.full_name as sender_name,
               sender.profile_picture as sender_picture
        FROM messages m
        JOIN users sender ON m.sender_id = sender.id
        WHERE (m.sender_id = %s AND m.recipient_id = %s)
           OR (m.sender_id = %s AND m.recipient_id = %s)
        ORDER BY m.created_at ASC
    ''', (session['user_id'], user_id, user_id, session['user_id']), fetch=True) or []
    
    # Mark received messages as read
    db.execute_query('''
        UPDATE messages SET is_read = TRUE
        WHERE sender_id = %s AND recipient_id = %s AND is_read = FALSE
    ''', (user_id, session['user_id']))
    
    return render_template('messaging/conversation.html', 
                         partner=partner, 
                         messages=messages)

@messaging_bp.route('/send', methods=['POST'])
@require_login
def send_message():
    '''Send a message'''
    recipient_id = request.form.get('recipient_id')
    message = request.form.get('message', '').strip()
    subject = request.form.get('subject', '').strip()
    
    if not recipient_id or not message:
        flash('Please provide recipient and message.', 'danger')
        return redirect(url_for('messaging.inbox'))
    
    try:
        recipient_id = int(recipient_id)
        
        # Verify recipient exists
        recipient = db.execute_query(
            "SELECT full_name FROM users WHERE id = %s",
            (recipient_id,),
            fetch=True,
            fetchone=True
        )
        
        if not recipient:
            flash('Recipient not found.', 'danger')
            return redirect(url_for('messaging.inbox'))
        
        # Send message
        db.execute_query('''
            INSERT INTO messages (sender_id, recipient_id, subject, message)
            VALUES (%s, %s, %s, %s)
        ''', (session['user_id'], recipient_id, subject, message))
        
        # Notify recipient
        current_app.create_notification(
            recipient_id,
            'new_message',
            'New Message',
            f"{session['user_name']} sent you a message",
            url_for('messaging.conversation', user_id=session['user_id'])
        )
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messaging.conversation', user_id=recipient_id))
        
    except Exception as e:
        flash('An error occurred while sending the message.', 'danger')
        print(f"Send message error: {e}")
        return redirect(url_for('messaging.inbox'))

@messaging_bp.route('/compose')
@require_login
def compose():
    '''Compose new message'''
    # Get recipient from query string (optional)
    recipient_id = request.args.get('to')
    recipient = None
    
    if recipient_id:
        recipient = db.execute_query(
            "SELECT id, full_name FROM users WHERE id = %s",
            (recipient_id,),
            fetch=True,
            fetchone=True
        )
    
    # Get all users for recipient selection
    users = db.execute_query(
        "SELECT id, full_name FROM users WHERE id != %s ORDER BY full_name",
        (session['user_id'],),
        fetch=True
    ) or []
    
    return render_template('messaging/compose.html', users=users, recipient=recipient)

@messaging_bp.route('/delete/<int:message_id>', methods=['POST'])
@require_login
def delete_message(message_id):
    '''Delete a message'''
    # Verify ownership (can delete if sender or recipient)
    message = db.execute_query(
        "SELECT sender_id, recipient_id FROM messages WHERE id = %s",
        (message_id,),
        fetch=True,
        fetchone=True
    )
    
    if message and (message['sender_id'] == session['user_id'] or 
                   message['recipient_id'] == session['user_id']):
        db.execute_query("DELETE FROM messages WHERE id = %s", (message_id,))
        flash('Message deleted.', 'info')
    else:
        flash('You do not have permission to delete this message.', 'danger')
    
    return redirect(request.referrer or url_for('messaging.inbox'))
"""

# ============================================================================
# FORUM CONTROLLER
# ============================================================================

FORUM_CONTROLLER = """
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from config.database import db
from werkzeug.utils import secure_filename
from datetime import datetime
import os

forum_bp = Blueprint('forum', __name__)

def require_login(f):
    '''Decorator to require login'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@forum_bp.route('/')
def list_forums():
    '''List all public forums'''
    forums = db.execute_query('''
        SELECT f.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM forum_members WHERE forum_id = f.id) as member_count,
               (SELECT COUNT(*) FROM forum_posts WHERE forum_id = f.id) as post_count
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.is_public = TRUE
        ORDER BY f.updated_at DESC
    ''', fetch=True) or []
    
    # Check membership for current user
    if 'user_id' in session:
        for forum in forums:
            member = db.execute_query(
                "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s",
                (forum['id'], session['user_id']),
                fetch=True,
                fetchone=True
            )
            forum['is_member'] = member is not None
    
    return render_template('forum/list.html', forums=forums)

@forum_bp.route('/create', methods=['GET', 'POST'])
@require_login
def create_forum():
    '''Create a new forum'''
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        is_public = request.form.get('is_public') == 'on'
        
        if not title or len(title) < 5:
            flash('Forum title must be at least 5 characters.', 'danger')
            return render_template('forum/create.html')
        
        try:
            forum_id = db.execute_query('''
                INSERT INTO forums (title, description, creator_id, is_public)
                VALUES (%s, %s, %s, %s)
            ''', (title, description, session['user_id'], is_public), return_lastrowid=True)
            
            # Add creator as admin
            db.execute_query('''
                INSERT INTO forum_members (forum_id, user_id, role)
                VALUES (%s, %s, 'admin')
            ''', (forum_id, session['user_id']))
            
            flash('Forum created successfully!', 'success')
            return redirect(url_for('forum.view', forum_id=forum_id))
            
        except Exception as e:
            flash('An error occurred while creating the forum.', 'danger')
            print(f"Forum creation error: {e}")
    
    return render_template('forum/create.html')

@forum_bp.route('/<int:forum_id>')
def view(forum_id):
    '''View forum and its posts'''
    forum = db.execute_query('''
        SELECT f.*, u.full_name as creator_name
        FROM forums f
        JOIN users u ON f.creator_id = u.id
        WHERE f.id = %s
    ''', (forum_id,), fetch=True, fetchone=True)
    
    if not forum:
        flash('Forum not found.', 'danger')
        return redirect(url_for('forum.list_forums'))
    
    # Check if user is member
    is_member = False
    user_role = None
    
    if 'user_id' in session:
        member = db.execute_query(
            "SELECT role FROM forum_members WHERE forum_id = %s AND user_id = %s",
            (forum_id, session['user_id']),
            fetch=True,
            fetchone=True
        )
        is_member = member is not None
        user_role = member['role'] if member else None
    
    # If private forum and not a member, deny access
    if not forum['is_public'] and not is_member:
        flash('This is a private forum.', 'danger')
        return redirect(url_for('forum.list_forums'))
    
    # Get posts (top-level only)
    posts = db.execute_query('''
        SELECT p.*, u.full_name as author_name, u.profile_picture as author_picture,
               (SELECT COUNT(*) FROM forum_posts WHERE parent_post_id = p.id) as reply_count
        FROM forum_posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.forum_id = %s AND p.parent_post_id IS NULL
        ORDER BY p.created_at DESC
    ''', (forum_id,), fetch=True) or []
    
    # Get member count
    member_count = db.execute_query(
        "SELECT COUNT(*) as count FROM forum_members WHERE forum_id = %s",
        (forum_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    # Get moderators
    moderators = db.execute_query('''
        SELECT u.id, u.full_name, u.profile_picture, fm.role
        FROM forum_members fm
        JOIN users u ON fm.user_id = u.id
        WHERE fm.forum_id = %s AND fm.role IN ('admin', 'moderator')
    ''', (forum_id,), fetch=True) or []
    
    return render_template('forum/view.html',
                         forum=forum,
                         posts=posts,
                         is_member=is_member,
                         user_role=user_role,
                         member_count=member_count,
                         moderators=moderators)

@forum_bp.route('/<int:forum_id>/join', methods=['POST'])
@require_login
def join(forum_id):
    '''Join a forum'''
    # Verify forum exists and is public
    forum = db.execute_query(
        "SELECT is_public, title FROM forums WHERE id = %s",
        (forum_id,),
        fetch=True,
        fetchone=True
    )
    
    if not forum:
        return jsonify({'success': False, 'message': 'Forum not found'}), 404
    
    if not forum['is_public']:
        return jsonify({'success': False, 'message': 'This is a private forum'}), 403
    
    # Check if already member
    existing = db.execute_query(
        "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s",
        (forum_id, session['user_id']),
        fetch=True,
        fetchone=True
    )
    
    if existing:
        return jsonify({'success': False, 'message': 'Already a member'}), 400
    
    try:
        db.execute_query('''
            INSERT INTO forum_members (forum_id, user_id, role)
            VALUES (%s, %s, 'member')
        ''', (forum_id, session['user_id']))
        
        return jsonify({'success': True, 'message': 'Joined forum successfully'})
        
    except Exception as e:
        print(f"Join forum error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@forum_bp.route('/<int:forum_id>/leave', methods=['POST'])
@require_login
def leave(forum_id):
    '''Leave a forum'''
    try:
        db.execute_query(
            "DELETE FROM forum_members WHERE forum_id = %s AND user_id = %s",
            (forum_id, session['user_id'])
        )
        
        flash('You have left the forum.', 'info')
        return redirect(url_for('forum.list_forums'))
        
    except Exception as e:
        flash('An error occurred.', 'danger')
        print(f"Leave forum error: {e}")
        return redirect(url_for('forum.view', forum_id=forum_id))

@forum_bp.route('/<int:forum_id>/post', methods=['POST'])
@require_login
def create_post(forum_id):
    '''Create a new post in forum'''
    # Check membership
    member = db.execute_query(
        "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s",
        (forum_id, session['user_id']),
        fetch=True,
        fetchone=True
    )
    
    if not member:
        flash('You must be a member to post.', 'danger')
        return redirect(url_for('forum.view', forum_id=forum_id))
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    parent_post_id = request.form.get('parent_post_id')
    
    if not content:
        flash('Post content cannot be empty.', 'danger')
        return redirect(url_for('forum.view', forum_id=forum_id))
    
    # Handle attachment
    attachment = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file and file.filename and current_app.allowed_file(file.filename):
            filename = secure_filename(f"forum_{forum_id}_{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'forums', filename)
            file.save(filepath)
            attachment = f"uploads/forums/{filename}"
    
    try:
        db.execute_query('''
            INSERT INTO forum_posts (forum_id, user_id, title, content, parent_post_id, attachment)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (forum_id, session['user_id'], title or None, content, 
              parent_post_id or None, attachment))
        
        # Update forum's updated_at
        db.execute_query(
            "UPDATE forums SET updated_at = NOW() WHERE id = %s",
            (forum_id,)
        )
        
        flash('Post created successfully!', 'success')
        
    except Exception as e:
        flash('An error occurred while creating the post.', 'danger')
        print(f"Create post error: {e}")
    
    return redirect(url_for('forum.view', forum_id=forum_id))

@forum_bp.route('/post/<int:post_id>')
def view_post(post_id):
    '''View a post and its replies'''
    post = db.execute_query('''
        SELECT p.*, u.full_name as author_name, u.profile_picture as author_picture,
               f.id as forum_id, f.title as forum_title
        FROM forum_posts p
        JOIN users u ON p.user_id = u.id
        JOIN forums f ON p.forum_id = f.id
        WHERE p.id = %s
    ''', (post_id,), fetch=True, fetchone=True)
    
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('forum.list_forums'))
    
    # Get replies
    replies = db.execute_query('''
        SELECT p.*, u.full_name as author_name, u.profile_picture as author_picture
        FROM forum_posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.parent_post_id = %s
        ORDER BY p.created_at ASC
    ''', (post_id,), fetch=True) or []
    
    # Check if user is member
    is_member = False
    if 'user_id' in session:
        member = db.execute_query(
            "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s",
            (post['forum_id'], session['user_id']),
            fetch=True,
            fetchone=True
        )
        is_member = member is not None
    
    return render_template('forum/post_detail.html', 
                         post=post, 
                         replies=replies,
                         is_member=is_member)

@forum_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@require_login
def delete_post(post_id):
    '''Delete a post'''
    post = db.execute_query(
        "SELECT user_id, forum_id FROM forum_posts WHERE id = %s",
        (post_id,),
        fetch=True,
        fetchone=True
    )
    
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('forum.list_forums'))
    
    # Check if user is author or moderator
    can_delete = post['user_id'] == session['user_id']
    
    if not can_delete:
        member = db.execute_query(
            "SELECT role FROM forum_members WHERE forum_id = %s AND user_id = %s",
            (post['forum_id'], session['user_id']),
            fetch=True,
            fetchone=True
        )
        can_delete = member and member['role'] in ['admin', 'moderator']
    
    if not can_delete:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('forum.view', forum_id=post['forum_id']))
    
    try:
        db.execute_query("DELETE FROM forum_posts WHERE id = %s", (post_id,))
        flash('Post deleted.', 'info')
    except Exception as e:
        flash('An error occurred.', 'danger')
        print(f"Delete post error: {e}")
    
    return redirect(url_for('forum.view', forum_id=post['forum_id']))

@forum_bp.route('/<int:forum_id>/moderators', methods=['POST'])
@require_login
def add_moderator(forum_id):
    '''Add a moderator to forum'''
    # Check if current user is admin
    admin = db.execute_query(
        "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s AND role = 'admin'",
        (forum_id, session['user_id']),
        fetch=True,
        fetchone=True
    )
    
    if not admin:
        return jsonify({'success': False, 'message': 'Only admins can add moderators'}), 403
    
    user_id = request.form.get('user_id')
    
    try:
        db.execute_query(
            "UPDATE forum_members SET role = 'moderator' WHERE forum_id = %s AND user_id = %s",
            (forum_id, user_id)
        )
        
        flash('Moderator added successfully.', 'success')
        return redirect(url_for('forum.view', forum_id=forum_id))
        
    except Exception as e:
        flash('An error occurred.', 'danger')
        print(f"Add moderator error: {e}")
        return redirect(url_for('forum.view', forum_id=forum_id))
"""

# ============================================================================
# CONTINUE TO NEXT PART...
# ============================================================================

def main():
    print_header("📦 PART 3B: Creating Messaging & Forum Controllers")
    
    print_section("Creating messaging controller...")
    create_file('src/controllers/messaging_controller.py', MESSAGING_CONTROLLER)
    
    print_section("Creating forum controller...")
    create_file('src/controllers/forum_controller.py', FORUM_CONTROLLER)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 3B Complete!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 3C for System Manager controller{Colors.END}")

if __name__ == '__main__':
    main()