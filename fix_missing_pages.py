import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING ALL MISSING ROUTES & TEMPLATES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

fixed_items = []

# Create directories
os.makedirs('templates/events', exist_ok=True)
os.makedirs('templates/profile', exist_ok=True)
os.makedirs('templates/forums', exist_ok=True)

# ============================================================================
# 1. FIX DASHBOARD ROUTE in app.py
# ============================================================================
print(f"{Colors.CYAN}Checking app.py for dashboard route...{Colors.END}")

APP_DASHBOARD_ROUTE = """
# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    '''User dashboard'''
    from src.database.db import execute_query
    
    user_id = session.get('user_id')
    
    # Get stats
    stats = {
        'registered_events': execute_query(
            "SELECT COUNT(*) as count FROM event_registrations WHERE user_id = %s",
            (user_id,), fetch=True, fetchone=True
        )['count'] if execute_query("SELECT COUNT(*) as count FROM event_registrations WHERE user_id = %s", (user_id,), fetch=True, fetchone=True) else 0,
        
        'connections': execute_query(
            "SELECT COUNT(*) as count FROM connections WHERE user_id = %s OR connected_user_id = %s",
            (user_id, user_id), fetch=True, fetchone=True
        )['count'] if execute_query("SELECT COUNT(*) as count FROM connections WHERE user_id = %s OR connected_user_id = %s", (user_id, user_id), fetch=True, fetchone=True) else 0,
        
        'scans': execute_query(
            "SELECT COUNT(*) as count FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s",
            (user_id, user_id), fetch=True, fetchone=True
        )['count'] if execute_query("SELECT COUNT(*) as count FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s", (user_id, user_id), fetch=True, fetchone=True) else 0,
        
        'forum_posts': execute_query(
            "SELECT COUNT(*) as count FROM forum_posts WHERE user_id = %s",
            (user_id,), fetch=True, fetchone=True
        )['count'] if execute_query("SELECT COUNT(*) as count FROM forum_posts WHERE user_id = %s", (user_id,), fetch=True, fetchone=True) else 0
    }
    
    # Get upcoming events
    upcoming_events = execute_query(
        \"\"\"
        SELECT e.* FROM events e
        JOIN event_registrations er ON e.id = er.event_id
        WHERE er.user_id = %s AND e.event_date >= CURDATE()
        ORDER BY e.event_date ASC
        LIMIT 5
        \"\"\",
        (user_id,), fetch=True
    ) or []
    
    # Recent activity (placeholder)
    recent_activity = []
    
    return render_template('dashboard.html', 
                         stats=stats,
                         upcoming_events=upcoming_events,
                         recent_activity=recent_activity)
"""

# Note: User needs to manually add this to app.py after the imports
print(f"{Colors.YELLOW}⚠{Colors.END} Add dashboard route to app.py manually (see dashboard_route.txt)")
with open('dashboard_route.txt', 'w') as f:
    f.write(APP_DASHBOARD_ROUTE.strip())
fixed_items.append("dashboard_route.txt created")

# ============================================================================
# 2. MY EVENTS TEMPLATE
# ============================================================================
MY_EVENTS = """{% extends 'base.html' %}

{% block title %}My Events{% endblock %}

{% block content %}
<div class="container mt-4">
    
    <div class="text-center mb-4 text-white animate-in">
        <h1 class="display-4 fw-bold">
            <i class="fas fa-calendar-check me-3"></i>
            My Events
        </h1>
        <p class="lead">Events you've registered for</p>
    </div>
    
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">
                <i class="fas fa-list me-2"></i>
                Registered Events
            </h5>
        </div>
        <div class="card-body">
            {% if events %}
                <div class="row g-4">
                    {% for event in events %}
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title fw-bold">{{ event.title or event['title'] }}</h5>
                                <p class="card-text text-muted">
                                    {{ (event.description or event['description'])[:150] }}...
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-calendar text-primary me-2"></i>
                                    {% if event.event_date %}
                                        {{ event.event_date.strftime('%B %d, %Y') if event.event_date.__class__.__name__ != 'str' else event.event_date }}
                                    {% else %}
                                        {{ event['event_date'] }}
                                    {% endif %}
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-clock text-primary me-2"></i>
                                    {{ event.event_time or event['event_time'] }}
                                </p>
                                <p class="mb-3">
                                    <i class="fas fa-map-marker-alt text-primary me-2"></i>
                                    {{ event.location or event['location'] }}
                                </p>
                                <a href="/events/{{ event.id or event['id'] }}" class="btn btn-primary">
                                    View Details
                                </a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-calendar-times fa-5x text-muted mb-4"></i>
                    <h4>No Events Registered</h4>
                    <p class="text-muted">Browse events and register to see them here</p>
                    <a href="/events" class="btn btn-primary">
                        <i class="fas fa-calendar me-2"></i>
                        Browse Events
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
    
</div>
{% endblock %}
"""

