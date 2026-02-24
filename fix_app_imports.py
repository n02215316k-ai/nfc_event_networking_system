class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING app.py IMPORTS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_imports2', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_imports2{Colors.END}\n")

original = content

# Fix the import on line 3
content = content.replace('from database import db', 'from database import get_db_connection')

# Also fix any usage of 'db.' to 'get_db_connection()'
# But first, let's just fix the import and see what happens

if content != original:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ IMPORT FIXED!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Changed line 3:{Colors.END}")
    print(f"  {Colors.RED}from database import db{Colors.END}")
    print(f"  {Colors.GREEN}from database import get_db_connection{Colors.END}\n")
else:
    print(f"{Colors.YELLOW}No changes needed{Colors.END}\n")

print(f"{Colors.BOLD}Now try:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")

print(f"{Colors.YELLOW}Note: If you get errors about 'db' not defined,{Colors.END}")
print(f"{Colors.YELLOW}we'll need to check if app.py uses 'db' anywhere.{Colors.END}\n")