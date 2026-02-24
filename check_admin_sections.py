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
print(f"{Colors.BOLD}{Colors.CYAN}ADMIN & SYSTEM ADMIN SECTIONS CHECK{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
except FileNotFoundError:
    print(f"{Colors.RED}❌ app.py not found!{Colors.END}")
    exit(1)

# Check for admin-related files
admin_files = {
    'Controllers': [
        'src/controllers/admin_controller.py',
        'src/controllers/system_controller.py'
    ],
    'Templates': [
        'templates/admin/dashboard.html',
        'templates/admin/users.html',
        'templates/admin/events.html',
        'templates/admin/reports.html',
        'templates/system/dashboard.html',
        'templates/system/users.html',
        'templates/system/settings.html',
        'templates/system/logs.html'
    ]
}

print(f"{Colors.BOLD}📁 Checking Admin Files:{Colors.END}\n")

missing_files = []
existing_files = []

for category, files in admin_files.items():
    print(f"{Colors.CYAN}{category}:{Colors.END}")
    for file_path in files:
        if os.path.exists(file_path):
            print(f"  {Colors.GREEN}✓{Colors.END} {file_path}")
            existing_files.append(file_path)
        else:
            print(f"  {Colors.RED}✗{Colors.END} {file_path} (MISSING)")
            missing_files.append(file_path)
    print()

# Check admin routes in app.py
print(f"{Colors.BOLD}🔍 Checking Admin Routes in app.py:{Colors.END}\n")

admin_routes = {
    '/admin': 'Admin Dashboard',
    '/admin/dashboard': 'Admin Dashboard (alt)',
    '/admin/users': 'User Management',
    '/admin/events': 'Event Management',
    '/admin/reports': 'Reports',
    '/system': 'System Manager Dashboard',
    '/system/dashboard': 'System Dashboard (alt)',
    '/system/users': 'System User Management',
    '/system/settings': 'System Settings',
    '/system/logs': 'System Logs'
}

missing_routes = []
existing_routes = []

for route, description in admin_routes.items():
    route_pattern = f"@app.route\\('{route}'\\)"
    if re.search(route_pattern, app_content):
        print(f"  {Colors.GREEN}✓{Colors.END} {route} - {description}")
        existing_routes.append(route)
    else:
        print(f"  {Colors.RED}✗{Colors.END} {route} - {description} (MISSING)")
        missing_routes.append((route, description))

# Check for role decorators
print(f"\n{Colors.BOLD}🔐 Checking Role-Based Access Control:{Colors.END}\n")

decorators = {
    '@admin_required': 'Admin access decorator',
    '@system_manager_required': 'System manager decorator',
    'role_required': 'Generic role decorator',
    'check_role': 'Role check function'
}

for decorator, description in decorators.items():
    if decorator in app_content or decorator.replace('@', 'def ') in app_content:
        print(f"  {Colors.GREEN}✓{Colors.END} {description}")
    else:
        print(f"  {Colors.YELLOW}⚠{Colors.END} {description} (NOT FOUND)")

# Check database tables for admin features
print(f"\n{Colors.BOLD}🗄️ Required Database Tables for Admin:{Colors.END}\n")

required_tables = [
    'users (with role column)',
    'events',
    'event_registrations',
    'connections',
    'nfc_scans',
    'forums',
    'forum_posts',
    'messages',
    'system_logs (optional)',
    'admin_actions (optional)'
]

for table in required_tables:
    print(f"  {Colors.CYAN}•{Colors.END} {table}")

# Summary
print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}SUMMARY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

print(f"{Colors.BOLD}Files Status:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Existing: {len(existing_files)}")
print(f"  {Colors.RED}✗{Colors.END} Missing: {len(missing_files)}")

print(f"\n{Colors.BOLD}Routes Status:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Existing: {len(existing_routes)}")
print(f"  {Colors.RED}✗{Colors.END} Missing: {len(missing_routes)}")

if missing_files or missing_routes:
    print(f"\n{Colors.BOLD}{Colors.RED}❌ ADMIN SECTIONS ARE INCOMPLETE{Colors.END}")
    print(f"\n{Colors.YELLOW}Would you like me to create the missing admin components?{Colors.END}")
else:
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ ALL ADMIN SECTIONS ARE COMPLETE{Colors.END}")

# Test recommendations
print(f"\n{Colors.BOLD}🧪 To Test Admin Sections:{Colors.END}")
print(f"\n1. Create an admin user in database:")
print(f"   {Colors.CYAN}UPDATE users SET role = 'event_admin' WHERE email = 'your@email.com';{Colors.END}")
print(f"\n2. Create a system manager:")
print(f"   {Colors.CYAN}UPDATE users SET role = 'system_manager' WHERE email = 'your@email.com';{Colors.END}")
print(f"\n3. Login and try accessing:")
print(f"   • http://localhost:5000/admin")
print(f"   • http://localhost:5000/system")

print(f"\n{Colors.BOLD}📊 User Roles in System:{Colors.END}")
print(f"  • {Colors.CYAN}attendee{Colors.END} - Regular user")
print(f"  • {Colors.CYAN}event_admin{Colors.END} - Can manage events")
print(f"  • {Colors.CYAN}system_manager{Colors.END} - Full system access")
print()

# Generate missing components list
if missing_routes:
    print(f"\n{Colors.BOLD}{Colors.YELLOW}MISSING ADMIN ROUTES:{Colors.END}")
    for route, desc in missing_routes:
        print(f"  • {route} - {desc}")

if missing_files:
    print(f"\n{Colors.BOLD}{Colors.YELLOW}MISSING ADMIN FILES:{Colors.END}")
    for file in missing_files:
        print(f"  • {file}")

print()