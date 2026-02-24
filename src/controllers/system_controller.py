from flask import render_template, redirect, session, flash, request
from functools import wraps

def system_manager_required(f):
    '''Decorator to require system manager role'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect('/login')
        if session.get('role') != 'system_manager':
            flash('Access denied. System manager privileges required.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    '''Decorator to require admin role (event_admin or system_manager)'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect('/login')
        if session.get('role') not in ['event_admin', 'system_manager']:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def get_all_users():
    '''Get all users from database'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, full_name, email, role, job_title, company, 
                   phone, created_at, nfc_badge_id
            FROM users 
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Error getting users: {e}")
        return []

def get_system_stats():
    '''Get system-wide statistics'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        stats = {}
        
        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        stats['total_users'] = cursor.fetchone()['count']
        
        # Total events
        cursor.execute("SELECT COUNT(*) as count FROM events")
        stats['total_events'] = cursor.fetchone()['count']
        
        # Total connections
        cursor.execute("SELECT COUNT(*) as count FROM connections")
        stats['total_connections'] = cursor.fetchone()['count']
        
        # Total scans
        cursor.execute("SELECT COUNT(*) as count FROM nfc_scans")
        stats['total_scans'] = cursor.fetchone()['count']
        
        # Users by role
        cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
        role_data = cursor.fetchall()
        stats['users_by_role'] = role_data
        stats['role_labels'] = [r['role'] for r in role_data]
        stats['role_counts'] = [r['count'] for r in role_data]
        
        # Recent scans
        cursor.execute("""
            SELECT s.*, u1.full_name as scanner_name, u2.full_name as scanned_name
            FROM nfc_scans s
            LEFT JOIN users u1 ON s.scanner_id = u1.id
            LEFT JOIN users u2 ON s.scanned_user_id = u2.id
            ORDER BY s.scanned_at DESC
            LIMIT 10
        """)
        stats['recent_scans'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return stats
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return {
            'total_users': 0,
            'total_events': 0,
            'total_connections': 0,
            'total_scans': 0,
            'users_by_role': [],
            'role_labels': [],
            'role_counts': [],
            'recent_scans': []
        }

def get_all_events():
    '''Get all events from database'''
    try:
        from database import get_db_connection
        from datetime import datetime
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, 
                   COUNT(DISTINCT er.user_id) as attendee_count
            FROM events e
            LEFT JOIN event_registrations er ON e.id = er.event_id
            GROUP BY e.id
            ORDER BY e.event_date DESC
        """)
        events = cursor.fetchall()
        
        # Count upcoming and past events
        now = datetime.now().date()
        upcoming_count = sum(1 for e in events if e.get('event_date') and e['event_date'] >= now)
        past_count = len(events) - upcoming_count
        
        # Total registrations
        cursor.execute("SELECT COUNT(*) as count FROM event_registrations")
        total_registrations = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return {
            'events': events,
            'upcoming_count': upcoming_count,
            'past_count': past_count,
            'total_registrations': total_registrations
        }
    except Exception as e:
        print(f"Error getting events: {e}")
        return {
            'events': [],
            'upcoming_count': 0,
            'past_count': 0,
            'total_registrations': 0
        }

def update_user_role(user_id, new_role):
    '''Update user role'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating user role: {e}")
        return False

def delete_user(user_id):
    '''Delete user from system'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete related records first
        cursor.execute("DELETE FROM event_registrations WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM connections WHERE user_id = %s OR connected_user_id = %s", (user_id, user_id))
        cursor.execute("DELETE FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s", (user_id, user_id))
        cursor.execute("DELETE FROM forum_posts WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM messages WHERE sender_id = %s OR receiver_id = %s", (user_id, user_id))
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def delete_event(event_id):
    '''Delete event from system'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete related records
        cursor.execute("DELETE FROM event_registrations WHERE event_id = %s", (event_id,))
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting event: {e}")
        return False