import os
import re
from collections import defaultdict

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ALL WORKING ROUTES BY USER ROLE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Scan all controllers
routes_by_blueprint = defaultdict(list)

# Scan app.py
print(f"{Colors.YELLOW}Scanning app.py...{Colors.END}")
if os.path.exists('app.py'):
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    app_routes = re.findall(r"@app\.route\('([^']+)'(?:,\s*methods=\[([^\]]+)\])?", content)
    for route, methods in app_routes:
        method_list = methods.replace("'", "").replace('"', '').split(',') if methods else ['GET']
        routes_by_blueprint['app'].append((route, method_list))

# Scan controllers
print(f"{Colors.YELLOW}Scanning controllers...{Colors.END}\n")
for root, dirs, files in os.walk('src/controllers'):
    for file in files:
        if file.endswith('_controller.py'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find blueprint name
            bp_match = re.search(r"(\w+)_bp\s*=\s*Blueprint\('(\w+)'", content)
            if bp_match:
                bp_var = bp_match.group(1)
                bp_name = bp_match.group(2)
                
                # Find routes
                route_pattern = rf"@{bp_var}_bp\.route\('([^']+)'(?:,\s*methods=\[([^\]]+)\])?"
                routes = re.findall(route_pattern, content)
                
                for route, methods in routes:
                    method_list = methods.replace("'", "").replace('"', '').split(',') if methods else ['GET']
                    routes_by_blueprint[bp_name].append((route, method_list))

# Organize routes by user role
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}ROUTES BY USER ROLE{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

# ==================== NOT LOGGED IN ====================
print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.MAGENTA}👤 NOT LOGGED IN (PUBLIC){Colors.END}")
print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}\n")

public_routes = [
    ('/', ['GET'], 'app', 'Home page'),
    ('/about', ['GET'], 'app', 'About page'),
    ('/auth/login', ['GET', 'POST'], 'auth', 'Login page'),
    ('/auth/signup', ['GET', 'POST'], 'auth', 'Sign up page'),
    ('/auth/register', ['GET', 'POST'], 'auth', 'Register (alias)'),
    ('/events', ['GET'], 'events', 'Browse events'),
    ('/events/<id>', ['GET'], 'events', 'View event details'),
]

for route, methods, blueprint, description in public_routes:
    methods_str = ', '.join(methods)
    print(f"{Colors.CYAN}{route:40}{Colors.END} {Colors.YELLOW}[{methods_str:15}]{Colors.END} {description}")

# ==================== ATTENDEE ====================
print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.BLUE}👤 ATTENDEE (Regular User){Colors.END}")
print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

attendee_routes = [
    ('/', ['GET'], 'app', 'Dashboard/Home'),
    ('/dashboard', ['GET'], 'app', 'Dashboard (redirects to /)'),
    ('/events', ['GET'], 'events', 'Browse all events'),
    ('/events/<id>', ['GET'], 'events', 'View event details'),
    ('/events/<id>/register', ['POST'], 'events', 'Register for event'),
    ('/profile/edit', ['GET', 'POST'], 'profile', 'Edit profile'),
    ('/profile/my-events', ['GET'], 'profile', 'My registered events'),
    ('/messages', ['GET'], 'messaging', 'Inbox'),
    ('/messages/compose', ['GET', 'POST'], 'messaging', 'Compose message'),
    ('/messages/send', ['POST'], 'messaging', 'Send message'),
    ('/messages/<id>', ['GET'], 'messaging', 'Read message'),
    ('/forum', ['GET'], 'forum', 'Forum list'),
    ('/forum/<id>', ['GET'], 'forum', 'View forum thread'),
    ('/forum/create', ['GET', 'POST'], 'forum', 'Create thread'),
    ('/nfc/scanner', ['GET'], 'nfc', 'NFC scanner'),
    ('/nfc/scan', ['POST'], 'nfc', 'Process NFC scan'),
    ('/auth/logout', ['GET'], 'auth', 'Logout'),
    ('/auth/change-password', ['GET', 'POST'], 'auth', 'Change password'),
]

for route, methods, blueprint, description in attendee_routes:
    methods_str = ', '.join(methods)
    print(f"{Colors.CYAN}{route:40}{Colors.END} {Colors.YELLOW}[{methods_str:15}]{Colors.END} {description}")

# ==================== ORGANIZER ====================
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}👤 ORGANIZER{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.YELLOW}All ATTENDEE routes plus:{Colors.END}\n")

