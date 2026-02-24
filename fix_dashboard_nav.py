import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIX: ADD DASHBOARD TO NAVIGATION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

nav_helper_path = 'src/utils/navigation.py'

if not os.path.exists(nav_helper_path):
    print(f"{Colors.RED}❌ {nav_helper_path} not found!{Colors.END}\n")
    print(f"{Colors.YELLOW}Run create_dynamic_nav.py first!{Colors.END}\n")
    exit(1)

# Updated navigation helper with Dashboard always visible
updated_nav_helper = '''"""
Navigation Helper
Provides dynamic navigation based on user role
"""

def get_user_navigation(user):
    """
    Returns navigation items based on user role
    
    Args:
        user: Current user object with 'role' attribute
        
    Returns:
        List of navigation items with {name, url, icon}
    """
    if not user:
        # Not logged in
        return [
            {'name': 'Home', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'About', 'url': '/about', 'icon': 'fas fa-info-circle'},
            {'name': 'Login', 'url': '/auth/login', 'icon': 'fas fa-sign-in-alt'},
            {'name': 'Sign Up', 'url': '/auth/signup', 'icon': 'fas fa-user-plus'},
        ]
    
    role = user.get('role', 'attendee')
    
    # Role-specific navigation with Dashboard first
    if role == 'system_manager':
        return [
            {'name': 'Dashboard', 'url': '/system-manager/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'Users', 'url': '/system-manager/users', 'icon': 'fas fa-users'},
            {'name': 'Events', 'url': '/system-manager/events', 'icon': 'fas fa-calendar-alt'},
            {'name': 'Verifications', 'url': '/system-manager/verifications', 'icon': 'fas fa-check-circle'},
            {'name': 'Reports', 'url': '/system-manager/reports', 'icon': 'fas fa-chart-bar'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
        ]
    
    elif role == 'event_admin':
        return [
            {'name': 'Dashboard', 'url': '/event-admin/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'My Events', 'url': '/event-admin/events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'All Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    elif role == 'organizer':
        return [
            {'name': 'Dashboard', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'All Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    else:  # attendee or default
        return [
            {'name': 'Dashboard', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]


def get_user_dropdown(user):
    """
    Returns dropdown menu items for user profile section
    
    Args:
        user: Current user object
        
    Returns:
        List of dropdown items
    """
    if not user:
        return []
    
    role = user.get('role', 'attendee')
    
    dropdown = []
    
    # Add Dashboard link to dropdown as well
    dashboard_url = get_dashboard_url(user)
    if dashboard_url != '/':
        dropdown.append({'name': 'Dashboard', 'url': dashboard_url, 'icon': 'fas fa-tachometer-alt'})
        dropdown.append({'divider': True})
    
    dropdown.extend([
        {'name': 'My Profile', 'url': '/profile/edit', 'icon': 'fas fa-user'},
        {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar'},
        {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
        {'divider': True},
        {'name': 'Change Password', 'url': '/auth/change-password', 'icon': 'fas fa-key'},
        {'name': 'Logout', 'url': '/auth/logout', 'icon': 'fas fa-sign-out-alt'},
    ])
    
    return dropdown


def get_dashboard_url(user):
    """
    Returns the appropriate dashboard URL based on user role
    
    Args:
        user: Current user object
        
    Returns:
        Dashboard URL string
    """
    if not user:
        return '/'
    
    role = user.get('role', 'attendee')
    
    dashboards = {
        'system_manager': '/system-manager/dashboard',
        'event_admin': '/event-admin/dashboard',
        'organizer': '/',
        'attendee': '/',
    }
    
    return dashboards.get(role, '/')
'''

# Backup original
with open(nav_helper_path + '.backup', 'w', encoding='utf-8') as f:
    with open(nav_helper_path, 'r', encoding='utf-8') as orig:
        f.write(orig.read())

# Write updated version
with open(nav_helper_path, 'w', encoding='utf-8') as f:
    f.write(updated_nav_helper)

print(f"{Colors.GREEN}✓ Updated: {nav_helper_path}{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ DASHBOARD ADDED TO NAVIGATION!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Navigation now shows:{Colors.END}\n")

print(f"{Colors.BOLD}System Manager:{Colors.END}")
print(f"  • Dashboard → /system-manager/dashboard")
print(f"  • Users, Events, Verifications, Reports, etc.\n")

print(f"{Colors.BOLD}Event Admin:{Colors.END}")
print(f"  • Dashboard → /event-admin/dashboard")
print(f"  • My Events, Create Event, etc.\n")

print(f"{Colors.BOLD}Organizer/Attendee:{Colors.END}")
print(f"  • Dashboard → / (home)")
print(f"  • Events, My Events, Messages, etc.\n")

print(f"{Colors.YELLOW}Dashboard appears as FIRST item for all users!{Colors.END}\n")

print(f"{Colors.BOLD}Restart Flask:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")