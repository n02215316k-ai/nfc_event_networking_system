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
print(f"{Colors.BOLD}{Colors.CYAN}FIXING REGISTRATION ROUTE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Find the registration route
files_to_check = [
    'app.py',
    'src/controllers/auth_controller.py',
    'routes/auth.py',
]

found_file = None
for file_path in files_to_check:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '@app.route(\'/register\'' in content or '@auth_bp.route(\'/register\'' in content:
                found_file = file_path
                break

if not found_file:
    print(f"{Colors.RED}❌ Could not find registration route!{Colors.END}")
    print(f"{Colors.YELLOW}Please share the file containing the /register route{Colors.END}\n")
    exit(1)

print(f"{Colors.GREEN}✓ Found registration route in: {found_file}{Colors.END}\n")

# Read the file
with open(found_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
backup_file = found_file + '.backup_reg'
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: {backup_file}{Colors.END}\n")

# Fix common issues
original_content = content

# 1. Fix column name: password -> password_hash
content = re.sub(
    r'INSERT INTO users.*?password.*?VALUES',
    lambda m: m.group(0).replace('password', 'password_hash'),
    content,
    flags=re.IGNORECASE | re.DOTALL
)

# 2. Fix INSERT statements more specifically
content = re.sub(
    r'INSERT INTO users \((.*?)\) VALUES',
    lambda m: m.group(0).replace(', password,', ', password_hash,').replace('(password,', '(password_hash,'),
    content,
    flags=re.IGNORECASE
)

# 3. Fix bcrypt to werkzeug for scrypt
if 'bcrypt.hashpw' in content:
    print(f"{Colors.YELLOW}⚠ Detected bcrypt password hashing{Colors.END}")
    print(f"{Colors.CYAN}Your database uses scrypt. Updating...{Colors.END}\n")
    
    # Add werkzeug import if not present
    if 'from werkzeug.security import' not in content:
        # Find imports section
        import_pattern = r'(from flask import.*?\n)'
        if re.search(import_pattern, content):
            content = re.sub(
                import_pattern,
                r'\1from werkzeug.security import generate_password_hash, check_password_hash\n',
                content,
                count=1
            )
    
    # Replace bcrypt.hashpw with generate_password_hash
    content = re.sub(
        r'bcrypt\.hashpw\((.*?)\.encode\([\'"]utf-8[\'"]\),\s*bcrypt\.gensalt\(\)\)\.decode\([\'"]utf-8[\'"]\)',
        r'generate_password_hash(\1)',
        content
    )
    
    # Simpler pattern
    content = re.sub(
        r'bcrypt\.hashpw\((.*?),.*?gensalt.*?\)',
        r'generate_password_hash(\1)',
        content
    )

# 4. Fix phone -> phone_number
content = content.replace("'phone'", "'phone_number'")
content = content.replace('"phone"', '"phone_number"')

# 5. Fix job_title, company, bio to match your schema
content = content.replace("'job_title'", "'current_employment'")
content = content.replace('"job_title"', '"current_employment"')
content = content.replace("'bio'", "'biography'")
content = content.replace('"bio"', '"biography"')

if content != original_content:
    # Write fixed content
    with open(found_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ REGISTRATION ROUTE FIXED!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Changes made:{Colors.END}")
    print(f"  {Colors.GREEN}✓{Colors.END} password → password_hash")
    print(f"  {Colors.GREEN}✓{Colors.END} phone → phone_number")
    print(f"  {Colors.GREEN}✓{Colors.END} job_title → current_employment")
    print(f"  {Colors.GREEN}✓{Colors.END} bio → biography")
    if 'bcrypt' in original_content:
        print(f"  {Colors.GREEN}✓{Colors.END} bcrypt → werkzeug (scrypt)")
    print()
else:
    print(f"{Colors.YELLOW}No changes needed or could not auto-fix{Colors.END}\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. Restart Flask: {Colors.CYAN}python app.py{Colors.END}")
print(f"  2. Try registration: {Colors.CYAN}http://localhost:5000/register{Colors.END}\n")