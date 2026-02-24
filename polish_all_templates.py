import os
import shutil

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}POLISHING ALL UI TEMPLATES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Create backup
backup_dir = 'templates_backup'
if os.path.exists('templates') and not os.path.exists(backup_dir):
    shutil.copytree('templates', backup_dir)
    print(f"{Colors.GREEN}✓{Colors.END} Backup created at: {backup_dir}\n")

# Ensure directories exist
os.makedirs('templates/auth', exist_ok=True)
os.makedirs('templates/events', exist_ok=True)
os.makedirs('templates/profile', exist_ok=True)
os.makedirs('templates/nfc', exist_ok=True)
os.makedirs('templates/forums', exist_ok=True)

templates_created = []

# ============================================================================
# 1. DASHBOARD
# ============================================================================
DASHBOARD = """{% extends 'base.html' %}

{% block title %}Dashboard - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-4">
    
    <!-- Welcome Banner -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow-lg animate-in" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none;">
                <div class="card-body text-white p-5">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h1 class="display-4 fw-bold mb-3">
                                <i class="fas fa-hand-wave me-2"></i>
                                Welcome back, {{ session.full_name }}!
                            </h1>
                            <p class="lead mb-0">
                                <i class="fas fa-briefcase me-2"></i>
                                {{ session.job_title or 'Event Attendee' }} 
                                {% if session.company %}at {{ session.company }}{% endif %}
                            </p>
                        </div>
                        <div class="col-md-4 text-end">
                            <div class="bg-white bg-opacity-25 rounded-3 p-3">
                                <h5 class="mb-2">Quick Actions</h5>
                                <div class="d-grid gap-2">
                                    <a href="/nfc/scanner" class="btn btn-light btn-sm">
                                        <i class="fas fa-qrcode me-2"></i>Scan Now
                                    </a>
                                    <a href="/profile/my-nfc" class="btn btn-light btn-sm">
                                        <i class="fas fa-id-card me-2"></i>My QR
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Stats Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card shadow-sm animate-in">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-calendar-check fa-3x text-primary"></i>
                    </div>
                    <h3 class="fw-bold">{{ stats.registered_events or 0 }}</h3>
                    <p class="text-muted mb-0">Registered Events</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card shadow-sm animate-in">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-users fa-3x text-success"></i>
                    </div>
                    <h3 class="fw-bold">{{ stats.connections or 0 }}</h3>
                    <p class="text-muted mb-0">Connections</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card shadow-sm animate-in">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-qrcode fa-3x text-info"></i>
                    </div>
                    <h3 class="fw-bold">{{ stats.scans or 0 }}</h3>
                    <p class="text-muted mb-0">Total Scans</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card shadow-sm animate-in">
                <div class="card-body text-center">
                    <div class="mb-3">
                        <i class="fas fa-comments fa-3x text-warning"></i>
                    </div>
                    <h3 class="fw-bold">{{ stats.forum_posts or 0 }}</h3>
                    <p class="text-muted mb-0">Forum Posts</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main Content Row -->
    <div class="row g-4">
        
        <!-- Upcoming Events -->
        <div class="col-lg-8">
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-calendar-alt me-2"></i>
                        Upcoming Events
                    </h5>
                </div>
                <div class="card-body">
                    {% if upcoming_events %}
                        <div class="list-group list-group-flush">
                            {% for event in upcoming_events %}
                            <a href="/events/{{ event.id }}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between align-items-center">
                                    <div>
                                        <h6 class="mb-1 fw-bold">{{ event.title }}</h6>
                                        <p class="mb-1 text-muted small">
                                            <i class="fas fa-map-marker-alt me-1"></i>
                                            {{ event.location }}
                                        </p>
                                    </div>
                                    <div class="text-end">
                                        <span class="badge bg-primary">
                                            <i class="fas fa-calendar me-1"></i>
                                            {{ event.event_date.strftime('%b %d') }}
                                        </span>
                                    </div>
                                </div>
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-5 text-muted">
                            <i class="fas fa-calendar-times fa-3x mb-3"></i>
                            <p>No upcoming events</p>
                            <a href="/events" class="btn btn-primary">Browse Events</a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="col-lg-4">
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-bolt me-2"></i>
                        Recent Activity
                    </h5>
                </div>
                <div class="card-body">
                    {% if recent_activity %}
                        <div class="timeline">
                            {% for activity in recent_activity %}
                            <div class="timeline-item mb-3">
                                <div class="d-flex">
                                    <div class="flex-shrink-0">
                                        <i class="fas fa-{{ activity.icon }} text-primary"></i>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <p class="mb-0 small">{{ activity.description }}</p>
                                        <small class="text-muted">{{ activity.time }}</small>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4 text-muted">
                            <i class="fas fa-history fa-2x mb-2"></i>
                            <p class="mb-0 small">No recent activity</p>
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <!-- Quick Links -->
            <div class="card shadow-lg mt-4 animate-in">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-link me-2"></i>
                        Quick Links
                    </h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="/nfc/scanner" class="btn btn-outline-primary">
                            <i class="fas fa-qrcode me-2"></i>Scanner
                        </a>
                        <a href="/events" class="btn btn-outline-primary">
                            <i class="fas fa-calendar me-2"></i>Browse Events
                        </a>
                        <a href="/nfc/my-connections" class="btn btn-outline-primary">
                            <i class="fas fa-users me-2"></i>My Connections
                        </a>
                        <a href="/forums" class="btn btn-outline-primary">
                            <i class="fas fa-comments me-2"></i>Forums
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</div>
{% endblock %}
"""

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(DASHBOARD.strip())
templates_created.append('dashboard.html')

