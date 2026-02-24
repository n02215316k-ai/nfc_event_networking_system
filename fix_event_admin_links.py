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
print(f"{Colors.BOLD}{Colors.CYAN}FIXING EVENT ADMIN NAVIGATION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

print(f"{Colors.YELLOW}Creating role-aware navigation...{Colors.END}\n")

# Find base.html
base_template = None
for root, dirs, files in os.walk('templates'):
    if 'base.html' in files:
        base_template = os.path.join(root, 'base.html')
        break

if not base_template:
    print(f"{Colors.RED}❌ base.html not found!{Colors.END}\n")
    exit(1)

print(f"{Colors.CYAN}Found: {base_template}{Colors.END}\n")

with open(base_template, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open(base_template + '.backup_event_admin', 'w', encoding='utf-8') as f:
    f.write(content)

# Find the Admin dropdown section and replace it
old_admin_dropdown = r'''{% if session\.user\.role == 'system_manager' %}.*?{% endif %}'''

new_admin_dropdown = '''{% if session.user.role == 'system_manager' %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-cog"></i> System Manager
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/system-manager/dashboard">
                                <i class="fas fa-tachometer-alt"></i> Dashboard
                            </a></li>
                            <li><a class="dropdown-item" href="/system-manager/users">
                                <i class="fas fa-users"></i> Users
                            </a></li>
                            <li><a class="dropdown-item" href="/system-manager/events">
                                <i class="fas fa-calendar"></i> Events
                            </a></li>
                            <li><a class="dropdown-item" href="/system-manager/verifications">
                                <i class="fas fa-check-circle"></i> Verifications
                            </a></li>
                            <li><a class="dropdown-item" href="/system-manager/reports">
                                <i class="fas fa-chart-bar"></i> Reports
                            </a></li>
                        </ul>
                    </li>
                    {% endif %}
                    
                    {% if session.user.role == 'event_admin' %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="eventAdminDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-cog"></i> Event Admin
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/event-admin/dashboard">
                                <i class="fas fa-tachometer-alt"></i> Dashboard
                            </a></li>
                            <li><a class="dropdown-item" href="/event-admin/events">
                                <i class="fas fa-calendar"></i> My Events
                            </a></li>
                            <li><a class="dropdown-item" href="/events/create">
                                <i class="fas fa-plus"></i> Create Event
                            </a></li>
                        </ul>
                    </li>
                    {% endif %}'''

# Replace the admin dropdown section
content = re.sub(old_admin_dropdown, new_admin_dropdown, content, flags=re.DOTALL)

# Write updated content
with open(base_template, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{Colors.GREEN}✓ Updated base.html with role-aware navigation{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ EVENT ADMIN NAVIGATION ADDED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Navigation now shows:{Colors.END}\n")

print(f"{Colors.BOLD}System Manager sees:{Colors.END}")
print(f"  • System Manager dropdown:")
print(f"    - Dashboard → /system-manager/dashboard")
print(f"    - Users → /system-manager/users")
print(f"    - Events → /system-manager/events")
print(f"    - Verifications → /system-manager/verifications")
print(f"    - Reports → /system-manager/reports\n")

print(f"{Colors.BOLD}Event Admin sees:{Colors.END}")
print(f"  • Event Admin dropdown:")
print(f"    - Dashboard → /event-admin/dashboard")
print(f"    - My Events → /event-admin/events")
print(f"    - Create Event → /events/create\n")

print(f"{Colors.BOLD}Restart Flask:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")