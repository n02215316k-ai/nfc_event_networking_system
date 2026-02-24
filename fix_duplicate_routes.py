import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING DUPLICATE ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Check forum_controller.py
forum_controller = 'src/controllers/forum_controller.py'

if os.path.exists(forum_controller):
    print(f"{Colors.YELLOW}Checking {forum_controller}...{Colors.END}\n")
    
    with open(forum_controller, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all route definitions
    route_pattern = r"@forum_bp\.route\('([^']+)'(?:,\s*methods=\[([^\]]+)\])?\)\s*def\s+(\w+)"
    matches = list(re.finditer(route_pattern, content))
    
    # Check for duplicates
    routes_found = {}
    duplicates = []
    
    for match in matches:
        route = match.group(1)
        function = match.group(3)
        
        if function in routes_found:
            duplicates.append((function, route, routes_found[function]))
            print(f"{Colors.RED}✗ DUPLICATE: {function}(){Colors.END}")
            print(f"  First:  {routes_found[function]}")
            print(f"  Second: {route}\n")
        else:
            routes_found[function] = route
            print(f"{Colors.GREEN}✓ OK: {function}() -> {route}{Colors.END}")
    
    if duplicates:
        print(f"\n{Colors.BOLD}{Colors.RED}Found {len(duplicates)} duplicate(s)!{Colors.END}\n")
        
        # Restore from backup if it exists
        backup_file = forum_controller + '.backup_routes'
        if os.path.exists(backup_file):
            print(f"{Colors.YELLOW}Restoring from backup...{Colors.END}\n")
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            with open(forum_controller, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            print(f"{Colors.GREEN}✓ Restored from backup!{Colors.END}\n")
        else:
            print(f"{Colors.RED}No backup found. Please manually remove duplicates.{Colors.END}\n")
    else:
        print(f"\n{Colors.GREEN}✓ No duplicates found in forum_controller.py{Colors.END}\n")

else:
    print(f"{Colors.RED}✗ forum_controller.py not found{Colors.END}\n")

# Check all other controllers
controllers_dir = 'src/controllers'
if os.path.exists(controllers_dir):
    print(f"{Colors.BOLD}Checking all controllers...{Colors.END}\n")
    
    for file in os.listdir(controllers_dir):
        if file.endswith('_controller.py'):
            file_path = os.path.join(controllers_dir, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find blueprint variable name
            bp_match = re.search(r"(\w+)_bp\s*=\s*Blueprint", content)
            if not bp_match:
                continue
            
            bp_var = bp_match.group(1)
            
            # Find all functions
            route_pattern = rf"@{bp_var}_bp\.route\([^)]+\)\s*def\s+(\w+)"
            functions = re.findall(route_pattern, content)
            
            # Check for duplicates
            function_counts = {}
            for func in functions:
                function_counts[func] = function_counts.get(func, 0) + 1
            
            dupes = [f for f, count in function_counts.items() if count > 1]
            
            if dupes:
                print(f"{Colors.RED}✗ {file}: Found duplicates: {', '.join(dupes)}{Colors.END}")
                
                # Try to restore from backup
                backup_file = file_path + '.backup_routes'
                if os.path.exists(backup_file):
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        backup_content = f.read()
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(backup_content)
                    
                    print(f"  {Colors.GREEN}✓ Restored from backup{Colors.END}")
            else:
                print(f"{Colors.GREEN}✓ {file}: OK{Colors.END}")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ DUPLICATE CHECK COMPLETE{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.YELLOW}python app.py{Colors.END} - Try running Flask again\n")