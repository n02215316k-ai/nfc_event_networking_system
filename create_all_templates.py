import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

# Profile Edit Template
PROFILE_EDIT = """
{% extends "base.html" %}

{% block title %}Edit Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="fas fa-user-edit me-2"></i>Complete Your Profile</h4>
                </div>
                <div class="card-body">
                    <form method="POST" enctype="multipart/form-data">
                        <div class="text-center mb-4">
                            <img src="{{ url_for('static', filename=user.profile_picture if user.profile_picture else 'uploads/default-avatar.png') }}" 
                                 class="rounded-circle" 
                                 style="width: 120px; height: 120px; object-fit: cover;"
                                 alt="Profile" id="preview">
                            <div class="mt-3">
                                <label for="profile_picture" class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-camera me-1"></i>Change Photo
                                </label>
                                <input type="file" id="profile_picture" name="profile_picture" 
                                       class="d-none" accept="image/*">
                            </div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Full Name *</label>
                            <input type="text" class="form-control" name="full_name" 
                                   value="{{ user.full_name }}" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" value="{{ user.email }}" readonly>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Phone Number</label>
                            <input type="tel" class="form-control" name="phone_number" 
                                   value="{{ user.phone_number or '' }}">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Date of Birth</label>
                            <input type="date" class="form-control" name="date_of_birth" 
                                   value="{{ user.date_of_birth }}">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Gender</label>
                            <select class="form-select" name="gender">
                                <option value="">Select...</option>
                                <option value="male" {% if user.gender == 'male' %}selected{% endif %}>Male</option>
                                <option value="female" {% if user.gender == 'female' %}selected{% endif %}>Female</option>
                                <option value="other" {% if user.gender == 'other' %}selected{% endif %}>Other</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Current Employment/Institution</label>
                            <input type="text" class="form-control" name="current_employment" 
                                   value="{{ user.current_employment or '' }}">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Biography</label>
                            <textarea class="form-control" name="biography" rows="3">{{ user.biography or '' }}</textarea>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Skills (comma separated)</label>
                            <input type="text" class="form-control" name="skills" 
                                   value="{{ user.skills or '' }}">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Interests (comma separated)</label>
                            <input type="text" class="form-control" name="interests" 
                                   value="{{ user.interests or '' }}">
                        </div>

                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Save Profile
                            </button>
                            <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">
                                Skip for Now
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

# Profile View Template
PROFILE_VIEW = """
{% extends "base.html" %}

{% block title %}{{ user.full_name }} - Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-4">
            <div class="card shadow-sm mb-4">
                <div class="card-body text-center">
                    <img src="{{ url_for('static', filename=user.profile_picture if user.profile_picture else 'uploads/default-avatar.png') }}" 
                         class="rounded-circle mb-3" 
                         style="width: 150px; height: 150px; object-fit: cover;"
                         alt="{{ user.full_name }}">
                    <h4>{{ user.full_name }}</h4>
                    <p class="text-muted">{{ user.current_employment or 'No employment info' }}</p>
                    
                    {% if current_user and current_user.id == user.id %}
                    <a href="{{ url_for('profile.edit') }}" class="btn btn-primary btn-sm">
                        <i class="fas fa-edit me-1"></i>Edit Profile
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5>About</h5>
                    <p>{{ user.biography or 'No biography yet.' }}</p>
                    
                    {% if user.skills %}
                    <h5 class="mt-4">Skills</h5>
                    <p>{{ user.skills }}</p>
                    {% endif %}
                    
                    {% if user.interests %}
                    <h5 class="mt-4">Interests</h5>
                    <p>{{ user.interests }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# About Page
ABOUT = """
{% extends "base.html" %}

{% block title %}About Us{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>About NFC Event System</h1>
    <p>Welcome to our NFC-enabled event management and social networking platform.</p>
</div>
{% endblock %}
"""

# Help Page
HELP = """
{% extends "base.html" %}

{% block title %}Help{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Help & Support</h1>
    <p>Find answers to common questions and get support.</p>
</div>
{% endblock %}
"""

# Notifications
NOTIFICATIONS = """
{% extends "base.html" %}

{% block title %}Notifications{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h2><i class="fas fa-bell me-2"></i>Notifications</h2>
        <form method="POST" action="{{ url_for('mark_all_read') }}">
            <button type="submit" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-check-double me-1"></i>Mark All Read
            </button>
        </form>
    </div>
    
    {% if notifications %}
        {% for notif in notifications %}
        <div class="card mb-2 {% if not notif.is_read %}border-primary{% endif %}">
            <div class="card-body">
                <h6>{{ notif.title }}</h6>
                <p class="mb-1">{{ notif.message }}</p>
                <small class="text-muted">{{ notif.created_at|timeago }}</small>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="alert alert-info">No notifications yet.</div>
    {% endif %}
</div>
{% endblock %}
"""

# Search Page
SEARCH = """
{% extends "base.html" %}

{% block title %}Search Results{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Search Results for "{{ query }}"</h2>
    
    <h4 class="mt-4">Events</h4>
    {% if results.events %}
        {% for event in results.events %}
        <div class="card mb-2">
            <div class="card-body">
                <h5>{{ event.title }}</h5>
                <p>{{ event.description[:100] }}...</p>
                <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-sm btn-primary">View</a>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <p class="text-muted">No events found.</p>
    {% endif %}
    
    <h4 class="mt-4">Users</h4>
    {% if results.users %}
        {% for user in results.users %}
        <div class="card mb-2">
            <div class="card-body">
                <h5>{{ user.full_name }}</h5>
                <p>{{ user.current_employment or 'No info' }}</p>
                <a href="{{ url_for('profile.view', user_id=user.id) }}" class="btn btn-sm btn-primary">View Profile</a>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <p class="text-muted">No users found.</p>
    {% endif %}
</div>
{% endblock %}
"""

print(f"\n{Colors.CYAN}Creating missing templates...{Colors.END}\n")

create_file('templates/profile/edit.html', PROFILE_EDIT)
create_file('templates/profile/view.html', PROFILE_VIEW)
create_file('templates/about.html', ABOUT)
create_file('templates/help.html', HELP)
create_file('templates/notifications.html', NOTIFICATIONS)
create_file('templates/search.html', SEARCH)

print(f"\n{Colors.GREEN}✅ All templates created!{Colors.END}")
print(f"\n{Colors.YELLOW}Now restart the app:{Colors.END}")
print(f"   python app.py\n")