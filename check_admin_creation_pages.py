import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CHECKING ADMIN CREATION PAGES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Check for admin creation pages
pages_to_check = {
    'User Creation Pages': [
        'templates/admin/create_user.html',
        'templates/admin/add_user.html',
        'templates/system/create_user.html',
        'templates/system/add_admin.html',
    ],
    'Registration Page': [
        'templates/register.html',
        'templates/signup.html',
    ],
    'User Management Pages': [
        'templates/admin/users.html',
        'templates/system/users.html',
    ]
}

print(f"{Colors.BOLD}📁 Checking for Admin Creation Pages:{Colors.END}\n")

found_pages = []
missing_pages = []

for category, pages in pages_to_check.items():
    print(f"{Colors.CYAN}{category}:{Colors.END}")
    for page in pages:
        if os.path.exists(page):
            print(f"  {Colors.GREEN}✓{Colors.END} {page}")
            found_pages.append(page)
        else:
            print(f"  {Colors.RED}✗{Colors.END} {page} (MISSING)")
            missing_pages.append(page)
    print()

# Check routes in app.py
print(f"{Colors.BOLD}🔍 Checking Routes in app.py:{Colors.END}\n")

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    routes_to_check = {
        '/admin/users/create': 'Create user (admin)',
        '/admin/create-user': 'Create user (admin alt)',
        '/system/users/create': 'Create user (system)',
        '/system/create-admin': 'Create admin user',
        '/register': 'Public registration',
    }
    
    for route, description in routes_to_check.items():
        if f"@app.route('{route}')" in app_content:
            print(f"  {Colors.GREEN}✓{Colors.END} {route} - {description}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {route} - {description} (MISSING)")

except FileNotFoundError:
    print(f"{Colors.RED}❌ app.py not found{Colors.END}")

# Summary
print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}SUMMARY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

print(f"{Colors.BOLD}Current Status:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Found: {len(found_pages)} pages")
print(f"  {Colors.RED}✗{Colors.END} Missing: {len(missing_pages)} pages")

if len(found_pages) == 0:
    print(f"\n{Colors.BOLD}{Colors.RED}❌ NO ADMIN CREATION PAGES FOUND{Colors.END}")
    print(f"\n{Colors.YELLOW}You currently have NO dedicated pages for creating admins.{Colors.END}")
else:
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Some admin management pages exist{Colors.END}")

print(f"\n{Colors.BOLD}Current Options:{Colors.END}\n")

print(f"1️⃣  {Colors.CYAN}Database Method{Colors.END} (Currently available)")
print(f"   Update existing user roles via SQL:")
print(f"   {Colors.YELLOW}UPDATE users SET role = 'event_admin' WHERE email = 'user@example.com';{Colors.END}")
print(f"   {Colors.YELLOW}UPDATE users SET role = 'system_manager' WHERE email = 'user@example.com';{Colors.END}\n")

print(f"2️⃣  {Colors.CYAN}System Manager Panel{Colors.END} (If you have system access)")
print(f"   Login as system_manager → /system/users → Change role dropdown\n")

print(f"3️⃣  {Colors.CYAN}Create Dedicated Admin Creation Pages{Colors.END} (Recommended)")
print(f"   I can create pages for:")
print(f"   • /admin/users/create - Create new users with specific roles")
print(f"   • /system/create-admin - Create admin users directly")
print(f"   • Enhanced user management with role selection\n")

print(f"{Colors.BOLD}{Colors.YELLOW}Would you like me to create admin creation pages?{Colors.END}\n")