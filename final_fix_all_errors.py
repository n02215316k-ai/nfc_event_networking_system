import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FINAL FIX - ALL REMAINING ERRORS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

fixed = []

# Create directories
os.makedirs('templates/events', exist_ok=True)
os.makedirs('templates/forums', exist_ok=True)
os.makedirs('templates/profile', exist_ok=True)
os.makedirs('templates/static_pages', exist_ok=True)

# ============================================================================
# 1. FIX EVENTS LIST - Handle dict objects properly
# ============================================================================
print(f"{Colors.CYAN}Fixing events/list.html (dict compatibility)...{Colors.END}")

EVENTS_LIST_COMPLETE_FIX = """{% extends 'base.html' %}

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
            {% set is_dict = event.__class__.__name__ == 'dict' %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-lg animate-in">
                    {% if is_dict %}
                        {% set event_image = event.get('image_url') %}
                        {% set event_title = event.get('title', 'Untitled Event') %}
                        {% set event_desc = event.get('description', 'No description available') %}
                        {% set event_date = event.get('event_date', 'TBD') %}
                        {% set event_time = event.get('event_time', 'TBD') %}
                        {% set event_location = event.get('location', 'TBD') %}
                        {% set event_id = event.get('id') %}
                        {% set attendee_count = event.get('attendee_count', 0) %}
                    {% else %}
                        {% set event_image = event.image_url %}
                        {% set event_title = event.title %}
                        {% set event_desc = event.description %}
                        {% set event_date = event.event_date %}
                        {% set event_time = event.event_time %}
                        {% set event_location = event.location %}
                        {% set event_id = event.id %}
                        {% set attendee_count = event.attendee_count or 0 %}
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
                        <p class="card-text text-muted">
                            {{ event_desc[:100] }}{% if event_desc|length > 100 %}...{% endif %}
                        </p>
                        
                        <div class="mb-2">
                            <i class="fas fa-calendar text-primary me-2"></i>
                            <small>
                                {% if event_date %}
                                    {% if event_date.__class__.__name__ == 'date' or event_date.__class__.__name__ == 'datetime' %}
                                        {{ event_date.strftime('%B %d, %Y') }}
                                    {% else %}
                                        {{ event_date }}
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

<script>
// Search functionality
document.getElementById('searchEvents')?.addEventListener('input', function(e) {
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

with open('templates/events/list.html', 'w', encoding='utf-8') as f:
    f.write(EVENTS_LIST_COMPLETE_FIX.strip())
fixed.append('events/list.html - DICT COMPATIBILITY FIXED')

# ============================================================================
# 2. CREATE FORUMS DIRECTORY TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating forums/create.html...{Colors.END}")

os.makedirs('templates/forums', exist_ok=True)

FORUMS_CREATE = """{% extends 'base.html' %}

{% block title %}Create Forum{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <div class=