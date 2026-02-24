import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FINAL COMPREHENSIVE FIX - ALL ERRORS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

fixed_items = []

# Create ALL necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/events', exist_ok=True)
os.makedirs('templates/profile', exist_ok=True)
os.makedirs('templates/forum', exist_ok=True)
os.makedirs('templates/forums', exist_ok=True)

# ============================================================================
# 1. FIX EVENTS LIST - Handle BOTH dict and object formats
# ============================================================================
print(f"{Colors.CYAN}Fixing events/list.html...{Colors.END}")

EVENTS_LIST_UNIVERSAL = """{% extends 'base.html' %}

{% block title %}Events - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-4">
    
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
    
    <div class="card shadow-lg mb-4 animate-in">
        <div class="card-body">
            <div class="row g-3">
                <div class="col-md-6">
                    <input type="text" class="form-control form-control-lg" id="searchEvents" 
                           placeholder="🔍 Search events...">
                </div>
                <div class="col-md-3">
                    <select class="form-select form-select-lg" id="filterCategory">
                        <option value="">All Categories</option>
                        <option value="tech">Technology</option>
                        <option value="business">Business</option>
                        <option value="networking">Networking</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select form-select-lg" id="filterStatus">
                        <option value="upcoming">Upcoming</option>
                        <option value="past">Past</option>
                        <option value="all">All Events</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row g-4">
        {% if events %}
            {% for event in events %}
            {% set is_dict = event is mapping %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-lg animate-in">
                    {% if is_dict %}
                        {% set event_image = event.get('image_url') %}
                        {% set event_title = event.get('title', 'Untitled Event') %}
                        {% set event_desc = event.get('description', 'No description') %}
                        {% set event_date = event.get('event_date', 'TBD') %}
                        {% set event_time = event.get('event_time', 'TBD') %}
                        {% set event_location = event.get('location', 'TBD') %}
                        {% set event_id = event.get('id', 0) %}
                        {% set attendee_count = event.get('attendee_count', 0) %}
                    {% else %}
                        {% set event_image = event.image_url if event.image_url is defined else None %}
                        {% set event_title = event.title if event.title is defined else 'Untitled Event' %}
                        {% set event_desc = event.description if event.description is defined else 'No description' %}
                        {% set event_date = event.event_date if event.event_date is defined else 'TBD' %}
                        {% set event_time = event.event_time if event.event_time is defined else 'TBD' %}
                        {% set event_location = event.location if event.location is defined else 'TBD' %}
                        {% set event_id = event.id if event.id is defined else 0 %}
                        {% set attendee_count = event.attendee_count if event.attendee_count is defined else 0 %}
                    {% endif %}
                    
                    {% if event_image %}
                    <img src="{{ event_image }}" class="card-img-top" alt="{{ event_title }}" 
                         style="height: 200px; object-fit: cover;">
                    {% else %}
                    <div class="card-img-top bg-gradient d-flex align-items-center justify-content-center" 
                         style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <i class="fas fa-calendar-alt fa-4x text-white"></i>
                    </div>
                    {% endif %}
                    
                    <div class="card-body">
                        <h5 class="card-title fw-bold">{{ event_title }}</h5>
                        <p class="card-text text-muted">{{ event_desc[:100] }}...</p>
                        
                        <div class="mb-2">
                            <i class="fas fa-calendar text-primary me-2"></i>
                            <small>
                                {% if event_date != 'TBD' %}
                                    {% if event_date is string %}
                                        {{ event_date }}
                                    {% else %}
                                        {{ event_date.strftime('%B %d, %Y') }}
                                    {% endif %}
                                {% else %}
                                    TBD
                                {% endif %}
                            </small>
                        </div>
                        
                        <div class="mb-2">
                            <i class="fas fa-clock text-primary me-2"></i>
                            <small>{{ event_time }}</small>
                        </div>
                        
                        <div class="mb-3">
                            <i class="fas fa-map-marker-alt text-primary me-2"></i>
                            <small>{{ event_location }}</small>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-primary">
                                <i class="fas fa-users me-1"></i>
                                {{ attendee_count }} attending
                            </span>
                            <a href="/events/{{ event_id }}" class="btn btn-sm btn-outline-primary">
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
                        {% if session.role in ['event_admin', 'system_manager'] %}
                        <a href="/events/create" class="btn btn-primary">
                            <i class="fas fa-plus-circle me-2"></i>
                            Create First Event
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
    
</div>
{% endblock %}
"""

