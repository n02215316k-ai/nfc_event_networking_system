import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

print("=" * 80)
print(f"{Colors.CYAN}🔧 FIXING INDENTATION ERROR{Colors.END}")
print("=" * 80)

event_admin_path = 'src/controllers/event_admin_controller.py'

if os.path.exists(event_admin_path):
    with open(event_admin_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Show the error area (around line 321)
    print(f"\n{Colors.CYAN}📍 Error location (around line 321):{Colors.END}\n")
    for i in range(max(0, 318), min(len(lines), 330)):
        line_num = i + 1
        marker = f"{Colors.RED}>>>{Colors.END}" if line_num == 321 else "   "
        print(f"{marker} {line_num:4d}: {lines[i].rstrip()}")
    
    print(f"\n{Colors.CYAN}🔍 Analyzing indentation...{Colors.END}")
    
    # Find the function around line 321
    function_start = None
    for i in range(320, max(0, 300), -1):
        if 'def ' in lines[i]:
            function_start = i
            print(f"{Colors.GREEN}✓{Colors.END} Found function start at line {i+1}: {lines[i].strip()}")
            break
    
    if function_start:
        # Check indentation levels
        base_indent = len(lines[function_start]) - len(lines[function_start].lstrip())
        expected_indent = base_indent + 4
        
        print(f"{Colors.CYAN}📏 Expected indent: {expected_indent} spaces{Colors.END}")
        
        # Fix line 321 and surrounding lines
        fixed = False
        for i in range(max(0, function_start), min(len(lines), function_start + 100)):
            line = lines[i]
            if 'cursor.execute("""' in line:
                current_indent = len(line) - len(line.lstrip())
                if current_indent != expected_indent:
                    # Fix indentation
                    lines[i] = ' ' * expected_indent + line.lstrip()
                    print(f"{Colors.GREEN}✓{Colors.END} Fixed line {i+1}: Changed indent from {current_indent} to {expected_indent}")
                    fixed = True
    
    # Write back
    if fixed:
        with open(event_admin_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"\n{Colors.GREEN}✅ File saved with fixes{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Could not auto-fix. Manual fix needed.{Colors.END}")
        
        # Provide manual fix instructions
        print(f"\n{Colors.CYAN}📝 Manual Fix Instructions:{Colors.END}\n")
        print("1. Open: src/controllers/event_admin_controller.py")
        print("2. Go to line 321")
        print("3. Check the indentation matches the function body")
        print("4. Lines inside a function should be indented 4 spaces from 'def'")

else:
    print(f"{Colors.RED}✗{Colors.END} File not found: {event_admin_path}")

print("\n" + "=" * 80)