import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing NFC import path in profile_controller.py...{Colors.END}\n")

filepath = 'src/controllers/profile_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the import path
    content = content.replace(
        'from controllers.nfc_controller import',
        'from src.controllers.nfc_controller import'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Fixed NFC controller import path")
    print(f"\n{Colors.GREEN}✅ Profile controller fixed!{Colors.END}\n")

except Exception as e:
    print(f"❌ Error: {e}")