organizer_routes = [
    ('/events/create', ['GET', 'POST'], 'events', 'Create new event'),
    ('/events/<id>/edit', ['GET', 'POST'], 'events', 'Edit own event'),
    ('/events/<id>/delete', ['POST'], 'events', 'Delete own event'),
    ('/events/<id>/attendees', ['GET'], 'events', 'View event attendees'),
]

for route, methods, blueprint, description in organizer_routes:
    methods_str = ', '.join(methods)
    print(f"{Colors.CYAN}{route:40}{Colors.END} {Colors.YELLOW}[{methods_str:15}]{Colors.END} {description}")

# ==================== EVENT ADMIN ====================
print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.MAGENTA}👤 EVENT ADMIN{Colors.END}")
print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}\n")

print(f"{Colors.YELLOW}All ORGANIZER routes plus:{Colors.END}\n")

event_admin_routes = [
    ('/event-admin/dashboard', ['GET'], 'event_admin', 'Event Admin dashboard'),
    ('/event-admin/events', ['GET'], 'event_admin', 'Manage all assigned events'),
    ('/event-admin/events/<id>', ['GET'], 'event_admin', 'Event details'),
    ('/event-admin/events/<id>/approve', ['POST'], 'event_admin', 'Approve event'),
    ('/event-admin/events/<id>/reject', ['POST'], 'event_admin', 'Reject event'),
]

for route, methods, blueprint, description in event_admin_routes:
    methods_str = ', '.join(methods)
    print(f"{Colors.CYAN}{route:40}{Colors.END} {Colors.YELLOW}[{methods_str:15}]{Colors.END} {description}")

# ==================== SYSTEM MANAGER ====================
print(f"\n{Colors.BOLD}{Colors.RED}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.RED}👤 SYSTEM MANAGER (Super Admin){Colors.END}")
print(f"{Colors.BOLD}{Colors.RED}{'='*80}{Colors.END}\n")

print(f"{Colors.YELLOW}All routes from all roles plus:{Colors.END}\n")

system_manager_routes = [
    ('/system-manager/dashboard', ['GET'], 'system_manager', 'System Manager dashboard'),
    ('/system-manager/users', ['GET'], 'system_manager', 'User management'),
    ('/system-manager/users/create', ['GET', 'POST'], 'system_manager', 'Create user'),
    ('/system-manager/users/<id>/edit', ['GET', 'POST'], 'system_manager', 'Edit user'),
    ('/system-manager/users/<id>/delete', ['POST'], 'system_manager', 'Delete user'),
    ('/system-manager/events', ['GET'], 'system_manager', 'All events management'),
    ('/system-manager/events/<id>', ['GET'], 'system_manager', 'Event details'),
    ('/system-manager/events/<id>/approve', ['POST'], 'system_manager', 'Approve event'),
    ('/system-manager/events/<id>/reject', ['POST'], 'system_manager', 'Reject event'),
    ('/system-manager/verifications', ['GET'], 'system_manager', 'User verifications'),
    ('/system-manager/verifications/<id>/approve', ['POST'], 'system_manager', 'Approve verification'),
    ('/system-manager/verifications/<id>/reject', ['POST'], 'system_manager', 'Reject verification'),
    ('/system-manager/reports', ['GET'], 'system_manager', 'System reports'),
    ('/system-manager/reports/users', ['GET'], 'system_manager', 'User reports'),
    ('/system-manager/reports/events', ['GET'], 'system_manager', 'Event reports'),
]

for route, methods, blueprint, description in system_manager_routes:
    methods_str = ', '.join(methods)
    print(f"{Colors.CYAN}{route:40}{Colors.END} {Colors.YELLOW}[{methods_str:15}]{Colors.END} {description}")

# ==================== ACTUAL DETECTED ROUTES ====================
print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ACTUALLY DETECTED ROUTES (FROM CODE){Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

for blueprint, routes in sorted(routes_by_blueprint.items()):
    if routes:
        print(f"{Colors.BOLD}{Colors.GREEN}Blueprint: {blueprint}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'─'*80}{Colors.END}")
        
        for route, methods in sorted(routes):
            methods_str = ', '.join(methods)
            full_route = f"/{blueprint}{route}" if blueprint != 'app' else route
            print(f"  {Colors.CYAN}{full_route:50}{Colors.END} {Colors.YELLOW}[{methods_str}]{Colors.END}")
        print()

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ROUTE LISTING COMPLETE{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.YELLOW}Note: Routes marked with <id> require an ID parameter{Colors.END}")
print(f"{Colors.YELLOW}Example: /events/123, /messages/456, etc.{Colors.END}\n")