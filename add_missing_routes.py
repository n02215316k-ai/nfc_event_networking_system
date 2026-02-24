import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADDING MISSING ROUTE ALIASES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Track what we add
added_routes = []

# ============================================================================
# 1. EVENTS CONTROLLER - Add missing routes
# ============================================================================
print(f"{Colors.YELLOW}1. Adding routes to events_controller.py...{Colors.END}\n")

events_controller = 'src/controllers/events_controller.py'

if os.path.exists(events_controller):
    with open(events_controller, 'r', encoding='utf-8') as f:
        events_content = f.read()
    
    # Backup
    with open(events_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(events_content)
    
    # Add missing routes before the last line
    missing_events_routes = '''

@events_bp.route('/events/<int:event_id>/attendees', methods=['GET'])
def event_attendees(event_id):
    """View event attendees (organizer/admin only)"""
    user = session.get('user')
    if not user:
        flash('Please login first', 'error')
        return redirect('/auth/login')
    
    event = Event.query.get_or_404(event_id)
    
    # Check if user is organizer or admin
    if event.organizer_id != user['id'] and user['role'] not in ['event_admin', 'system_manager']:
        flash('Access denied', 'error')
        return redirect('/')
    
    # Get all registrations
    registrations = Registration.query.filter_by(event_id=event_id).all()
    
    return render_template('events/attendees.html', 
                         event=event, 
                         registrations=registrations)
'''
    
    # Insert before last line (usually if __name__)
    if 'if __name__' not in events_content:
        events_content += missing_events_routes
    else:
        insert_pos = events_content.rfind('if __name__')
        events_content = events_content[:insert_pos] + missing_events_routes + '\n' + events_content[insert_pos:]
    
    with open(events_controller, 'w', encoding='utf-8') as f:
        f.write(events_content)
    
    added_routes.append('events/attendees')
    print(f"{Colors.GREEN}✓ Added /events/<id>/attendees route{Colors.END}")

else:
    print(f"{Colors.RED}✗ events_controller.py not found{Colors.END}")

# ============================================================================
# 2. PROFILE CONTROLLER - Add my-events route
# ============================================================================
print(f"\n{Colors.YELLOW}2. Adding routes to profile_controller.py...{Colors.END}\n")

profile_controller = 'src/controllers/profile_controller.py'

if os.path.exists(profile_controller):
    with open(profile_controller, 'r', encoding='utf-8') as f:
        profile_content = f.read()
    
    # Backup
    with open(profile_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(profile_content)
    
    # Add my-events route
    my_events_route = '''

@profile_bp.route('/profile/my-events', methods=['GET'])
def my_events():
    """View my registered events"""
    user = session.get('user')
    if not user:
        flash('Please login first', 'error')
        return redirect('/auth/login')
    
    # Get user's registrations
    registrations = Registration.query.filter_by(user_id=user['id']).all()
    events = [r.event for r in registrations if r.event]
    
    return render_template('events/my-events.html', events=events)
'''
    
    # Insert before last line
    if 'if __name__' not in profile_content:
        profile_content += my_events_route
    else:
        insert_pos = profile_content.rfind('if __name__')
        profile_content = profile_content[:insert_pos] + my_events_route + '\n' + profile_content[insert_pos:]
    
    with open(profile_controller, 'w', encoding='utf-8') as f:
        f.write(profile_content)
    
    added_routes.append('profile/my-events')
    print(f"{Colors.GREEN}✓ Added /profile/my-events route{Colors.END}")

else:
    print(f"{Colors.RED}✗ profile_controller.py not found{Colors.END}")

# ============================================================================
# 3. MESSAGING CONTROLLER - Add alias routes
# ============================================================================
print(f"\n{Colors.YELLOW}3. Adding routes to messaging_controller.py...{Colors.END}\n")

messaging_controller = 'src/controllers/messaging_controller.py'

if os.path.exists(messaging_controller):
    with open(messaging_controller, 'r', encoding='utf-8') as f:
        messaging_content = f.read()
    
    # Backup
    with open(messaging_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(messaging_content)
    
    # Add alias routes
    messaging_aliases = '''

# Alias routes for compatibility
@messaging_bp.route('/messages', methods=['GET'])
def messages_inbox_alias():
    """Alias for /messaging/"""
    return redirect('/messaging/')

@messaging_bp.route('/messages/<int:message_id>', methods=['GET'])  
def read_message_alias(message_id):
    """Alias for reading a message"""
    # Get the message to find the other user
    message = Message.query.get_or_404(message_id)
    user = session.get('user')
    
    # Determine the other user in conversation
    if message.sender_id == user['id']:
        other_user_id = message.receiver_id
    else:
        other_user_id = message.sender_id
    
    return redirect(f'/messaging/conversation/{other_user_id}')

@messaging_bp.route('/messages/send', methods=['POST'])
def send_message_alias():
    """Alias for send - preserve POST"""
    from flask import request
    # Forward the POST request
    return send_message()
'''
    
    # Insert before last line
    if 'if __name__' not in messaging_content:
        messaging_content += messaging_aliases
    else:
        insert_pos = messaging_content.rfind('if __name__')
        messaging_content = messaging_content[:insert_pos] + messaging_aliases + '\n' + messaging_content[insert_pos:]
    
    with open(messaging_controller, 'w', encoding='utf-8') as f:
        f.write(messaging_content)
    
    added_routes.extend(['messages', 'messages/<id>', 'messages/send'])
    print(f"{Colors.GREEN}✓ Added messaging alias routes{Colors.END}")

else:
    print(f"{Colors.RED}✗ messaging_controller.py not found{Colors.END}")

# ============================================================================
# 4. FORUM CONTROLLER - Add alias routes
# ============================================================================
print(f"\n{Colors.YELLOW}4. Adding routes to forum_controller.py...{Colors.END}\n")

forum_controller = 'src/controllers/forum_controller.py'

if os.path.exists(forum_controller):
    with open(forum_controller, 'r', encoding='utf-8') as f:
        forum_content = f.read()
    
    # Backup
    with open(forum_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(forum_content)
    
    # Add alias routes
    forum_aliases = '''

# Alias routes for compatibility
@forum_bp.route('/forum', methods=['GET'])
def forum_list_alias():
    """Alias for /forum/"""
    return redirect('/forum/')

@forum_bp.route('/forum/create', methods=['GET', 'POST'])
def create_forum():
    """Create a new forum"""
    user = session.get('user')
    if not user:
        flash('Please login first', 'error')
        return redirect('/auth/login')
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        new_forum = Forum(
            title=title,
            description=description,
            creator_id=user['id']
        )
        
        db.session.add(new_forum)
        db.session.commit()
        
        flash('Forum created successfully!', 'success')
        return redirect(f'/forum/{new_forum.id}')
    
    return render_template('forum/create.html')
'''
    
    # Insert before last line
    if 'if __name__' not in forum_content:
        forum_content += forum_aliases
    else:
        insert_pos = forum_content.rfind('if __name__')
        forum_content = forum_content[:insert_pos] + forum_aliases + '\n' + forum_content[insert_pos:]
    
    with open(forum_controller, 'w', encoding='utf-8') as f:
        f.write(forum_content)
    
    added_routes.extend(['forum', 'forum/create'])
    print(f"{Colors.GREEN}✓ Added forum alias routes{Colors.END}")

else:
    print(f"{Colors.RED}✗ forum_controller.py not found{Colors.END}")

# ============================================================================
# 5. EVENT ADMIN CONTROLLER - Add hyphenated routes
# ============================================================================
print(f"\n{Colors.YELLOW}5. Adding routes to event_admin_controller.py...{Colors.END}\n")

event_admin_controller = 'src/controllers/event_admin_controller.py'

if os.path.exists(event_admin_controller):
    with open(event_admin_controller, 'r', encoding='utf-8') as f:
        event_admin_content = f.read()
    
    # Backup
    with open(event_admin_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(event_admin_content)
    
    # Add hyphenated alias routes
    event_admin_aliases = '''

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
'''
    
    # Insert before last line
    if 'if __name__' not in event_admin_content:
        event_admin_content += event_admin_aliases
    else:
        insert_pos = event_admin_content.rfind('if __name__')
        event_admin_content = event_admin_content[:insert_pos] + event_admin_aliases + '\n' + event_admin_content[insert_pos:]
    
    with open(event_admin_controller, 'w', encoding='utf-8') as f:
        f.write(event_admin_content)
    
    added_routes.extend(['event-admin/dashboard', 'event-admin/events', 'event-admin/events/<id>/approve'])
    print(f"{Colors.GREEN}✓ Added event-admin alias routes{Colors.END}")

else:
    print(f"{Colors.RED}✗ event_admin_controller.py not found{Colors.END}")

# ============================================================================
# 6. SYSTEM MANAGER CONTROLLER - Add hyphenated routes
# ============================================================================
print(f"\n{Colors.YELLOW}6. Adding routes to system_manager_controller.py...{Colors.END}\n")

system_manager_controller = 'src/controllers/system_manager_controller.py'

if os.path.exists(system_manager_controller):
    with open(system_manager_controller, 'r', encoding='utf-8') as f:
        system_manager_content = f.read()
    
    # Backup
    with open(system_manager_controller + '.backup_routes', 'w', encoding='utf-8') as f:
        f.write(system_manager_content)
    
    # Add hyphenated alias routes
    system_manager_aliases = '''

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
'''
    
    # Insert before last line
    if 'if __name__' not in system_manager_content:
        system_manager_content += system_manager_aliases
    else:
        insert_pos = system_manager_content.rfind('if __name__')
        system_manager_content = system_manager_content[:insert_pos] + system_manager_aliases + '\n' + system_manager_content[insert_pos:]
    
    with open(system_manager_controller, 'w', encoding='utf-8') as f:
        f.write(system_manager_content)
    
    added_routes.extend(['system-manager/dashboard', 'system-manager/users/create', 'system-manager/reports/users'])
    print(f"{Colors.GREEN}✓ Added system-manager alias routes{Colors.END}")

else:
    print(f"{Colors.RED}✗ system_manager_controller.py not found{Colors.END}")

# Summary
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ MISSING ROUTES ADDED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.BOLD}Added {len(added_routes)} routes:{Colors.END}\n")
for route in added_routes:
    print(f"  {Colors.CYAN}✓{Colors.END} /{route}")

print(f"\n{Colors.BOLD}Backups created:{Colors.END}")
print(f"  All modified files have .backup_routes files\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.YELLOW}python create_missing_templates.py{Colors.END} - Create missing templates")
print(f"  2. {Colors.YELLOW}python verify_routes_correct.py{Colors.END} - Verify completion")
print(f"  3. {Colors.YELLOW}python app.py{Colors.END} - Restart Flask\n")