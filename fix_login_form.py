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
print(f"{Colors.BOLD}{Colors.CYAN}FIX 1: LOGIN FORM ACTION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Find login template
login_files = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if 'login' in file.lower() and file.endswith('.html'):
            login_files.append(os.path.join(root, file))

if not login_files:
    print(f"{Colors.RED}❌ No login template found!{Colors.END}\n")
else:
    for template in login_files:
        print(f"{Colors.CYAN}Processing: {template}{Colors.END}")
        
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix form action
        content = re.sub(r'action=["\']/?login["\']', 'action="/auth/login"', content)
        content = re.sub(r'action="{{\s*url_for\(["\']login["\']\)\s*}}"', 'action="{{ url_for(\'auth.login\') }}"', content)
        
        if content != original:
            with open(template, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{Colors.GREEN}✓ Fixed login form action{Colors.END}\n")
        else:
            print(f"{Colors.YELLOW}Already correct{Colors.END}\n")

print(f"{Colors.GREEN}Done!{Colors.END}\n")