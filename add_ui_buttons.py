import os
import shutil

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def backup_file(filepath):
    """Create backup of file"""
    if os.path.exists(filepath):
        backup_path = filepath + '.backup_' + str(int(__import__('time').time()))
        shutil.copy2(filepath, backup_path)
        print(f"{Colors.GREEN}✓{Colors.END} Backup: {backup_path}")
        return True
    return False

def add_nfc_buttons_to_base():
    """Add NFC quick access buttons to base.html navigation"""
    filepath = 'templates/base.html'
    
    if not os.path.exists(filepath):
        print(f"{Colors.YELLOW}⚠{Colors.END} base.html not found")
        return
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'NFC Scanner' in content and 'nav-link' in content:
        print(f"{Colors.YELLOW}○{Colors.END} NFC buttons already in navigation")
        return
    
    # Add NFC buttons to navbar
    nfc_nav_items = """
                    <!-- NFC/QR Features -->
                    <li class="nav-item">
                        <a class="nav-link" href="/nfc/scanner">
                            <i class="fas fa-qrcode me-1"></i>Scanner
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/profile/my-nfc">
                            <i class="fas fa-id-card me-1"></i>My QR
                        </a>
                    </li>
"""
    
    # Find where to insert (after Events link)
    if '<a class="nav-link" href="{{ url_for(\'events.index\') }}">' in content:
        content = content.replace(
            '</a>\n                    </li>\n                    <!-- Messages',
            '</a>\n                    </li>' + nfc_nav_items + '\n                    <!-- Messages'
        )
    
    # Add Event Admin for admins
    event_admin_nav = """
                    <!-- Event Admin (for event_admin and system_manager) -->
                    {% if session.get('role') in ['event_admin', 'system_manager'] %}
                    <li class="nav-item">
                        <a class="nav-link" href="/event-admin/dashboard">
                            <i class="fas fa-calendar-check me-1"></i>Event Admin
                        </a>
                    </li>
                    {% endif %}
"""
    
    # Add before System Manager
    if 'System Manager' in content and 'Event Admin' not in content:
        content = content.replace(
            '<!-- System Manager',
            event_admin_nav + '\n                    <!-- System Manager'
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Added NFC buttons to navigation")

def add_nfc_widget_to_events_page():
    """Add NFC quick access widget to events index page"""
    filepath = 'templates/events/index.html'
    
    if not os.path.exists(filepath):
        print(f"{Colors.YELLOW}⚠{Colors.END} events/index.html not found")
        return
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'NFC Quick Access' in content:
        print(f"{Colors.YELLOW}○{Colors.END} NFC widget already in events page")
        return
    
    widget = """
<!-- NFC Quick Access Widget -->
<div class="row mb-4">
    <div class="col-12">
        <div class="card border-primary">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h5 class="mb-2"><i class="fas fa-qrcode text-primary me-2"></i>NFC Quick Access</h5>
                        <p class="mb-0 text-muted">Check-in to events or network with attendees using NFC/QR technology</p>
                    </div>
                    <div class="col-md-4 text-end">
                        <a href="/nfc/scanner" class="btn btn-primary me-2">
                            <i class="fas fa-camera me-1"></i>Open Scanner
                        </a>
                        <a href="/profile/my-nfc" class="btn btn-outline-primary">
                            <i class="fas fa-id-card me-1"></i>My QR Code
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""
    
    # Insert after {% block content %} or after first h2
    if '{% block content %}' in content:
        content = content.replace(
            '{% block content %}',
            '{% block content %}\n' + widget
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Added NFC widget to events page")

def add_nfc_buttons_to_event_detail():
    """Add NFC check-in button to event detail page"""
    filepath = 'templates/events/detail.html'
    
    if not os.path.exists(filepath):
        print(f"{Colors.YELLOW}⚠{Colors.END} events/detail.html not found")
        return
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Quick Check-in' in content:
        print(f"{Colors.YELLOW}○{Colors.END} Check-in button already exists")
        return
    
    checkin_button = """
    <!-- Quick NFC Check-in -->
    <div class="alert alert-info mt-3">
        <div class="row align-items-center">
            <div class="col-md-8">
                <h6 class="mb-1"><i class="fas fa-qrcode me-2"></i>Quick Check-in Available</h6>
                <small>Use NFC/QR scanner to check-in to this event</small>
            </div>
            <div class="col-md-4 text-end">
                <a href="/nfc/scanner" class="btn btn-primary">
                    <i class="fas fa-camera me-1"></i>Scan to Check-in
                </a>
            </div>
        </div>
    </div>
"""
    
    # Find registration button area and add check-in option
    if 'Register for Event' in content or 'Already Registered' in content:
        # Add after the registration section
        content = content.replace(
            '</form>',
            '</form>' + checkin_button
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Added check-in button to event detail")

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}PHASE 1: ADDING UI BUTTONS TO EXISTING PAGES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

add_nfc_buttons_to_base()
add_nfc_widget_to_events_page()
add_nfc_buttons_to_event_detail()

print(f"\n{Colors.GREEN}✅ UI buttons added to existing pages!{Colors.END}\n")