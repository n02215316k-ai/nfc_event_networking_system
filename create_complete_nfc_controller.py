import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

NFC_CONTROLLER = """
from flask import Blueprint, render_template, request, jsonify, session
from database import get_db_connection
from datetime import datetime
import qrcode
import io
import base64
import hashlib
import json

nfc_bp = Blueprint('nfc', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@nfc_bp.route('/scanner')
@login_required
def scanner_page():
    '''NFC/QR Scanner page'''
    user_id = session.get('user_id')
    
    # Get user's registered events
    events = db.execute_query('''
        SELECT DISTINCT e.id, e.title, e.start_date, e.end_date
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id
        WHERE e.creator_id = %s OR er.user_id = %s
        ORDER BY e.start_date DESC
    ''', (user_id, user_id), fetch=True) or []
    
    return render_template('nfc/scanner.html', events=events)

@nfc_bp.route('/scan', methods=['POST'])
@login_required
def scan():
    '''Handle NFC scan for check-in/check-out'''
    try:
        data = request.get_json()
        scanner_id = session.get('user_id')
        scanned_data = data.get('scan_data')
        event_id = data.get('event_id')
        scan_type = data.get('scan_type', 'check_in')  # check_in, check_out, networking
        
        if not scanned_data:
            return jsonify({'success': False, 'message': 'No scan data provided'})
        
        # Decode scanned data (format: user_id:timestamp:hash)
        try:
            parts = scanned_data.split(':')
            scanned_user_id = int(parts[0])
        except:
            return jsonify({'success': False, 'message': 'Invalid scan data'})
        
        # Get scanned user info
        scanned_user = db.execute_query('''
            SELECT id, full_name, email, role FROM users WHERE id = %s
        ''', (scanned_user_id,), fetch=True, fetchone=True)
        
        if not scanned_user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Log the scan
        db.execute_query('''
            INSERT INTO nfc_scans 
            (scanner_id, scanned_user_id, event_id, scan_type, scan_data)
            VALUES (%s, %s, %s, %s, %s)
        ''', (scanner_id, scanned_user_id, event_id, scan_type, scanned_data))
        
        # Handle different scan types
        if scan_type == 'check_in':
            result = handle_check_in(scanned_user_id, event_id, 'nfc')
        elif scan_type == 'check_out':
            result = handle_check_out(scanned_user_id, event_id, 'nfc')
        elif scan_type == 'networking':
            result = handle_networking(scanner_id, scanned_user_id, event_id)
        else:
            result = {'success': False, 'message': 'Invalid scan type'}
        
        if result['success']:
            result['user'] = {
                'name': scanned_user['full_name'],
                'email': scanned_user['email'],
                'role': scanned_user['role']
            }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"NFC scan error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@nfc_bp.route('/qr-scan', methods=['POST'])
@login_required
def qr_scan():
    '''Handle QR code scan'''
    try:
        data = request.get_json()
        scanner_id = session.get('user_id')
        qr_data = data.get('qr_data')
        scan_type = data.get('scan_type', 'check_in')
        
        if not qr_data:
            return jsonify({'success': False, 'message': 'No QR data provided'})
        
        # Decode QR data (format: event_id:user_id:registration_id:hash)
        try:
            qr_parts = qr_data.split(':')
            event_id = int(qr_parts[0])
            user_id = int(qr_parts[1])
            registration_id = int(qr_parts[2])
        except:
            return jsonify({'success': False, 'message': 'Invalid QR code'})
        
        # Verify registration
        registration = db.execute_query('''
            SELECT er.*, u.full_name, u.email
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            WHERE er.id = %s AND er.event_id = %s AND er.user_id = %s
        ''', (registration_id, event_id, user_id), fetch=True, fetchone=True)
        
        if not registration:
            return jsonify({'success': False, 'message': 'Invalid registration'})
        
        # Log the scan
        db.execute_query('''
            INSERT INTO nfc_scans 
            (scanner_id, scanned_user_id, event_id, scan_type, scan_data)
            VALUES (%s, %s, %s, %s, %s)
        ''', (scanner_id, user_id, event_id, scan_type, qr_data))
        
        # Handle check-in/check-out
        if scan_type == 'check_in':
            result = handle_check_in(user_id, event_id, 'qr')
        elif scan_type == 'check_out':
            result = handle_check_out(user_id, event_id, 'qr')
        else:
            result = {'success': False, 'message': 'Invalid scan type'}
        
        if result['success']:
            result['user'] = {
                'name': registration['full_name'],
                'email': registration['email']
            }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"QR scan error: {e}")
        return jsonify({'success': False, 'message': str(e)})

def handle_check_in(user_id, event_id, method='nfc'):
    '''Handle event check-in'''
    try:
        # Check if already checked in
        existing = db.execute_query('''
            SELECT id, check_out_time FROM attendance 
            WHERE user_id = %s AND event_id = %s
            ORDER BY check_in_time DESC LIMIT 1
        ''', (user_id, event_id), fetch=True, fetchone=True)
        
        if existing and not existing['check_out_time']:
            return {'success': False, 'message': 'Already checked in'}
        
        # Create attendance record
        db.execute_query('''
            INSERT INTO attendance 
            (event_id, user_id, check_in_time, check_in_method, status)
            VALUES (%s, %s, NOW(), %s, 'present')
        ''', (event_id, user_id, method))
        
        # Update registration status
        db.execute_query('''
            UPDATE event_registrations 
            SET status = 'attended', checked_in_at = NOW()
            WHERE event_id = %s AND user_id = %s
        ''', (event_id, user_id))
        
        return {
            'success': True, 
            'message': 'Checked in successfully',
            'action': 'check_in',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    except Exception as e:
        print(f"Check-in error: {e}")
        return {'success': False, 'message': str(e)}

def handle_check_out(user_id, event_id, method='nfc'):
    '''Handle event check-out'''
    try:
        # Find active check-in
        attendance = db.execute_query('''
            SELECT id FROM attendance 
            WHERE user_id = %s AND event_id = %s 
            AND check_out_time IS NULL
            ORDER BY check_in_time DESC LIMIT 1
        ''', (user_id, event_id), fetch=True, fetchone=True)
        
        if not attendance:
            return {'success': False, 'message': 'No active check-in found'}
        
        # Update attendance with check-out
        db.execute_query('''
            UPDATE attendance 
            SET check_out_time = NOW(), check_out_method = %s
            WHERE id = %s
        ''', (method, attendance['id']))
        
        # Update registration
        db.execute_query('''
            UPDATE event_registrations 
            SET checked_out_at = NOW()
            WHERE event_id = %s AND user_id = %s
        ''', (event_id, user_id))
        
        return {
            'success': True, 
            'message': 'Checked out successfully',
            'action': 'check_out',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    except Exception as e:
        print(f"Check-out error: {e}")
        return {'success': False, 'message': str(e)}

def handle_networking(scanner_id, scanned_user_id, event_id):
    '''Handle networking connection via NFC'''
    try:
        # Prevent self-connection
        if scanner_id == scanned_user_id:
            return {'success': False, 'message': 'Cannot connect with yourself'}
        
        # Check if connection already exists
        existing = db.execute_query('''
            SELECT id FROM networking_connections 
            WHERE ((user1_id = %s AND user2_id = %s) 
                OR (user1_id = %s AND user2_id = %s))
            AND event_id = %s
        ''', (scanner_id, scanned_user_id, scanned_user_id, scanner_id, event_id), 
        fetch=True, fetchone=True)
        
        if existing:
            return {'success': False, 'message': 'Already connected'}
        
        # Create networking connection
        db.execute_query('''
            INSERT INTO networking_connections 
            (user1_id, user2_id, event_id, initiated_by, connection_type, status)
            VALUES (%s, %s, %s, %s, 'nfc_scan', 'connected')
        ''', (scanner_id, scanned_user_id, event_id, scanner_id))
        
        # Create notification for both users
        scanned_user = db.execute_query(
            'SELECT full_name FROM users WHERE id = %s',
            (scanned_user_id,), fetch=True, fetchone=True
        )
        
        scanner_user = db.execute_query(
            'SELECT full_name FROM users WHERE id = %s',
            (scanner_id,), fetch=True, fetchone=True
        )
        
        # Notify scanned user
        db.execute_query('''
            INSERT INTO notifications 
            (user_id, notification_type, title, message, link)
            VALUES (%s, 'networking', 'New Connection', %s, %s)
        ''', (scanned_user_id, 
              f"{scanner_user['full_name']} connected with you via NFC",
              f"/profile/{scanner_id}"))
        
        # Notify scanner
        db.execute_query('''
            INSERT INTO notifications 
            (user_id, notification_type, title, message, link)
            VALUES (%s, 'networking', 'New Connection', %s, %s)
        ''', (scanner_id,
              f"You connected with {scanned_user['full_name']} via NFC",
              f"/profile/{scanned_user_id}"))
        
        return {
            'success': True,
            'message': 'Networking connection established',
            'action': 'networking',
            'connection_name': scanned_user['full_name']
        }
    
    except Exception as e:
        print(f"Networking error: {e}")
        return {'success': False, 'message': str(e)}

def generate_user_nfc_code(user_id):
    '''Generate NFC code for user'''
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_input = f"{user_id}:{timestamp}:nfc_secret_key"
    hash_code = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    return f"{user_id}:{timestamp}:{hash_code}"

def generate_event_qr_code(event_id, user_id, registration_id):
    '''Generate QR code for event registration'''
    qr_data = f"{event_id}:{user_id}:{registration_id}:{hashlib.sha256(f'{event_id}{user_id}{registration_id}'.encode()).hexdigest()[:8]}"
    
    # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return qr_data, f"data:image/png;base64,{img_str}"
"""

print(f"\n{Colors.CYAN}Creating complete NFC controller...{Colors.END}\n")

filepath = 'src/controllers/nfc_controller.py'
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(NFC_CONTROLLER.strip())

print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")
print(f"\n{Colors.GREEN}✅ NFC Controller created successfully!{Colors.END}\n")