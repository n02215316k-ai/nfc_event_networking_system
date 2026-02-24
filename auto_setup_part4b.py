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
# FORUM TEMPLATES
# ============================================================================

FORUM_LIST_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Forums - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2><i class="fas fa-comments me-2"></i>Discussion Forums</h2>
            <p class="text-muted">Join conversations and connect with others</p>
        </div>
        <a href="{{ url_for('forum.create_forum') }}" class="btn btn-primary">
            <i class="fas fa-plus-circle me-2"></i>Create Forum
        </a>
    </div>
    
    <div class="row">
        {% if forums %}
            {% for forum in forums %}
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title mb-0">{{ forum.title }}</h5>
                            {% if forum.is_member %}
                            <span class="badge bg-success">Joined</span>
                            {% endif %}
                        </div>
                        
                        <p class="card-text text-muted">{{ forum.description|truncate_words(30) }}</p>
                        
                        <div class="mb-3">
                            <small class="text-muted">
                                <i class="fas fa-user me-1"></i>{{ forum.creator_name }}
                            </small>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <small class="text-muted me-3">
                                    <i class="fas fa-users me-1"></i>{{ forum.member_count }} members
                                </small>
                                <small class="text-muted">
                                    <i class="fas fa-comment me-1"></i>{{ forum.post_count }} posts
                                </small>
                            </div>
                            <a href="{{ url_for('forum.view', forum_id=forum.id) }}" class="btn btn-primary btn-sm">
                                View Forum <i class="fas fa-arrow-right ms-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
        <div class="col-12">
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle fa-2x mb-3"></i>
                <h5>No forums available</h5>
                <a href="{{ url_for('forum.create_forum') }}" class="btn btn-primary mt-2">
                    <i class="fas fa-plus-circle me-2"></i>Create First Forum
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
"""

FORUM_VIEW_TEMPLATE = """
{% extends "base.html" %}

