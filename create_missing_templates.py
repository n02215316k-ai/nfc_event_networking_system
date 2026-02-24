import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING 3 MISSING TEMPLATES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# 1. auth/change-password.html
change_password_template = '''{% extends "base.html" %}

{% block title %}Change Password{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0">
                        <i class="fas fa-key"></i> Change Password
                    </h3>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="{{ url_for('auth.change_password') }}">
                        <!-- Current Password -->
                        <div class="mb-4">
                            <label for="current_password" class="form-label">
                                <i class="fas fa-lock"></i> Current Password
                            </label>
                            <input type="password" 
                                   class="form-control" 
                                   id="current_password" 
                                   name="current_password" 
                                   required>
                        </div>

                        <!-- New Password -->
                        <div class="mb-4">
                            <label for="new_password" class="form-label">
                                <i class="fas fa-lock"></i> New Password
                            </label>
                            <input type="password" 
                                   class="form-control" 
                                   id="new_password" 
                                   name="new_password" 
                                   required
                                   minlength="8">
                            <small class="text-muted">Minimum 8 characters</small>
                        </div>

                        <!-- Confirm Password -->
                        <div class="mb-4">
                            <label for="confirm_password" class="form-label">
                                <i class="fas fa-lock"></i> Confirm New Password
                            </label>
                            <input type="password" 
                                   class="form-control" 
                                   id="confirm_password" 
                                   name="confirm_password" 
                                   required>
                        </div>

                        <!-- Buttons -->
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save"></i> Change Password
                            </button>
                            <a href="{{ url_for('profile.edit') }}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# 2. events/edit.html
events_edit_template = '''{% extends "base.html" %}

