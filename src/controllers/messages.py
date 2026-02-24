# filepath: c:\Users\lenovo\Downloads\nfc\src\controllers\messages.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_db_connection
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
