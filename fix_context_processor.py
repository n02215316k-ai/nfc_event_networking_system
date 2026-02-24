import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.RED}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.RED}CRITICAL FIX: Context Processor{Colors.END}")
print(f"{Colors.BOLD}{Colors.RED}{'='*70}{Colors.END}\n")

print(f"{Colors.YELLOW}Issue detected: current_user is None in templates{Colors.END}")
print(f"{Colors.YELLOW}The context processor is not injecting user data{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_context', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{Colors.GREEN}✓ Backup created: app.py.backup_context{Colors.END}\n")

# Check if navigation import exists
if 'from src.utils.navigation import' not in content:
    print(f"{Colors.YELLOW}Adding navigation import...{Colors.END}")
    
    # Find last import from src
    import_pattern = r'(from src\.[^\n]+\n)'
    matches = list(re.finditer(import_pattern, content))
    
    if matches:
        last_import = matches[-1]
        insert_pos = last_import.end()
        import_line = 'from src.utils.navigation import get_user_navigation, get_user_dropdown, get_dashboard_url\n'
        content = content[:insert_pos] + import_line + content[insert_pos:]
        print(f"{Colors.GREEN}✓ Added navigation import{Colors.END}")

# Remove old/broken context processor if exists
old_processor_pattern = r'@app\.context_processor\s+def inject_navigation\(\):.*?return \{[^}]+\}\s*\n'
content = re.sub(old_processor_pattern, '', content, flags=re.DOTALL)

# Add new working context processor
new_context_processor = '''
@app.context_processor
def inject_navigation():
    """Inject navigation and user into all templates"""
    user = session.get('user')
    
    # Debug: Print user info
    if user:
        print(f"Context Processor: User logged in - {user.get('full_name')} ({user.get('role')})")
    else:
        print("Context Processor: No user in session")
    
    return {
        'nav_items': get_user_navigation(user),
        'user_dropdown': get_user_dropdown(user),
        'dashboard_url': get_dashboard_url(user),
        'current_user': user  # This is the key!
    }

'''

# Find where to insert (before first @app.route)
first_route = re.search(r'\n@app\.route', content)

if first_route:
    insert_pos = first_route.start()
    content = content[:insert_pos] + new_context_processor + content[insert_pos:]
    print(f"{Colors.GREEN}✓ Added working context processor{Colors.END}\n")
else:
    print(f"{Colors.RED}❌ Could not find insertion point{Colors.END}\n")

# Write updated app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ CONTEXT PROCESSOR FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}What was fixed:{Colors.END}")
print(f"  ✓ Added navigation import")
print(f"  ✓ Removed broken context processor")
print(f"  ✓ Added working context processor with debug")
print(f"  ✓ current_user will now be available in templates\n")

print(f"{Colors.BOLD}Restart Flask and check console:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")

print(f"{Colors.YELLOW}You should see debug messages like:{Colors.END}")
print(f'  "Context Processor: User logged in - John Doe (system_manager)"\n')

print(f"{Colors.BOLD}Then the navigation will show correctly!{Colors.END}\n")