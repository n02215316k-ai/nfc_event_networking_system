import os
import sys

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")

# ============================================================================
# NFC CONTROLLER (Enhanced with networking feature)
# ============================================================================

NFC_CONTROLLER = """
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from config.database import db
from datetime import datetime

nfc_bp = Blueprint('nfc', __name__)

def require_login(f):
    '''Decorator to require login'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function

@nfc_bp.route('/scan', methods=['POST'])
@require_login
def scan():
    '''Handle NFC badge scan - both event check-in and networking'''
    data = request.get_json()
    
    badge_id = data.get('badge_id', '').strip()
    scan_type = data.get('scan_type', 'networking')  # 'event' or 'networking'
    event_id = data.get('event_id')
    
    if not badge_id:
        return jsonify({'success': False, 'message': 'No badge ID provided'}), 400
    
    # Find user with this badge
    scanned_user = db.execute_query(
        "SELECT * FROM users WHERE nfc_badge_id = %s",
        (badge_id,),
        fetch=True,
        fetchone=True
    )
    
    if not scanned_user:
        # Log failed scan
        db.execute_query('''
            INSERT INTO nfc_scan_logs (scanner_id, scanned_badge_id, scan_type, success, notes)
            VALUES (%s, %s, %s, FALSE, 'Badge not found in system')
        ''', (session['user_id'], badge_id, scan_type))
        
        return jsonify({
            'success': False,
            'message': 'Badge not registered in the system'
        }), 404
    
    # NETWORKING SCAN - View profile
    if scan_type == 'networking':
        # Log networking scan
        db.execute_query('''
            INSERT INTO nfc_scan_logs (scanner_id, scanned_badge_id, scanned_user_id, scan_type, success)
            VALUES (%s, %s, %s, 'networking', TRUE)
        ''', (session['user_id'], badge_id, scanned_user['id']))
        
        # Create notification for scanned user
        current_app.create_notification(
            scanned_user['id'],
            'profile_view',
            'Profile Viewed',
            f"{session['user_name']} viewed your profile via NFC scan",
            url_for('profile.view', user_id=session['user_id'])
        )
        
        return jsonify({
            'success': True,
            'scan_type': 'networking',
            'message': f'Scanned: {scanned_user["full_name"]}',
            'redirect_url': url_for('profile.view', user_id=scanned_user['id'])
        })
    
    # EVENT CHECK-IN/CHECK-OUT SCAN
    elif scan_type == 'event':
        if not event_id:
            return jsonify({'success': False, 'message': 'No event specified'}), 400
        
        # Verify event exists
        event = db.execute_query(
            "SELECT * FROM events WHERE id = %s",
            (event_id,),
            fetch=True,
            fetchone=True
        )
        
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        # Check if scanner has permission (must be event creator, admin, or system manager)
        can_scan = (event['creator_id'] == session['user_id'] or 
                   session.get('user_role') in ['system_manager', 'event_manager'])
        
        if not can_scan:
            return jsonify({
                'success': False,
                'message': 'You do not have permission to scan for this event'
            }), 403
        
        # Check if scanned user is registered for event
        attendance = db.execute_query(
            "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
            (event_id, scanned_user['id']),
            fetch=True,
            fetchone=True
        )
        
        if not attendance:
            # Auto-register user if not registered
            db.execute_query('''
                INSERT INTO attendance (event_id, user_id, status, registration_date)
                VALUES (%s, %s, 'registered', NOW())
            ''', (event_id, scanned_user['id']))
            
            attendance = db.execute_query(
                "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
                (event_id, scanned_user['id']),
                fetch=True,
                fetchone=True
            )
        
        current_status = attendance['status']
        new_status = None
        action = None
        
        # Toggle between check-in and check-out
        if current_status == 'registered' or current_status == 'checked_out':
            # CHECK IN
            new_status = 'checked_in'
            action = 'check_in'
            
            db.execute_query('''
                UPDATE attendance 
                SET status = 'checked_in', 
                    check_in_time = NOW(),
                    check_in_method = 'nfc',
                    scanner_id = %s,
                    scanner_name = %s
                WHERE id = %s
            ''', (session['user_id'], session['user_name'], attendance['id']))
            
            # Update event current attendees count
            db.execute_query(
                "UPDATE events SET current_attendees = current_attendees + 1 WHERE id = %s",
                (event_id,)
            )
            
            # AUTO-JOIN EVENT FORUM (New feature from prompt)
            forum = db.execute_query(
                "SELECT id FROM forums WHERE event_id = %s",
                (event_id,),
                fetch=True,
                fetchone=True
            )
            
            if forum:
                # Check if already a member
                existing_member = db.execute_query(
                    "SELECT id FROM forum_members WHERE forum_id = %s AND user_id = %s",
                    (forum['id'], scanned_user['id']),
                    fetch=True,
                    fetchone=True
                )
                
                if not existing_member:
                    db.execute_query('''
                        INSERT INTO forum_members (forum_id, user_id, role)
                        VALUES (%s, %s, 'member')
                    ''', (forum['id'], scanned_user['id']))
            
            message = f"Checked in: {scanned_user['full_name']}"
            
        elif current_status == 'checked_in':
            # CHECK OUT
            new_status = 'checked_out'
            action = 'check_out'
            
            db.execute_query('''
                UPDATE attendance 
                SET status = 'checked_out', 
                    check_out_time = NOW()
                WHERE id = %s
            ''', (attendance['id'],))
            
            # Update event current attendees count
            db.execute_query(
                "UPDATE events SET current_attendees = GREATEST(current_attendees - 1, 0) WHERE id = %s",
                (event_id,)
            )
            
            message = f"Checked out: {scanned_user['full_name']}"
        
        # Log the attendance action
        db.execute_query('''
            INSERT INTO attendance_logs (attendance_id, action, scanner_id, scanner_name, scan_method)
            VALUES (%s, %s, %s, %s, 'nfc')
        ''', (attendance['id'], action, session['user_id'], session['user_name']))
        
        # Log NFC scan
        db.execute_query('''
            INSERT INTO nfc_scan_logs (scanner_id, scanned_badge_id, scanned_user_id, 
                                      scan_type, event_id, success, notes)
            VALUES (%s, %s, %s, %s, %s, TRUE, %s)
        ''', (session['user_id'], badge_id, scanned_user['id'], 
              f'event_{action}', event_id, message))
        
        # Notify user
        current_app.create_notification(
            scanned_user['id'],
            f'event_{action}',
            f'Event {action.replace("_", " ").title()}',
            f'You have been {action.replace("_", " ")} for {event["title"]} by {session["user_name"]}',
            url_for('events.detail', event_id=event_id)
        )
        
        return jsonify({
            'success': True,
            'scan_type': 'event',
            'action': action,
            'status': new_status,
            'message': message,
            'user': {
                'id': scanned_user['id'],
                'name': scanned_user['full_name'],
                'profile_picture': scanned_user['profile_picture']
            }
        })
    
    return jsonify({'success': False, 'message': 'Invalid scan type'}), 400

@nfc_bp.route('/qr-scan', methods=['POST'])
@require_login
def qr_scan():
    '''Handle QR code scan (backup for NFC)'''
    data = request.get_json()
    
    qr_data = data.get('qr_data', '').strip()
    
    if not qr_data:
        return jsonify({'success': False, 'message': 'No QR data provided'}), 400
    
    # Parse QR data (format: "EVENT:123" or "USER:456")
    try:
        scan_type, entity_id = qr_data.split(':')
        entity_id = int(entity_id)
    except:
        return jsonify({'success': False, 'message': 'Invalid QR code format'}), 400
    
    if scan_type == 'EVENT':
        # Redirect to event detail
        return jsonify({
            'success': True,
            'redirect_url': url_for('events.detail', event_id=entity_id)
        })
    
    elif scan_type == 'USER':
        # Redirect to user profile
        return jsonify({
            'success': True,
            'redirect_url': url_for('profile.view', user_id=entity_id)
        })
    
    return jsonify({'success': False, 'message': 'Unknown QR code type'}), 400

@nfc_bp.route('/scanner')
@require_login
def scanner_page():
    '''NFC Scanner interface page'''
    event_id = request.args.get('event_id')
    
    event = None
    if event_id:
        event = db.execute_query(
            "SELECT * FROM events WHERE id = %s",
            (event_id,),
            fetch=True,
            fetchone=True
        )
    
    return render_template('nfc/scanner.html', event=event)
"""