with open('templates/events/my_events.html', 'w', encoding='utf-8') as f:
    f.write(MY_EVENTS.strip())
fixed_items.append('events/my_events.html')

# ============================================================================
# 3. FIX EVENTS LIST TEMPLATE (handle dict objects)
# ============================================================================
EVENTS_LIST_FIXED = """{% extends 'base.html' %}

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
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-lg animate-in">
                    {% set event_image = event.image_url or event.get('image_url') %}
                    {% if event_image %}
                    <img src="{{ event_image }}" class="card-img-top" alt="{{ event.title or event['title'] }}" 
                         style="height: 200px; object-fit: cover;">
                    {% else %}
                    <div class="card-img-top bg-gradient d-flex align-items-center justify-content-center" 
                         style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <i class="fas fa-calendar-alt fa-4x text-white"></i>
                    </div>
                    {% endif %}
                    
                    <div class="card-body">
                        <h5 class="card-title fw-bold">{{ event.title or event['title'] }}</h5>
                        <p class="card-text text-muted">
                            {{ (event.description or event['description'] or 'No description')[:100] }}...
                        </p>
                        
                        <div class="mb-2">
                            <i class="fas fa-calendar text-primary me-2"></i>
                            <small>
                                {% set event_date = event.event_date or event['event_date'] %}
                                {% if event_date %}
                                    {{ event_date.strftime('%B %d, %Y') if event_date.__class__.__name__ != 'str' else event_date }}
                                {% else %}
                                    TBD
                                {% endif %}
                            </small>
                        </div>
                        
                        <div class="mb-2">
                            <i class="fas fa-clock text-primary me-2"></i>
                            <small>{{ event.event_time or event['event_time'] or 'TBD' }}</small>
                        </div>
                        
                        <div class="mb-3">
                            <i class="fas fa-map-marker-alt text-primary me-2"></i>
                            <small>{{ event.location or event['location'] or 'TBD' }}</small>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-primary">
                                <i class="fas fa-users me-1"></i>
                                {{ event.attendee_count or event.get('attendee_count') or 0 }} attending
                            </span>
                            <a href="/events/{{ event.id or event['id'] }}" class="btn btn-sm btn-outline-primary">
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
    f.write(EVENTS_LIST_FIXED.strip())
fixed_items.append('events/list.html (FIXED)')

# ============================================================================
# 4. PROFILE VIEW PAGE
# ============================================================================
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
                            <img src="{{ session.avatar or '/static/uploads/default-avatar.png' }}" 
                                 class="rounded-circle" 
                                 style="width: 150px; height: 150px; object-fit: cover; border: 5px solid #4F46E5;">
                        </div>
                        <h2 class="fw-bold">{{ session.full_name }}</h2>
                        <p class="text-muted">{{ session.email }}</p>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-briefcase me-2"></i>Job Title:</strong>
                            <p class="text-muted">{{ session.job_title or 'Not specified' }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-building me-2"></i>Company:</strong>
                            <p class="text-muted">{{ session.company or 'Not specified' }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-phone me-2"></i>Phone:</strong>
                            <p class="text-muted">{{ session.phone or 'Not specified' }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong><i class="fas fa-id-badge me-2"></i>NFC Badge ID:</strong>
                            <p class="text-muted"><code>{{ session.nfc_badge_id or 'Not assigned' }}</code></p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="d-grid gap-2">
                        <a href="/profile/edit" class="btn btn-primary">
                            <i class="fas fa-edit me-2"></i>Edit Profile
                        </a>
                        <a href="/profile/my-nfc" class="btn btn-outline-primary">
                            <i class="fas fa-qrcode me-2"></i>View My QR Code
                        </a>
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
# 5. PROFILE SETTINGS PAGE
# ============================================================================
PROFILE_SETTINGS = """{% extends 'base.html' %}

