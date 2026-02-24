import os
import sys

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")

# ============================================================================
# EVENT TEMPLATES
# ============================================================================

EVENT_LIST_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Events - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Page Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2><i class="fas fa-calendar-alt me-2"></i>All Events</h2>
            <p class="text-muted">Discover and register for upcoming events</p>
        </div>
        {% if current_user %}
        <div>
            <a href="{{ url_for('events.create') }}" class="btn btn-primary">
                <i class="fas fa-plus-circle me-2"></i>Create Event
            </a>
        </div>
        {% endif %}
    </div>
    
    <!-- Filters -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" action="{{ url_for('events.list_events') }}">
                <div class="row align-items-end">
                    <div class="col-md-4">
                        <label class="form-label">Category</label>
                        <select name="category" class="form-select" onchange="this.form.submit()">
                            <option value="">All Categories</option>
                            <option value="conference" {% if selected_category == 'conference' %}selected{% endif %}>Conference</option>
                            <option value="workshop" {% if selected_category == 'workshop' %}selected{% endif %}>Workshop</option>
                            <option value="seminar" {% if selected_category == 'seminar' %}selected{% endif %}>Seminar</option>
                            <option value="networking" {% if selected_category == 'networking' %}selected{% endif %}>Networking</option>
                            <option value="other" {% if selected_category == 'other' %}selected{% endif %}>Other</option>
                        </select>
                    </div>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Events Grid -->
    <div class="row">
        {% if events %}
            {% for event in events %}
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    {% if event.cover_image %}
                    <img src="{{ url_for('static', filename=event.cover_image) }}" 
                         class="card-img-top" style="height: 200px; object-fit: cover;" 
                         alt="{{ event.title }}">
                    {% else %}
                    <div class="card-img-top bg-primary text-white d-flex align-items-center justify-content-center" 
                         style="height: 200px;">
                        <i class="fas fa-calendar-alt fa-4x"></i>
                    </div>
                    {% endif %}
                    
                    <div class="card-body d-flex flex-column">
                        <div class="mb-2">
                            <span class="badge bg-info">{{ event.category|title }}</span>
                            {% if event.is_registered %}
                            <span class="badge bg-success">Registered</span>
                            {% endif %}
                        </div>
                        
                        <h5 class="card-title">{{ event.title }}</h5>
                        
                        <p class="card-text text-muted small flex-grow-1">
                            {{ event.description|truncate_words(20) }}
                        </p>
                        
                        <div class="mb-2">
                            <small class="text-muted">
                                <i class="fas fa-user me-1"></i>{{ event.creator_name }}
                            </small>
                        </div>
                        
                        <div class="mb-2">
                            <small class="text-muted">
                                <i class="fas fa-calendar me-1"></i>
                                {{ event.start_date|datetime_format('%b %d, %Y at %I:%M %p') }}
                            </small>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted">
                                <i class="fas fa-map-marker-alt me-1"></i>{{ event.location }}
                            </small>
                        </div>
                        
                        <div class="mb-2">
                            <small class="text-muted">
                                <i class="fas fa-users me-1"></i>
                                {{ event.registration_count }} registered
                                {% if event.max_attendees %}
                                / {{ event.max_attendees }} max
                                {% endif %}
                            </small>
                        </div>
                        
                        <a href="{{ url_for('events.detail', event_id=event.id) }}" 
                           class="btn btn-primary w-100 mt-auto">
                            View Details <i class="fas fa-arrow-right ms-1"></i>
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
        <div class="col-12">
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle fa-2x mb-3"></i>
                <h5>No events found</h5>
                <p>There are no events available at the moment.</p>
                {% if current_user %}
                <a href="{{ url_for('events.create') }}" class="btn btn-primary mt-2">
                    <i class="fas fa-plus-circle me-2"></i>Create First Event
                </a>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
"""

EVENT_DETAIL_TEMPLATE = """
{% extends "base.html" %}

