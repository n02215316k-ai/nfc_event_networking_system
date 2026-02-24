import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Checking app.py around line 44...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("Lines 35-50:")
    print("=" * 80)
    
    for i in range(34, min(50, len(lines))):
        line_num = i + 1
        marker = ">>> " if i == 43 else "    "
        # Show indentation
        spaces = len(lines[i]) - len(lines[i].lstrip())
        print(f"{marker}{line_num:3d} | [{spaces:2d} spaces] {lines[i]}", end='')
    
    print("=" * 80)
    
    # Fix indentation
    print(f"\n{Colors.CYAN}Fixing indentation...{Colors.END}\n")
    
    fixed_lines = []
    for i, line in enumerate(lines):
        # Check if this is the problematic line
        if i == 43:  # Line 44 (0-indexed)
            # Check previous line's indentation
            prev_line = lines[i-1]
            prev_indent = len(prev_line) - len(prev_line.lstrip())
            
            # Apply same indentation
            if 'app.register_blueprint(event_admin_bp)' in line:
                fixed_lines.append(' ' * prev_indent + 'app.register_blueprint(event_admin_bp)\n')
            else:
                fixed_lines.append(line)
        elif i == 44 and 'app.register_blueprint(nfc_bp)' in lines[i]:
            # Fix line 45 too
            prev_line = lines[i-1]
            prev_indent = len(prev_line) - len(prev_line.lstrip())
            fixed_lines.append(' ' * prev_indent + 'app.register_blueprint(nfc_bp)\n')
        else:
            fixed_lines.append(line)
    
    # Backup
    with open(filepath + '.backup2', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Write fixed version
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"{Colors.GREEN}✓{Colors.END} Fixed indentation")
    print(f"{Colors.GREEN}✓{Colors.END} Backup: app.py.backup2")
    print(f"\n{Colors.GREEN}✅ Try running: python app.py{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")
    print(f"\n{Colors.CYAN}Manual fix needed:{Colors.END}")
    print("Check that lines 44-45 have the SAME indentation as the line above (line 43)")