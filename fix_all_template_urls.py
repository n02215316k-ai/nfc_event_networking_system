import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}COMPREHENSIVE TEMPLATE URL FIX{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Complete blueprint route mappings based on app.py
blueprint_routes = {
    # Auth routes
    'login': 'auth.login',
    'register': 'auth.register',
    'logout': 'auth.logout',
    
    # Event routes
    'events': 'events.list_events',
    'event_detail': 'events.detail',
    'create_event': 'events.create',
    'edit_event': 'events.edit',
    'delete_event': 'events.delete',
    'register_event': 'events.register',
    'event_checkin': 'events.checkin',
    
    # Profile routes
    'profile': 'profile.view',
    'edit_profile': 'profile.edit',
    'my_events': 'profile.my_events',
    'my_connections': 'profile.connections',
    
    # NFC routes
    'nfc_scan': 'nfc.scan',
    'nfc_badge': 'nfc.badge',
    'nfc_logs': 'nfc.logs',
    
    # Messaging routes
    'messages': 'messaging.inbox',
    'send_message': 'messaging.send',
    'message_detail': 'messaging.detail',
    
    # Forum routes
    'forums': 'forum.list',
    'forum_detail': 'forum.detail',
    'create_post': 'forum.create_post',
    
    # System Manager routes
    'system_dashboard': 'system_manager.dashboard',
    'manage_users': 'system_manager.users',
    'manage_events': 'system_manager.events',
    
    # Event Admin routes
    'admin_dashboard': 'event_admin.dashboard',
    'admin_events': 'event_admin.events',
}

# URL prefix mappings
url_prefixes = {
    '/login': '/auth/login',
    '/register': '/auth/register',
    '/logout': '/auth/logout',
    '/events': '/events',
    '/profile': '/profile',
    '/nfc': '/nfc',
    '/messages': '/messages',
    '/forum': '/forum',
    '/system-manager': '/system-manager',
    '/event-admin': '/event-admin',
}

fixed_files = []
total_replacements = 0

# Find all HTML templates
template_files = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            template_files.append(os.path.join(root, file))

print(f"{Colors.CYAN}Found {len(template_files)} template files{Colors.END}\n")

for file_path in template_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        file_changes = 0
        
        # 1. Fix url_for() calls - MOST IMPORTANT
        for old_route, new_route in blueprint_routes.items():
            # Match url_for('route_name')
            pattern1 = rf"url_for\(['\"]({old_route})['\"]\)"
            replacement1 = f"url_for('{new_route}')"
            new_content = re.sub(pattern1, replacement1, content)
            if new_content != content:
                count = len(re.findall(pattern1, content))
                file_changes += count
                content = new_content
        
        # 2. Fix direct URL paths in href, action, etc.
        # Fix href="/login" style links
        for old_url, new_url in url_prefixes.items():
            # href="/login"
            pattern = rf'href=["\']({old_url})["\']'
            replacement = f'href="{new_url}"'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                file_changes += count
                content = new_content
            
            # action="/login"
            pattern = rf'action=["\']({old_url})["\']'
            replacement = f'action="{new_url}"'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                file_changes += count
                content = new_content
        
        # 3. Fix redirect() calls in templates (shouldn't be many)
        for old_url, new_url in url_prefixes.items():
            pattern = rf"redirect\(['\"]({old_url})['\"]\)"
            replacement = f"redirect('{new_url}')"
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                file_changes += count
                content = new_content
        
        # 4. Fix form actions without quotes (edge case)
        pattern = r'action=/([a-z_-]+)'
        def fix_action(match):
            route = match.group(1)
            if route in ['login', 'register', 'logout']:
                return f'action="/auth/{route}"'
            return match.group(0)
        
        new_content = re.sub(pattern, fix_action, content)
        if new_content != content:
            file_changes += 1
            content = new_content
        
        # Write changes if any were made
        if content != original:
            # Backup original
            backup_path = file_path + '.backup_urls'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixed_files.append(file_path)
            total_replacements += file_changes
            
            print(f"{Colors.GREEN}✓ Fixed: {file_path}{Colors.END}")
            print(f"  {Colors.CYAN}{file_changes} replacements made{Colors.END}")
    
    except Exception as e:
        print(f"{Colors.RED}✗ Error fixing {file_path}: {e}{Colors.END}")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ TEMPLATE FIX COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Summary:{Colors.END}")
print(f"  Files processed: {len(template_files)}")
print(f"  Files modified: {len(fixed_files)}")
print(f"  Total replacements: {total_replacements}\n")

if fixed_files:
    print(f"{Colors.BOLD}Modified files:{Colors.END}")
    for file in fixed_files:
        print(f"  • {file}")
    print()

print(f"{Colors.BOLD}Blueprint URL Structure:{Colors.END}")
print(f"  Auth routes:         /auth/login, /auth/register, /auth/logout")
print(f"  Event routes:        /events/...")
print(f"  Profile routes:      /profile/...")
print(f"  NFC routes:          /nfc/...")
print(f"  Messaging routes:    /messages/...")
print(f"  Forum routes:        /forum/...")
print(f"  System Manager:      /system-manager/...")
print(f"  Event Admin:         /event-admin/...\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.CYAN}python app.py{Colors.END} - Restart Flask")
print(f"  2. {Colors.CYAN}http://localhost:5000{Colors.END} - Test the app")
print(f"  3. Check all navigation links work correctly\n")

print(f"{Colors.YELLOW}Note: Backups saved as *.backup_urls{Colors.END}\n")