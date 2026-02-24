import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATE DYNAMIC NAVIGATION SYSTEM{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Step 1: Create navigation helper in utils
utils_dir = 'src/utils'
os.makedirs(utils_dir, exist_ok=True)

nav_helper = '''"""
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
    
    # Common navigation for all logged-in users
    common_nav = [
        {'name': 'Home', 'url': '/', 'icon': 'fas fa-home'},
        {'name': 'Events', 'url': '/events', 'icon': 'fas fa-calendar'},
        {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
        {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
        {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
    ]
    
    # Role-specific navigation
    if role == 'system_manager':
        return [
            {'name': 'Dashboard', 'url': '/system-manager/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'Users', 'url': '/system-manager/users', 'icon': 'fas fa-users'},
            {'name': 'Events', 'url': '/system-manager/events', 'icon': 'fas fa-calendar-alt'},
            {'name': 'Verifications', 'url': '/system-manager/verifications', 'icon': 'fas fa-check-circle'},
            {'name': 'Reports', 'url': '/system-manager/reports', 'icon': 'fas fa-chart-bar'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
        ]
    
    elif role == 'event_admin':
        return [
            {'name': 'Dashboard', 'url': '/event-admin/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'My Events', 'url': '/event-admin/events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    elif role == 'organizer':
        return [
            {'name': 'Dashboard', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'NFC Scanner', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    else:  # attendee or default
        return common_nav


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
    
    dropdown = [
        {'name': 'My Profile', 'url': '/profile/edit', 'icon': 'fas fa-user'},
        {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar'},
        {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
        {'divider': True},
    ]
    
    # Add role-specific items
    if role in ['system_manager', 'event_admin']:
        dropdown.insert(0, {'name': 'Dashboard', 'url': f'/{role.replace("_", "-")}/dashboard', 'icon': 'fas fa-tachometer-alt'})
        dropdown.insert(1, {'divider': True})
    
    dropdown.extend([
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

nav_helper_path = os.path.join(utils_dir, 'navigation.py')
with open(nav_helper_path, 'w', encoding='utf-8') as f:
    f.write(nav_helper)

print(f"{Colors.GREEN}✓ Created: {nav_helper_path}{Colors.END}\n")

# Step 2: Update app.py to inject navigation
print(f"{Colors.BOLD}Updating app.py...{Colors.END}\n")

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Add import
import_line = 'from src.utils.navigation import get_user_navigation, get_user_dropdown, get_dashboard_url\n'

if import_line.strip() not in app_content:
    # Find where to add import
    import re
    last_import = None
    for match in re.finditer(r'^from src\.[^\n]+\n', app_content, re.MULTILINE):
        last_import = match
    
    if last_import:
        insert_pos = last_import.end()
        app_content = app_content[:insert_pos] + import_line + app_content[insert_pos:]
        print(f"{Colors.GREEN}✓ Added navigation import{Colors.END}")

# Add context processor
context_processor = '''
@app.context_processor
def inject_navigation():
    """Inject navigation items into all templates"""
    user = session.get('user')
    return {
        'nav_items': get_user_navigation(user),
        'user_dropdown': get_user_dropdown(user),
        'dashboard_url': get_dashboard_url(user),
        'current_user': user
    }

'''

if '@app.context_processor' not in app_content or 'inject_navigation' not in app_content:
    # Find where to insert (after imports, before first route)
    first_route = re.search(r'\n@app\.route', app_content)
    if first_route:
        insert_pos = first_route.start()
        app_content = app_content[:insert_pos] + '\n' + context_processor + app_content[insert_pos:]
        print(f"{Colors.GREEN}✓ Added navigation context processor{Colors.END}")

# Write updated app.py
with open('app.py.backup_nav', 'w', encoding='utf-8') as f:
    # Backup first
    with open('app.py', 'r', encoding='utf-8') as orig:
        f.write(orig.read())

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print(f"{Colors.GREEN}✓ Updated app.py{Colors.END}\n")

# Step 3: Create updated navigation template snippet
print(f"{Colors.BOLD}Creating navigation template...{Colors.END}\n")

nav_template = '''<!-- Dynamic Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <i class="fas fa-wifi"></i> NFC Events
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                {% for item in nav_items %}
                <li class="nav-item">
                    <a class="nav-link" href="{{ item.url }}">
                        <i class="{{ item.icon }}"></i> {{ item.name }}
                    </a>
                </li>
                {% endfor %}
            </ul>
            
            <ul class="navbar-nav">
                {% if current_user %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle"></i> {{ current_user.full_name }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        {% for item in user_dropdown %}
                            {% if item.divider %}
                            <li><hr class="dropdown-divider"></li>
                            {% else %}
                            <li>
                                <a class="dropdown-item" href="{{ item.url }}">
                                    <i class="{{ item.icon }}"></i> {{ item.name }}
                                </a>
                            </li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
'''

nav_snippet_path = 'templates/partials/navigation.html'
os.makedirs('templates/partials', exist_ok=True)

with open(nav_snippet_path, 'w', encoding='utf-8') as f:
    f.write(nav_template)

print(f"{Colors.GREEN}✓ Created: {nav_snippet_path}{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ DYNAMIC NAVIGATION SYSTEM CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}What was created:{Colors.END}")
print(f"  1. src/utils/navigation.py - Navigation logic")
print(f"  2. Updated app.py - Added context processor")
print(f"  3. templates/partials/navigation.html - Navigation template\n")

print(f"{Colors.BOLD}To use in your base template:{Colors.END}")
print(f'{Colors.CYAN}  Replace navbar with: {{% include "partials/navigation.html" %}}{Colors.END}\n')

print(f"{Colors.BOLD}Features:{Colors.END}")
print(f"  ✓ Different navigation for each role")
print(f"  ✓ System Manager sees admin links")
print(f"  ✓ Event Admin sees event management")
print(f"  ✓ Attendees see standard navigation")
print(f"  ✓ Dynamic dashboard links\n")

print(f"{Colors.YELLOW}Next: Update base.html to use the new navigation{Colors.END}\n")