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

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}COMPREHENSIVE ROUTE VERIFICATION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.END}\n")

# All routes from the specification
routes_to_verify = {
    'public': [
        ('/', 'GET', 'Home page', 'index.html or home.html'),
        ('/about', 'GET', 'About page', 'about.html'),
        ('/auth/login', 'GET,POST', 'Login', 'auth/login.html'),
        ('/auth/signup', 'GET,POST', 'Signup', 'auth/signup.html'),
        ('/events', 'GET', 'Browse events', 'events/list.html'),
        ('/events/<id>', 'GET', 'Event details', 'events/detail.html'),
    ],
    'attendee': [
        ('/profile/edit', 'GET,POST', 'Edit profile', 'profile/edit.html'),
        ('/profile/my-events', 'GET', 'My events', 'profile/my-events.html'),
        ('/messages', 'GET', 'Inbox', 'messaging/inbox.html'),
        ('/messages/compose', 'GET,POST', 'Compose', 'messaging/compose.html'),
        ('/messages/<id>', 'GET', 'Read message', 'messaging/conversation.html'),
        ('/forum', 'GET', 'Forum list', 'forum/list.html'),
        ('/forum/<id>', 'GET', 'Forum thread', 'forum/detail.html'),
        ('/forum/create', 'GET,POST', 'Create thread', 'forum/create.html'),
        ('/nfc/scanner', 'GET', 'NFC scanner', 'nfc/scanner.html'),
        ('/nfc/scan', 'POST', 'Process scan', None),
        ('/auth/change-password', 'GET,POST', 'Change password', 'auth/change-password.html'),
    ],
    'organizer': [
        ('/events/create', 'GET,POST', 'Create event', 'events/create.html'),
        ('/events/<id>/edit', 'GET,POST', 'Edit event', 'events/edit.html'),
        ('/events/<id>/delete', 'POST', 'Delete event', None),
        ('/events/<id>/attendees', 'GET', 'Event attendees', 'events/attendees.html'),
    ],
    'event_admin': [
        ('/event-admin/dashboard', 'GET', 'Dashboard', 'event_admin/dashboard.html'),
        ('/event-admin/events', 'GET', 'Events list', 'event_admin/events.html'),
        ('/event-admin/events/<id>', 'GET', 'Event detail', 'event_admin/event.html'),
    ],
    'system_manager': [
        ('/system-manager/dashboard', 'GET', 'Dashboard', 'system_manager/dashboard.html'),
        ('/system-manager/users', 'GET', 'User list', 'system_manager/users.html'),
        ('/system-manager/users/create', 'GET,POST', 'Create user', 'system_manager/user_form.html'),
        ('/system-manager/users/<id>/edit', 'GET,POST', 'Edit user', 'system_manager/user_form.html'),
        ('/system-manager/events', 'GET', 'Events', 'system_manager/events.html'),
        ('/system-manager/verifications', 'GET', 'Verifications', 'system_manager/verifications.html'),
        ('/system-manager/reports', 'GET', 'Reports', 'system_manager/reports.html'),
    ],
}

# Function to check if controller exists
def check_controller(blueprint_name):
    controller_path = f'src/controllers/{blueprint_name}_controller.py'
    return os.path.exists(controller_path), controller_path

# Function to check if template exists
def check_template(template_path):
    if not template_path:
        return True, None  # No template needed
    
    full_path = f'templates/{template_path}'
    exists = os.path.exists(full_path)
    return exists, full_path

