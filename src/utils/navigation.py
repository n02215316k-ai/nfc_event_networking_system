"""
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