{% block title %}{{ event.title }} - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Event Header -->
    <div class="row mb-4">
        <div class="col-12">
            {% if event.cover_image %}
            <img src="{{ url_for('static', filename=event.cover_image) }}" 
                 class="w-100" style="height: 300px; object-fit: cover; border-radius: 10px;" 
                 alt="{{ event.title }}">
            {% endif %}
        </div>
    </div>
    
    <div class="row">
        <!-- Main Content -->
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-body">
                    <div class="mb-3">
                        <span class="badge bg-info">{{ event.category|title }}</span>
                        <span class="badge bg-secondary">{{ event.status|title }}</span>
                    </div>
                    
                    <h2 class="mb-3">{{ event.title }}</h2>
                    
                    <div class="mb-3">
                        <small class="text-muted">
                            <i class="fas fa-user me-1"></i>
                            Organized by <a href="{{ url_for('profile.view', user_id=event.creator_id) }}">{{ event.creator_name }}</a>
                        </small>
                    </div>
                    
                    <hr>
                    
                    <h5><i class="fas fa-info-circle me-2"></i>Description</h5>
                    <p class="text-muted">{{ event.description }}</p>
                    
                    <hr>
                    
                    <h5><i class="fas fa-calendar me-2"></i>Event Details</h5>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong>Start Date & Time:</strong><br>
                            <i class="fas fa-calendar-check text-primary me-2"></i>
                            {{ event.start_date|datetime_format('%B %d, %Y at %I:%M %p') }}
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>End Date & Time:</strong><br>
                            <i class="fas fa-calendar-times text-danger me-2"></i>
                            {{ event.end_date|datetime_format('%B %d, %Y at %I:%M %p') }}
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Location:</strong><br>
                            <i class="fas fa-map-marker-alt text-danger me-2"></i>
                            {{ event.location }}
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Venue:</strong><br>
                            <i class="fas fa-building text-primary me-2"></i>
                            {{ event.venue or 'TBA' }}
                        </div>
                    </div>
                    
                    {% if event.qr_code %}
                    <hr>
                    <h5><i class="fas fa-qrcode me-2"></i>Event QR Code</h5>
                    <img src="{{ url_for('static', filename=event.qr_code) }}" 
                         alt="QR Code" style="max-width: 200px;">
                    <p class="text-muted small">Scan this code for quick event check-in</p>
                    {% endif %}
                </div>
            </div>
            
            <!-- Attendees Section -->
            {% if can_manage or is_registered %}
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-users me-2"></i>Attendees ({{ attendees|length }})
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        {% for attendee in attendees %}
                        <div class="col-md-6 mb-3">
                            <div class="d-flex align-items-center">
                                {% if attendee.profile_picture %}
                                <img src="{{ url_for('static', filename=attendee.profile_picture) }}" 
                                     class="profile-img me-3" alt="{{ attendee.full_name }}">
                                {% else %}
                                <div class="profile-img bg-primary text-white d-flex align-items-center justify-content-center me-3">
                                    <i class="fas fa-user"></i>
                                </div>
                                {% endif %}
                                <div>
                                    <a href="{{ url_for('profile.view', user_id=attendee.id) }}">
                                        <strong>{{ attendee.full_name }}</strong>
                                    </a>
                                    <br>
                                    <small class="badge bg-{{ 'success' if attendee.status == 'checked_in' else 'warning' }}">
                                        {{ attendee.status|replace('_', ' ')|title }}
                                    </small>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
        
        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Registration Card -->
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-ticket-alt me-2"></i>Registration</h6>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <strong>Capacity:</strong>
                        <div class="progress mt-2" style="height: 25px;">
                            {% set percentage = (attendees|length / event.max_attendees * 100) if event.max_attendees else 0 %}
                            <div class="progress-bar" role="progressbar" 
                                 style="width: {{ percentage }}%">
                                {{ attendees|length }}{% if event.max_attendees %} / {{ event.max_attendees }}{% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <strong>Checked In:</strong>
                        <p class="mb-0">
                            <i class="fas fa-check-circle text-success me-1"></i>
                            {{ event.checked_in_count }} attendees
                        </p>
                    </div>
                    
                    {% if current_user %}
                        {% if is_registered %}
                            <div class="alert alert-success">
                                <i class="fas fa-check-circle me-2"></i>
                                You are registered!
                                {% if user_attendance %}
                                <br><small>Status: {{ user_attendance.status|replace('_', ' ')|title }}</small>
                                {% endif %}
                            </div>
                            <form method="POST" action="{{ url_for('events.unregister', event_id=event.id) }}">
                                <button type="submit" class="btn btn-outline-danger w-100">
                                    <i class="fas fa-times-circle me-2"></i>Unregister
                                </button>
                            </form>
                        {% else %}
                            <form method="POST" action="{{ url_for('events.register', event_id=event.id) }}">
                                <button type="submit" class="btn btn-primary w-100 btn-lg">
                                    <i class="fas fa-check-circle me-2"></i>Register Now
                                </button>
                            </form>
                        {% endif %}
                    {% else %}
                        <a href="{{ url_for('auth.login') }}" class="btn btn-primary w-100">
                            Login to Register
                        </a>
                    {% endif %}
                </div>
            </div>
            
            <!-- Event Forum -->
            {% if forum %}
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-comments me-2"></i>Discussion Forum</h6>
                </div>
                <div class="card-body">
                    <p class="text-muted">{{ forum.title }}</p>
                    <a href="{{ url_for('forum.view', forum_id=forum.id) }}" class="btn btn-outline-primary w-100">
                        <i class="fas fa-arrow-right me-2"></i>Go to Forum
                    </a>
                </div>
            </div>
            {% endif %}
            
            <!-- Management Actions -->
            {% if can_manage %}
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-cog me-2"></i>Manage Event</h6>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('events.edit', event_id=event.id) }}" class="btn btn-outline-primary">
                            <i class="fas fa-edit me-2"></i>Edit Event
                        </a>
                        <a href="{{ url_for('nfc.scanner_page', event_id=event.id) }}" class="btn btn-outline-success">
                            <i class="fas fa-qrcode me-2"></i>NFC Scanner
                        </a>
                        {% if current_user.role == 'system_manager' %}
                        <a href="{{ url_for('system_manager.event_analytics', event_id=event.id) }}" 
                           class="btn btn-outline-info">
                            <i class="fas fa-chart-bar me-2"></i>Analytics
                        </a>
                        {% endif %}
                        <form method="POST" action="{{ url_for('events.delete', event_id=event.id) }}" 
                              onsubmit="return confirm('Delete this event?')">
                            <button type="submit" class="btn btn-outline-danger w-100">
                                <i class="fas fa-trash me-2"></i>Delete Event
                            </button>
                        </form>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

EVENT_CREATE_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Create Event - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">
                        <i class="fas fa-plus-circle me-2"></i>Create New Event
                    </h4>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('events.create_event') }}" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="title" class="form-label">Event Title *</label>
                            <input type="text" class="form-control" id="title" name="title" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="description" class="form-label">Description *</label>
                            <textarea class="form-control" id="description" name="description" 
                                      rows="5" required></textarea>
                            <small class="text-muted">Minimum 20 characters</small>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="category" class="form-label">Category *</label>
                                <select class="form-select" id="category" name="category" required>
                                    <option value="conference">Conference</option>
                                    <option value="workshop">Workshop</option>
                                    <option value="seminar">Seminar</option>
                                    <option value="networking">Networking</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="max_attendees" class="form-label">Max Attendees</label>
                                <input type="number" class="form-control" id="max_attendees" name="max_attendees" min="1">
                                <small class="text-muted">Leave empty for unlimited</small>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="location" class="form-label">Location *</label>
                                <input type="text" class="form-control" id="location" name="location" 
                                       placeholder="e.g., Harare, Zimbabwe" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="venue" class="form-label">Venue</label>
                                <input type="text" class="form-control" id="venue" name="venue" 
                                       placeholder="e.g., Rainbow Towers">
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="start_date" class="form-label">Start Date & Time *</label>
                                <input type="datetime-local" class="form-control" id="start_date" name="start_date" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="end_date" class="form-label">End Date & Time *</label>
                                <input type="datetime-local" class="form-control" id="end_date" name="end_date" required>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="cover_image" class="form-label">Cover Image</label>
                            <input type="file" class="form-control" id="cover_image" name="cover_image" accept="image/*">
                            <small class="text-muted">Recommended size: 800x400px</small>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-check-circle me-2"></i>Create Event
                            </button>
                            <a href="{{ url_for('events.list_events') }}" class="btn btn-outline-secondary">
                                <i class="fas fa-times me-2"></i>Cancel
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