# ============================================================================
# 2. LOGIN PAGE
# ============================================================================
LOGIN = """{% extends 'base.html' %}

{% block title %}Login - Event Social Network{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
        <div class="col-md-5">
            <div class="card shadow-lg animate-in">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="fas fa-calendar-alt fa-4x mb-3" style="background: linear-gradient(135deg, #4F46E5, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
                        <h2 class="fw-bold">Welcome Back!</h2>
                        <p class="text-muted">Login to your account</p>
                    </div>
                    
                    <form method="POST" action="/login">
                        <div class="mb-4">
                            <label class="form-label fw-bold">
                                <i class="fas fa-envelope me-2"></i>Email
                            </label>
                            <input type="email" name="email" class="form-control form-control-lg" 
                                   placeholder="your.email@example.com" required autofocus>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">
                                <i class="fas fa-lock me-2"></i>Password
                            </label>
                            <input type="password" name="password" class="form-control form-control-lg" 
                                   placeholder="Enter your password" required>
                        </div>
                        
                        <div class="mb-4 form-check">
                            <input type="checkbox" name="remember" class="form-check-input" id="remember">
                            <label class="form-check-label" for="remember">
                                Remember me
                            </label>
                        </div>
                        
                        <div class="d-grid mb-3">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-sign-in-alt me-2"></i>
                                Login
                            </button>
                        </div>
                        
                        <div class="text-center">
                            <p class="text-muted mb-0">
                                Don't have an account? 
                                <a href="/register" class="text-decoration-none fw-bold">Register here</a>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(LOGIN.strip())
templates_created.append('auth/login.html')

# ============================================================================
# 3. REGISTER PAGE
# ============================================================================
REGISTER = """{% extends 'base.html' %}

