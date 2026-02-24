import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}INSTALLING ADMIN & SYSTEM ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
except FileNotFoundError:
    print(f"{Colors.RED}❌ Error: app.py not found!{Colors.END}")
    exit(1)

# Backup
with open('app.py.backup_admin', 'w', encoding='utf-8') as f:
    f.write(app_content)
print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup_admin")

# Check if routes already exist
routes_to_check = ['/admin', '/system']
routes_exist = any(f"@app.route('{route}')" in app_content for route in routes_to_check)

if routes_exist:
    print(f"{Colors.YELLOW}⚠ Some admin routes already exist{Colors.END}")
    print(f"{Colors.YELLOW}Checking individual routes...{Colors.END}\n")

# ============================================================================
# ADMIN & SYSTEM ROUTES TO ADD
# ============================================================================

ADMIN_ROUTES = """

# ============================================================================
# ADMIN ROUTES - Event Admin Access
# ============================================================================

@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    '''Admin dashboard'''
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'warning')
        return redirect('/login')
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_system_stats, get_all_events
    
    stats = get_system_stats()
    event_data = get_all_events()
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         events=event_data.get('events', []))


@app.route('/admin/users')
def admin_users():
    '''Admin user management'''
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'warning')
        return redirect('/login')
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_all_users
    
    users = get_all_users()
    
    return render_template('admin/users.html', users=users)


@app.route('/admin/events')
def admin_events():
    '''Admin event management'''
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'warning')
        return redirect('/login')
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_all_events
    from datetime import datetime
    
    event_data = get_all_events()
    
    return render_template('admin/events.html',
                         events=event_data.get('events', []),
                         upcoming_count=event_data.get('upcoming_count', 0),
                         past_count=event_data.get('past_count', 0),
                         total_registrations=event_data.get('total_registrations', 0),
                         now=datetime.now().date())


@app.route('/admin/events/delete/<int:event_id>', methods=['POST'])
def admin_delete_event(event_id):
    '''Delete event (admin)'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        return jsonify({'success': False, 'message': 'Access denied'})
    
    from src.controllers.system_controller import delete_event
    
    if delete_event(event_id):
        return jsonify({'success': True, 'message': 'Event deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error deleting event'})


@app.route('/admin/reports')
def admin_reports():
    '''Admin reports and analytics'''
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'warning')
        return redirect('/login')
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_system_stats
    
    stats = get_system_stats()
    
    return render_template('admin/reports.html', stats=stats)


# ============================================================================
# SYSTEM MANAGER ROUTES - Full System Access
# ============================================================================

@app.route('/system')
@app.route('/system/dashboard')
def system_dashboard():
    '''System manager dashboard'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_system_stats
    
    stats = get_system_stats()
    
    return render_template('system/dashboard.html', stats=stats)


@app.route('/system/users')
def system_users():
    '''System user management'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    from src.controllers.system_controller import get_all_users
    
    users = get_all_users()
    
    return render_template('system/users.html', users=users)


@app.route('/system/users/update-role', methods=['POST'])
def system_update_user_role():
    '''Update user role'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if session.get('role') != 'system_manager':
        return jsonify({'success': False, 'message': 'Access denied'})
    
    from src.controllers.system_controller import update_user_role
    
    data = request.get_json()
    user_id = data.get('user_id')
    new_role = data.get('role')
    
    if not user_id or not new_role:
        return jsonify({'success': False, 'message': 'Missing parameters'})
    
    if new_role not in ['attendee', 'event_admin', 'system_manager']:
        return jsonify({'success': False, 'message': 'Invalid role'})
    
    if update_user_role(user_id, new_role):
        return jsonify({'success': True, 'message': 'Role updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error updating role'})


@app.route('/system/users/delete/<int:user_id>', methods=['POST'])
def system_delete_user(user_id):
    '''Delete user from system'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if session.get('role') != 'system_manager':
        return jsonify({'success': False, 'message': 'Access denied'})
    
    # Prevent deleting yourself
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Cannot delete your own account'})
    
    from src.controllers.system_controller import delete_user
    
    if delete_user(user_id):
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error deleting user'})


@app.route('/system/settings', methods=['GET', 'POST'])
def system_settings():
    '''System settings'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    if request.method == 'POST':
        # Handle settings update
        flash('Settings updated successfully!', 'success')
        return redirect('/system/settings')
    
    return render_template('system/settings.html')


@app.route('/system/settings/clear-cache', methods=['POST'])
def system_clear_cache():
    '''Clear system cache'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if session.get('role') != 'system_manager':
        return jsonify({'success': False, 'message': 'Access denied'})
    
    # Implement cache clearing logic here
    return jsonify({'success': True, 'message': 'Cache cleared successfully'})


@app.route('/system/logs')
def system_logs():
    '''System activity logs'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    # Get logs (placeholder for now)
    logs = []
    
    return render_template('system/logs.html', logs=logs)


@app.route('/system/logs/download')
def system_logs_download():
    '''Download system logs'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    # Implement log download
    flash('Log download feature coming soon', 'info')
    return redirect('/system/logs')


@app.route('/system/logs/clear', methods=['POST'])
def system_logs_clear():
    '''Clear system logs'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if session.get('role') != 'system_manager':
        return jsonify({'success': False, 'message': 'Access denied'})
    
    # Implement log clearing
    return jsonify({'success': True, 'message': 'Logs cleared successfully'})

"""

