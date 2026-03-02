from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_db_connection
from datetime import datetime, timedelta
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


event_admin_bp = Blueprint('event_admin', __name__, url_prefix='/event-admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def event_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
        
        user = execute_query(
            'SELECT role FROM users WHERE id = %s',
            (session['user_id'],), fetch=True, fetchone=True
        )
        
        if not user or user['role'] not in ['event_admin', 'system_manager']:
            flash('Access denied. Event Admin privileges required.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

@event_admin_bp.route('/dashboard')
@login_required
@event_admin_required
def dashboard():
    '''Event Admin Dashboard'''
    user_id = session.get('user_id')
    
    # Get admin's events
    my_events = execute_query('''
        SELECT 
            e.*,
            COUNT(DISTINCT er.id) as total_registrations,
            COUNT(DISTINCT a.id) as total_attended,
            COUNT(DISTINCT CASE WHEN a.check_out_time IS NULL AND a.check_in_time IS NOT NULL 
                  THEN a.id END) as currently_present
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id
        LEFT JOIN attendance a ON e.id = a.event_id
        WHERE e.creator_id = %s
        GROUP BY e.id
        ORDER BY e.start_date DESC
    ''', (user_id,), fetch=True) or []
    
    # Statistics
    stats = {
        'total_events': len(my_events),
        'upcoming_events': sum(1 for e in my_events if e['start_date'] > datetime.now()),
        'total_registrations': sum(e['total_registrations'] for e in my_events),
        'total_attended': sum(e['total_attended'] for e in my_events)
    }
    
    # Recent activity
    recent_activity = execute_query('''
        SELECT 
            ns.scan_type,
            ns.created_at,
            u.full_name as user_name,
            e.title as event_title,
            e.id as event_id
        FROM nfc_scans ns
        JOIN users u ON ns.scanned_user_id = u.id
        JOIN events e ON ns.event_id = e.id
        WHERE e.creator_id = %s
        ORDER BY ns.created_at DESC
        LIMIT 20
    ''', (user_id,), fetch=True) or []
    
    return render_template('event_admin/dashboard.html',
                         my_events=my_events,
                         stats=stats,
                         recent_activity=recent_activity)

@event_admin_bp.route('/event/<int:event_id>')
@login_required
@event_admin_required
def event_details(event_id):
    '''Event management page'''
    user_id = session.get('user_id')
    
    # Get event details
    event = execute_query('''
        SELECT e.*, u.full_name as creator_name
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.id = %s AND e.creator_id = %s
    ''', (event_id, user_id), fetch=True, fetchone=True)
    
    if not event:
        flash('Event not found or access denied', 'error')
        return redirect(url_for('event_admin.dashboard'))
    
    # Get registrations with attendance status
    registrations = execute_query('''
        SELECT 
            er.*,
            u.full_name,
            u.email,
            a.check_in_time,
            a.check_out_time,
            a.check_in_method,
            CASE 
                WHEN a.check_in_time IS NOT NULL AND a.check_out_time IS NULL THEN 'present'
                WHEN a.check_out_time IS NOT NULL THEN 'checked_out'
                ELSE 'registered'
            END as current_status
        FROM event_registrations er
        JOIN users u ON er.user_id = u.id
        LEFT JOIN attendance a ON er.event_id = a.event_id AND er.user_id = a.user_id
        WHERE er.event_id = %s
        ORDER BY er.registration_date DESC
    ''', (event_id,), fetch=True) or []
    
    # Attendance statistics
    attendance_stats = execute_query('''
        SELECT 
            COUNT(DISTINCT er.id) as total_registered,
            COUNT(DISTINCT a.id) as total_checked_in,
            COUNT(DISTINCT CASE WHEN a.check_out_time IS NOT NULL THEN a.id END) as total_checked_out,
            COUNT(DISTINCT CASE WHEN a.check_in_time IS NOT NULL AND a.check_out_time IS NULL 
                  THEN a.id END) as currently_present
        FROM event_registrations er
        LEFT JOIN attendance a ON er.event_id = a.event_id AND er.user_id = a.user_id
        WHERE er.event_id = %s
    ''', (event_id,), fetch=True, fetchone=True) or {}
    
    # Check-in methods breakdown
    checkin_methods = execute_query('''
        SELECT 
            check_in_method,
            COUNT(*) as count
        FROM attendance
        WHERE event_id = %s
        GROUP BY check_in_method
    ''', (event_id,), fetch=True) or []
    
    return render_template('event_admin/event_details.html',
                         event=event,
                         registrations=registrations,
                         attendance_stats=attendance_stats,
                         checkin_methods=checkin_methods)

@event_admin_bp.route('/event/<int:event_id>/attendance/live')
@login_required
@event_admin_required
def live_attendance(event_id):
    '''Real-time attendance monitoring'''
    user_id = session.get('user_id')
    
    # Verify ownership
    event = execute_query(
        'SELECT * FROM events WHERE id = %s AND creator_id = %s',
        (event_id, user_id), fetch=True, fetchone=True
    )
    
    if not event:
        flash('Event not found or access denied', 'error')
        return redirect(url_for('event_admin.dashboard'))
    
    return render_template('event_admin/live_attendance.html', event=event)

@event_admin_bp.route('/event/<int:event_id>/attendance/data')
@login_required
@event_admin_required
def attendance_data(event_id):
    '''API endpoint for real-time attendance data'''
    user_id = session.get('user_id')
    
    # Verify ownership
    event = execute_query(
        'SELECT id FROM events WHERE id = %s AND creator_id = %s',
        (event_id, user_id), fetch=True, fetchone=True
    )
    
    if not event:
        return jsonify({'error': 'Access denied'}), 403
    
    # Get current attendance
    current_attendance = execute_query('''
        SELECT 
            u.id,
            u.full_name,
            u.email,
            a.check_in_time,
            a.check_in_method,
            a.check_out_time
        FROM attendance a
        JOIN users u ON a.user_id = u.id
        WHERE a.event_id = %s
        AND a.check_in_time IS NOT NULL
        ORDER BY a.check_in_time DESC
    ''', (event_id,), fetch=True) or []
    
    # Format timestamps
    for record in current_attendance:
        if record['check_in_time']:
            record['check_in_time'] = record['check_in_time'].strftime('%Y-%m-%d %H:%M:%S')
        if record['check_out_time']:
            record['check_out_time'] = record['check_out_time'].strftime('%Y-%m-%d %H:%M:%S')
    
    # Statistics
    stats = execute_query('''
        SELECT 
            COUNT(DISTINCT er.id) as total_registered,
            COUNT(DISTINCT a.id) as total_checked_in,
            COUNT(DISTINCT CASE WHEN a.check_in_time IS NOT NULL AND a.check_out_time IS NULL 
                  THEN a.id END) as currently_present
        FROM event_registrations er
        LEFT JOIN attendance a ON er.event_id = a.event_id AND er.user_id = a.user_id
        WHERE er.event_id = %s
    ''', (event_id,), fetch=True, fetchone=True) or {}
    
    return jsonify({
        'attendance': current_attendance,
        'stats': stats
    })

@event_admin_bp.route('/event/<int:event_id>/reports')
@login_required
@event_admin_required
def event_reports(event_id):
    '''Generate event reports'''
    user_id = session.get('user_id')
    
    event = execute_query(
        'SELECT * FROM events WHERE id = %s AND creator_id = %s',
        (event_id, user_id), fetch=True, fetchone=True
    )
    
    if not event:
        flash('Event not found or access denied', 'error')
        return redirect(url_for('event_admin.dashboard'))
    
    # Attendance over time
    attendance_timeline = execute_query('''
        SELECT 
            DATE_FORMAT(check_in_time, '%Y-%m-%d %H:00:00') as hour,
            COUNT(*) as count
        FROM attendance
        WHERE event_id = %s
        GROUP BY DATE_FORMAT(check_in_time, '%Y-%m-%d %H:00:00')
        ORDER BY hour
    ''', (event_id,), fetch=True) or []
    
    # Check-in methods
    checkin_methods = execute_query('''
        SELECT 
            check_in_method,
            COUNT(*) as count
        FROM attendance
        WHERE event_id = %s
        GROUP BY check_in_method
    ''', (event_id,), fetch=True) or []
    
    # Networking stats
    networking_stats = execute_query('''
        SELECT COUNT(*) as total_connections
        FROM networking_connections
        WHERE event_id = %s
    ''', (event_id,), fetch=True, fetchone=True) or {'total_connections': 0}
    
    # Top networkers
    top_networkers = execute_query('''
        SELECT 
            u.full_name,
            COUNT(*) as connections
        FROM networking_connections nc
        JOIN users u ON nc.user1_id = u.id OR nc.user2_id = u.id
        WHERE nc.event_id = %s
        GROUP BY u.id, u.full_name
        ORDER BY connections DESC
        LIMIT 10
    ''', (event_id,), fetch=True) or []
    
    
        # Calculate attendance statistics
            
    # Calculate attendance statistics
    attendance_stats = execute_query("""
        SELECT 
            COUNT(DISTINCT er.user_id) as total_registered,
            COUNT(DISTINCT ec.user_id) as total_checked_in
        FROM event_registrations er
        LEFT JOIN event_checkins ec ON er.event_id = ec.event_id AND er.user_id = ec.user_id
        WHERE er.event_id = %s
    """, (event_id,), fetch=True, fetchone=True) or {
        'total_registered': 0,
        'total_checked_in': 0
    }
    
    return render_template('event_admin/reports.html',
                         attendance_stats=attendance_stats,
                             
                         event=event,
                         attendance_timeline=attendance_timeline,
                         checkin_methods=checkin_methods,
                         networking_stats=networking_stats,
                         top_networkers=top_networkers)

@event_admin_bp.route('/event/<int:event_id>/qr-codes')
@login_required
@event_admin_required
def generate_qr_codes(event_id):
    '''Generate QR codes for all registrations'''
    user_id = session.get('user_id')
    
    event = execute_query(
        'SELECT * FROM events WHERE id = %s AND creator_id = %s',
        (event_id, user_id), fetch=True, fetchone=True
    )
    
    if not event:
        flash('Event not found or access denied', 'error')
        return redirect(url_for('event_admin.dashboard'))
    
    # Get all registrations
    registrations = execute_query('''
        SELECT er.*, u.full_name, u.email
        FROM event_registrations er
        JOIN users u ON er.user_id = u.id
        WHERE er.event_id = %s
        ORDER BY u.full_name
    ''', (event_id,), fetch=True) or []
    
    # Generate QR codes if not already generated
    from src.controllers.nfc_controller import generate_event_qr_code
    
    for reg in registrations:
        if not reg.get('qr_code'):
            qr_data, qr_image = generate_event_qr_code(event_id, reg['user_id'], reg['id'])
            
            # Update registration with QR code
            execute_query('''
                UPDATE event_registrations 
                SET qr_code = %s
                WHERE id = %s
            ''', (qr_data, reg['id']))
            
            reg['qr_code'] = qr_data
            reg['qr_image'] = qr_image
    
    return render_template('event_admin/qr_codes.html',
                         event=event,
                         registrations=registrations)

@event_admin_bp.route('/event/<int:event_id>/manual-checkin', methods=['POST'])
@login_required
@event_admin_required
def manual_checkin(event_id):
    '''Manual check-in for attendees'''
    user_id = session.get('user_id')
    
    # Verify ownership
    event = execute_query(
        'SELECT id FROM events WHERE id = %s AND creator_id = %s',
        (event_id, user_id), fetch=True, fetchone=True
    )
    
    if not event:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    attendee_id = data.get('user_id')
    
    # Check if already checked in
    existing = execute_query('''
        SELECT id FROM attendance 
        WHERE user_id = %s AND event_id = %s AND check_out_time IS NULL
    ''', (attendee_id, event_id), fetch=True, fetchone=True)
    
    if existing:
        return jsonify({'success': False, 'message': 'Already checked in'})
    
    # Create attendance record
    execute_query('''
        INSERT INTO attendance 
        (event_id, user_id, check_in_time, check_in_method, status)
        VALUES (%s, %s, NOW(), 'manual', 'present')
    ''', (event_id, attendee_id))
    
    # Update registration
    execute_query('''
        UPDATE event_registrations 
        SET status = 'attended', checked_in_at = NOW()
        WHERE event_id = %s AND user_id = %s
    ''', (event_id, attendee_id))
    
    return jsonify({
        'success': True,
        'message': 'Manual check-in successful'
    })

@event_admin_bp.route('/networking-analytics')
@login_required
@event_admin_required
def networking_analytics():
    '''Networking analytics across all events'''
    user_id = session.get('user_id')
    
    # Get networking stats for admin's events
    networking_by_event = execute_query('''
        SELECT 
            e.title,
            e.id,
            COUNT(nc.id) as total_connections
        FROM events e
        LEFT JOIN networking_connections nc ON e.id = nc.event_id
        WHERE e.creator_id = %s
        GROUP BY e.id, e.title
        ORDER BY total_connections DESC
    ''', (user_id,), fetch=True) or []
    
    # Overall stats
    total_connections = execute_query('''
        SELECT COUNT(*) as count
        FROM networking_connections nc
        JOIN events e ON nc.event_id = e.id
        WHERE e.creator_id = %s
    ''', (user_id,), fetch=True, fetchone=True) or {'count': 0}
    
    return render_template('event_admin/networking_analytics.html',
                         networking_by_event=networking_by_event,
                         total_connections=total_connections['count'])

# Hyphenated URL aliases for consistency
@event_admin_bp.route('/event-admin/dashboard', methods=['GET'])
def dashboard_hyphenated():
    """Alias for /event_admin/dashboard"""
    return redirect('/event_admin/dashboard')

@event_admin_bp.route('/event-admin/events', methods=['GET'])
def events_list():
    """List all assigned events"""
    user = session.get('user')
    if not user or user['role'] != 'event_admin':
        flash('Access denied', 'error')
        return redirect('/')
    
    # Get events assigned to this admin
    events = Event.query.filter_by(admin_id=user['id']).all()
    
    return render_template('event_admin/events.html', events=events)

@event_admin_bp.route('/event-admin/events/<int:event_id>', methods=['GET'])
def event_detail_hyphenated(event_id):
    """Alias for event detail"""
    return redirect(f'/event_admin/event/{event_id}')

@event_admin_bp.route('/event-admin/events/<int:event_id>/approve', methods=['POST'])
def approve_event(event_id):
    """Approve an event"""
    user = session.get('user')
    if not user or user['role'] != 'event_admin':
        return jsonify({'error': 'Access denied'}), 403
    
    event = Event.query.get_or_404(event_id)
    event.status = 'approved'
    db.session.commit()
    
    flash('Event approved successfully!', 'success')
    return redirect(f'/event_admin/event/{event_id}')

@event_admin_bp.route('/event-admin/events/<int:event_id>/reject', methods=['POST'])
def reject_event(event_id):
    """Reject an event"""
    user = session.get('user')
    if not user or user['role'] != 'event_admin':
        return jsonify({'error': 'Access denied'}), 403
    
    event = Event.query.get_or_404(event_id)
    event.status = 'rejected'
    db.session.commit()
    
    flash('Event rejected', 'info')
    return redirect(f'/event_admin/event/{event_id}')