# Function to check if route exists in controller
def check_route_in_controller(controller_path, route_pattern):
    if not os.path.exists(controller_path):
        return False
    
    with open(controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean up route pattern for regex
    pattern = route_pattern.replace('<id>', '<int:\\w+>')
    pattern = pattern.replace('/', '\\/')
    
    # Check for route definition
    route_regex = rf"@\w+_bp\.route\('{pattern}'"
    return bool(re.search(route_regex, content))

# Function to find blueprint from route
def get_blueprint_from_route(route):
    if route.startswith('/auth/'):
        return 'auth'
    elif route.startswith('/events/'):
        return 'events'
    elif route.startswith('/profile/'):
        return 'profile'
    elif route.startswith('/messages/') or route.startswith('/messaging/'):
        return 'messaging'
    elif route.startswith('/forum/'):
        return 'forum'
    elif route.startswith('/nfc/'):
        return 'nfc'
    elif route.startswith('/event-admin/'):
        return 'event_admin'
    elif route.startswith('/system-manager/'):
        return 'system_manager'
    else:
        return 'app'

# Verification results
results = {
    'total': 0,
    'controller_exists': 0,
    'route_exists': 0,
    'template_exists': 0,
    'fully_implemented': 0,
    'missing_controller': [],
    'missing_route': [],
    'missing_template': [],
}

print(f"{Colors.BOLD}Legend:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} = Exists/Implemented")
print(f"  {Colors.RED}✗{Colors.END} = Missing")
print(f"  {Colors.YELLOW}~{Colors.END} = Not required\n")

# Verify each route
for role, routes in routes_to_verify.items():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}ROLE: {role.upper()}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.END}\n")
    
    print(f"{'Route':<40} {'Controller':<15} {'Route Logic':<15} {'Template':<20} Status")
    print(f"{'-'*40} {'-'*15} {'-'*15} {'-'*20} {'-'*20}")
    
    for route, methods, description, template in routes:
        results['total'] += 1
        
        # Get blueprint
        blueprint = get_blueprint_from_route(route)
        
        # Check controller
        controller_exists, controller_path = check_controller(blueprint)
        controller_status = f"{Colors.GREEN}✓{Colors.END}" if controller_exists else f"{Colors.RED}✗{Colors.END}"
        
        # Check route in controller
        route_exists = check_route_in_controller(controller_path, route) if controller_exists else False
        route_status = f"{Colors.GREEN}✓{Colors.END}" if route_exists else f"{Colors.RED}✗{Colors.END}"
        
        # Check template
        template_exists, template_path = check_template(template)
        if template is None:
            template_status = f"{Colors.YELLOW}~{Colors.END}"
        else:
            template_status = f"{Colors.GREEN}✓{Colors.END}" if template_exists else f"{Colors.RED}✗{Colors.END}"
        
        # Overall status
        if controller_exists:
            results['controller_exists'] += 1
        else:
            results['missing_controller'].append((route, blueprint))
        
        if route_exists:
            results['route_exists'] += 1
        else:
            results['missing_route'].append((route, blueprint))
        
        if template_exists or template is None:
            results['template_exists'] += 1
        else:
            results['missing_template'].append((route, template))
        
        if controller_exists and route_exists and (template_exists or template is None):
            results['fully_implemented'] += 1
            overall = f"{Colors.GREEN}COMPLETE{Colors.END}"
        else:
            overall = f"{Colors.RED}INCOMPLETE{Colors.END}"
        
        # Print row
        route_display = route[:38] + '..' if len(route) > 40 else route
        blueprint_display = blueprint[:13] + '..' if len(blueprint) > 15 else blueprint
        
        print(f"{route_display:<40} {controller_status} {blueprint_display:<13} {route_status} {'Route logic':<13} {template_status} {template or 'N/A':<18} {overall}")

# Summary
print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}VERIFICATION SUMMARY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.END}\n")

print(f"{Colors.BOLD}Overall Statistics:{Colors.END}")
print(f"  Total routes verified: {results['total']}")
print(f"  Fully implemented: {Colors.GREEN}{results['fully_implemented']}{Colors.END} ({results['fully_implemented']/results['total']*100:.1f}%)")
print(f"  Controllers exist: {Colors.GREEN}{results['controller_exists']}{Colors.END}/{results['total']}")
print(f"  Routes implemented: {Colors.GREEN}{results['route_exists']}{Colors.END}/{results['total']}")
print(f"  Templates exist: {Colors.GREEN}{results['template_exists']}{Colors.END}/{results['total']}\n")

# Missing items
if results['missing_controller']:
    print(f"{Colors.BOLD}{Colors.RED}Missing Controllers:{Colors.END}")
    for route, blueprint in results['missing_controller']:
        print(f"  {Colors.RED}✗{Colors.END} {blueprint}_controller.py for route: {route}")
    print()

if results['missing_route']:
    print(f"{Colors.BOLD}{Colors.RED}Missing Route Logic:{Colors.END}")
    for route, blueprint in results['missing_route'][:10]:  # Show first 10
        print(f"  {Colors.RED}✗{Colors.END} Route {route} not found in {blueprint}_controller.py")
    if len(results['missing_route']) > 10:
        print(f"  ... and {len(results['missing_route']) - 10} more")
    print()

if results['missing_template']:
    print(f"{Colors.BOLD}{Colors.RED}Missing Templates:{Colors.END}")
    for route, template in results['missing_template'][:10]:  # Show first 10
        print(f"  {Colors.RED}✗{Colors.END} templates/{template}")
    if len(results['missing_template']) > 10:
        print(f"  ... and {len(results['missing_template']) - 10} more")
    print()

# Recommendations
print(f"{Colors.BOLD}{Colors.YELLOW}Recommendations:{Colors.END}\n")

if results['fully_implemented'] == results['total']:
    print(f"  {Colors.GREEN}✓ All routes are fully implemented! Great job!{Colors.END}\n")
else:
    completion_rate = results['fully_implemented'] / results['total'] * 100
    
    if completion_rate >= 80:
        print(f"  {Colors.GREEN}System is {completion_rate:.1f}% complete - Almost there!{Colors.END}")
    elif completion_rate >= 60:
        print(f"  {Colors.YELLOW}System is {completion_rate:.1f}% complete - Good progress{Colors.END}")
    else:
        print(f"  {Colors.RED}System is {completion_rate:.1f}% complete - Needs work{Colors.END}")
    
    print(f"\n  Priority fixes:")
    if results['missing_controller']:
        print(f"    1. Create missing controllers")
    if results['missing_route']:
        print(f"    2. Implement missing route logic")
    if results['missing_template']:
        print(f"    3. Create missing templates")
    print()

print(f"{Colors.BOLD}{Colors.GREEN}{'='*100}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ VERIFICATION COMPLETE{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*100}{Colors.END}\n")