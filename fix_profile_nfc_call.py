import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing profile_controller.py NFC function call...{Colors.END}\n")

profile_path = 'src/controllers/profile_controller.py'

if os.path.exists(profile_path):
    with open(profile_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the function call - add email parameter
    old_call = "nfc_code = generate_user_nfc_code(user_id)"
    new_call = "nfc_code = generate_user_nfc_code(user['id'], user['email'])"
    
    if old_call in content:
        content = content.replace(old_call, new_call)
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"{Colors.GREEN}✓{Colors.END} Fixed profile_controller.py")
        print(f"  Changed: {Colors.RED}{old_call}{Colors.END}")
        print(f"  To:      {Colors.GREEN}{new_call}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠{Colors.END} Function call not found or already fixed")
        
        # Try alternative fix
        alt_old = "nfc_code = generate_user_nfc_code(user_id"
        if alt_old in content:
            print(f"{Colors.YELLOW}Found similar call, please manually update line 331{Colors.END}")
        else:
            print(f"{Colors.GREEN}✓{Colors.END} Looks like it might already be correct")
else:
    print(f"{Colors.RED}✗{Colors.END} profile_controller.py not found")

print(f"\n{Colors.CYAN}Next steps:{Colors.END}")
print(f"  1. Restart app: python app.py")
print(f"  2. Test: http://localhost:5000/profile/my-nfc")
print()