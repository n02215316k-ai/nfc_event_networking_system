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
print(f"{Colors.BOLD}{Colors.CYAN}FIXING FORUM CONTROLLER DUPLICATE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

forum_controller = 'src/controllers/forum_controller.py'

if os.path.exists(forum_controller):
    with open(forum_controller, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup first
    backup_file = forum_controller + '.backup_fix'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{Colors.GREEN}✓ Backup created: {backup_file}{Colors.END}\n")
    
    # Find the section added by add_missing_routes.py
    # This is usually at the end of the file
    duplicate_section_pattern = r"\n# Alias routes for compatibility.*?(?=\nif __name__|$)"
    
    if re.search(duplicate_section_pattern, content, re.DOTALL):
        # Remove the duplicate section
        content_fixed = re.sub(duplicate_section_pattern, '', content, flags=re.DOTALL)
        
        with open(forum_controller, 'w', encoding='utf-8') as f:
            f.write(content_fixed)
        
        print(f"{Colors.GREEN}✓ Removed duplicate 'Alias routes for compatibility' section{Colors.END}\n")
    else:
        # Manual search for duplicate create_forum
        create_forum_pattern = r"@forum_bp\.route\('/forum/create'.*?\ndef create_forum\(.*?\).*?(?=\n@|\nif __name__|$)"
        matches = list(re.finditer(create_forum_pattern, content, re.DOTALL))
        
        if len(matches) > 1:
            print(f"{Colors.YELLOW}Found {len(matches)} create_forum definitions{Colors.END}")
            print(f"{Colors.YELLOW}Removing the last one...{Colors.END}\n")
            
            # Remove the last occurrence
            last_match = matches[-1]
            content_fixed = content[:last_match.start()] + content[last_match.end():]
            
            with open(forum_controller, 'w', encoding='utf-8') as f:
                f.write(content_fixed)
            
            print(f"{Colors.GREEN}✓ Removed duplicate create_forum function{Colors.END}\n")
        else:
            print(f"{Colors.YELLOW}Only one create_forum found. Checking for other issues...{Colors.END}\n")
            
            # List all route functions
            all_routes = re.findall(r"@forum_bp\.route\([^)]+\)\s*def\s+(\w+)", content)
            
            # Find duplicates
            from collections import Counter
            counts = Counter(all_routes)
            duplicates = {func: count for func, count in counts.items() if count > 1}
            
            if duplicates:
                print(f"{Colors.RED}Found duplicate functions:{Colors.END}")
                for func, count in duplicates.items():
                    print(f"  {Colors.RED}✗ {func}: {count} times{Colors.END}")
                
                print(f"\n{Colors.YELLOW}Please manually edit {forum_controller}{Colors.END}")
                print(f"{Colors.YELLOW}and remove duplicate function definitions.{Colors.END}\n")
            else:
                print(f"{Colors.GREEN}✓ No duplicate functions found{Colors.END}\n")
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ FIX COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

else:
    print(f"{Colors.RED}✗ {forum_controller} not found{Colors.END}\n")

print(f"{Colors.BOLD}Next step:{Colors.END}")
print(f"  {Colors.YELLOW}python app.py{Colors.END}\n")