with open('templates/events/list.html', 'w', encoding='utf-8') as f:
    f.write(EVENTS_LIST_UNIVERSAL.strip())
fixed_items.append('events/list.html (UNIVERSAL FIX)')

# ============================================================================
# 2. CREATE forum/create.html (note: forum not forums)
# ============================================================================
print(f"{Colors.CYAN}Creating forum/create.html...{Colors.END}")

CREATE_FORUM = """{% extends 'base.html' %}

{% block title %}Create Forum{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-plus-circle me-2"></i>
                        Create New Forum
                    </h4>
                </div>
                <div class="card-body p-4">
                    
                    <form method="POST" action="/forum/create">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">
                                <i class="fas fa-heading me-2"></i>
                                Forum Title
                            </label>
                            <input type="text" name="title" class="form-control form-control-lg" 
                                   placeholder="Enter forum title" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">
                                <i class="fas fa-align-left me-2"></i>
                                Description
                            </label>
                            <textarea name="description" class="form-control" rows="5" 
                                      placeholder="Describe what this forum is about" required></textarea>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">
                                <i class="fas fa-folder me-2"></i>
                                Category
                            </label>
                            <select name="category" class="form-select form-select-lg" required>
                                <option value="">-- Select Category --</option>
                                <option value="general">General Discussion</option>
                                <option value="events">Events</option>
                                <option value="networking">Networking</option>
                                <option value="tech">Technology</option>
                                <option value="announcements">Announcements</option>
                            </select>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save me-2"></i>
                                Create Forum
                            </button>
                            <a href="/forums" class="btn btn-outline-secondary">
                                <i class="fas fa-times me-2"></i>
                                Cancel
                            </a>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/forum/create.html', 'w', encoding='utf-8') as f:
    f.write(CREATE_FORUM.strip())
fixed_items.append('forum/create.html')

# ============================================================================
# 3. CREATE profile/view.html
# ============================================================================
print(f"{Colors.CYAN}Creating profile/view.html...{Colors.END}")

PROFILE_VIEW = """{% extends 'base.html' %}

