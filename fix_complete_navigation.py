import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}COMPLETE NAVIGATION FIX{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Complete navigation helper with ALL features
complete_nav = '''"""
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
    
    # Role-specific navigation
    if role == 'system_manager':
        return [
            {'name': 'Dashboard', 'url': '/system-manager/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'Users', 'url': '/system-manager/users', 'icon': 'fas fa-users'},
            {'name': 'Events', 'url': '/system-manager/events', 'icon': 'fas fa-calendar-alt'},
            {'name': 'Verifications', 'url': '/system-manager/verifications', 'icon': 'fas fa-check-circle'},
            {'name': 'Reports', 'url': '/system-manager/reports', 'icon': 'fas fa-chart-bar'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'Scan', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    elif role == 'event_admin':
        return [
            {'name': 'Dashboard', 'url': '/event-admin/dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'My Events', 'url': '/event-admin/events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'All Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'Scan', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    elif role == 'organizer':
        return [
            {'name': 'Dashboard', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Create Event', 'url': '/events/create', 'icon': 'fas fa-plus-circle'},
            {'name': 'Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'Scan', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
        ]
    
    else:  # attendee or default
        return [
            {'name': 'Dashboard', 'url': '/', 'icon': 'fas fa-home'},
            {'name': 'Events', 'url': '/events', 'icon': 'fas fa-calendar'},
            {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar-check'},
            {'name': 'Messages', 'url': '/messages', 'icon': 'fas fa-envelope'},
            {'name': 'Forum', 'url': '/forum', 'icon': 'fas fa-comments'},
            {'name': 'Scan', 'url': '/nfc/scanner', 'icon': 'fas fa-qrcode'},
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
    
    dropdown = [
        {'name': 'My Profile', 'url': '/profile/edit', 'icon': 'fas fa-user'},
        {'name': 'My Events', 'url': '/profile/my-events', 'icon': 'fas fa-calendar'},
        {'name': 'Settings', 'url': '/profile/edit', 'icon': 'fas fa-cog'},
        {'divider': True},
        {'name': 'Change Password', 'url': '/auth/change-password', 'icon': 'fas fa-key'},
        {'divider': True},
        {'name': 'Logout', 'url': '/auth/logout', 'icon': 'fas fa-sign-out-alt'},
    ]
    
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

# Write to navigation.py
nav_path = 'src/utils/navigation.py'
os.makedirs(os.path.dirname(nav_path), exist_ok=True)

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(complete_nav)

print(f"{Colors.GREEN}✓ Updated: {nav_path}{Colors.END}\n")

# Now update the navigation template to show dropdown properly
nav_template = '''<!-- Dynamic Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ dashboard_url if current_user else '/' }}">
            <i class="fas fa-wifi"></i> NFC Events
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <!-- Main Navigation -->
            <ul class="navbar-nav me-auto">
                {% for item in nav_items %}
                <li class="nav-item">
                    <a class="nav-link" href="{{ item.url }}">
                        <i class="{{ item.icon }}"></i> {{ item.name }}
                    </a>
                </li>
                {% endfor %}
            </ul>
            
            <!-- User Dropdown (Right Side) -->
            <ul class="navbar-nav">
                {% if current_user %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" 
                       data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-user-circle"></i> {{ current_user.full_name }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
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
                {% else %}
                <!-- Not logged in - show Login/Signup -->
                <li class="nav-item">
                    <a class="nav-link" href="/auth/login">
                        <i class="fas fa-sign-in-alt"></i> Login
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/auth/signup">
                        <i class="fas fa-user-plus"></i> Sign Up
                    </a>
                </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
'''

nav_template_path = 'templates/partials/navigation.html'
os.makedirs(os.path.dirname(nav_template_path), exist_ok=True)

with open(nav_template_path, 'w', encoding='utf-8') as f:
    f.write(nav_template)

print(f"{Colors.GREEN}✓ Updated: {nav_template_path}{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ COMPLETE NAVIGATION RESTORED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Main Navigation Items:{Colors.END}")
print(f"  ✓ Dashboard (role-specific)")
print(f"  ✓ Events/My Events")
print(f"  ✓ Messages")
print(f"  ✓ Forum")
print(f"  ✓ Scan (NFC Scanner)\n")

print(f"{Colors.CYAN}User Dropdown Menu:{Colors.END}")
print(f"  ✓ My Profile")
print(f"  ✓ My Events")
print(f"  ✓ Settings")
print(f"  ✓ Change Password")
print(f"  ✓ Logout\n")

print(f"{Colors.BOLD}Restart Flask:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")