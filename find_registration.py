import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FINDING REGISTRATION ROUTE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Search patterns
patterns = [
    "@app.route('/register'",
    "@app.route(\"/register\"",
    "@auth_bp.route('/register'",
    "def register(",
    "route('/register'",
]

found_files = []

# Search all Python files
for root, dirs, files in os.walk('.'):
    # Skip common directories
    if any(skip in root for skip in ['venv', '__pycache__', '.git', 'node_modules']):
        continue
    
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check if file contains registration route
                    for pattern in patterns:
                        if pattern in content:
                            found_files.append(file_path)
                            break
            except:
                pass

if not found_files:
    print(f"{Colors.RED}❌ No registration route found!{Colors.END}\n")
    exit(1)

print(f"{Colors.GREEN}✓ Found registration route in {len(found_files)} file(s):{Colors.END}\n")

for file_path in found_files:
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}File: {Colors.CYAN}{file_path}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.END}\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the registration route
    in_register_route = False
    route_start = 0
    route_code = []
    indent_level = 0
    
    for i, line in enumerate(lines, 1):
        # Check if this is the start of register route
        if any(pattern in line for pattern in patterns):
            in_register_route = True
            route_start = i
            indent_level = len(line) - len(line.lstrip())
            route_code.append(f"{i:4d} | {line.rstrip()}")
            continue
        
        # If we're in the route, collect lines
        if in_register_route:
            current_indent = len(line) - len(line.lstrip())
            
            # Stop if we hit another function or route at same/lower indent
            if line.strip() and current_indent <= indent_level and (line.strip().startswith('def ') or line.strip().startswith('@')):
                break
            
            route_code.append(f"{i:4d} | {line.rstrip()}")
            
            # Stop after reasonable amount of lines
            if len(route_code) > 100:
                break
    
    # Print the route code
    print(f"{Colors.CYAN}Registration Route Code:{Colors.END}\n")
    for line in route_code[:50]:  # Show first 50 lines
        if 'password' in line.lower():
            print(f"{Colors.YELLOW}{line}{Colors.END}")
        elif 'INSERT' in line or 'insert' in line:
            print(f"{Colors.RED}{line}{Colors.END}")
        else:
            print(line)
    
    if len(route_code) > 50:
        print(f"\n{Colors.YELLOW}... (truncated, showing first 50 lines){Colors.END}")
    
    print(f"\n{Colors.BOLD}Line {route_start}-{route_start + len(route_code)}{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ SEARCH COMPLETE{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.YELLOW}To edit the file:{Colors.END}")
for file_path in found_files:
    print(f"  code {file_path}")
print()