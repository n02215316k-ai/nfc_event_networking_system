class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CHECKING database.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

try:
    with open('database.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"{Colors.GREEN}✓ database.py found{Colors.END}\n")
    
    # Show the first 50 lines
    lines = content.split('\n')
    print(f"{Colors.BOLD}First 50 lines of database.py:{Colors.END}\n")
    
    for i, line in enumerate(lines[:50], 1):
        if 'def ' in line or 'class ' in line:
            print(f"{Colors.YELLOW}{i:3d}: {line}{Colors.END}")
        elif 'import' in line:
            print(f"{Colors.CYAN}{i:3d}: {line}{Colors.END}")
        else:
            print(f"{i:3d}: {line}")
    
    if len(lines) > 50:
        print(f"\n... ({len(lines) - 50} more lines)")
    
    # Find all function and class definitions
    print(f"\n{Colors.BOLD}Functions and classes in database.py:{Colors.END}\n")
    
    functions = []
    classes = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('def '):
            func_name = stripped.split('(')[0].replace('def ', '')
            functions.append(func_name)
            print(f"  {Colors.GREEN}Function:{Colors.END} {func_name}")
        elif stripped.startswith('class '):
            class_name = stripped.split('(')[0].split(':')[0].replace('class ', '')
            classes.append(class_name)
            print(f"  {Colors.YELLOW}Class:{Colors.END} {class_name}")
    
    # Check what should be imported
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}IMPORT RECOMMENDATIONS:{Colors.END}\n")
    
    if 'get_db_connection' in functions:
        print(f"  {Colors.GREEN}✓{Colors.END} Use: {Colors.CYAN}from database import get_db_connection{Colors.END}")
    
    if classes:
        print(f"  {Colors.GREEN}✓{Colors.END} Available classes: {', '.join(classes)}")
    
    if not functions and not classes:
        print(f"  {Colors.RED}⚠ No functions or classes found!{Colors.END}")
        print(f"  {Colors.YELLOW}The file might only have configuration.{Colors.END}")

except FileNotFoundError:
    print(f"{Colors.RED}❌ database.py not found!{Colors.END}\n")
    
    # Check for database folder
    import os
    if os.path.isdir('database'):
        print(f"{Colors.CYAN}Found database/ folder instead:{Colors.END}\n")
        for file in os.listdir('database'):
            if file.endswith('.py'):
                print(f"  • database/{file}")

print()