{% block title %}{{ forum.title }} - Forum{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h2>{{ forum.title }}</h2>
                    <p class="text-muted">{{ forum.description }}</p>
                    <small class="text-muted">
                        Created by {{ forum.creator_name }} | 
                        {{ member_count }} members | 
                        {% if forum.is_public %}Public{% else %}Private{% endif %}
                    </small>
                </div>
                <div>
                    {% if is_member %}
                    <form method="POST" action="{{ url_for('forum.leave', forum_id=forum.id) }}" class="d-inline">
                        <button type="submit" class="btn btn-outline-danger">
                            <i class="fas fa-sign-out-alt me-2"></i>Leave
                        </button>
                    </form>
                    {% else %}
                    <button class="btn btn-primary join-forum-btn" data-forum-id="{{ forum.id }}">
                        <i class="fas fa-sign-in-alt me-2"></i>Join Forum
                    </button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    {% if is_member %}
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0"><i class="fas fa-plus-circle me-2"></i>Create New Post</h5>
        </div>
        <div class="card-body">
            <form method="POST" action="{{ url_for('forum.create_post', forum_id=forum.id) }}" enctype="multipart/form-data">
                <div class="mb-3">
                    <label class="form-label">Title (Optional)</label>
                    <input type="text" class="form-control" name="title">
                </div>
                <div class="mb-3">
                    <label class="form-label">Content *</label>
                    <textarea class="form-control" name="content" rows="4" required></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label">Attachment</label>
                    <input type="file" class="form-control" name="attachment">
                </div>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-paper-plane me-2"></i>Post
                </button>
            </form>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0"><i class="fas fa-comments me-2"></i>Posts</h5>
        </div>
        <div class="card-body">
            {% if posts %}
            {% for post in posts %}
            <div class="card mb-3">
                <div class="card-body">
                    <div class="d-flex align-items-start">
                        <img src="{{ url_for('static', filename=post.author_picture or 'uploads/default-avatar.png') }}" 
                             class="profile-img me-3" alt="{{ post.author_name }}">
                        <div class="flex-grow-1">
                            <div class="d-flex justify-content-between">
                                <h6 class="mb-1">{{ post.author_name }}</h6>
                                <small class="text-muted">{{ post.created_at|timeago }}</small>
                            </div>
                            {% if post.title %}
                            <h5 class="mt-2">{{ post.title }}</h5>
                            {% endif %}
                            <p class="mb-2">{{ post.content }}</p>
                            
                            {% if post.attachment %}
                            <a href="{{ url_for('static', filename=post.attachment) }}" target="_blank" class="btn btn-sm btn-outline-primary mb-2">
                                <i class="fas fa-paperclip me-1"></i>View Attachment
                            </a>
                            {% endif %}
                            
                            <div class="d-flex gap-2">
                                <a href="{{ url_for('forum.view_post', post_id=post.id) }}" class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-reply me-1"></i>Reply ({{ post.reply_count }})
                                </a>
                                
                                {% if current_user.id == post.user_id or user_role in ['admin', 'moderator'] %}
                                <form method="POST" action="{{ url_for('forum.delete_post', post_id=post.id) }}" 
                                      class="d-inline" onsubmit="return confirm('Delete this post?')">
                                    <button type="submit" class="btn btn-sm btn-outline-danger">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </form>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
            {% else %}
            <p class="text-muted text-center">No posts yet. Be the first to post!</p>
            {% endif %}
        </div>
    </div>
    {% else %}
    <div class="alert alert-warning">
        <i class="fas fa-lock me-2"></i>You must join this forum to view posts.
    </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    $('.join-forum-btn').click(function() {
        var forumId = $(this).data('forum-id');
        $.ajax({
            url: '/forum/' + forumId + '/join',
            method: 'POST',
            success: function(response) {
                if (response.success) {
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
# MESSAGING TEMPLATES
# ============================================================================

MESSAGING_INBOX_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Messages - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-envelope me-2"></i>Messages</h2>
        <a href="{{ url_for('messaging.compose') }}" class="btn btn-primary">
            <i class="fas fa-edit me-2"></i>Compose
        </a>
    </div>
    
    <div class="card">
        <div class="card-body p-0">
            {% if conversations %}
            <div class="list-group list-group-flush">
                {% for conv in conversations %}
                <a href="{{ url_for('messaging.conversation', user_id=conv.partner_id) }}" 
                   class="list-group-item list-group-item-action {% if not conv.is_read %}bg-light{% endif %}">
                    <div class="d-flex align-items-center">
                        <img src="{{ url_for('static', filename=conv.partner_picture or 'uploads/default-avatar.png') }}" 
                             class="profile-img me-3" alt="{{ conv.partner_name }}">
                        <div class="flex-grow-1">
                            <div class="d-flex justify-content-between">
                                <h6 class="mb-1">{{ conv.partner_name }}</h6>
                                <small class="text-muted">{{ conv.last_message_time|timeago }}</small>
                            </div>
                            <p class="mb-0 text-muted small">{{ conv.last_message }}</p>
                        </div>
                        {% if conv.unread_count > 0 %}
                        <span class="badge bg-primary rounded-pill">{{ conv.unread_count }}</span>
                        {% endif %}
                    </div>
                </a>
                {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-5">
                <i class="fas fa-inbox fa-4x text-muted mb-3"></i>
                <h5 class="text-muted">No messages yet</h5>
                <a href="{{ url_for('messaging.compose') }}" class="btn btn-primary mt-3">
                    <i class="fas fa-edit me-2"></i>Send Your First Message
                </a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

MESSAGING_CONVERSATION_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Conversation with {{ partner.full_name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header">
            <div class="d-flex align-items-center">
                <a href="{{ url_for('messaging.inbox') }}" class="btn btn-sm btn-outline-secondary me-3">
                    <i class="fas fa-arrow-left"></i>
                </a>
                <img src="{{ url_for('static', filename=partner.profile_picture or 'uploads/default-avatar.png') }}" 
                     class="profile-img me-3" alt="{{ partner.full_name }}">
                <div>
                    <h5 class="mb-0">{{ partner.full_name }}</h5>
                    <small class="text-muted">{{ partner.current_employment or 'User' }}</small>
                </div>
            </div>
        </div>
        
        <div class="card-body" style="height: 500px; overflow-y: auto;">
            {% for message in messages %}
            <div class="mb-3 {% if message.sender_id == current_user.id %}text-end{% endif %}">
                <div class="d-inline-block" style="max-width: 70%;">
                    <div class="card {% if message.sender_id == current_user.id %}bg-primary text-white{% else %}bg-light{% endif %}">
                        <div class="card-body py-2 px-3">
                            {% if message.subject %}
                            <strong>{{ message.subject }}</strong><br>
                            {% endif %}
                            {{ message.message }}
                            <div class="mt-1">
                                <small class="{% if message.sender_id == current_user.id %}text-white-50{% else %}text-muted{% endif %}">
                                    {{ message.created_at|datetime_format('%b %d, %I:%M %p') }}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="card-footer">
            <form method="POST" action="{{ url_for('messaging.send_message') }}">
                <input type="hidden" name="recipient_id" value="{{ partner.id }}">
                <div class="input-group">
                    <input type="text" class="form-control" name="message" 
                           placeholder="Type your message..." required>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# NFC SCANNER TEMPLATE
# ============================================================================

NFC_SCANNER_TEMPLATE = """
{% extends "base.html" %}

{% block title %}NFC Scanner - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">
                        <i class="fas fa-qrcode me-2"></i>NFC/QR Scanner
                    </h4>
                </div>
                <div class="card-body text-center">
                    {% if event %}
                    <div class="alert alert-info">
                        <h5><i class="fas fa-calendar-check me-2"></i>{{ event.title }}</h5>
                        <p class="mb-0">Scanning for event check-in/check-out</p>
                    </div>
                    {% else %}
                    <div class="alert alert-primary">
                        <h5><i class="fas fa-network-wired me-2"></i>Networking Mode</h5>
                        <p class="mb-0">Scan NFC badges to view profiles</p>
                    </div>
                    {% endif %}
                    
                    <div class="my-4">
                        <i class="fas fa-qrcode fa-5x text-primary mb-3"></i>
                        <h5>Enter Badge ID or QR Code</h5>
                    </div>
                    
                    <form id="scanForm" class="mb-4">
                        <div class="input-group input-group-lg">
                            <input type="text" class="form-control" id="badgeInput" 
                                   placeholder="Scan or enter badge ID..." autofocus>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-search me-2"></i>Scan
                            </button>
                        </div>
                    </form>
                    
                    <div id="scanResult" class="mt-4"></div>
                    
                    <div class="mt-4">
                        <h6>Recent Scans</h6>
                        <div id="recentScans" class="list-group"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    $('#scanForm').submit(function(e) {
        e.preventDefault();
        
        var badgeId = $('#badgeInput').val().trim();
        if (!badgeId) {
            alert('Please enter a badge ID');
            return;
        }
        
        var scanData = {
            badge_id: badgeId,
            scan_type: '{{ "event" if event else "networking" }}',
            {% if event %}event_id: {{ event.id }}{% endif %}
        };
        
        $.ajax({
            url: '/nfc/scan',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(scanData),
            success: function(response) {
                if (response.success) {
                    $('#scanResult').html(
                        '<div class="alert alert-success">' +
                        '<i class="fas fa-check-circle fa-2x mb-2"></i><br>' +
                        '<h5>' + response.message + '</h5>' +
                        '</div>'
                    );
                    
                    if (response.redirect_url) {
                        setTimeout(function() {
                            window.location.href = response.redirect_url;
                        }, 1500);
                    }
                    
                    $('#badgeInput').val('').focus();
                } else {
                    $('#scanResult').html(
                        '<div class="alert alert-danger">' +
                        '<i class="fas fa-times-circle fa-2x mb-2"></i><br>' +
                        '<h5>' + response.message + '</h5>' +
                        '</div>'
                    );
                }
            },
            error: function() {
                $('#scanResult').html(
                    '<div class="alert alert-danger">' +
                    '<i class="fas fa-exclamation-triangle fa-2x mb-2"></i><br>' +
                    '<h5>Scan failed. Please try again.</h5>' +
                    '</div>'
                );
            }
        });
    });
    
    // Auto-focus on input
    setInterval(function() {
        $('#badgeInput').focus();
    }, 1000);
});
</script>
{% endblock %}
"""

# ============================================================================
# SYSTEM MANAGER DASHBOARD TEMPLATE
# ============================================================================

SYSTEM_MANAGER_DASHBOARD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}System Manager Dashboard{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <h2 class="mb-4">
        <i class="fas fa-cogs me-2"></i>System Manager Dashboard
    </h2>
    
    <!-- Stats Row -->
    <div class="row mb-4">
        <div class="col-md-3 mb-3">
            <div class="card stat-card">
                <div class="card-body text-center">
                    <i class="fas fa-users fa-3x text-primary mb-3"></i>
                    <h3>{{ stats.total_users }}</h3>
                    <p class="text-muted mb-0">Total Users</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card">
                <div class="card-body text-center">
                    <i class="fas fa-calendar-alt fa-3x text-primary mb-3"></i>
                    <h3>{{ stats.total_events }}</h3>
                    <p class="text-muted mb-0">Total Events</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card">
                <div class="card-body text-center">
                    <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
                    <h3>{{ stats.checked_in_now }}</h3>
                    <p class="text-muted mb-0">Currently Checked In</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card">
                <div class="card-body text-center">
                    <i class="fas fa-hourglass-half fa-3x text-warning mb-3"></i>
                    <h3>{{ stats.pending_verifications }}</h3>
                    <p class="text-muted mb-0">Pending Verifications</p>
                    <a href="{{ url_for('system_manager.verifications') }}" class="btn btn-sm btn-warning mt-2">
                        Review
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick Links -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-bolt me-2"></i>Quick Actions</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-2">
                            <a href="{{ url_for('system_manager.users') }}" class="btn btn-outline-primary w-100">
                                <i class="fas fa-users me-2"></i>Manage Users
                            </a>
                        </div>
                        <div class="col-md-3 mb-2">
                            <a href="{{ url_for('system_manager.events') }}" class="btn btn-outline-primary w-100">
                                <i class="fas fa-calendar me-2"></i>Manage Events
                            </a>
                        </div>
                        <div class="col-md-3 mb-2">
                            <a href="{{ url_for('system_manager.verifications') }}" class="btn btn-outline-warning w-100">
                                <i class="fas fa-certificate me-2"></i>Verifications
                            </a>
                        </div>
                        <div class="col-md-3 mb-2">
                            <a href="{{ url_for('system_manager.reports') }}" class="btn btn-outline-info w-100">
                                <i class="fas fa-chart-bar me-2"></i>Reports
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Recent Activity -->
    <div class="row">
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-user-plus me-2"></i>Recent Users</h5>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        {% for user in recent_users %}
                        <div class="list-group-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ user.full_name }}</strong><br>
                                    <small class="text-muted">{{ user.email }}</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-info">{{ user.role }}</span><br>
                                    <small class="text-muted">{{ user.created_at|timeago }}</small>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-calendar-plus me-2"></i>Recent Events</h5>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        {% for event in recent_events %}
                        <div class="list-group-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ event.title }}</strong><br>
                                    <small class="text-muted">by {{ event.creator_name }}</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-{{ 'success' if event.status == 'published' else 'warning' }}">
                                        {{ event.status }}
                                    </span><br>
                                    <small class="text-muted">{{ event.created_at|timeago }}</small>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# SEARCH & NOTIFICATIONS TEMPLATES
# ============================================================================

SEARCH_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Search - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-body">
            <h2 class="mb-4"><i class="fas fa-search me-2"></i>Search</h2>
            
            <form method="GET" action="{{ url_for('search') }}">
                <div class="input-group input-group-lg mb-4">
                    <input type="text" class="form-control" name="q" 
                           placeholder="Search events, users, forums..." 
                           value="{{ query }}" autofocus>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search me-2"></i>Search
                    </button>
                </div>
            </form>
            
            {% if query %}
            <h5 class="mb-3">Search Results for "{{ query }}"</h5>
            
            <ul class="nav nav-tabs mb-4">
                <li class="nav-item">
                    <a class="nav-link active" data-bs-toggle="tab" href="#events">
                        Events ({{ results.events|length }})
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-bs-toggle="tab" href="#users">
                        Users ({{ results.users|length }})
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-bs-toggle="tab" href="#forums">
                        Forums ({{ results.forums|length }})
                    </a>
                </li>
            </ul>
            
            <div class="tab-content">
                <div class="tab-pane fade show active" id="events">
                    {% if results.events %}
                    <div class="list-group">
                        {% for event in results.events %}
                        <a href="{{ url_for('events.detail', event_id=event.id) }}" 
                           class="list-group-item list-group-item-action">
                            <h6>{{ event.title }}</h6>
                            <p class="mb-1 text-muted">{{ event.description|truncate_words(20) }}</p>
                            <small class="text-muted">
                                <i class="fas fa-calendar me-1"></i>
                                {{ event.start_date|datetime_format('%b %d, %Y') }}
                            </small>
                        </a>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted">No events found.</p>
                    {% endif %}
                </div>
                
                <div class="tab-pane fade" id="users">
                    {% if results.users %}
                    <div class="row">
                        {% for user in results.users %}
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <div class="d-flex align-items-center">
                                        <img src="{{ url_for('static', filename=user.profile_picture or 'uploads/default-avatar.png') }}" 
                                             class="profile-img me-3" alt="{{ user.full_name }}">
                                        <div>
                                            <h6 class="mb-0">{{ user.full_name }}</h6>
                                            <small class="text-muted">{{ user.current_employment or 'User' }}</small>
                                        </div>
                                    </div>
                                    <a href="{{ url_for('profile.view', user_id=user.id) }}" 
                                       class="btn btn-sm btn-outline-primary mt-2 w-100">
                                        View Profile
                                    </a>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted">No users found.</p>
                    {% endif %}
                </div>
                
                <div class="tab-pane fade" id="forums">
                    {% if results.forums %}
                    <div class="list-group">
                        {% for forum in results.forums %}
                        <a href="{{ url_for('forum.view', forum_id=forum.id) }}" 
                           class="list-group-item list-group-item-action">
                            <h6>{{ forum.title }}</h6>
                            <p class="mb-1 text-muted">{{ forum.description|truncate_words(20) }}</p>
                            <small class="text-muted">
                                <i class="fas fa-users me-1"></i>{{ forum.member_count }} members
                            </small>
                        </a>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted">No forums found.</p>
                    {% endif %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

NOTIFICATIONS_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Notifications - NFC Events{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h4 class="mb-0"><i class="fas fa-bell me-2"></i>Notifications</h4>
            <form method="POST" action="{{ url_for('mark_all_read') }}" class="d-inline">
                <button type="submit" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-check-double me-1"></i>Mark All Read
                </button>
            </form>
        </div>
        <div class="card-body p-0">
            {% if notifications %}
            <div class="list-group list-group-flush">
                {% for notif in notifications %}
                <a href="{{ notif.link or '#' }}" 
                   class="list-group-item list-group-item-action {% if not notif.is_read %}bg-light{% endif %}">
                    <div class="d-flex justify-content-between">
                        <h6 class="mb-1">{{ notif.title }}</h6>
                        <small class="text-muted">{{ notif.created_at|timeago }}</small>
                    </div>
                    <p class="mb-0 text-muted">{{ notif.message }}</p>
                </a>
                {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-5">
                <i class="fas fa-bell-slash fa-4x text-muted mb-3"></i>
                <h5 class="text-muted">No notifications</h5>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("📦 PART 4B: Creating Final Templates")
    
    print_section("Creating forum templates...")
    create_file('templates/forum/list.html', FORUM_LIST_TEMPLATE)
    create_file('templates/forum/view.html', FORUM_VIEW_TEMPLATE)
    
    print_section("Creating messaging templates...")
    create_file('templates/messaging/inbox.html', MESSAGING_INBOX_TEMPLATE)
    create_file('templates/messaging/conversation.html', MESSAGING_CONVERSATION_TEMPLATE)
    
    print_section("Creating NFC scanner template...")
    create_file('templates/nfc/scanner.html', NFC_SCANNER_TEMPLATE)
    
    print_section("Creating system manager templates...")
    create_file('templates/system_manager/dashboard.html', SYSTEM_MANAGER_DASHBOARD_TEMPLATE)
    
    print_section("Creating search & notifications templates...")
    create_file('templates/search.html', SEARCH_TEMPLATE)
    create_file('templates/notifications.html', NOTIFICATIONS_TEMPLATE)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 4B Complete - ALL TEMPLATES DONE!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.CYAN}🎉 COMPLETE TEMPLATE SUMMARY:{Colors.END}")
    print(f"  ✅ base.html - Blue & White theme")
    print(f"  ✅ Auth templates (login, signup, password)")
    print(f"  ✅ home.html - Dashboard")
    print(f"  ✅ Event templates (list, detail, create)")
    print(f"  ✅ Profile template")
    print(f"  ✅ Forum templates (list, view)")
    print(f"  ✅ Messaging templates (inbox, conversation)")
    print(f"  ✅ NFC scanner template")
    print(f"  ✅ System Manager dashboard")
    print(f"  ✅ Search & Notifications")
    
    print(f"\n{Colors.YELLOW}📋 Next Steps:{Colors.END}")
    print(f"  1. Run part 5 to create app.py (main application file)")
    print(f"  2. Test the complete system!")

if __name__ == '__main__':
    main()