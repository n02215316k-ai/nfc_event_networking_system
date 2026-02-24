from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app, send_file
from database import get_db_connection
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import os


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


system_manager_bp = Blueprint('system_manager', __name__)

def require_system_manager(f):
    '''Decorator to require system manager role'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if session.get('user_role') != 'system_manager':
            flash('Access denied. System Manager privileges required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

@system_manager_bp.route('/dashboard')
@require_system_manager
def dashboard():
    '''System Manager Dashboard'''
    
    # Get overall statistics
    stats = {
        'total_users': execute_query(
            "SELECT COUNT(*) as count FROM users",
            fetch=True, fetchone=True
        )['count'],
        
        'total_events': execute_query(
            "SELECT COUNT(*) as count FROM events",
            fetch=True, fetchone=True
        )['count'],
        
        'active_events': execute_query(
            "SELECT COUNT(*) as count FROM events WHERE status = 'published' AND end_date > NOW()",
            fetch=True, fetchone=True
        )['count'],
        
        'total_forums': execute_query(
            "SELECT COUNT(*) as count FROM forums",
            fetch=True, fetchone=True
        )['count'],
        
        'pending_verifications': execute_query(
            "SELECT COUNT(*) as count FROM qualifications WHERE verification_status = 'pending'",
            fetch=True, fetchone=True
        )['count'],
        
        'total_attendance': execute_query(
            "SELECT COUNT(*) as count FROM attendance",
            fetch=True, fetchone=True
        )['count'],
        
        'checked_in_now': execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE status = 'checked_in'",
            fetch=True, fetchone=True
        )['count'],
        
        'total_messages': execute_query(
            "SELECT COUNT(*) as count FROM messages",
            fetch=True, fetchone=True
        )['count']
    }
    
    # Get user role distribution
    user_roles = execute_query('''
        SELECT role, COUNT(*) as count
        FROM users
        GROUP BY role
    ''', fetch=True) or []
    
    # Get recent activities (last 10)
    recent_users = execute_query('''
        SELECT id, full_name, email, role, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT 5
    ''', fetch=True) or []
    
    recent_events = execute_query('''
        SELECT e.*, u.full_name as creator_name
        FROM events e
        JOIN users u ON e.creator_id = u.id
        ORDER BY e.created_at DESC
        LIMIT 5
    ''', fetch=True) or []
    
    # Get event statistics by category
    event_categories = execute_query('''
        SELECT category, COUNT(*) as count
        FROM events
        WHERE status = 'published'
        GROUP BY category
    ''', fetch=True) or []
    
    # Get monthly registration trend (last 6 months)
    monthly_registrations = execute_query('''
        SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) as count
        FROM users
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(created_at, '%Y-%m')
        ORDER BY month ASC
    ''', fetch=True) or []
    
    return render_template('system_manager/dashboard.html',
                         stats=stats,
                         user_roles=user_roles,
                         recent_users=recent_users,
                         recent_events=recent_events,
                         event_categories=event_categories,
                         monthly_registrations=monthly_registrations)

@system_manager_bp.route('/users')
@require_system_manager
def users():
    '''View all users in the system'''
    search_query = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '')
    
    query = '''
        SELECT u.*,
               (SELECT COUNT(*) FROM followers WHERE following_id = u.id) as followers_count,
               (SELECT COUNT(*) FROM followers WHERE follower_id = u.id) as following_count,
               (SELECT COUNT(*) FROM events WHERE creator_id = u.id) as events_created,
               (SELECT COUNT(*) FROM qualifications WHERE user_id = u.id) as qualifications_count
        FROM users u
        WHERE 1=1
    '''
    
    params = []
    
    if search_query:
        query += " AND (u.full_name LIKE %s OR u.email LIKE %s OR u.current_employment LIKE %s)"
        search_term = f'%{search_query}%'
        params.extend([search_term, search_term, search_term])
    
    if role_filter:
        query += " AND u.role = %s"
        params.append(role_filter)
    
    query += " ORDER BY u.created_at DESC"
    
    users_list = execute_query(query, tuple(params) if params else None, fetch=True) or []
    
    return render_template('system_manager/users.html', 
                         users=users_list,
                         search_query=search_query,
                         role_filter=role_filter)

@system_manager_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@require_system_manager
def edit_user(user_id):
    '''Edit user details'''
    user = execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('system_manager.users'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'user')
        is_verified = request.form.get('is_verified') == 'on'
        nfc_badge_id = request.form.get('nfc_badge_id', '').strip()
        
        try:
            execute_query('''
                UPDATE users
                SET full_name = %s, email = %s, role = %s, is_verified = %s, nfc_badge_id = %s
                WHERE id = %s
            ''', (full_name, email, role, is_verified, nfc_badge_id or None, user_id))
            
            flash('User updated successfully!', 'success')
            return redirect(url_for('system_manager.users'))
            
        except Exception as e:
            flash('An error occurred while updating user.', 'danger')
            print(f"Edit user error: {e}")
    
    return render_template('system_manager/edit_user.html', user=user)

@system_manager_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@require_system_manager
def delete_user(user_id):
    '''Delete a user'''
    if user_id == session['user_id']:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('system_manager.users'))
    
    try:
        execute_query("DELETE FROM users WHERE id = %s", (user_id,))
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash('An error occurred while deleting user.', 'danger')
        print(f"Delete user error: {e}")
    
    return redirect(url_for('system_manager.users'))

@system_manager_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@require_system_manager
def reset_password(user_id):
    '''Reset user password'''
    new_password = request.form.get('new_password', '')
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long.', 'danger')
        return redirect(url_for('system_manager.edit_user', user_id=user_id))
    
    try:
        password_hash = generate_password_hash(new_password)
        execute_query(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )
        
        flash('Password reset successfully!', 'success')
    except Exception as e:
        flash('An error occurred while resetting password.', 'danger')
        print(f"Reset password error: {e}")
    
    return redirect(url_for('system_manager.edit_user', user_id=user_id))

@system_manager_bp.route('/events')
@require_system_manager
def events():
    '''View all events'''
    status_filter = request.args.get('status', '')
    
    query = '''
        SELECT e.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id) as total_registrations,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id AND status = 'checked_in') as checked_in_count
        FROM events e
        JOIN users u ON e.creator_id = u.id
    '''
    
    params = []
    
    if status_filter:
        query += " WHERE e.status = %s"
        params.append(status_filter)
    
    query += " ORDER BY e.created_at DESC"
    
    events_list = execute_query(query, tuple(params) if params else None, fetch=True) or []
    
    return render_template('system_manager/events.html', 
                         events=events_list,
                         status_filter=status_filter)

@system_manager_bp.route('/events/<int:event_id>/analytics')
@require_system_manager
def event_analytics(event_id):
    '''View detailed analytics for an event'''
    event = execute_query('''
        SELECT e.*, u.full_name as creator_name, u.email as creator_email
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.id = %s
    ''', (event_id,), fetch=True, fetchone=True)
    
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('system_manager.events'))
    
    # Get attendance statistics
    attendance_stats = {
        'total_registered': execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE event_id = %s",
            (event_id,), fetch=True, fetchone=True
        )['count'],
        
        'checked_in': execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE event_id = %s AND status = 'checked_in'",
            (event_id,), fetch=True, fetchone=True
        )['count'],
        
        'checked_out': execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE event_id = %s AND status = 'checked_out'",
            (event_id,), fetch=True, fetchone=True
        )['count'],
        
        'registered_only': execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE event_id = %s AND status = 'registered'",
            (event_id,), fetch=True, fetchone=True
        )['count']
    }
    
    # Get check-in timeline (hourly)
    checkin_timeline = execute_query('''
        SELECT DATE_FORMAT(check_in_time, '%Y-%m-%d %H:00:00') as hour,
               COUNT(*) as count
        FROM attendance
        WHERE event_id = %s AND check_in_time IS NOT NULL
        GROUP BY DATE_FORMAT(check_in_time, '%Y-%m-%d %H:00:00')
        ORDER BY hour ASC
    ''', (event_id,), fetch=True) or []
    
    # Get attendee list
    attendees = execute_query('''
        SELECT u.*, a.status, a.check_in_time, a.check_out_time, a.scanner_name
        FROM attendance a
        JOIN users u ON a.user_id = u.id
        WHERE a.event_id = %s
        ORDER BY a.check_in_time DESC NULLS LAST
    ''', (event_id,), fetch=True) or []
    
    # Get scan logs
    scan_logs = execute_query('''
        SELECT al.*, u.full_name as user_name, s.full_name as scanner_name
        FROM attendance_logs al
        JOIN attendance a ON al.attendance_id = a.id
        JOIN users u ON a.user_id = u.id
        LEFT JOIN users s ON al.scanner_id = s.id
        WHERE a.event_id = %s
        ORDER BY al.created_at DESC
        LIMIT 50
    ''', (event_id,), fetch=True) or []
    
    return render_template('system_manager/event_analytics.html',
                         event=event,
                         attendance_stats=attendance_stats,
                         checkin_timeline=checkin_timeline,
                         attendees=attendees,
                         scan_logs=scan_logs)

@system_manager_bp.route('/verifications')
@require_system_manager
def verifications():
    '''View pending qualification verifications'''
    status_filter = request.args.get('status', 'pending')
    
    qualifications = execute_query('''
        SELECT q.*, u.full_name as user_name, u.email as user_email,
               v.full_name as verifier_name
        FROM qualifications q
        JOIN users u ON q.user_id = u.id
        LEFT JOIN users v ON q.verified_by = v.id
        WHERE q.verification_status = %s
        ORDER BY q.created_at DESC
    ''', (status_filter,), fetch=True) or []
    
    return render_template('system_manager/verifications.html',
                         qualifications=qualifications,
                         status_filter=status_filter)

@system_manager_bp.route('/verifications/<int:qual_id>/view')
@require_system_manager
def view_qualification(qual_id):
    '''View qualification details and document'''
    qualification = execute_query('''
        SELECT q.*, u.full_name as user_name, u.email as user_email, u.id as user_id
        FROM qualifications q
        JOIN users u ON q.user_id = u.id
        WHERE q.id = %s
    ''', (qual_id,), fetch=True, fetchone=True)
    
    if not qualification:
        flash('Qualification not found.', 'danger')
        return redirect(url_for('system_manager.verifications'))
    
    return render_template('system_manager/view_qualification.html',
                         qualification=qualification)

@system_manager_bp.route('/verifications/<int:qual_id>/verify', methods=['POST'])
@require_system_manager
def verify_qualification(qual_id):
    '''Verify a qualification'''
    try:
        execute_query('''
            UPDATE qualifications
            SET verification_status = 'verified',
                verified_by = %s,
                verified_at = NOW()
            WHERE id = %s
        ''', (session['user_id'], qual_id))
        
        # Log verification
        execute_query('''
            INSERT INTO verification_logs (qualification_id, verifier_id, action, notes)
            VALUES (%s, %s, 'verified', 'Verified by system manager')
        ''', (qual_id, session['user_id']))
        
        # Get qualification details for notification
        qual = execute_query(
            "SELECT user_id, qualification_type, institution FROM qualifications WHERE id = %s",
            (qual_id,),
            fetch=True,
            fetchone=True
        )
        
        if qual:
            # Notify user
            current_app.create_notification(
                qual['user_id'],
                'qualification_verified',
                'Qualification Verified',
                f'Your {qual["qualification_type"]} from {qual["institution"]} has been verified.',
                url_for('profile.view', user_id=qual['user_id'])
            )
        
        flash('Qualification verified successfully!', 'success')
        
    except Exception as e:
        flash('An error occurred while verifying qualification.', 'danger')
        print(f"Verify qualification error: {e}")
    
    return redirect(url_for('system_manager.verifications'))

@system_manager_bp.route('/verifications/<int:qual_id>/reject', methods=['POST'])
@require_system_manager
def reject_qualification(qual_id):
    '''Reject a qualification'''
    reason = request.form.get('reason', '').strip()
    
    if not reason:
        flash('Please provide a reason for rejection.', 'danger')
        return redirect(url_for('system_manager.view_qualification', qual_id=qual_id))
    
    try:
        execute_query('''
            UPDATE qualifications
            SET verification_status = 'rejected',
                verified_by = %s,
                verified_at = NOW(),
                rejection_reason = %s
            WHERE id = %s
        ''', (session['user_id'], reason, qual_id))
        
        # Log rejection
        execute_query('''
            INSERT INTO verification_logs (qualification_id, verifier_id, action, notes)
            VALUES (%s, %s, 'rejected', %s)
        ''', (qual_id, session['user_id'], reason))
        
        # Get qualification details for notification
        qual = execute_query(
            "SELECT user_id, qualification_type, institution FROM qualifications WHERE id = %s",
            (qual_id,),
            fetch=True,
            fetchone=True
        )
        
        if qual:
            # Notify user
            current_app.create_notification(
                qual['user_id'],
                'qualification_rejected',
                'Qualification Rejected',
                f'Your {qual["qualification_type"]} from {qual["institution"]} was not verified. Reason: {reason}',
                url_for('profile.view', user_id=qual['user_id'])
            )
        
        flash('Qualification rejected.', 'info')
        
    except Exception as e:
        flash('An error occurred while rejecting qualification.', 'danger')
        print(f"Reject qualification error: {e}")
    
    return redirect(url_for('system_manager.verifications'))


@system_manager_bp.route('/reports')
@require_system_manager
def reports():
    '''Generate system reports'''
    report_type = request.args.get('type', 'overview')
    
    reports_data = {}
    
    if report_type == 'overview':
        # Overall system statistics
        reports_data = {
            'total_users': execute_query(
                "SELECT COUNT(*) as count FROM users",
                fetch=True, fetchone=True
            )['count'],
            'total_events': execute_query(
                "SELECT COUNT(*) as count FROM events",
                fetch=True, fetchone=True
            )['count'],
            'total_forums': execute_query(
                "SELECT COUNT(*) as count FROM forums",
                fetch=True, fetchone=True
            )['count'],
            'total_messages': execute_query(
                "SELECT COUNT(*) as count FROM messages",
                fetch=True, fetchone=True
            )['count']
        }
    
    elif report_type == 'events':
        # Event statistics
        reports_data['by_status'] = execute_query('''
            SELECT status, COUNT(*) as count
            FROM events
            GROUP BY status
        ''', fetch=True) or []
        
        reports_data['by_category'] = execute_query('''
            SELECT category, COUNT(*) as count
            FROM events
            GROUP BY category
        ''', fetch=True) or []
        
        reports_data['top_events'] = execute_query('''
            SELECT e.title, e.start_date, COUNT(a.id) as registrations
            FROM events e
            LEFT JOIN attendance a ON e.id = a.event_id
            GROUP BY e.id, e.title, e.start_date
            ORDER BY registrations DESC
            LIMIT 10
        ''', fetch=True) or []
    
    elif report_type == 'users':
        # User statistics
        reports_data['by_role'] = execute_query('''
            SELECT role, COUNT(*) as count
            FROM users
            GROUP BY role
        ''', fetch=True) or []
        
        reports_data['registration_trend'] = execute_query('''
            SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) as count
            FROM users
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY month ASC
        ''', fetch=True) or []
    
    # FIX: Add stats variable for template
    stats = reports_data if report_type == 'overview' else {}
    
    return render_template('system_manager/reports.html',
                         report_type=report_type,
                         reports_data=reports_data,
                         stats=stats)  # ADDED stats parameter

@system_manager_bp.route('/nfc-logs')
@require_system_manager
def nfc_logs():
    '''View NFC scan logs'''
    logs = execute_query('''
        SELECT nsl.*, 
               scanner.full_name as scanner_name,
               scanned_user.full_name as scanned_user_name,
               e.title as event_title
        FROM nfc_scan_logs nsl
        JOIN users scanner ON nsl.scanner_id = scanner.id
        LEFT JOIN users scanned_user ON nsl.scanned_user_id = scanned_user.id
        LEFT JOIN events e ON nsl.event_id = e.id
        ORDER BY nsl.created_at DESC
        LIMIT 100
    ''', fetch=True) or []
    
    return render_template('system_manager/nfc_logs.html', logs=logs)

@system_manager_bp.route('/settings', methods=['GET', 'POST'])
@require_system_manager
def settings():
    '''System settings'''
    if request.method == 'POST':
        # Handle system settings updates
        flash('Settings updated successfully!', 'success')
    
    return render_template('system_manager/settings.html')

# Hyphenated URL aliases for consistency
@system_manager_bp.route('/system-manager/dashboard', methods=['GET'])
def dashboard_hyphenated():
    """Alias for /system_manager/dashboard"""
    return redirect('/system_manager/dashboard')

@system_manager_bp.route('/system-manager/users/create', methods=['GET', 'POST'])
def create_user_hyphenated():
    """Create new user"""
    user = session.get('user')
    if not user or user['role'] != 'system_manager':
        flash('Access denied', 'error')
        return redirect('/')
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        password = request.form.get('password')
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return render_template('system_manager/user_form.html')
        
        # Create user
        new_user = User(
            email=email,
            full_name=full_name,
            role=role,
            password=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('User created successfully!', 'success')
        return redirect('/system_manager/users')
    
    return render_template('system_manager/user_form.html')

@system_manager_bp.route('/system-manager/events/<int:event_id>/approve', methods=['POST'])
def approve_event_hyphenated(event_id):
    """Approve event"""
    user = session.get('user')
    if not user or user['role'] != 'system_manager':
        return jsonify({'error': 'Access denied'}), 403
    
    event = Event.query.get_or_404(event_id)
    event.status = 'approved'
    db.session.commit()
    
    flash('Event approved!', 'success')
    return redirect('/system_manager/events')

@system_manager_bp.route('/system-manager/verifications/<int:qual_id>/approve', methods=['POST'])
def approve_verification_hyphenated(qual_id):
    """Approve verification"""
    return verify_qualification(qual_id)

@system_manager_bp.route('/system-manager/reports/users', methods=['GET'])
def user_reports():
    """User reports"""
    user = session.get('user')
    if not user or user['role'] != 'system_manager':
        flash('Access denied', 'error')
        return redirect('/')
    
    # Get user statistics
    total_users = User.query.count()
    users_by_role = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    
    return render_template('system_manager/reports.html', 
                         total_users=total_users,
                         users_by_role=users_by_role,
                         report_type='users')

@system_manager_bp.route('/system-manager/reports/events', methods=['GET'])
def event_reports():
    """Event reports"""
    user = session.get('user')
    if not user or user['role'] != 'system_manager':
        flash('Access denied', 'error')
        return redirect('/')
    
    # Get event statistics
    total_events = Event.query.count()
    events_by_status = db.session.query(Event.status, db.func.count(Event.id)).group_by(Event.status).all()
    
    return render_template('system_manager/reports.html', 
                         total_events=total_events,
                         events_by_status=events_by_status,
                         report_type='events')