{% block title %}Settings{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-cog me-2"></i>
                        Account Settings
                    </h4>
                </div>
                <div class="card-body p-4">
                    
                    <form method="POST" action="/profile/settings">
                        
                        <h5 class="mb-3">
                            <i class="fas fa-lock me-2"></i>
                            Change Password
                        </h5>
                        
                        <div class="mb-3">
                            <label class="form-label">Current Password</label>
                            <input type="password" name="current_password" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">New Password</label>
                            <input type="password" name="new_password" class="form-control" required minlength="6">
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label">Confirm New Password</label>
                            <input type="password" name="confirm_password" class="form-control" required>
                        </div>
                        
                        <hr>
                        
                        <h5 class="mb-3">
                            <i class="fas fa-bell me-2"></i>
                            Notifications
                        </h5>
                        
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" name="email_notifications" id="emailNotif" checked>
                            <label class="form-check-label" for="emailNotif">
                                Email notifications for new events
                            </label>
                        </div>
                        
                        <div class="form-check mb-4">
                            <input class="form-check-input" type="checkbox" name="connection_notifications" id="connNotif" checked>
                            <label class="form-check-label" for="connNotif">
                                Notify me when someone scans my QR code
                            </label>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save me-2"></i>
                                Save Settings
                            </button>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/profile/settings.html', 'w', encoding='utf-8') as f:
    f.write(PROFILE_SETTINGS.strip())
fixed_items.append('profile/settings.html')

# ============================================================================
# 6. FORUMS LIST PAGE
# ============================================================================
FORUMS_LIST = """{% extends 'base.html' %}

{% block title %}Forums{% endblock %}

{% block content %}
<div class="container mt-4">
    
    <div class="text-center mb-4 text-white animate-in">
        <h1 class="display-4 fw-bold">
            <i class="fas fa-comments me-3"></i>
            Discussion Forums
        </h1>
        <p class="lead">Connect and discuss with the community</p>
    </div>
    
    <div class="text-end mb-3">
        <a href="/forum/create" class="btn btn-success btn-lg">
            <i class="fas fa-plus-circle me-2"></i>
            Create Forum
        </a>
    </div>
    
    <div class="card shadow-lg animate-in">
        <div class="card-body">
            <div class="text-center py-5 text-muted">
                <i class="fas fa-comments fa-5x mb-4"></i>
                <h4>Forums Coming Soon</h4>
                <p>Discussion forums will be available shortly</p>
            </div>
        </div>
    </div>
    
</div>
{% endblock %}
"""

with open('templates/forums/list.html', 'w', encoding='utf-8') as f:
    f.write(FORUMS_LIST.strip())
fixed_items.append('forums/list.html')

# ============================================================================
# 7. CREATE FORUM PAGE
# ============================================================================
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
                            <label class="form-label fw-bold">Forum Title</label>
                            <input type="text" name="title" class="form-control form-control-lg" 
                                   placeholder="Enter forum title" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Description</label>
                            <textarea name="description" class="form-control" rows="5" 
                                      placeholder="Describe what this forum is about" required></textarea>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">Category</label>
                            <select name="category" class="form-select form-select-lg" required>
                                <option value="">-- Select Category --</option>
                                <option value="general">General Discussion</option>
                                <option value="events">Events</option>
                                <option value="networking">Networking</option>
                                <option value="tech">Technology</option>
                            </select>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save me-2"></i>
                                Create Forum
                            </button>
                            <a href="/forums" class="btn btn-outline-secondary">
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
# SUMMARY
# ============================================================================
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ MISSING PAGES FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Fixed items ({len(fixed_items)}):{Colors.END}")
for item in fixed_items:
    print(f"  {Colors.GREEN}✓{Colors.END} {item}")

print(f"\n{Colors.BOLD}{Colors.YELLOW}MANUAL STEP REQUIRED:{Colors.END}")
print(f"{Colors.YELLOW}Add the dashboard route from 'dashboard_route.txt' to your app.py file{Colors.END}")
print(f"{Colors.YELLOW}Place it after the login route and before the other routes{Colors.END}")

print(f"\n{Colors.CYAN}Routes that should now work:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} /dashboard")
print(f"  {Colors.GREEN}✓{Colors.END} /events/my-events")
print(f"  {Colors.GREEN}✓{Colors.END} /events (fixed dict error)")
print(f"  {Colors.GREEN}✓{Colors.END} /profile/view")
print(f"  {Colors.GREEN}✓{Colors.END} /profile/settings")
print(f"  {Colors.GREEN}✓{Colors.END} /forums")
print(f"  {Colors.GREEN}✓{Colors.END} /forum/create")

print(f"\n{Colors.BOLD}{Colors.CYAN}Next steps:{Colors.END}")
print(f"  1. Open app.py")
print(f"  2. Copy content from dashboard_route.txt")
print(f"  3. Paste it after the @login_required decorator import")
print(f"  4. Run: {Colors.BOLD}python app.py{Colors.END}")
print()