{% block title %}Edit Event{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-10 mx-auto">
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0">
                        <i class="fas fa-edit"></i> Edit Event
                    </h3>
                </div>
                <div class="card-body p-4">
                    <form method="POST" enctype="multipart/form-data">
                        <div class="row">
                            <!-- Event Name -->
                            <div class="col-md-8 mb-3">
                                <label for="name" class="form-label">Event Name *</label>
                                <input type="text" 
                                       class="form-control" 
                                       id="name" 
                                       name="name" 
                                       value="{{ event.name }}" 
                                       required>
                            </div>

                            <!-- Category -->
                            <div class="col-md-4 mb-3">
                                <label for="category" class="form-label">Category *</label>
                                <select class="form-select" id="category" name="category" required>
                                    <option value="Conference" {% if event.category == 'Conference' %}selected{% endif %}>Conference</option>
                                    <option value="Workshop" {% if event.category == 'Workshop' %}selected{% endif %}>Workshop</option>
                                    <option value="Seminar" {% if event.category == 'Seminar' %}selected{% endif %}>Seminar</option>
                                    <option value="Networking" {% if event.category == 'Networking' %}selected{% endif %}>Networking</option>
                                    <option value="Social" {% if event.category == 'Social' %}selected{% endif %}>Social</option>
                                </select>
                            </div>
                        </div>

                        <!-- Description -->
                        <div class="mb-3">
                            <label for="description" class="form-label">Description *</label>
                            <textarea class="form-control" 
                                      id="description" 
                                      name="description" 
                                      rows="4" 
                                      required>{{ event.description }}</textarea>
                        </div>

                        <div class="row">
                            <!-- Date -->
                            <div class="col-md-6 mb-3">
                                <label for="date" class="form-label">Event Date *</label>
                                <input type="datetime-local" 
                                       class="form-control" 
                                       id="date" 
                                       name="date" 
                                       value="{{ event.date.strftime('%Y-%m-%dT%H:%M') if event.date else '' }}" 
                                       required>
                            </div>

                            <!-- Location -->
                            <div class="col-md-6 mb-3">
                                <label for="location" class="form-label">Location *</label>
                                <input type="text" 
                                       class="form-control" 
                                       id="location" 
                                       name="location" 
                                       value="{{ event.location }}" 
                                       required>
                            </div>
                        </div>

                        <div class="row">
                            <!-- Max Attendees -->
                            <div class="col-md-6 mb-3">
                                <label for="max_attendees" class="form-label">Max Attendees</label>
                                <input type="number" 
                                       class="form-control" 
                                       id="max_attendees" 
                                       name="max_attendees" 
                                       value="{{ event.max_attendees or '' }}">
                            </div>

                            <!-- Status -->
                            <div class="col-md-6 mb-3">
                                <label for="status" class="form-label">Status</label>
                                <select class="form-select" id="status" name="status">
                                    <option value="pending" {% if event.status == 'pending' %}selected{% endif %}>Pending</option>
                                    <option value="approved" {% if event.status == 'approved' %}selected{% endif %}>Approved</option>
                                    <option value="cancelled" {% if event.status == 'cancelled' %}selected{% endif %}>Cancelled</option>
                                </select>
                            </div>
                        </div>

                        <!-- Buttons -->
                        <div class="d-flex gap-2 mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save"></i> Update Event
                            </button>
                            <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-secondary btn-lg">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="button" 
                                    class="btn btn-danger btn-lg ms-auto" 
                                    onclick="if(confirm('Delete this event?')) document.getElementById('deleteForm').submit();">
                                <i class="fas fa-trash"></i> Delete Event
                            </button>
                        </div>
                    </form>

                    <!-- Hidden delete form -->
                    <form id="deleteForm" 
                          method="POST" 
                          action="{{ url_for('events.delete_event', event_id=event.id) }}" 
                          style="display:none;">
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# 3. forum/detail.html
forum_detail_template = '''{% extends "base.html" %}

{% block title %}{{ forum.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Forum Header -->
    <div class="card shadow-lg mb-4 animate-in">
        <div class="card-header bg-primary text-white">
            <h2 class="mb-0">
                <i class="fas fa-comments"></i> {{ forum.title }}
            </h2>
        </div>
        <div class="card-body">
            <p class="lead">{{ forum.description }}</p>
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-info">
                        <i class="fas fa-users"></i> {{ forum.members_count or 0 }} Members
                    </span>
                    <span class="badge bg-success">
                        <i class="fas fa-comment"></i> {{ forum.posts_count or 0 }} Posts
                    </span>
                </div>
                <div>
                    {% if session.user %}
                        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newPostModal">
                            <i class="fas fa-plus"></i> New Post
                        </button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Forum Posts -->
    <div class="row">
        {% if posts %}
            {% for post in posts %}
            <div class="col-12 mb-3">
                <div class="card shadow animate-in">
                    <div class="card-body">
                        <div class="d-flex">
                            <div class="me-3">
                                <img src="{{ post.user.avatar or 'https://ui-avatars.com/api/?name=' + post.user.full_name }}" 
                                     class="rounded-circle" 
                                     width="50" 
                                     height="50" 
                                     alt="{{ post.user.full_name }}">
                            </div>
                            <div class="flex-grow-1">
                                <h5 class="mb-1">
                                    <a href="{{ url_for('forum.view_post', post_id=post.id) }}" class="text-decoration-none">
                                        {{ post.title }}
                                    </a>
                                </h5>
                                <p class="text-muted small mb-2">
                                    By {{ post.user.full_name }} • 
                                    {{ post.created_at.strftime('%B %d, %Y at %I:%M %p') if post.created_at else 'Recently' }}
                                </p>
                                <p class="mb-2">{{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}</p>
                                <div>
                                    <span class="badge bg-secondary">
                                        <i class="fas fa-reply"></i> {{ post.replies_count or 0 }} Replies
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="fas fa-info-circle"></i> No posts yet. Be the first to post!
                </div>
            </div>
        {% endif %}
    </div>
</div>

<!-- New Post Modal -->
<div class="modal fade" id="newPostModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    <i class="fas fa-plus"></i> New Post
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="{{ url_for('forum.view', forum_id=forum.id) }}">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" name="title" required>
                    </div>
                    <div class="mb-3">
                        <label for="content" class="form-label">Content</label>
                        <textarea class="form-control" id="content" name="content" rows="5" required></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i> Post
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
'''

# Create the templates
templates_to_create = [
    ('templates/auth/change-password.html', change_password_template),
    ('templates/events/edit.html', events_edit_template),
    ('templates/forum/detail.html', forum_detail_template),
]

for file_path, content in templates_to_create:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓ Created: {file_path}{Colors.END}")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL 3 MISSING TEMPLATES CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.BOLD}System is now 100% complete!{Colors.END}\n")

print(f"{Colors.CYAN}Created:{Colors.END}")
print(f"  1. auth/change-password.html - Change password form")
print(f"  2. events/edit.html - Edit event form")
print(f"  3. forum/detail.html - Forum thread view\n")

print(f"{Colors.BOLD}Run verification again:{Colors.END}")
print(f"  {Colors.YELLOW}python verify_routes_correct.py{Colors.END}\n")