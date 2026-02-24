class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}DIAGNOSING app.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"{Colors.GREEN}✓ File loaded: {total_lines} lines{Colors.END}\n")
    
    # Find ALL routes
    print(f"{Colors.BOLD}All routes found:{Colors.END}\n")
    routes = []
    for i, line in enumerate(lines, 1):
        if '@app.route' in line or '@auth_bp.route' in line:
            routes.append((i, line.strip()))
            print(f"  Line {i:4d}: {line.strip()}")
    
    if not routes:
        print(f"  {Colors.RED}No routes found!{Colors.END}")
    
    # Find register-related lines
    print(f"\n{Colors.BOLD}Lines containing 'register':{Colors.END}\n")
    register_lines = []
    for i, line in enumerate(lines, 1):
        if 'register' in line.lower():
            register_lines.append(i)
            if len(register_lines) <= 20:  # Show first 20
                print(f"  Line {i:4d}: {line.rstrip()}")
    
    if len(register_lines) > 20:
        print(f"  ... and {len(register_lines) - 20} more lines")
    
    # Check for indentation errors
    print(f"\n{Colors.BOLD}Checking for indentation issues around line 1008:{Colors.END}\n")
    start = max(0, 1005)
    end = min(total_lines, 1015)
    
    for i in range(start, end):
        line = lines[i]
        indent = len(line) - len(line.lstrip())
        marker = f"{Colors.RED}<<<{Colors.END}" if i == 1007 else ""  # Line 1008 (0-indexed)
        print(f"  {i+1:4d} (indent={indent:2d}): {line.rstrip()} {marker}")
    
    # Show file size
    import os
    file_size = os.path.getsize('app.py')
    print(f"\n{Colors.CYAN}File size: {file_size:,} bytes{Colors.END}")
    
    # Check if file looks corrupted
    print(f"\n{Colors.BOLD}File health check:{Colors.END}")
    
    # Count functions
    functions = sum(1 for line in lines if line.strip().startswith('def '))
    print(f"  Functions defined: {functions}")
    
    # Count routes
    print(f"  Routes defined: {len(routes)}")
    
    # Check for common imports
    has_flask = any('from flask import' in line or 'import flask' in line for line in lines)
    print(f"  Flask imported: {Colors.GREEN if has_flask else Colors.RED}{'Yes' if has_flask else 'No'}{Colors.END}")
    
except FileNotFoundError:
    print(f"{Colors.RED}❌ app.py not found!{Colors.END}")
except Exception as e:
    print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
    import traceback
    traceback.print_exc()

print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.YELLOW}RECOMMENDATIONS{Colors.END}")
print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}\n")

print("Based on the diagnosis above:")
print(f"  1. If no routes found: File may be corrupted - restore backup")
print(f"  2. If routes found but no register: It may have been deleted")
print(f"  3. Check line 1008 for the indentation error\n")