{% block title %}Register - Event Social Network{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center my-5">
        <div class="col-md-6">
            <div class="card shadow-lg animate-in">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="fas fa-user-plus fa-4x mb-3" style="background: linear-gradient(135deg, #4F46E5, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
                        <h2 class="fw-bold">Create Account</h2>
                        <p class="text-muted">Join our event community</p>
                    </div>
                    
                    <form method="POST" action="/register">
                        <div class="row">
                            <div class="col-md-12 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-user me-2"></i>Full Name
                                </label>
                                <input type="text" name="full_name" class="form-control form-control-lg" 
                                       placeholder="John Doe" required>
                            </div>
                            
                            <div class="col-md-12 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-envelope me-2"></i>Email
                                </label>
                                <input type="email" name="email" class="form-control form-control-lg" 
                                       placeholder="john.doe@example.com" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-briefcase me-2"></i>Job Title
                                </label>
                                <input type="text" name="job_title" class="form-control form-control-lg" 
                                       placeholder="Software Engineer">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-building me-2"></i>Company
                                </label>
                                <input type="text" name="company" class="form-control form-control-lg" 
                                       placeholder="Acme Corp">
                            </div>
                            
                            <div class="col-md-12 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-phone me-2"></i>Phone
                                </label>
                                <input type="tel" name="phone" class="form-control form-control-lg" 
                                       placeholder="+1234567890">
                            </div>
                            
                            <div class="col-md-12 mb-3">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-lock me-2"></i>Password
                                </label>
                                <input type="password" name="password" class="form-control form-control-lg" 
                                       placeholder="Min 6 characters" required minlength="6">
                            </div>
                            
                            <div class="col-md-12 mb-4">
                                <label class="form-label fw-bold">
                                    <i class="fas fa-lock me-2"></i>Confirm Password
                                </label>
                                <input type="password" name="confirm_password" class="form-control form-control-lg" 
                                       placeholder="Re-enter password" required>
                            </div>
                        </div>
                        
                        <div class="d-grid mb-3">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-user-plus me-2"></i>
                                Create Account
                            </button>
                        </div>
                        
                        <div class="text-center">
                            <p class="text-muted mb-0">
                                Already have an account? 
                                <a href="/login" class="text-decoration-none fw-bold">Login here</a>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/auth/register.html', 'w', encoding='utf-8') as f:
    f.write(REGISTER.strip())
templates_created.append('auth/register.html')

# ============================================================================
# 4. EVENTS LIST
# ============================================================================
EVENTS_LIST = """{% extends 'base.html' %}

{% block title %}Events - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-4">
    
    <!-- Page Header -->
    <div class="row mb-4">
        <div class="col-md-8">
            <h1 class="display-5 fw-bold text-white">
                <i class="fas fa-calendar-alt me-3"></i>
                All Events
            </h1>
            <p class="lead text-white">Discover and join amazing events</p>
        </div>
        <div class="col-md-4 text-end">
            {% if session.role in ['event_admin', 'system_manager'] %}
            <a href="/events/create" class="btn btn-success btn-lg">
                <i class="fas fa-plus-circle me-2"></i>
                Create Event
            </a>
            {% endif %}
        </div>
    </div>
    
    <!-- Filter Bar -->
    <div class="card shadow-lg mb-4 animate-in">
        <div class="card-body">
            <div class="row g-3">
                <div class="col-md-4">
                    <input type="text" class="form-control" id="searchEvents" 
                           placeholder="🔍 Search events...">
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="filterCategory">
                        <option value="">All Categories</option>
                        <option value="tech">Technology</option>
                        <option value="business">Business</option>
                        <option value="networking">Networking</option>
                        <option value="workshop">Workshop</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="filterStatus">
                        <option value="upcoming">Upcoming</option>
                        <option value="past">Past</option>
                        <option value="all">All Events</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-primary w-100">
                        <i class="fas fa-filter me-2"></i>Filter
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Events Grid -->
    <div class="row g-4">
        {% if events %}
            {% for event in events %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-lg animate-in">
                    {% if event.image_url %}
                    <img src="{{ event.image_url }}" class="card-img-top" alt="{{ event.title }}" style="height: 200px; object-fit: cover;">
                    {% else %}
                    <div class="card-img-top bg-gradient d-flex align-items-center justify-content-center" 
                         style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <i class="fas fa-calendar-alt fa-4x text-white"></i>
                    </div>
                    {% endif %}
                    
                    <div class="card-body">
                        <h5 class="card-title fw-bold">{{ event.title }}</h5>
                        <p class="card-text text-muted">{{ event.description[:100] }}...</p>
                        
                        <div class="mb-2">
                            <i class="fas fa-calendar text-primary me-2"></i>
                            <small>{{ event.event_date.strftime('%B %d, %Y') }}</small>
                        </div>
                        
                        <div class="mb-2">
                            <i class="fas fa-clock text-primary me-2"></i>
                            <small>{{ event.event_time }}</small>
                        </div>
                        
                        <div class="mb-3">
                            <i class="fas fa-map-marker-alt text-primary me-2"></i>
                            <small>{{ event.location }}</small>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-primary">
                                <i class="fas fa-users me-1"></i>
                                {{ event.attendee_count or 0 }} attending
                            </span>
                            <a href="/events/{{ event.id }}" class="btn btn-sm btn-outline-primary">
                                View Details
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="card shadow-lg">
                    <div class="card-body text-center py-5">
                        <i class="fas fa-calendar-times fa-5x text-muted mb-4"></i>
                        <h3>No Events Found</h3>
                        <p class="text-muted">Check back later for upcoming events</p>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
    
</div>
{% endblock %}
"""

with open('templates/events/list.html', 'w', encoding='utf-8') as f:
    f.write(EVENTS_LIST.strip())
templates_created.append('events/list.html')

# ============================================================================
# 5. MY NFC/QR CODE PAGE
# ============================================================================
MY_NFC = """{% extends 'base.html' %}

{% block title %}My NFC/QR Code{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <!-- Page Header -->
            <div class="text-center mb-4 text-white animate-in">
                <h1 class="display-4 fw-bold">
                    <i class="fas fa-id-card me-3"></i>
                    My NFC Badge
                </h1>
                <p class="lead">Share this QR code for instant networking</p>
            </div>
            
            <!-- Main QR Card -->
            <div class="card shadow-lg mb-4 animate-in">
                <div class="card-body p-5 text-center">
                    <h3 class="mb-4 fw-bold">{{ user.full_name }}</h3>
                    
                    {% if user.job_title %}
                    <p class="text-muted mb-1">{{ user.job_title }}</p>
                    {% endif %}
                    {% if user.company %}
                    <p class="text-muted mb-4">{{ user.company }}</p>
                    {% endif %}
                    
                    <!-- QR Code -->
                    {% if nfc_code %}
                    <div class="mb-4">
                        <div class="border rounded-3 p-4 d-inline-block" style="background: white;">
                            <img src="{{ nfc_code }}" alt="QR Code" style="width: 300px; height: 300px;">
                        </div>
                    </div>
                    {% endif %}
                    
                    <!-- Badge ID -->
                    <div class="alert alert-info">
                        <strong>Badge ID:</strong>
                        <code class="fs-5">{{ user.nfc_badge_id }}</code>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="row g-3 mt-4">
                        <div class="col-md-4">
                            <button class="btn btn-primary w-100" onclick="downloadQR()">
                                <i class="fas fa-download me-2"></i>
                                Download QR
                            </button>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-success w-100" onclick="shareQR()">
                                <i class="fas fa-share-alt me-2"></i>
                                Share
                            </button>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-info w-100" onclick="printQR()">
                                <i class="fas fa-print me-2"></i>
                                Print
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Event QR Codes -->
            {% if upcoming_events %}
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-calendar-check me-2"></i>
                        Event Check-in QR Codes
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        {% for event in upcoming_events %}
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-body text-center">
                                    <h6 class="fw-bold">{{ event.title }}</h6>
                                    <small class="text-muted">{{ event.event_date.strftime('%B %d, %Y') }}</small>
                                    {% if event.qr_code %}
                                    <div class="mt-3">
                                        <img src="{{ event.qr_code }}" alt="Event QR" style="width: 150px; height: 150px;">
                                    </div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}
            
        </div>
    </div>
</div>

<script>
function downloadQR() {
    const link = document.createElement('a');
    link.download = 'my-qr-code.png';
    link.href = '{{ nfc_code }}';
    link.click();
}

function shareQR() {
    if (navigator.share) {
        navigator.share({
            title: 'My Event Badge',
            text: 'Connect with me at events!',
            url: window.location.href
        });
    } else {
        alert('Share functionality not supported on this device');
    }
}

function printQR() {
    window.print();
}
</script>
{% endblock %}
"""

with open('templates/profile/my_nfc.html', 'w', encoding='utf-8') as f:
    f.write(MY_NFC.strip())
templates_created.append('profile/my_nfc.html')

# ============================================================================
# 6. MY CONNECTIONS PAGE
# ============================================================================
CONNECTIONS = """{% extends 'base.html' %}

{% block title %}My Connections{% endblock %}

{% block content %}
<div class="container mt-4">
    
    <!-- Page Header -->
    <div class="text-center mb-4 text-white animate-in">
        <h1 class="display-4 fw-bold">
            <i class="fas fa-users me-3"></i>
            My Connections
        </h1>
        <p class="lead">People you've connected with at events</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-4">
            <div class="card shadow-lg text-center animate-in">
                <div class="card-body">
                    <i class="fas fa-users fa-3x text-primary mb-3"></i>
                    <h3 class="fw-bold">{{ connections|length }}</h3>
                    <p class="text-muted mb-0">Total Connections</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-lg text-center animate-in">
                <div class="card-body">
                    <i class="fas fa-qrcode fa-3x text-success mb-3"></i>
                    <h3 class="fw-bold">{{ connections|selectattr('connection_method', 'equalto', 'qr')|list|length }}</h3>
                    <p class="text-muted mb-0">QR Scans</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-lg text-center animate-in">
                <div class="card-body">
                    <i class="fas fa-wifi fa-3x text-info mb-3"></i>
                    <h3 class="fw-bold">{{ connections|selectattr('connection_method', 'equalto', 'nfc')|list|length }}</h3>
                    <p class="text-muted mb-0">NFC Taps</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Search Bar -->
    <div class="card shadow-lg mb-4 animate-in">
        <div class="card-body">
            <div class="input-group input-group-lg">
                <span class="input-group-text">
                    <i class="fas fa-search"></i>
                </span>
                <input type="text" class="form-control" id="searchConnections" 
                       placeholder="Search connections by name, company, or job title...">
            </div>
        </div>
    </div>
    
    <!-- Connections List -->
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">
                <i class="fas fa-address-book me-2"></i>
                All Connections
            </h5>
        </div>
        <div class="card-body">
            {% if connections %}
                <div class="row g-3">
                    {% for conn in connections %}
                    <div class="col-md-6 col-lg-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="flex-shrink-0">
                                        <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center" 
                                             style="width: 50px; height: 50px;">
                                            <span class="fw-bold fs-4">{{ conn.full_name[0] }}</span>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <h6 class="mb-0 fw-bold">{{ conn.full_name }}</h6>
                                        <small class="text-muted">{{ conn.job_title or 'Event Attendee' }}</small>
                                    </div>
                                </div>
                                
                                {% if conn.company %}
                                <p class="text-muted mb-2">
                                    <i class="fas fa-building me-2"></i>
                                    {{ conn.company }}
                                </p>
                                {% endif %}
                                
                                <p class="text-muted mb-2">
                                    <i class="fas fa-envelope me-2"></i>
                                    {{ conn.email }}
                                </p>
                                
                                <div class="d-flex justify-content-between align-items-center mt-3">
                                    <span class="badge bg-{{ 'success' if conn.connection_method == 'nfc' else 'primary' }}">
                                        <i class="fas fa-{{ 'wifi' if conn.connection_method == 'nfc' else 'qrcode' }} me-1"></i>
                                        {{ conn.connection_method.upper() }}
                                    </span>
                                    <small class="text-muted">
                                        {{ conn.connected_at.strftime('%b %d, %Y') if conn.connected_at else 'N/A' }}
                                    </small>
                                </div>
                                
                                <div class="d-grid gap-2 mt-3">
                                    <a href="mailto:{{ conn.email }}" class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-envelope me-1"></i> Email
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-user-friends fa-5x text-muted mb-4"></i>
                    <h4>No Connections Yet</h4>
                    <p class="text-muted">Start scanning QR codes to build your network!</p>
                    <a href="/nfc/scanner" class="btn btn-primary">
                        <i class="fas fa-qrcode me-2"></i>
                        Start Scanning
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
    
</div>

<script>
// Search functionality
document.getElementById('searchConnections').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.col-md-6.col-lg-4');
    
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});
</script>
{% endblock %}
"""

with open('templates/nfc/connections.html', 'w', encoding='utf-8') as f:
    f.write(CONNECTIONS.strip())
templates_created.append('nfc/connections.html')

# Summary
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ UI POLISH COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Templates created/updated ({len(templates_created)}):{Colors.END}")
for template in templates_created:
    print(f"  {Colors.GREEN}✓{Colors.END} {template}")

print(f"\n{Colors.CYAN}Features added to ALL pages:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Modern gradient backgrounds")
print(f"  {Colors.GREEN}✓{Colors.END} Large, visible buttons")
print(f"  {Colors.GREEN}✓{Colors.END} Card-based layouts")
print(f"  {Colors.GREEN}✓{Colors.END} Icon integration")
print(f"  {Colors.GREEN}✓{Colors.END} Responsive design")
print(f"  {Colors.GREEN}✓{Colors.END} Smooth animations")
print(f"  {Colors.GREEN}✓{Colors.END} Professional typography")

print(f"\n{Colors.BOLD}{Colors.CYAN}Next steps:{Colors.END}")
print(f"  1. Run: {Colors.BOLD}python app.py{Colors.END}")
print(f"  2. Visit: {Colors.BOLD}http://localhost:5000{Colors.END}")
print(f"  3. Login and explore all pages")
print()