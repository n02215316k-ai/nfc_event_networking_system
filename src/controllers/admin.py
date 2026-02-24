# filepath: c:\Users\lenovo\Downloads\nfc\src\controllers\admin.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
from database import get_db_connection

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
