import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING AUTH CONTROLLER{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

auth_file = 'src/controllers/auth_controller.py'

if not os.path.exists(auth_file):
    print(f"{Colors.RED}❌ {auth_file} not found!{Colors.END}\n")
    
    # Try alternate locations
    alternatives = [
        'controllers/auth_controller.py',
        'auth_controller.py',
        'src/auth.py',
        'auth.py'
    ]
    
    for alt in alternatives:
        if os.path.exists(alt):
            auth_file = alt
            print(f"{Colors.GREEN}✓ Found at: {auth_file}{Colors.END}\n")
            break
    else:
        print(f"{Colors.YELLOW}Searching for auth files...{Colors.END}\n")
        for root, dirs, files in os.walk('.'):
            for file in files:
                if 'auth' in file.lower() and file.endswith('.py'):
                    print(f"  Found: {os.path.join(root, file)}")
        exit(1)

# Read the file
with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
backup_file = auth_file + '.backup'
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: {backup_file}{Colors.END}\n")

# Fix column names
original = content

# Fix INSERT statement
import re

# Pattern 1: Fix password -> password_hash in INSERT
content = re.sub(
    r'INSERT INTO users \([^)]*\bpassword\b[^)]*\)',
    lambda m: m.group(0).replace('password,', 'password_hash,').replace('(password,', '(password_hash,'),
    content
)

# Pattern 2: Fix phone -> phone_number
content = re.sub(
    r"request\.form\.get\('phone'",
    "request.form.get('phone_number'",
    content
)
content = content.replace(', phone,', ', phone_number,')
content = content.replace('(phone,', '(phone_number,')

# Pattern 3: Fix job_title -> current_employment
content = content.replace("'job_title'", "'current_employment'")
content = content.replace('"job_title"', '"current_employment"')
content = content.replace(', job_title,', ', current_employment,')

# Pattern 4: Use werkzeug instead of bcrypt
if 'bcrypt.hashpw' in content:
    print(f"{Colors.YELLOW}Converting bcrypt to werkzeug...{Colors.END}")
    
    # Add import if needed
    if 'from werkzeug.security import' not in content:
        content = re.sub(
            r'(from flask import[^\n]+)',
            r'\1\nfrom werkzeug.security import generate_password_hash, check_password_hash',
            content,
            count=1
        )
    
    # Replace bcrypt.hashpw
    content = re.sub(
        r'bcrypt\.hashpw\((.*?)\.encode\([\'"]utf-8[\'"]\),\s*bcrypt\.gensalt\(\)\)(?:\.decode\([\'"]utf-8[\'"]\))?',
        r'generate_password_hash(\1)',
        content
    )

if content != original:
    # Write fixed content
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ AUTH CONTROLLER FIXED!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Fixed in: {auth_file}{Colors.END}\n")
    print(f"{Colors.GREEN}✓{Colors.END} password → password_hash")
    print(f"{Colors.GREEN}✓{Colors.END} phone → phone_number")
    print(f"{Colors.GREEN}✓{Colors.END} job_title → current_employment")
    if 'bcrypt' in original:
        print(f"{Colors.GREEN}✓{Colors.END} bcrypt → werkzeug\n")
else:
    print(f"{Colors.YELLOW}No changes needed or couldn't auto-fix{Colors.END}\n")

print(f"{Colors.BOLD}Now restart Flask:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")