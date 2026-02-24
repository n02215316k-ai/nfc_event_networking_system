from flask import Blueprint, render_template, request, jsonify, session
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
        scanned_user = execute_query(
            "SELECT * FROM users WHERE nfc_badge_id = %s",
            (badge_id,), fetch=True, fetchone=True
        )
        
        if not scanned_user:
            return jsonify({'success': False, 'error': 'Invalid badge ID'})
        
        if scan_type == 'event' and event_id:
            # Check if user is registered
            attendance = execute_query(
                "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
                (event_id, scanned_user['id']), fetch=True, fetchone=True
            )
            
            if not attendance:
                return jsonify({'success': False, 'error': 'User not registered for this event'})
            
            # Toggle check-in/out
            if attendance['status'] == 'registered' or attendance['status'] == 'checked_out':
                execute_query("""
                    UPDATE attendance 
                    SET status = 'checked_in', check_in_time = %s, scan_count = scan_count + 1
                    WHERE id = %s
                """, (datetime.now(), attendance['id']))
                message = f"{scanned_user['full_name']} checked in successfully!"
            else:
                execute_query("""
                    UPDATE attendance 
                    SET status = 'checked_out', check_out_time = %s, scan_count = scan_count + 1
                    WHERE id = %s
                """, (datetime.now(), attendance['id']))
                message = f"{scanned_user['full_name']} checked out successfully!"
            
            return jsonify({'success': True, 'message': message})
        
        return jsonify({'success': False, 'error': 'Invalid scan type'})
    
    return render_template('scan/scanner.html')
