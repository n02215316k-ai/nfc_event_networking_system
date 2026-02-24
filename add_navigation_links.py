import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

NAVIGATION_ADDITIONS = """
                    <!-- NFC Scanner -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('nfc.scanner_page') }}">
                            <i class="fas fa-qrcode me-1"></i>Scanner
                        </a>
                    </li>
                    
                    <!-- My NFC/QR Code -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('profile.my_nfc') }}">
                            <i class="fas fa-id-card me-1"></i>My QR Code
                        </a>
                    </li>
"""

EVENT_ADMIN_NAV = """
                    <!-- Event Admin Dashboard (only for event_admin and system_manager) -->
                    {% if session.get('role') in ['event_admin', 'system_manager'] %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="eventAdminDropdown" role="button" 
                           data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-calendar-check me-1"></i>Event Admin
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="eventAdminDropdown">
                            <li><a class="dropdown-item" href="{{ url_for('event_admin.dashboard') }}">
                                <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                            </a></li>
                            <li><a class="dropdown-item" href="{{ url_for('events.create_event') }}">
                                <i class="fas fa-plus me-2"></i>Create Event
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('event_admin.networking_analytics') }}">
                                <i class="fas fa-project-diagram me-2"></i>Networking Analytics
                            </a></li>
                        </ul>
                    </li>
                    {% endif %}
"""

print(f"\n{Colors.CYAN}Adding navigation links to base template...{Colors.END}\n")

filepath = 'templates/base.html'

if not os.path.exists(filepath):
    print(f"{Colors.YELLOW}⚠{Colors.END} base.html not found at {filepath}")
    print("Trying templates/layouts/base.html...")
    filepath = 'templates/layouts/base.html'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Scanner' not in content:
        # Find the navigation section (look for Events or Profile link)
        if '<a class="nav-link" href="{{ url_for(\'events.index\')' in content:
            # Add after Events link
            content = content.replace(
                '</a>\n                    </li>\n                    <!-- Profile',
                '</a>\n                    </li>' + NAVIGATION_ADDITIONS + '\n                    <!-- Profile'
            )
        
        # Add Event Admin dropdown before System Manager
        if 'System Manager' in content and 'Event Admin' not in content:
            content = content.replace(
                '<!-- System Manager',
                EVENT_ADMIN_NAV + '\n                    <!-- System Manager'
            )
        
        # Backup
        with open(filepath + '.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write updated
        with open(filepath, 'w', encoding='utf-8') as f_out:
            f_out.write(content)
        
        print(f"{Colors.GREEN}✓{Colors.END} Added NFC Scanner link")
        print(f"{Colors.GREEN}✓{Colors.END} Added My QR Code link")
        print(f"{Colors.GREEN}✓{Colors.END} Added Event Admin dropdown")
        print(f"{Colors.GREEN}✓{Colors.END} Backup created: {filepath}.backup")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} Navigation links already exist")
    
    print(f"\n{Colors.GREEN}✅ Navigation updated!{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")
    print(f"\n{Colors.CYAN}Manual steps:{Colors.END}")
    print("1. Open templates/base.html")
    print("2. Add these navigation links in the navbar")