# ============================================================================
# PROFILE CONTROLLER (Enhanced with research_area)
# ============================================================================

PROFILE_CONTROLLER = """
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from config.database import db
from werkzeug.utils import secure_filename
from datetime import datetime
import os

profile_bp = Blueprint('profile', __name__)

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

@profile_bp.route('/<int:user_id>')
def view(user_id):
    '''View user profile'''
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get qualifications
    qualifications = db.execute_query(
        "SELECT * FROM qualifications WHERE user_id = %s ORDER BY year_obtained DESC",
        (user_id,),
        fetch=True
    ) or []
    
    # Get follower/following counts
    followers_count = db.execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE following_id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    following_count = db.execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE follower_id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    # Check if current user is following this user
    is_following = False
    if 'user_id' in session and session['user_id'] != user_id:
        follow_record = db.execute_query(
            "SELECT id FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id),
            fetch=True,
            fetchone=True
        )
        is_following = follow_record is not None
    
    # Get recent events (created or attending)
    recent_events = db.execute_query('''
        SELECT e.*, 'creator' as relation
        FROM events e
        WHERE e.creator_id = %s AND e.status = 'published'
        UNION
        SELECT e.*, 'attendee' as relation
        FROM events e
        JOIN attendance a ON e.id = a.event_id
        WHERE a.user_id = %s AND e.status = 'published'
        ORDER BY start_date DESC
        LIMIT 5
    ''', (user_id, user_id), fetch=True) or []
    
    # Get forum memberships
    forum_count = db.execute_query(
        "SELECT COUNT(*) as count FROM forum_members WHERE user_id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )['count']
    
    is_own_profile = 'user_id' in session and session['user_id'] == user_id
    
    return render_template('profile/view.html',
                         user=user,
                         qualifications=qualifications,
                         followers_count=followers_count,
                         following_count=following_count,
                         is_following=is_following,
                         recent_events=recent_events,
                         forum_count=forum_count,
                         is_own_profile=is_own_profile)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@require_login
def edit():
    '''Edit current user profile'''
    user = db.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (session['user_id'],),
        fetch=True,
        fetchone=True
    )
    
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        date_of_birth = request.form.get('date_of_birth', '')
        gender = request.form.get('gender', '')
        biography = request.form.get('biography', '').strip()
        current_employment = request.form.get('current_employment', '').strip()
        current_research_area = request.form.get('current_research_area', '').strip()  # NEW FIELD
        
        # Handle profile picture upload
        profile_picture = user['profile_picture']
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename and current_app.allowed_file(file.filename):
                filename = secure_filename(f"profile_{session['user_id']}_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
                file.save(filepath)
                profile_picture = f"uploads/profiles/{filename}"
        
        # Update user
        try:
            db.execute_query('''
                UPDATE users 
                SET full_name = %s, phone_number = %s, date_of_birth = %s, gender = %s,
                    biography = %s, current_employment = %s, current_research_area = %s,
                    profile_picture = %s, updated_at = NOW()
                WHERE id = %s
            ''', (full_name, phone_number, date_of_birth or None, gender or None,
                  biography, current_employment, current_research_area,
                  profile_picture, session['user_id']))
            
            # Update session
            session['user_name'] = full_name
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.view', user_id=session['user_id']))
            
        except Exception as e:
            flash('An error occurred while updating your profile.', 'danger')
            print(f"Profile update error: {e}")
    
    return render_template('profile/edit.html', user=user)

@profile_bp.route('/qualifications/add', methods=['POST'])
@require_login
def add_qualification():
    '''Add a qualification'''
    qualification_type = request.form.get('qualification_type', '')
    institution = request.form.get('institution', '').strip()
    field_of_study = request.form.get('field_of_study', '').strip()
    year_obtained = request.form.get('year_obtained', '')
    
    # Handle document upload
    document_path = None
    if 'document' in request.files:
        file = request.files['document']
        if file and file.filename and current_app.allowed_file(file.filename):
            filename = secure_filename(f"qual_{session['user_id']}_{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'qualifications', filename)
            file.save(filepath)
            document_path = f"uploads/qualifications/{filename}"
    
    if not institution or not qualification_type:
        flash('Please provide qualification type and institution.', 'danger')
    else:
        try:
            db.execute_query('''
                INSERT INTO qualifications (user_id, qualification_type, institution, 
                                          field_of_study, year_obtained, document_path, verification_status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            ''', (session['user_id'], qualification_type, institution, field_of_study,
                  year_obtained or None, document_path))
            
            flash('Qualification added successfully! Pending verification.', 'success')
            
        except Exception as e:
            flash('An error occurred while adding qualification.', 'danger')
            print(f"Add qualification error: {e}")
    
    return redirect(url_for('profile.view', user_id=session['user_id']))

@profile_bp.route('/qualifications/<int:qual_id>/delete', methods=['POST'])
@require_login
def delete_qualification(qual_id):
    '''Delete a qualification'''
    # Verify ownership
    qual = db.execute_query(
        "SELECT user_id FROM qualifications WHERE id = %s",
        (qual_id,),
        fetch=True,
        fetchone=True
    )
    
    if qual and qual['user_id'] == session['user_id']:
        db.execute_query("DELETE FROM qualifications WHERE id = %s", (qual_id,))
        flash('Qualification deleted.', 'info')
    else:
        flash('You do not have permission to delete this qualification.', 'danger')
    
    return redirect(url_for('profile.view', user_id=session['user_id']))

@profile_bp.route('/follow/<int:user_id>', methods=['POST'])
@require_login
def follow(user_id):
    '''Follow a user'''
    if user_id == session['user_id']:
        return jsonify({'success': False, 'message': 'Cannot follow yourself'}), 400
    
    # Check if already following
    existing = db.execute_query(
        "SELECT id FROM followers WHERE follower_id = %s AND following_id = %s",
        (session['user_id'], user_id),
        fetch=True,
        fetchone=True
    )
    
    if existing:
        return jsonify({'success': False, 'message': 'Already following'}), 400
    
    try:
        db.execute_query(
            "INSERT INTO followers (follower_id, following_id) VALUES (%s, %s)",
            (session['user_id'], user_id)
        )
        
        # Notify user
        user = db.execute_query(
            "SELECT full_name FROM users WHERE id = %s",
            (user_id,),
            fetch=True,
            fetchone=True
        )
        
        if user:
            current_app.create_notification(
                user_id,
                'new_follower',
                'New Follower',
                f"{session['user_name']} started following you",
                url_for('profile.view', user_id=session['user_id'])
            )
        
        return jsonify({'success': True, 'message': 'Now following'})
        
    except Exception as e:
        print(f"Follow error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@profile_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@require_login
def unfollow(user_id):
    '''Unfollow a user'''
    try:
        db.execute_query(
            "DELETE FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id)
        )
        
        return jsonify({'success': True, 'message': 'Unfollowed'})
        
    except Exception as e:
        print(f"Unfollow error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@profile_bp.route('/followers/<int:user_id>')
def followers(user_id):
    '''View user followers'''
    user = db.execute_query(
        "SELECT full_name FROM users WHERE id = %s",
        (user_id,),
        fetch=True,
        fetchone=True
    )
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))
    
    followers_list = db.execute_query('''
        SELECT u.id, u.full_name, u.profile_picture, u.current_employment, f.created_at
        FROM followers f
        JOIN users u ON f.follower_id = u.id
        WHERE f.following_id = %s
        ORDER BY f.created_at DESC
    ''', (user_id,), fetch=True) or []
    
    following_list = db.execute_query('''
        SELECT u.id, u.full_name, u.profile_picture, u.current_employment, f.created_at
        FROM followers f
        JOIN users u ON f.following_id = u.id
        WHERE f.follower_id = %s
        ORDER BY f.created_at DESC
    ''', (user_id,), fetch=True) or []
    
    return render_template('profile/followers.html',
                         user=user,
                         followers=followers_list,
                         following=following_list,
                         user_id=user_id)
"""

# ============================================================================
# CONTINUE IN NEXT MESSAGE...
# ============================================================================

def main():
    print_header("📦 PART 3A: Creating NFC & Profile Controllers")
    
    print_section("Creating NFC controller...")
    create_file('src/controllers/nfc_controller.py', NFC_CONTROLLER)
    
    print_section("Creating profile controller...")
    create_file('src/controllers/profile_controller.py', PROFILE_CONTROLLER)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 3A Complete!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 3B for Messaging & Forum controllers{Colors.END}")

if __name__ == '__main__':
    main()