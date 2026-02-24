class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING DATABASE IMPORT{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_dbimport', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_dbimport{Colors.END}\n")

original = content

# Fix the import - change from database.db import db to from database import db
content = content.replace('from database.db import db', 'from database import db')

# Also check for other variations
content = content.replace('from database.db import get_db_connection', 'from database import get_db_connection')

if content != original:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ IMPORT FIXED!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Changed:{Colors.END}")
    print(f"  {Colors.RED}from database.db import db{Colors.END}")
    print(f"  {Colors.GREEN}from database import db{Colors.END}\n")
else:
    print(f"{Colors.YELLOW}Import already correct or not found{Colors.END}\n")

print(f"{Colors.BOLD}Now try:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")