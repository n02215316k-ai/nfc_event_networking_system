import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def create_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

# 1. Update base.html navigation
BASE_NAV_UPDATE = """
                    <!-- Events -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('events.index') }}">
                            <i class="fas fa-calendar me-1"></i>Events
                        </a>
                    </li>
                    
                    <!-- NFC SCANNER - NEW -->
                    <li class="nav-item">
                        <a class="nav-link text-primary fw-bold" href="/nfc/scanner">
                            <i class="fas fa-qrcode me-1"></i>🆕 Scanner
                        </a>
                    </li>
                    
                    <!-- MY QR CODE - NEW -->
                    <li class="nav-item">
                        <a class="nav-link text-success fw-bold" href="/profile/my-nfc">
                            <i class="fas fa-id-card me-1"></i>🆕 My QR Code
                        </a>
                    </li>
"""

EVENT_ADMIN_NAV = """
                    <!-- EVENT ADMIN - NEW (for event_admin and system_manager only) -->
                    {% if session.get('role') in ['event_admin', 'system_manager'] %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle text-info fw-bold" href="#" id="eventAdminDropdown" 
                           role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-calendar-check me-1"></i>🆕 Event Admin
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="eventAdminDropdown">
                            <li>
                                <a class="dropdown-item" href="/event-admin/dashboard">
                                    <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="/events/create">
                                    <i class="fas fa-plus me-2"></i>Create Event
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="/event-admin/networking-analytics">
                                    <i class="fas fa-project-diagram me-2"></i>Networking Analytics
                                </a>
                            </li>
                        </ul>
                    </li>
                    {% endif %}
"""

# 2. Create a home page dashboard widget
HOME_DASHBOARD_WIDGET = """
{% extends "base.html" %}

{% block title %}Home - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Welcome Banner -->
    <div class="jumbotron bg-primary text-white p-5 rounded mb-4">
        <h1 class="display-4">Welcome to NFC Events! 🎉</h1>
        <p class="lead">Connect, Network, and Attend Events with NFC & QR Technology</p>
    </div>

    <!-- Quick Access Cards - NEW NFC FEATURES -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="mb-3"><i class="fas fa-rocket me-2"></i>🆕 New Features - Quick Access</h3>
        </div>
        
        <!-- Scanner Card -->
        <div class="col-md-4 mb-3">
            <div class="card border-primary h-100 shadow-sm hover-card">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-qrcode fa-4x text-primary"></i>
                    </div>
                    <h5 class="card-title">NFC/QR Scanner</h5>
                    <p class="card-text">Scan NFC tags or QR codes for event check-in and networking</p>
                    <a href="/nfc/scanner" class="btn btn-primary btn-lg w-100">
                        <i class="fas fa-camera me-2"></i>Open Scanner
                    </a>
                </div>
            </div>
        </div>

        <!-- My QR Code Card -->
        <div class="col-md-4 mb-3">
            <div class="card border-success h-100 shadow-sm hover-card">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-id-card fa-4x text-success"></i>
                    </div>
                    <h5 class="card-title">My Digital Pass</h5>
                    <p class="card-text">View and share your personal QR code for event check-ins</p>
                    <a href="/profile/my-nfc" class="btn btn-success btn-lg w-100">
                        <i class="fas fa-qrcode me-2"></i>View My QR
                    </a>
                </div>
            </div>
        </div>

        <!-- Event Admin Card (conditionally shown) -->
        {% if session.get('role') in ['event_admin', 'system_manager'] %}
        <div class="col-md-4 mb-3">
            <div class="card border-info h-100 shadow-sm hover-card">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-calendar-check fa-4x text-info"></i>
                    </div>
                    <h5 class="card-title">Event Admin Dashboard</h5>
                    <p class="card-text">Manage events, track attendance, and view analytics</p>
                    <a href="/event-admin/dashboard" class="btn btn-info btn-lg w-100">
                        <i class="fas fa-tachometer-alt me-2"></i>Open Dashboard
                    </a>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <!-- How It Works Section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-dark text-white">
                    <h4 class="mb-0"><i class="fas fa-info-circle me-2"></i>How NFC/QR Features Work</h4>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <h5><i class="fas fa-sign-in-alt text-primary me-2"></i>1. Check-In</h5>
                            <p>Use the Scanner to check-in to events by scanning QR codes or using NFC</p>
                        </div>
                        <div class="col-md-4 mb-3">
                            <h5><i class="fas fa-network-wired text-success me-2"></i>2. Network</h5>
                            <p>Automatically connect with attendees when you scan their NFC tag or QR code</p>
                        </div>
                        <div class="col-md-4 mb-3">
                            <h5><i class="fas fa-chart-line text-info me-2"></i>3. Track</h5>
                            <p>Event admins can track real-time attendance and networking analytics</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Upcoming Events -->
    <div class="row">
        <div class="col-12">
            <h3 class="mb-3"><i class="fas fa-calendar-alt me-2"></i>Upcoming Events</h3>
            <div class="card">
                <div class="card-body">
                    <p class="text-center">
                        <a href="/events" class="btn btn-primary btn-lg">
                            <i class="fas fa-calendar me-2"></i>Browse All Events
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.hover-card {
    transition: transform 0.3s, box-shadow 0.3s;
}
.hover-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}
</style>
{% endblock %}
"""

