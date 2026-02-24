class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADDING /register ALIAS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

auth_file = 'src/controllers/auth_controller.py'

with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open(auth_file + '.backup_alias', 'w', encoding='utf-8') as f:
    f.write(content)

# Find the signup route
import re
signup_match = re.search(r"(@auth_bp\.route\('/signup'[^)]*\)\s+def signup\(\):)", content, re.DOTALL)

if signup_match:
    # Add register alias before signup
    register_alias = '''
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Alias for signup route"""
    return signup()

'''
    
    # Insert before signup
    pos = signup_match.start()
    content = content[:pos] + register_alias + content[pos:]
    
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓ Added /register route as alias to /signup{Colors.END}\n")
    
    print(f"{Colors.BOLD}Both URLs now work:{Colors.END}")
    print(f"  {Colors.CYAN}/auth/register{Colors.END} → calls signup()")
    print(f"  {Colors.CYAN}/auth/signup{Colors.END} → original route\n")
else:
    print(f"{Colors.RED}❌ Could not find signup route{Colors.END}\n")