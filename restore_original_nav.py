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
print(f"{Colors.BOLD}{Colors.CYAN}RESTORING ORIGINAL NAVIGATION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Step 1: Remove context processor from app.py
print(f"{Colors.YELLOW}Step 1: Cleaning up app.py...{Colors.END}\n")

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Backup
with open('app.py.backup_restore', 'w', encoding='utf-8') as f:
    f.write(app_content)

# Remove navigation imports
app_content = re.sub(r'from src\.utils\.navigation import.*?\n', '', app_content)

# Remove context processor
app_content = re.sub(
    r'@app\.context_processor\s+def inject_navigation\(\):.*?return \{[^}]+\}\s*\n',
    '',
    app_content,
    flags=re.DOTALL
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print(f"{Colors.GREEN}✓ Removed dynamic navigation from app.py{Colors.END}\n")

# Step 2: Find base.html
base_templates = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file == 'base.html':
            base_templates.append(os.path.join(root, file))

if not base_templates:
    print(f"{Colors.RED}❌ base.html not found!{Colors.END}\n")
    exit(1)

base_template = base_templates[0]
print(f"{Colors.CYAN}Found: {base_template}{Colors.END}\n")

# Step 3: Check for backup
backup_file = base_template + '.backup_nav'

if os.path.exists(backup_file):
    print(f"{Colors.GREEN}✓ Found backup: {backup_file}{Colors.END}")
    
    # Restore from backup
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    
    with open(base_template, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    print(f"{Colors.GREEN}✓ Restored base.html from backup{Colors.END}\n")
else:
    print(f"{Colors.YELLOW}No backup found, creating simple navigation...{Colors.END}\n")
    
    # Read current base.html
    with open(base_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create simple static navigation
    simple_nav = '''<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <i class="fas fa-wifi"></i> NFC Events
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                {% if session.user %}
                    <!-- Logged in navigation -->
                    <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="fas fa-home"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/events">
                            <i class="fas fa-calendar"></i> Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/messages">
                            <i class="fas fa-envelope"></i> Messages
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/forum">
                            <i class="fas fa-comments"></i> Forum
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/nfc/scanner">
                            <i class="fas fa-qrcode"></i> Scan
                        </a>
                    </li>
                    
                    {% if session.user.role == 'system_manager' %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-cog"></i> Admin
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/system-manager/dashboard">Dashboard</a></li>
                            <li><a class="dropdown-item" href="/system-manager/users">Users</a></li>
                            <li><a class="dropdown-item" href="/system-manager/events">Events</a></li>
                            <li><a class="dropdown-item" href="/system-manager/verifications">Verifications</a></li>
                            <li><a class="dropdown-item" href="/system-manager/reports">Reports</a></li>
                        </ul>
                    </li>
                    {% endif %}
                    
                    {% if session.user.role == 'event_admin' %}
                    <li class="nav-item">
                        <a class="nav-link" href="/event-admin/dashboard">
                            <i class="fas fa-tachometer-alt"></i> Admin Panel
                        </a>
                    </li>
                    {% endif %}
                {% else %}
                    <!-- Not logged in -->
                    <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="fas fa-home"></i> Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/events">
                            <i class="fas fa-calendar"></i> Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">
                            <i class="fas fa-info-circle"></i> About
                        </a>
                    </li>
                {% endif %}
            </ul>
            
            <ul class="navbar-nav">
                {% if session.user %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user-circle"></i> {{ session.user.full_name }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="/profile/edit">
                                <i class="fas fa-user"></i> My Profile
                            </a></li>
                            <li><a class="dropdown-item" href="/profile/my-events">
                                <i class="fas fa-calendar"></i> My Events
                            </a></li>
                            <li><a class="dropdown-item" href="/profile/edit">
                                <i class="fas fa-cog"></i> Settings
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/auth/change-password">
                                <i class="fas fa-key"></i> Change Password
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/auth/logout">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a></li>
                        </ul>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/login">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/signup">
                            <i class="fas fa-user-plus"></i> Sign Up
                        </a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>'''
    
    # Replace navigation include or existing nav
    if '{% include "partials/navigation.html" %}' in content:
        content = content.replace('{% include "partials/navigation.html" %}', simple_nav)
    else:
        # Replace existing nav
        content = re.sub(
            r'<!-- Navigation -->.*?</nav>',
            simple_nav,
            content,
            flags=re.DOTALL
        )
    
    with open(base_template, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓ Added simple working navigation{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ORIGINAL NAVIGATION RESTORED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Navigation Features:{Colors.END}")
print(f"  ✓ Dashboard link")
print(f"  ✓ Events, Messages, Forum, Scan")
print(f"  ✓ Admin dropdown for system_manager")
print(f"  ✓ User dropdown with Profile, Settings, Logout")
print(f"  ✓ Uses session.user (works properly)\n")

print(f"{Colors.BOLD}Restart Flask:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")