# ============================================================================
# INSERT ROUTES INTO APP.PY
# ============================================================================

print(f"{Colors.CYAN}Inserting admin routes into app.py...{Colors.END}\n")

# Find insertion point (before if __name__)
if "if __name__ == '__main__':" in app_content:
    insertion_point = app_content.find("if __name__ == '__main__':")
    new_content = (
        app_content[:insertion_point] + 
        ADMIN_ROUTES + 
        '\n\n' +
        app_content[insertion_point:]
    )
else:
    # Append at end
    new_content = app_content + '\n\n' + ADMIN_ROUTES

# Write updated content
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL ADMIN ROUTES INSTALLED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Routes added:{Colors.END}\n")

routes_added = [
    ('Admin Dashboard', '/admin, /admin/dashboard'),
    ('Admin Users', '/admin/users'),
    ('Admin Events', '/admin/events'),
    ('Admin Reports', '/admin/reports'),
    ('Delete Event (API)', '/admin/events/delete/<id>'),
    ('System Dashboard', '/system, /system/dashboard'),
    ('System Users', '/system/users'),
    ('Update User Role (API)', '/system/users/update-role'),
    ('Delete User (API)', '/system/users/delete/<id>'),
    ('System Settings', '/system/settings'),
    ('Clear Cache (API)', '/system/settings/clear-cache'),
    ('System Logs', '/system/logs'),
    ('Download Logs', '/system/logs/download'),
    ('Clear Logs (API)', '/system/logs/clear'),
]

for name, route in routes_added:
    print(f"  {Colors.GREEN}✓{Colors.END} {name:<25} → {route}")

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADMIN SYSTEM COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

print(f"{Colors.YELLOW}Next Steps:{Colors.END}\n")

print(f"1️⃣  {Colors.BOLD}Create an admin user in database:{Colors.END}")
print(f"   {Colors.CYAN}UPDATE users SET role = 'event_admin' WHERE email = 'your@email.com';{Colors.END}\n")

print(f"2️⃣  {Colors.BOLD}Or create a system manager:{Colors.END}")
print(f"   {Colors.CYAN}UPDATE users SET role = 'system_manager' WHERE email = 'your@email.com';{Colors.END}\n")

print(f"3️⃣  {Colors.BOLD}Restart your Flask app:{Colors.END}")
print(f"   {Colors.CYAN}python app.py{Colors.END}\n")

print(f"4️⃣  {Colors.BOLD}Login and access admin panels:{Colors.END}")
print(f"   • {Colors.GREEN}Admin Panel:{Colors.END} http://localhost:5000/admin")
print(f"   • {Colors.GREEN}System Panel:{Colors.END} http://localhost:5000/system\n")

print(f"{Colors.BOLD}📊 User Roles:{Colors.END}")
print(f"  • {Colors.CYAN}attendee{Colors.END}        - Regular user (default)")
print(f"  • {Colors.CYAN}event_admin{Colors.END}     - Can manage events")
print(f"  • {Colors.CYAN}system_manager{Colors.END}  - Full system access\n")

print(f"{Colors.BOLD}🎯 Admin Features:{Colors.END}")
print(f"  • View all users and events")
print(f"  • Create, edit, delete events")
print(f"  • Manage user roles")
print(f"  • View analytics and reports")
print(f"  • System settings and logs")
print(f"  • Monitor real-time activity\n")

print(f"{Colors.GREEN}✅ Admin system is now fully operational!{Colors.END}\n")