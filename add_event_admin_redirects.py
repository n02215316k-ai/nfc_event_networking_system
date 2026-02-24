class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADDING EVENT ADMIN REDIRECTS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_event_admin', 'w', encoding='utf-8') as f:
    f.write(content)

event_admin_redirects = '''
# Redirect /admin based on user role
@app.route('/admin')
@app.route('/admin/')
def smart_admin_redirect():
    """Redirect /admin to appropriate dashboard based on role"""
    user = session.get('user')
    if user:
        role = user.get('role')
        if role == 'system_manager':
            return redirect('/system-manager/dashboard')
        elif role == 'event_admin':
            return redirect('/event-admin/dashboard')
    return redirect('/')

@app.route('/admin/dashboard')
def admin_dashboard_redirect():
    """Smart redirect for /admin/dashboard"""
    user = session.get('user')
    if user:
        role = user.get('role')
        if role == 'system_manager':
            return redirect('/system-manager/dashboard')
        elif role == 'event_admin':
            return redirect('/event-admin/dashboard')
    return redirect('/')

@app.route('/admin/events')
def admin_events_redirect():
    """Smart redirect for /admin/events"""
    user = session.get('user')
    if user:
        role = user.get('role')
        if role == 'system_manager':
            return redirect('/system-manager/events')
        elif role == 'event_admin':
            return redirect('/event-admin/events')
    return redirect('/events')

@app.route('/admin/users')
@app.route('/admin/users/create')
def admin_users_redirect():
    """Redirect to system-manager users (only for system_manager)"""
    user = session.get('user')
    if user and user.get('role') == 'system_manager':
        return redirect('/system-manager/users')
    return redirect('/')

@app.route('/admin/reports')
def admin_reports_redirect():
    """Redirect to system-manager reports (only for system_manager)"""
    user = session.get('user')
    if user and user.get('role') == 'system_manager':
        return redirect('/system-manager/reports')
    return redirect('/')

@app.route('/admin/verifications')
def admin_verifications_redirect():
    """Redirect to system-manager verifications (only for system_manager)"""
    user = session.get('user')
    if user and user.get('role') == 'system_manager':
        return redirect('/system-manager/verifications')
    return redirect('/')

'''

# Remove old redirects if they exist
import re
content = re.sub(r'@app\.route\(\'/admin.*?return redirect\([^\)]+\)\s*\n', '', content, flags=re.DOTALL)

# Find where to insert
main_block = re.search(r'\nif __name__ == [\'"]__main__[\'"]:', content)

if main_block:
    insert_pos = main_block.start()
    content = content[:insert_pos] + event_admin_redirects + content[insert_pos:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓ Added smart /admin redirects{Colors.END}\n")
    
    print(f"{Colors.CYAN}Smart redirects added:{Colors.END}")
    print(f"  /admin → Redirects based on user role")
    print(f"  /admin/dashboard → Role-specific dashboard")
    print(f"  /admin/events → Role-specific events page\n")
    
    print(f"{Colors.YELLOW}System Manager redirects to: /system-manager/*{Colors.END}")
    print(f"{Colors.YELLOW}Event Admin redirects to: /event-admin/*{Colors.END}\n")
else:
    print(f"{Colors.RED}Could not find insertion point{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}✅ DONE!{Colors.END}\n")