# ============================================================================
# PROFILE TEMPLATES - Continue in next message due to length...
# ============================================================================

PROFILE_VIEW_TEMPLATE = """
{% extends "base.html" %}

{% block title %}{{ user.full_name }} - Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Profile Header -->
    <div class="card mb-4">
        <div class="card-body">
            <div class="row align-items-center">
                <div class="col-md-3 text-center">
                    {% if user.profile_picture %}
                    <img src="{{ url_for('static', filename=user.profile_picture) }}" 
                         class="profile-img-lg rounded-circle mb-3" alt="{{ user.full_name }}">
                    {% else %}
                    <div class="profile-img-lg rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-3">
                        <i class="fas fa-user fa-4x"></i>
                    </div>
                    {% endif %}
                    
                    {% if user.is_verified %}
                    <span class="badge bg-success mb-2">
                        <i class="fas fa-check-circle me-1"></i>Verified
                    </span>
                    {% endif %}
                </div>
                
                <div class="col-md-6">
                    <h2 class="mb-2">{{ user.full_name }}</h2>
                    
                    {% if user.current_employment %}
                    <p class="text-muted mb-2">
                        <i class="fas fa-briefcase me-2"></i>{{ user.current_employment }}
                    </p>
                    {% endif %}
                    
                    {% if user.current_research_area %}
                    <p class="text-muted mb-2">
                        <i class="fas fa-flask me-2"></i>Research: {{ user.current_research_area }}
                    </p>
                    {% endif %}
                    
                    <p class="text-muted mb-2">
                        <i class="fas fa-envelope me-2"></i>{{ user.email }}
                    </p>
                    
                    {% if user.phone_number %}
                    <p class="text-muted mb-2">
                        <i class="fas fa-phone me-2"></i>{{ user.phone_number }}
                    </p>
                    {% endif %}
                    
                    <div class="mt-3">
                        <span class="badge bg-info me-2">
                            <i class="fas fa-users me-1"></i>{{ followers_count }} Followers
                        </span>
                        <span class="badge bg-info me-2">
                            <i class="fas fa-user-friends me-1"></i>{{ following_count }} Following
                        </span>
                        <span class="badge bg-info">
                            <i class="fas fa-comments me-1"></i>{{ forum_count }} Forums
                        </span>
                    </div>
                </div>
                
                <div class="col-md-3">
                    {% if is_own_profile %}
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('profile.edit') }}" class="btn btn-primary">
                            <i class="fas fa-edit me-2"></i>Edit Profile
                        </a>
                        <a href="{{ url_for('auth.change_password') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-key me-2"></i>Change Password
                        </a>
                    </div>
                    {% else %}
                    <div class="d-grid gap-2">
                        {% if is_following %}
                        <button class="btn btn-outline-secondary follow-btn" data-user-id="{{ user.id }}" data-action="unfollow">
                            <i class="fas fa-user-times me-2"></i>Unfollow
                        </button>
                        {% else %}
                        <button class="btn btn-primary follow-btn" data-user-id="{{ user.id }}" data-action="follow">
                            <i class="fas fa-user-plus me-2"></i>Follow
                        </button>
                        {% endif %}
                        
                        <a href="{{ url_for('messaging.compose', to=user.id) }}" class="btn btn-outline-primary">
                            <i class="fas fa-envelope me-2"></i>Message
                        </a>
                    </div>
                    {% endif %}
                </div>
            </div>
            
            {% if user.biography %}
            <hr>
            <h6><i class="fas fa-info-circle me-2"></i>Biography</h6>
            <p class="text-muted">{{ user.biography }}</p>
            {% endif %}
        </div>
    </div>
    
    <div class="row">
        <!-- Qualifications -->
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                        <i class="fas fa-graduation-cap me-2"></i>Qualifications
                    </h5>
                    {% if is_own_profile %}
                    <button class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addQualificationModal">
                        <i class="fas fa-plus me-1"></i>Add
                    </button>
                    {% endif %}
                </div>
                <div class="card-body">
                    {% if qualifications %}
                    <div class="list-group list-group-flush">
                        {% for qual in qualifications %}
                        <div class="list-group-item">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="mb-1">{{ qual.qualification_type }}</h6>
                                    <p class="mb-1"><strong>{{ qual.institution }}</strong></p>
                                    {% if qual.field_of_study %}
                                    <p class="mb-1 text-muted">{{ qual.field_of_study }}</p>
                                    {% endif %}
                                    <small class="text-muted">
                                        Year: {{ qual.year_obtained or 'N/A' }}
                                    </small>
                                </div>
                                <div>
                                    {% if qual.verification_status == 'verified' %}
                                    <span class="badge bg-success">Verified</span>
                                    {% elif qual.verification_status == 'pending' %}
                                    <span class="badge bg-warning">Pending</span>
                                    {% else %}
                                    <span class="badge bg-danger">Rejected</span>
                                    {% endif %}
                                    
                                    {% if is_own_profile %}
                                    <form method="POST" action="{{ url_for('profile.delete_qualification', qual_id=qual.id) }}" 
                                          class="d-inline" onsubmit="return confirm('Delete this qualification?')">
                                        <button type="submit" class="btn btn-sm btn-outline-danger mt-2">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </form>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center">No qualifications added yet.</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Recent Events -->
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-calendar-alt me-2"></i>Recent Events
                    </h5>
                </div>
                <div class="card-body">
                    {% if recent_events %}
                    <div class="list-group list-group-flush">
                        {% for event in recent_events %}
                        <a href="{{ url_for('events.detail', event_id=event.id) }}" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between">
                                <h6 class="mb-1">{{ event.title }}</h6>
                                <small class="badge bg-{{ 'success' if event.relation == 'creator' else 'info' }}">
                                    {{ event.relation|title }}
                                </small>
                            </div>
                            <small class="text-muted">
                                <i class="fas fa-calendar me-1"></i>
                                {{ event.start_date|datetime_format('%b %d, %Y') }}
                            </small>
                        </a>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center">No events yet.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Add Qualification Modal -->
{% if is_own_profile %}
<div class="modal fade" id="addQualificationModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Add Qualification</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="{{ url_for('profile.add_qualification') }}" enctype="multipart/form-data">
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Qualification Type *</label>
                        <select class="form-select" name="qualification_type" required>
                            <option value="PhD">PhD</option>
                            <option value="Masters">Masters</option>
                            <option value="Bachelors">Bachelors</option>
                            <option value="Diploma">Diploma</option>
                            <option value="Certificate">Certificate</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Institution *</label>
                        <input type="text" class="form-control" name="institution" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Field of Study</label>
                        <input type="text" class="form-control" name="field_of_study">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Year Obtained</label>
                        <input type="number" class="form-control" name="year_obtained" min="1950" max="2030">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Document (PDF)</label>
                        <input type="file" class="form-control" name="document" accept=".pdf">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Qualification</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    $('.follow-btn').click(function() {
        var btn = $(this);
        var userId = btn.data('user-id');
        var action = btn.data('action');
        
        $.ajax({
            url: action === 'follow' ? '/profile/follow/' + userId : '/profile/unfollow/' + userId,
            method: 'POST',
            success: function(response) {
                if (response.success) {
                    if (action === 'follow') {
                        btn.removeClass('btn-primary').addClass('btn-outline-secondary');
                        btn.html('<i class="fas fa-user-times me-2"></i>Unfollow');
                        btn.data('action', 'unfollow');
                    } else {
                        btn.removeClass('btn-outline-secondary').addClass('btn-primary');
                        btn.html('<i class="fas fa-user-plus me-2"></i>Follow');
                        btn.data('action', 'follow');
                    }
                    location.reload();
                }
            }
        });
    });
});
</script>
{% endblock %}
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("📦 PART 4A: Creating Event & Profile Templates")
    
    print_section("Creating event templates...")
    create_file('templates/events/list.html', EVENT_LIST_TEMPLATE)
    create_file('templates/events/detail.html', EVENT_DETAIL_TEMPLATE)
    create_file('templates/events/create.html', EVENT_CREATE_TEMPLATE)
    
    print_section("Creating profile templates...")
    create_file('templates/profile/view.html', PROFILE_VIEW_TEMPLATE)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 4A Complete!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.CYAN}📋 Templates Created:{Colors.END}")
    print(f"  ✅ events/list.html")
    print(f"  ✅ events/detail.html")
    print(f"  ✅ events/create.html")
    print(f"  ✅ profile/view.html")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 4B for remaining templates (Forum, Messaging, NFC, System Manager){Colors.END}")

if __name__ == '__main__':
    main()