import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing duplicate nfc_bp and indentation...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Backup
    with open(filepath + '.backup_final', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"{Colors.GREEN}✓{Colors.END} Backup: app.py.backup_final")
    
    # Fix the issues:
    # 1. nfc_bp is already registered on line 40 (correct)
    # 2. Remove line 44 (duplicate event_admin_bp without url_prefix)
    # 3. Remove line 45 (duplicate nfc_bp with wrong indentation)
    
    fixed_lines = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Skip line 44 and 45 (the problematic duplicates)
        if line_num == 44 and 'app.register_blueprint(event_admin_bp)' in line:
            print(f"{Colors.YELLOW}○{Colors.END} Removing line 44 (duplicate event_admin_bp)")
            # Instead, add it with url_prefix after line 43
            if i > 0:
                fixed_lines.append("app.register_blueprint(event_admin_bp, url_prefix='/event-admin')\n")
                print(f"{Colors.GREEN}✓{Colors.END} Added event_admin_bp with url_prefix")
            continue
        elif line_num == 45 and 'app.register_blueprint(nfc_bp)' in line:
            print(f"{Colors.YELLOW}○{Colors.END} Removing line 45 (duplicate nfc_bp)")
            continue
        else:
            fixed_lines.append(line)
    
    # Write fixed version
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"\n{Colors.GREEN}✅ Fixed app.py!{Colors.END}\n")
    
    # Show the fixed section
    print(f"{Colors.CYAN}Blueprint registrations (lines 37-44):{Colors.END}")
    print("=" * 80)
    for i in range(36, min(45, len(fixed_lines))):
        print(f"  {i+1:3d} | {fixed_lines[i]}", end='')
    print("=" * 80)
    
    print(f"\n{Colors.GREEN}✅ Now try: python app.py{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")