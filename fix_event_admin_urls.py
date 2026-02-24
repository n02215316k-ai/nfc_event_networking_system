import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing event_admin_controller.py url_for references...{Colors.END}\n")

filepath = 'src/controllers/event_admin_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace url_for('home') with url_for('index')
    content = content.replace("url_for('home')", "url_for('index')")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Fixed url_for('home') references")
    print(f"\n{Colors.GREEN}✅ Event admin controller fixed!{Colors.END}\n")

except Exception as e:
    print(f"Error: {e}")