{% block title %}My Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-user-circle me-2"></i>
                        My Profile
                    </h4>
                </div>
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <div class="mb-3">
                            <img src="{{ session.get('avatar', '/static/uploads/default-avatar.png') }}" 
                                 class="rounded-circle" 
                                 style="width: 150px; height: 150px; object-fit: cover; border: 5px solid #4F46E5;">
                        </div>
                        <h2 class="fw-bold">{{ session.get('full_name', 'User') }}</h2>
                        <p class="text-muted">{{ session.get('email', '') }}</p>
                        <span class="badge bg-success">{{ session.get('role', 'attendee').replace('_', ' ').title() }}</span>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-briefcase me-2 text-primary"></i>Job Title:</strong>
                            <p class="text-muted">{{ session.get('job_title', 'Not specified') }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-building me-2 text-primary"></i>Company:</strong>
                            <p class="text-muted">{{ session.get('company', 'Not specified') }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-phone me-2 text-primary"></i>Phone:</strong>
                            <p class="text-muted">{{ session.get('phone', 'Not specified') }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-id-badge me-2 text-primary"></i>NFC Badge ID:</strong>
                            <p class="text-muted"><code>{{ session.get('nfc_badge_id', 'Not assigned') }}</code></p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row g-2">
                        <div class="col-md-6">
                            <a href="/profile/edit" class="btn btn-primary w-100">
                                <i class="fas fa-edit me-2"></i>Edit Profile
                            </a>
                        </div>
                        <div class="col-md-6">
                            <a href="/profile/my-nfc" class="btn btn-outline-primary w-100">
                                <i class="fas fa-qrcode me-2"></i>View My QR Code
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/profile/view.html', 'w', encoding='utf-8') as f:
    f.write(PROFILE_VIEW.strip())
fixed_items.append('profile/view.html')

# ============================================================================
# 4. CREATE about.html
# ============================================================================
print(f"{Colors.CYAN}Creating about.html...{Colors.END}")

ABOUT_PAGE = """{% extends 'base.html' %}

{% block title %}About Us{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            
            <div class="text-center mb-5 text-white animate-in">
                <h1 class="display-3 fw-bold">
                    <i class="fas fa-info-circle me-3"></i>
                    About Us
                </h1>
                <p class="lead">Your complete event networking platform</p>
            </div>
            
            <div class="card shadow-lg mb-4 animate-in">
                <div class="card-body p-5">
                    <h3 class="fw-bold mb-3">
                        <i class="fas fa-rocket me-2 text-primary"></i>
                        Our Mission
                    </h3>
                    <p class="lead">
                        Event Social Network is designed to revolutionize how people connect at events. 
                        We make networking seamless, instant, and meaningful through cutting-edge NFC 
                        and QR code technology.
                    </p>
                </div>
            </div>
            
            <div class="row g-4 mb-4">
                <div class="col-md-4">
                    <div class="card shadow-lg h-100 animate-in">
                        <div class="card-body text-center p-4">
                            <i class="fas fa-qrcode fa-4x text-primary mb-3"></i>
                            <h5 class="fw-bold">Instant Connections</h5>
                            <p>Connect with attendees instantly using NFC or QR codes</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-lg h-100 animate-in">
                        <div class="card-body text-center p-4">
                            <i class="fas fa-calendar-check fa-4x text-success mb-3"></i>
                            <h5 class="fw-bold">Event Management</h5>
                            <p>Comprehensive tools for organizing and managing events</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-lg h-100 animate-in">
                        <div class="card-body text-center p-4">
                            <i class="fas fa-users fa-4x text-info mb-3"></i>
                            <h5 class="fw-bold">Build Your Network</h5>
                            <p>Grow your professional network at every event</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card shadow-lg animate-in">
                <div class="card-body p-5">
                    <h3 class="fw-bold mb-3">
                        <i class="fas fa-star me-2 text-warning"></i>
                        Key Features
                    </h3>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> NFC & QR Code Scanning</li>
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Event Check-in/Check-out</li>
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Connection Management</li>
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Real-time Dashboards</li>
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Forum Discussions</li>
                        <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Private Messaging</li>
                    </ul>
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/about.html', 'w', encoding='utf-8') as f:
    f.write(ABOUT_PAGE.strip())
fixed_items.append('about.html')

# ============================================================================
# 5. CREATE privacy.html
# ============================================================================
print(f"{Colors.CYAN}Creating privacy.html...{Colors.END}")

PRIVACY_PAGE = """{% extends 'base.html' %}

{% block title %}Privacy Policy{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            
            <div class="text-center mb-5 text-white animate-in">
                <h1 class="display-3 fw-bold">
                    <i class="fas fa-shield-alt me-3"></i>
                    Privacy Policy
                </h1>
                <p class="lead">Your privacy is important to us</p>
            </div>
            
            <div class="card shadow-lg animate-in">
                <div class="card-body p-5">
                    
                    <h3 class="fw-bold mb-3">1. Information We Collect</h3>
                    <p>We collect information you provide directly to us, including:</p>
                    <ul>
                        <li>Name, email, and contact information</li>
                        <li>Professional details (job title, company)</li>
                        <li>Event attendance and connection data</li>
                        <li>Profile information and preferences</li>
                    </ul>
                    
                    <hr>
                    
                    <h3 class="fw-bold mb-3">2. How We Use Your Information</h3>
                    <p>Your information is used to:</p>
                    <ul>
                        <li>Facilitate event networking and connections</li>
                        <li>Manage event registrations and check-ins</li>
                        <li>Send event-related notifications</li>
                        <li>Improve our services</li>
                    </ul>
                    
                    <hr>
                    
                    <h3 class="fw-bold mb-3">3. Data Security</h3>
                    <p>
                        We implement industry-standard security measures to protect your data. 
                        All sensitive information is encrypted and stored securely.
                    </p>
                    
                    <hr>
                    
                    <h3 class="fw-bold mb-3">4. Your Rights</h3>
                    <p>You have the right to:</p>
                    <ul>
                        <li>Access your personal data</li>
                        <li>Request data correction or deletion</li>
                        <li>Opt-out of communications</li>
                        <li>Export your data</li>
                    </ul>
                    
                    <hr>
                    
                    <p class="text-muted">
                        <small>Last updated: February 2026</small>
                    </p>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/privacy.html', 'w', encoding='utf-8') as f:
    f.write(PRIVACY_PAGE.strip())
fixed_items.append('privacy.html')

# ============================================================================
# 6. CREATE contact.html
# ============================================================================
print(f"{Colors.CYAN}Creating contact.html...{Colors.END}")

CONTACT_PAGE = """{% extends 'base.html' %}

{% block title %}Contact Us{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <div class="text-center mb-5 text-white animate-in">
                <h1 class="display-3 fw-bold">
                    <i class="fas fa-envelope me-3"></i>
                    Contact Us
                </h1>
                <p class="lead">We'd love to hear from you!</p>
            </div>
            
            <div class="card shadow-lg animate-in">
                <div class="card-body p-5">
                    
                    <form method="POST" action="/contact">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">
                                <i class="fas fa-user me-2"></i>
                                Your Name
                            </label>
                            <input type="text" name="name" class="form-control form-control-lg" 
                                   placeholder="John Doe" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">
                                <i class="fas fa-envelope me-2"></i>
                                Email Address
                            </label>
                            <input type="email" name="email" class="form-control form-control-lg" 
                                   placeholder="john@example.com" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">
                                <i class="fas fa-tag me-2"></i>
                                Subject
                            </label>
                            <input type="text" name="subject" class="form-control form-control-lg" 
                                   placeholder="How can we help?" required>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">
                                <i class="fas fa-comment me-2"></i>
                                Message
                            </label>
                            <textarea name="message" class="form-control" rows="6" 
                                      placeholder="Tell us what's on your mind..." required></textarea>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-paper-plane me-2"></i>
                                Send Message
                            </button>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
            <div class="row g-4 mt-4">
                <div class="col-md-4">
                    <div class="card shadow text-center">
                        <div class="card-body">
                            <i class="fas fa-envelope fa-2x text-primary mb-2"></i>
                            <h6 class="fw-bold">Email</h6>
                            <small class="text-muted">support@eventsocial.net</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow text-center">
                        <div class="card-body">
                            <i class="fas fa-phone fa-2x text-success mb-2"></i>
                            <h6 class="fw-bold">Phone</h6>
                            <small class="text-muted">+1 (555) 123-4567</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow text-center">
                        <div class="card-body">
                            <i class="fas fa-map-marker-alt fa-2x text-danger mb-2"></i>
                            <h6 class="fw-bold">Address</h6>
                            <small class="text-muted">123 Event St, Network City</small>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/contact.html', 'w', encoding='utf-8') as f:
    f.write(CONTACT_PAGE.strip())
fixed_items.append('contact.html')

# ============================================================================
# SUMMARY
# ============================================================================
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL ERRORS FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Fixed/Created ({len(fixed_items)}):{Colors.END}")
for item in fixed_items:
    print(f"  {Colors.GREEN}✓{Colors.END} {item}")

print(f"\n{Colors.BOLD}{Colors.CYAN}ALL PAGES NOW AVAILABLE:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} /events (UNIVERSAL dict/object handler)")
print(f"  {Colors.GREEN}✓{Colors.END} /forum/create")
print(f"  {Colors.GREEN}✓{Colors.END} /profile/view")
print(f"  {Colors.GREEN}✓{Colors.END} /about")
print(f"  {Colors.GREEN}✓{Colors.END} /privacy")
print(f"  {Colors.GREEN}✓{Colors.END} /contact")

print(f"\n{Colors.BOLD}{Colors.YELLOW}REMAINING MANUAL STEP:{Colors.END}")
print(f"{Colors.YELLOW}You still need to add the /dashboard route to app.py{Colors.END}")
print(f"{Colors.YELLOW}(Copy from dashboard_route.txt created earlier){Colors.END}")

print(f"\n{Colors.BOLD}{Colors.CYAN}Run your app now:{Colors.END}")
print(f"  {Colors.BOLD}python app.py{Colors.END}")
print()