import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIX 3: CHECK AUTH ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

auth_file = 'src/controllers/auth_controller.py'

if not os.path.exists(auth_file):
    print(f"{Colors.RED}❌ {auth_file} not found!{Colors.END}\n")
    exit(1)

with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all routes
import re
routes = re.findall(r"@\w+\.route\('([^']+)'[^)]*\)", content)

print(f"{Colors.BOLD}Routes in auth_controller.py:{Colors.END}\n")

if routes:
    for route in routes:
        full_url = f"/auth{route}"
        print(f"  {Colors.GREEN}✓{Colors.END} {full_url}")
    print()
    
    # Check for register route
    if '/register' in routes or any('register' in r for r in routes):
        print(f"{Colors.GREEN}✓ Register route exists{Colors.END}\n")
    else:
        print(f"{Colors.RED}❌ Register route NOT FOUND{Colors.END}")
        print(f"{Colors.YELLOW}Need to add register route to auth_controller.py{Colors.END}\n")
else:
    print(f"{Colors.RED}❌ No routes found in auth controller!{Colors.END}\n")

# Check for functions
functions = re.findall(r'def (\w+)\(', content)
print(f"{Colors.BOLD}Functions defined:{Colors.END}\n")
for func in functions:
    print(f"  • {func}()")
print()