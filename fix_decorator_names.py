import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing decorator names in profile_controller.py...{Colors.END}\n")

filepath = 'src/controllers/profile_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all @require_login with @login_required
    content = content.replace('@require_login', '@login_required')
    
    # Also check for def require_login and replace with login_required
    content = content.replace('def require_login(', 'def login_required(')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Replaced all @require_login with @login_required")
    print(f"\n{Colors.GREEN}✅ Decorator names fixed!{Colors.END}\n")

except Exception as e:
    print(f"❌ Error: {e}")