# 3. Update main route to show new dashboard
HOME_ROUTE_UPDATE = """
@app.route('/')
def index():
    '''Home page with NFC features showcase'''
    return render_template('index.html')
"""

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}INTEGRATING NFC/QR UI - MAKING EVERYTHING VISIBLE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Create new home page
print(f"{Colors.CYAN}Step 1: Creating new home page with NFC features...{Colors.END}\n")
create_file('templates/index.html', HOME_DASHBOARD_WIDGET)

print(f"\n{Colors.CYAN}Step 2: Creating navigation update instructions...{Colors.END}\n")

nav_instructions = f"""
{Colors.YELLOW}MANUAL STEP REQUIRED:{Colors.END}

Open: {Colors.CYAN}templates/base.html{Colors.END}

Find the navigation section (around line 30-50) where you see:
    <li class="nav-item">
        <a class="nav-link" href="{{{{ url_for('events.index') }}}}">Events</a>
    </li>

{Colors.GREEN}REPLACE IT WITH:{Colors.END}

{BASE_NAV_UPDATE}

{Colors.YELLOW}THEN ADD THIS BEFORE THE SYSTEM MANAGER DROPDOWN:{Colors.END}

{EVENT_ADMIN_NAV}
"""

with open('NAVIGATION_UPDATE_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
    f.write(nav_instructions)

print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}NAVIGATION_UPDATE_INSTRUCTIONS.txt{Colors.END}")

# Create a test routes file to verify everything works
TEST_ROUTES = """
# Add these test routes to app.py to verify NFC functionality

@app.route('/test-nfc')
def test_nfc():
    '''Test NFC routes'''
    return '''
    <h1>NFC Routes Test</h1>
    <ul>
        <li><a href="/nfc/scanner">Scanner Page</a></li>
        <li><a href="/profile/my-nfc">My QR Code</a></li>
        <li><a href="/event-admin/dashboard">Event Admin Dashboard</a></li>
    </ul>
    '''
"""

create_file('test_routes.txt', TEST_ROUTES)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}SETUP COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.CYAN}NEXT STEPS:{Colors.END}\n")
print(f"1. {Colors.YELLOW}Update base.html navigation:{Colors.END}")
print(f"   Open: NAVIGATION_UPDATE_INSTRUCTIONS.txt")
print(f"   Follow the instructions to update templates/base.html\n")

print(f"2. {Colors.YELLOW}Restart the app:{Colors.END}")
print(f"   python app.py\n")

print(f"3. {Colors.YELLOW}Access the new features:{Colors.END}")
print(f"   • Home: http://localhost:5000/")
print(f"   • Scanner: http://localhost:5000/nfc/scanner")
print(f"   • My QR Code: http://localhost:5000/profile/my-nfc")
print(f"   • Event Admin: http://localhost:5000/event-admin/dashboard")
print(f"   • Test Page: http://localhost:5000/test-nfc\n")

print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")