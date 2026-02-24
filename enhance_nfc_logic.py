import os
import shutil
import time

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def backup_file(filepath):
    if os.path.exists(filepath):
        backup = filepath + '.backup_' + str(int(time.time()))
        shutil.copy2(filepath, backup)
        print(f"{Colors.GREEN}✓{Colors.END} Backup: {backup}")
        return True
    return False

# Enhanced NFC Controller with networking and check-in logic
ENHANCED_NFC_CONTROLLER = """
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from database import get_db_connection
from datetime import datetime
from functools import wraps

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
        scanned_user = db.execute_query(
            "SELECT id, full_name, email, job_title, company FROM users WHERE id = %s",
            (scanned_user_id,),
            fetch=True,
            fetchone=True
        )
        
        if not scanned_user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Check if already connected
        existing_connection = db.execute_query(
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
        db.execute_query("""
            INSERT INTO connections (user_id, connected_user_id, connection_method, connected_at)
            VALUES (%s, %s, %s, NOW())
        """, (scanner_id, scanned_user_id, scan_method))
        
        # Log the networking event
        db.execute_query("""
            INSERT INTO networking_logs (scanner_id, scanned_user_id, scan_method, scanned_at)
            VALUES (%s, %s, %s, NOW())
        """, (scanner_id, scanned_user_id, scan_method))
        
        # Create notification for the scanned user
        db.execute_query("""
            INSERT INTO notifications (user_id, message, type, created_at)
            VALUES (%s, %s, 'connection', NOW())
        """, (scanned_user_id, f'New connection via {scan_method.upper()}'))
        
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
        event = db.execute_query(
            "SELECT id, title FROM events WHERE id = %s",
            (event_id,),
            fetch=True,
            fetchone=True
        )
        
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'})
        
        # Get attendee info
        attendee = db.execute_query(
            "SELECT id, full_name, email FROM users WHERE id = %s",
            (attendee_id,),
            fetch=True,
            fetchone=True
        )
        
        if not attendee:
            return jsonify({'success': False, 'message': 'Attendee not found'})
        
        # Check if attendee is registered for event
        registration = db.execute_query(
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
        current_checkin = db.execute_query("""
            SELECT id, checked_in_at, checked_out_at 
            FROM event_checkins 
            WHERE event_id = %s AND user_id = %s 
            ORDER BY checked_in_at DESC LIMIT 1
        """, (event_id, attendee_id), fetch=True, fetchone=True)
        
        action_taken = ''
        
        if not current_checkin or current_checkin['checked_out_at']:
            # CHECK-IN
            db.execute_query("""
                INSERT INTO event_checkins (event_id, user_id, checked_in_at, checked_in_by, scan_method)
                VALUES (%s, %s, NOW(), %s, %s)
            """, (event_id, attendee_id, admin_id, scan_method))
            
            action_taken = 'checked_in'
            message = f'{attendee["full_name"]} checked in successfully'
            
        else:
            # CHECK-OUT
            db.execute_query("""
                UPDATE event_checkins 
                SET checked_out_at = NOW(), checked_out_by = %s
                WHERE id = %s
            """, (admin_id, current_checkin['id']))
            
            action_taken = 'checked_out'
            message = f'{attendee["full_name"]} checked out successfully'
        
        # Log the admin action
        db.execute_query("""
            INSERT INTO admin_checkin_logs (event_id, admin_id, attendee_id, action, scan_method, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (event_id, admin_id, attendee_id, action_taken, scan_method))
        
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
    total_registered = db.execute_query(
        "SELECT COUNT(*) as count FROM event_registrations WHERE event_id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    checked_in = db.execute_query("""
        SELECT COUNT(DISTINCT user_id) as count 
        FROM event_checkins 
        WHERE event_id = %s AND checked_in_at IS NOT NULL AND checked_out_at IS NULL
    """, (event_id,), fetch=True, fetchone=True)['count']
    
    total_checkins_today = db.execute_query("""
        SELECT COUNT(*) as count 
        FROM event_checkins 
        WHERE event_id = %s AND DATE(checked_in_at) = CURDATE()
    """, (event_id,), fetch=True, fetchone=True)['count']
    
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
    event = db.execute_query(
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
        checkins = db.execute_query("""
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
        """, (event_id,), fetch=True)
        
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
    
    connections = db.execute_query("""
        SELECT 
            u.*,
            c.connected_at,
            c.connection_method
        FROM connections c
        JOIN users u ON (c.connected_user_id = u.id AND c.user_id = %s) 
                     OR (c.user_id = u.id AND c.connected_user_id = %s)
        WHERE c.user_id = %s OR c.connected_user_id = %s
        ORDER BY c.connected_at DESC
    """, (user_id, user_id, user_id, user_id), fetch=True)
    
    return render_template('nfc/connections.html', connections=connections or [])
"""

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}PHASE 1: ENHANCING NFC CONTROLLER WITH NETWORKING & CHECK-IN LOGIC{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

filepath = 'src/controllers/nfc_controller.py'
backup_file(filepath)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(ENHANCED_NFC_CONTROLLER.strip())

print(f"{Colors.GREEN}✓{Colors.END} Enhanced: {filepath}")
print(f"  - Added networking scan logic")
print(f"  - Added admin check-in/out logic")
print(f"  - Added real-time stats API")
print(f"  - Added connections management")
print(f"\n{Colors.GREEN}✅ NFC controller logic enhanced!{Colors.END}\n")