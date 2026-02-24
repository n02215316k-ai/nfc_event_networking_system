import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING MISSING ROUTE TEMPLATES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Template for events/attendees.html
events_attendees_template = '''{% extends "base.html" %}

{% block title %}{{ event.name }} - Attendees{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h3 class="mb-0">
                <i class="fas fa-users"></i> {{ event.name }} - Attendees
            </h3>
        </div>
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h5>Total Registered: <span class="badge bg-success">{{ registrations|length }}</span></h5>
                    {% if event.max_attendees %}
                    <p class="text-muted">Capacity: {{ registrations|length }} / {{ event.max_attendees }}</p>
                    {% endif %}
                </div>
                <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Back to Event
                </a>
            </div>

            {% if registrations %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Registered On</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for registration in registrations %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>
                                <a href="{{ url_for('profile.view', user_id=registration.user.id) }}">
                                    {{ registration.user.full_name }}
                                </a>
                            </td>
                            <td>{{ registration.user.email }}</td>
                            <td>{{ registration.registered_at.strftime('%B %d, %Y') if registration.registered_at else 'N/A' }}</td>
                            <td>
                                <span class="badge bg-success">Confirmed</span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i> No attendees yet
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

# Template for events/my-events.html
my_events_template = '''{% extends "base.html" %}

{% block title %}My Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h3 class="mb-0">
                <i class="fas fa-calendar-check"></i> My Registered Events
            </h3>
        </div>
        <div class="card-body">
            {% if events %}
            <div class="row">
                {% for event in events %}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm hover-lift">
                        <div class="card-body">
                            <h5 class="card-title">{{ event.name }}</h5>
                            <p class="card-text text-muted">
                                <i class="fas fa-calendar"></i> 
                                {{ event.date.strftime('%B %d, %Y') if event.date else 'TBD' }}
                            </p>
                            <p class="card-text text-muted">
                                <i class="fas fa-map-marker-alt"></i> {{ event.location }}
                            </p>
                            <span class="badge bg-{{ 'success' if event.status == 'approved' else 'warning' }}">
                                {{ event.status|title }}
                            </span>
                        </div>
                        <div class="card-footer bg-transparent">
                            <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-sm btn-primary w-100">
                                View Details
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i> You haven't registered for any events yet.
                <br><br>
                <a href="{{ url_for('events.list_events') }}" class="btn btn-primary">
                    <i class="fas fa-search"></i> Browse Events
                </a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

# Template for event_admin/events.html
event_admin_events_template = '''{% extends "base.html" %}

{% block title %}Manage Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h3 class="mb-0">
                <i class="fas fa-calendar-alt"></i> Manage Events
            </h3>
        </div>
        <div class="card-body">
            {% if events %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Event Name</th>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Status</th>
                            <th>Attendees</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for event in events %}
                        <tr>
                            <td>{{ event.name }}</td>
                            <td>{{ event.date.strftime('%b %d, %Y') if event.date else 'TBD' }}</td>
                            <td>{{ event.location }}</td>
                            <td>
                                <span class="badge bg-{{ 'success' if event.status == 'approved' else 'warning' }}">
                                    {{ event.status|title }}
                                </span>
                            </td>
                            <td>{{ event.registrations|length if event.registrations else 0 }}</td>
                            <td>
                                <a href="{{ url_for('event_admin.event_detail', event_id=event.id) }}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i> View
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i> No events assigned to you yet.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

# Template for system_manager/user_form.html
user_form_template = '''{% extends "base.html" %}

{% block title %}{{ 'Edit User' if user else 'Create User' }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-lg animate-in">
        <div class="card-header bg-primary text-white">
            <h3 class="mb-0">
                <i class="fas fa-user-plus"></i> {{ 'Edit User' if user else 'Create User' }}
            </h3>
        </div>
        <div class="card-body">
            <form method="POST">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="full_name" class="form-label">Full Name *</label>
                        <input type="text" class="form-control" id="full_name" name="full_name" 
                               value="{{ user.full_name if user else '' }}" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label for="email" class="form-label">Email *</label>
                        <input type="email" class="form-control" id="email" name="email" 
                               value="{{ user.email if user else '' }}" required>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="role" class="form-label">Role *</label>
                        <select class="form-select" id="role" name="role" required>
                            <option value="attendee" {% if user and user.role == 'attendee' %}selected{% endif %}>Attendee</option>
                            <option value="organizer" {% if user and user.role == 'organizer' %}selected{% endif %}>Organizer</option>
                            <option value="event_admin" {% if user and user.role == 'event_admin' %}selected{% endif %}>Event Admin</option>
                            <option value="system_manager" {% if user and user.role == 'system_manager' %}selected{% endif %}>System Manager</option>
                        </select>
                    </div>
                    {% if not user %}
                    <div class="col-md-6 mb-3">
                        <label for="password" class="form-label">Password *</label>
                        <input type="password" class="form-control" id="password" name="password" required minlength="8">
                    </div>
                    {% endif %}
                </div>

                <div class="d-flex gap-2 mt-4">
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="fas fa-save"></i> {{ 'Update User' if user else 'Create User' }}
                    </button>
                    <a href="{{ url_for('system_manager.users') }}" class="btn btn-secondary btn-lg">
                        <i class="fas fa-times"></i> Cancel
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
'''

# Create templates
templates_to_create = [
    ('templates/events/attendees.html', events_attendees_template),
    ('templates/events/my-events.html', my_events_template),
    ('templates/event_admin/events.html', event_admin_events_template),
    ('templates/system_manager/user_form.html', user_form_template),
]

created_count = 0

for file_path, content in templates_to_create:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    created_count += 1
    print(f"{Colors.GREEN}✓ Created: {file_path}{Colors.END}")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL {created_count} TEMPLATES CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.BOLD}Templates created:{Colors.END}")
print(f"  1. events/attendees.html - View event attendees")
print(f"  2. events/my-events.html - User's registered events")
print(f"  3. event_admin/events.html - Event admin events list")
print(f"  4. system_manager/user_form.html - Create/edit user form\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.YELLOW}python app.py{Colors.END} - Restart Flask")
print(f"  2. {Colors.YELLOW}python verify_routes_correct.py{Colors.END} - Verify completion\n")