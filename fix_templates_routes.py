import os
import re

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

def fix_template_routes(filepath):
    """Fix route references in template files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common route fixes based on the actual routes
        fixes = {
            # Events
            "url_for('events.create')": "url_for('events.create_event')",
            "url_for('events.list')": "url_for('events.list_events')",
            
            # Forum
            "url_for('forum.create')": "url_for('forum.create_forum')",
            "url_for('forum.list')": "url_for('forum.list_forums')",
            
            # Profile
            "url_for('profile.change_password')": "url_for('auth.change_password')",
            
            # Messaging
            "url_for('messaging.inbox')": "url_for('messaging.inbox')",
        }
        
        for old, new in fixes.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{Colors.GREEN}✓{Colors.END} Fixed: {Colors.CYAN}{filepath}{Colors.END}")
            return True
        else:
            print(f"{Colors.YELLOW}○{Colors.END} No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} Error fixing {filepath}: {e}")
        return False

def fix_all_templates():
    """Fix all template files"""
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.CYAN}Fixing Template Route References{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")
    
    templates_dir = 'templates'
    fixed_count = 0
    
    if not os.path.exists(templates_dir):
        print(f"{Colors.RED}✗{Colors.END} Templates directory not found")
        return
    
    # Walk through all template files
    for root, dirs, files in os.walk(templates_dir):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                if fix_template_routes(filepath):
                    fixed_count += 1
    
    print(f"\n{Colors.GREEN}{'=' * 80}{Colors.END}")
    print(f"{Colors.GREEN}✅ Template fixes complete!{Colors.END}")
    print(f"{Colors.GREEN}Fixed {fixed_count} file(s){Colors.END}")
    print(f"{Colors.GREEN}{'=' * 80}{Colors.END}\n")

if __name__ == '__main__':
    fix_all_templates()