from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from database import get_db_connection
from datetime import datetime


# Database helper function
def execute_query(query, params=None, fetch=False, fetchone=False):
    """Execute database query with proper connection handling"""
    from database import get_db_connection
    
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchone() if fetchone else cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid if cursor.lastrowid else True
        
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.close()
        return None


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
    messages = execute_query('''
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
        unread = execute_query('''
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
    partner = execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )
    
    if not partner:
        flash('User not found.', 'danger')
        return redirect(url_for('messaging.inbox'))
    
    # Get all messages between current user and partner
    messages = execute_query('''
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
    execute_query('''
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
        recipient = execute_query(
            "SELECT full_name FROM users WHERE id = %s",
            (recipient_id,),
            fetch=True,
            fetchone=True
        )
        
        if not recipient:
            flash('Recipient not found.', 'danger')
            return redirect(url_for('messaging.inbox'))
        
        # Send message
        execute_query('''
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
        recipient = execute_query(
            "SELECT id, full_name FROM users WHERE id = %s",
            (recipient_id,),
            fetch=True,
            fetchone=True
        )
    
    # Get all users for recipient selection
    users = execute_query(
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
    message = execute_query(
        "SELECT sender_id, recipient_id FROM messages WHERE id = %s",
        (message_id,),
        fetch=True,
        fetchone=True
    )
    
    if message and (message['sender_id'] == session['user_id'] or 
                   message['recipient_id'] == session['user_id']):
        execute_query("DELETE FROM messages WHERE id = %s", (message_id,))
        flash('Message deleted.', 'info')
    else:
        flash('You do not have permission to delete this message.', 'danger')
    
    return redirect(request.referrer or url_for('messaging.inbox'))

# Alias routes for compatibility
@messaging_bp.route('/messages', methods=['GET'])
def messages_inbox_alias():
    """Alias for /messaging/"""
    return redirect('/messaging/')

@messaging_bp.route('/messages/<int:message_id>', methods=['GET'])  
def read_message_alias(message_id):
    """Alias for reading a message"""
    # Get the message to find the other user
    message = Message.query.get_or_404(message_id)
    user = session.get('user')
    
    # Determine the other user in conversation
    if message.sender_id == user['id']:
        other_user_id = message.receiver_id
    else:
        other_user_id = message.sender_id
    
    return redirect(f'/messaging/conversation/{other_user_id}')

@messaging_bp.route('/messages/send', methods=['POST'])
def send_message_alias():
    """Alias for send - preserve POST"""
    from flask import request
    # Forward the POST request
    return send_message()


@messaging_bp.route('/send', methods=['POST'])
def send():
    """Send a message (API endpoint)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    recipient_id = request.form.get('recipient_id')
    subject = request.form.get('subject', '')
    message = request.form.get('message')
    
    if not all([recipient_id, message]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, recipient_id, subject, message, sent_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (session['user_id'], recipient_id, subject, message))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'Message sent'})
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
