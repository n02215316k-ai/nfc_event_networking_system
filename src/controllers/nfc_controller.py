from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from database import get_db_connection
from datetime import datetime
from functools import wraps


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


nfc_bp = Blueprint('nfc', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

@nfc_bp.route('/scanner')
@login_required
def scanner_page():
    '''NFC/QR Scanner page'''
    user_role = session.get('role', 'attendee')
    return render_template('nfc/scanner.html', user_role=user_role)

@nfc_bp.route('/scan', methods=['POST'])
@login_required
def process_scan():
    '''Process NFC/QR scan - handles both networking and check-in'''
    try:
        data = request.get_json()
        scan_data = data.get('scan_data')
        scan_method = data.get('scan_method', 'qr')
        scanner_id = session.get('user_id')
        scanner_role = session.get('role', 'attendee')
        
        if not scan_data:
            return jsonify({'success': False, 'message': 'No scan data received'})
        
        # Parse scan data
        # Format: "user:{user_id}:{email}" or "event:{event_id}:{user_id}"
        parts = scan_data.split(':')
        
        if len(parts) < 2:
            return jsonify({'success': False, 'message': 'Invalid QR code format'})
        
        scan_type = parts[0]
        
        # NETWORKING: User scanned another user's badge
        if scan_type == 'user':
            scanned_user_id = parts[1]
            return handle_networking_scan(scanner_id, scanned_user_id, scan_method)
        
        # CHECK-IN: Event check-in/out (only for admins)
        elif scan_type == 'event':
            event_id = parts[1]
            attendee_id = parts[2] if len(parts) > 2 else None
            
            if scanner_role in ['event_admin', 'system_manager']:
                return handle_checkin_scan(event_id, attendee_id, scanner_id, scan_method)
            else:
                return jsonify({
                    'success': False, 
                    'message': 'Only event admins can perform check-ins'
                })
        
        else:
            return jsonify({'success': False, 'message': 'Unknown scan type'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

def handle_networking_scan(scanner_id, scanned_user_id, scan_method):
    '''Handle user-to-user networking scan'''
    try:
        # Prevent self-scan
        if str(scanner_id) == str(scanned_user_id):
            return jsonify({'success': False, 'message': 'Cannot scan your own badge'})
        
        # Get scanned user info
        scanned_user = execute_query(
            "SELECT id, full_name, email, job_title, company FROM users WHERE id = %s",
            (scanned_user_id,),
            fetch=True,
            fetchone=True
        )
        
        if not scanned_user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Check if already connected
        existing_connection = execute_query(
            "SELECT id FROM connections WHERE (user_id = %s AND connected_user_id = %s) OR (user_id = %s AND connected_user_id = %s)",
            (scanner_id, scanned_user_id, scanned_user_id, scanner_id),
            fetch=True,
            fetchone=True
        )
        
        if existing_connection:
            return jsonify({
                'success': True,
                'message': f'Already connected with {scanned_user["full_name"]}',
                'user': scanned_user,
                'action': 'existing_connection'
            })
        
        # Create new connection
        connection_sql = """
            INSERT INTO connections (user_id, connected_user_id, connection_method, connected_at)
            VALUES (%s, %s, %s, NOW())
        """
        execute_query(connection_sql, (scanner_id, scanned_user_id, scan_method))
        
        # Log the networking event
        log_sql = """
            INSERT INTO networking_logs (scanner_id, scanned_user_id, scan_method, scanned_at)
            VALUES (%s, %s, %s, NOW())
        """
        execute_query(log_sql, (scanner_id, scanned_user_id, scan_method))
        
        # Create notification for the scanned user
        notif_sql = """
            INSERT INTO notifications (user_id, message, type, created_at)
            VALUES (%s, %s, 'connection', NOW())
        """
        execute_query(notif_sql, (scanned_user_id, f'New connection via {scan_method.upper()}'))
        
        return jsonify({
            'success': True,
            'message': f'Successfully connected with {scanned_user["full_name"]}!',
            'user': scanned_user,
            'action': 'new_connection'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Networking error: {str(e)}'})

def handle_checkin_scan(event_id, attendee_id, admin_id, scan_method):
    '''Handle event check-in/out by admin'''
    try:
        # Verify event exists
        event = execute_query(
            "SELECT id, title FROM events WHERE id = %s",
            (event_id,),
            fetch=True,
            fetchone=True
        )
        
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'})
        
        # Get attendee info
        attendee = execute_query(
            "SELECT id, full_name, email FROM users WHERE id = %s",
            (attendee_id,),
            fetch=True,
            fetchone=True
        )
        
        if not attendee:
            return jsonify({'success': False, 'message': 'Attendee not found'})
        
        # Check if attendee is registered for event
        registration = execute_query(
            "SELECT id, status FROM event_registrations WHERE event_id = %s AND user_id = %s",
            (event_id, attendee_id),
            fetch=True,
            fetchone=True
        )
        
        if not registration:
            return jsonify({
                'success': False, 
                'message': f'{attendee["full_name"]} is not registered for this event'
            })
        
        # Check current check-in status
        checkin_sql = """
            SELECT id, checked_in_at, checked_out_at 
            FROM event_checkins 
            WHERE event_id = %s AND user_id = %s 
            ORDER BY checked_in_at DESC LIMIT 1
        """
        current_checkin = execute_query(checkin_sql, (event_id, attendee_id), fetch=True, fetchone=True)
        
        action_taken = ''
        
        if not current_checkin or current_checkin['checked_out_at']:
            # CHECK-IN
            insert_checkin = """
                INSERT INTO event_checkins (event_id, user_id, checked_in_at, checked_in_by, scan_method)
                VALUES (%s, %s, NOW(), %s, %s)
            """
            execute_query(insert_checkin, (event_id, attendee_id, admin_id, scan_method))
            
            action_taken = 'checked_in'
            message = f'{attendee["full_name"]} checked in successfully'
            
        else:
            # CHECK-OUT
            update_checkout = """
                UPDATE event_checkins 
                SET checked_out_at = NOW(), checked_out_by = %s
                WHERE id = %s
            """
            execute_query(update_checkout, (admin_id, current_checkin['id']))
            
            action_taken = 'checked_out'
            message = f'{attendee["full_name"]} checked out successfully'
        
        # Log the admin action
        log_admin = """
            INSERT INTO admin_checkin_logs (event_id, admin_id, attendee_id, action, scan_method, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        execute_query(log_admin, (event_id, admin_id, attendee_id, action_taken, scan_method))
        
        # Get updated stats
        stats = get_event_checkin_stats(event_id)
        
        return jsonify({
            'success': True,
            'message': message,
            'action': action_taken,
            'attendee': attendee,
            'event': event,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Check-in error: {str(e)}'})

def get_event_checkin_stats(event_id):
    '''Get real-time check-in statistics'''
    total_registered = execute_query(
        "SELECT COUNT(*) as count FROM event_registrations WHERE event_id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    checked_in_sql = """
        SELECT COUNT(DISTINCT user_id) as count 
        FROM event_checkins 
        WHERE event_id = %s AND checked_in_at IS NOT NULL AND checked_out_at IS NULL
    """
    checked_in = execute_query(checked_in_sql, (event_id,), fetch=True, fetchone=True)['count']
    
    today_sql = """
        SELECT COUNT(*) as count 
        FROM event_checkins 
        WHERE event_id = %s AND DATE(checked_in_at) = CURDATE()
    """
    total_checkins_today = execute_query(today_sql, (event_id,), fetch=True, fetchone=True)['count']
    
    return {
        'total_registered': total_registered,
        'currently_checked_in': checked_in,
        'total_checkins_today': total_checkins_today,
        'attendance_rate': round((checked_in / total_registered * 100) if total_registered > 0 else 0, 1)
    }

@nfc_bp.route('/event/<int:event_id>/checkin-log')
@login_required
def event_checkin_log(event_id):
    '''Real-time check-in log for event admins'''
    user_role = session.get('role')
    
    if user_role not in ['event_admin', 'system_manager']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get event details
    event = execute_query(
        "SELECT * FROM events WHERE id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events.index'))
    
    return render_template('nfc/checkin_log.html', event=event)

@nfc_bp.route('/api/event/<int:event_id>/checkin-log')
@login_required
def api_checkin_log(event_id):
    '''API endpoint for real-time check-in log'''
    try:
        # Get recent check-ins (last 50)
        log_sql = """
            SELECT 
                ec.*,
                u.full_name,
                u.email,
                admin.full_name as admin_name,
                TIMESTAMPDIFF(MINUTE, ec.checked_in_at, COALESCE(ec.checked_out_at, NOW())) as duration_minutes
            FROM event_checkins ec
            JOIN users u ON ec.user_id = u.id
            LEFT JOIN users admin ON ec.checked_in_by = admin.id
            WHERE ec.event_id = %s
            ORDER BY ec.checked_in_at DESC
            LIMIT 50
        """
        checkins = execute_query(log_sql, (event_id,), fetch=True)
        
        # Get current stats
        stats = get_event_checkin_stats(event_id)
        
        return jsonify({
            'success': True,
            'checkins': checkins or [],
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@nfc_bp.route('/my-connections')
@login_required
def my_connections():
    '''View user's networking connections'''
    user_id = session.get('user_id')
    
    conn_sql = """
        SELECT 
            u.*,
            c.connected_at,
            c.connection_method
        FROM connections c
        JOIN users u ON (c.connected_user_id = u.id AND c.user_id = %s) 
                     OR (c.user_id = u.id AND c.connected_user_id = %s)
        WHERE c.user_id = %s OR c.connected_user_id = %s
        ORDER BY c.connected_at DESC
    """
    connections = execute_query(conn_sql, (user_id, user_id, user_id, user_id), fetch=True)
    
    return render_template('nfc/connections.html', connections=connections or [])

import qrcode
import io
import base64
from datetime import datetime

def generate_user_nfc_code(user_id, email):
    '''Generate QR code for user networking (NFC backup)'''
    try:
        # Format: "user:{user_id}:{email}"
        qr_data = f"user:{user_id}:{email}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating user QR code: {e}")
        return None

def generate_event_qr_code(event_id, user_id):
    '''Generate QR code for event check-in (NFC backup)'''
    try:
        # Format: "event:{event_id}:{user_id}"
        qr_data = f"event:{event_id}:{user_id}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating event QR code: {e}")
        return None
