import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Completely fixing app.py indentation...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup first
    with open(filepath + '.backup_before_fix', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup_before_fix")
    
    # Remove the problematic lines and re-add them properly
    lines = content.split('\n')
    
    # Find and remove the broken lines
    cleaned_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        # Skip the broken event_admin_bp and nfc_bp lines
        if 'app.register_blueprint(event_admin_bp)' in line or 'app.register_blueprint(nfc_bp)' in line:
            continue
        cleaned_lines.append(line)
    
    # Find where to insert the registrations (after system_manager_bp)
    insert_index = -1
    for i, line in enumerate(cleaned_lines):
        if 'app.register_blueprint(system_manager_bp)' in line:
            insert_index = i + 1
            break
    
    if insert_index > 0:
        # Get the indentation from the previous line
        prev_line = cleaned_lines[insert_index - 1]
        indent = len(prev_line) - len(prev_line.lstrip())
        
        # Insert with correct indentation
        cleaned_lines.insert(insert_index, ' ' * indent + 'app.register_blueprint(event_admin_bp)')
        cleaned_lines.insert(insert_index + 1, ' ' * indent + 'app.register_blueprint(nfc_bp)')
        
        # Write back
        new_content = '\n'.join(cleaned_lines)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"{Colors.GREEN}✓{Colors.END} Fixed app.register_blueprint(event_admin_bp)")
        print(f"{Colors.GREEN}✓{Colors.END} Fixed app.register_blueprint(nfc_bp)")
        print(f"\n{Colors.GREEN}✅ app.py fixed successfully!{Colors.END}\n")
        
        # Show the fixed section
        print(f"{Colors.CYAN}Fixed section (lines {insert_index-2} to {insert_index+3}):{Colors.END}")
        print("=" * 80)
        for i in range(max(0, insert_index-3), min(len(cleaned_lines), insert_index+3)):
            print(f"  {i+1:3d} | {cleaned_lines[i]}")
        print("=" * 80)
    else:
        print(f"{Colors.RED}✗{Colors.END} Could not find system_manager_bp registration")
        print("\nPlease add manually after all other app.register_blueprint() lines:")
        print("    app.register_blueprint(event_admin_bp)")
        print("    app.register_blueprint(nfc_bp)")

except Exception as e:
    print(f"{Colors.RED}✗{Colors.END} Error: {e}")
    print(f"\n{Colors.YELLOW}Manual fix required:{Colors.END}")
    print("1. Open app.py")
    print("2. Find all lines with app.register_blueprint()")
    print("3. Delete the lines with event_admin_bp and nfc_bp")
    print("4. Re-add them with the SAME indentation as other register_blueprint lines")
    print("\nExample:")
    print("    app.register_blueprint(system_manager_bp)")
    print("    app.register_blueprint(event_admin_bp)    # Same indentation as above")
    print("    app.register_blueprint(nfc_bp)            # Same indentation as above")