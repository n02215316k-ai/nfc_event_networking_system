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
print(f"{Colors.BOLD}{Colors.CYAN}FIXING ALL NAVIGATION LINKS IN ENTIRE SYSTEM{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Complete URL mapping
url_mappings = {
    # Auth routes
    r'href=["\']/?login["\']': 'href="/auth/login"',
    r'href=["\']/?register["\']': 'href="/auth/signup"',
    r'href=["\']/?logout["\']': 'href="/auth/logout"',
    r'href=["\']/?signup["\']': 'href="/auth/signup"',
    
    # Action attributes
    r'action=["\']/?login["\']': 'action="/auth/login"',
    r'action=["\']/?register["\']': 'action="/auth/signup"',
    r'action=["\']/?signup["\']': 'action="/auth/signup"',
    
    # url_for patterns
    r"url_for\(['\"]login['\"]\)": "url_for('auth.login')",
    r"url_for\(['\"]register['\"]\)": "url_for('auth.signup')",
    r"url_for\(['\"]signup['\"]\)": "url_for('auth.signup')",
    r"url_for\(['\"]logout['\"]\)": "url_for('auth.logout')",
    
    # Event routes
    r"url_for\(['\"]events['\"]\)": "url_for('events.list_events')",
    r"url_for\(['\"]create_event['\"]\)": "url_for('events.create')",
    
    # Profile routes
    r"url_for\(['\"]profile['\"]\)": "url_for('profile.view')",
    r"url_for\(['\"]edit_profile['\"]\)": "url_for('profile.edit')",
    
    # Messages
    r"url_for\(['\"]messages['\"]\)": "url_for('messaging.inbox')",
    
    # Forum
    r"url_for\(['\"]forums['\"]\)": "url_for('forum.list')",
    
    # NFC
    r"url_for\(['\"]nfc['\"]\)": "url_for('nfc.scan')",
}

fixed_files = []
total_changes = 0

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('.'):
    # Skip unwanted directories
    if any(skip in root for skip in ['__pycache__', '.git', 'venv', 'node_modules', 'static']):
        continue
    
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"{Colors.CYAN}Found {len(html_files)} HTML files to process{Colors.END}\n")

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        file_changes = 0
        
        # Apply all URL mappings
        for pattern, replacement in url_mappings.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                file_changes += len(matches)
        
        # Additional fixes for common patterns
        # Fix <a href="login"> without quotes
        content = re.sub(r'<a\s+href=login>', '<a href="/auth/login">', content, flags=re.IGNORECASE)
        content = re.sub(r'<a\s+href=register>', '<a href="/auth/signup">', content, flags=re.IGNORECASE)
        
        if content != original:
            # Backup
            with open(file_path + '.backup_nav', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixed_files.append(file_path)
            total_changes += file_changes
            
            print(f"{Colors.GREEN}✓ {file_path}{Colors.END}")
            print(f"  {Colors.CYAN}{file_changes} link(s) fixed{Colors.END}")
    
    except Exception as e:
        print(f"{Colors.RED}✗ Error processing {file_path}: {e}{Colors.END}")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ NAVIGATION FIX COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.CYAN}Summary:{Colors.END}")
print(f"  Files processed: {len(html_files)}")
print(f"  Files modified: {len(fixed_files)}")
print(f"  Total links fixed: {total_changes}\n")

print(f"{Colors.BOLD}Correct URLs:{Colors.END}")
print(f"  Login:     {Colors.CYAN}/auth/login{Colors.END}")
print(f"  Signup:    {Colors.CYAN}/auth/signup{Colors.END}")
print(f"  Logout:    {Colors.CYAN}/auth/logout{Colors.END}")
print(f"  Events:    {Colors.CYAN}/events{Colors.END}")
print(f"  Profile:   {Colors.CYAN}/profile{Colors.END}")
print(f"  Messages:  {Colors.CYAN}/messages{Colors.END}\n")

print(f"{Colors.YELLOW}Backups saved as: *.backup_nav{Colors.END}\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.CYAN}Start MySQL in XAMPP{Colors.END}")
print(f"  2. {Colors.CYAN}python app.py{Colors.END}")
print(f"  3. {Colors.CYAN}http://localhost:5000{Colors.END}\n")