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
# BASE TEMPLATE (Blue & White Theme)
# ============================================================================

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NFC Event & Social Network{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Custom CSS - Blue & White Theme -->
    <style>
        :root {
            /* Blue & White Color Scheme */
            --primary-blue: #0066CC;
            --secondary-blue: #3399FF;
            --light-blue: #66B2FF;
            --dark-blue: #004080;
            --white: #FFFFFF;
            --off-white: #F8F9FA;
            --border-blue: #B3D9FF;
            --text-dark: #212529;
            --text-muted: #6c757d;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--off-white);
            color: var(--text-dark);
        }
        
        /* Navbar - Blue */
        .navbar {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
            box-shadow: 0 2px 10px rgba(0, 102, 204, 0.3);
        }
        
        .navbar-brand, .nav-link {
            color: var(--white) !important;
            font-weight: 500;
        }
        
        .nav-link:hover {
            color: var(--light-blue) !important;
        }
        
        .navbar .badge {
            background-color: #ff4444;
            position: absolute;
            top: 5px;
            right: 5px;
            font-size: 0.7rem;
        }
        
        /* Buttons */
        .btn-primary {
            background-color: var(--primary-blue);
            border-color: var(--primary-blue);
        }
        
        .btn-primary:hover {
            background-color: var(--dark-blue);
            border-color: var(--dark-blue);
        }
        
        .btn-outline-primary {
            color: var(--primary-blue);
            border-color: var(--primary-blue);
        }
        
        .btn-outline-primary:hover {
            background-color: var(--primary-blue);
            border-color: var(--primary-blue);
            color: var(--white);
        }
        
        /* Cards */
        .card {
            border: 1px solid var(--border-blue);
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 102, 204, 0.1);
            background-color: var(--white);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
            color: var(--white);
            border-bottom: none;
            font-weight: 600;
        }
        
        /* Links */
        a {
            color: var(--primary-blue);
            text-decoration: none;
        }
        
        a:hover {
            color: var(--dark-blue);
            text-decoration: underline;
        }
        
        /* Badges */
        .badge-primary {
            background-color: var(--primary-blue);
        }
        
        .badge-info {
            background-color: var(--secondary-blue);
        }
        
        /* Alerts */
        .alert-primary {
            background-color: #e6f2ff;
            border-color: var(--border-blue);
            color: var(--dark-blue);
        }
        
        /* Tables */
        .table thead {
            background-color: var(--primary-blue);
            color: var(--white);
        }
        
        .table-striped tbody tr:nth-of-type(odd) {
            background-color: #f0f8ff;
        }
        
        /* Forms */
        .form-control:focus, .form-select:focus {
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 0.25rem rgba(0, 102, 204, 0.25);
        }
        
        /* Footer */
        footer {
            background: linear-gradient(135deg, var(--dark-blue) 0%, var(--primary-blue) 100%);
            color: var(--white);
            padding: 2rem 0;
            margin-top: 3rem;
        }
        
        footer a {
            color: var(--light-blue);
        }
        
        footer a:hover {
            color: var(--white);
        }
        
        /* Sidebar (for dashboard) */
        .sidebar {
            background-color: var(--white);
            border-right: 2px solid var(--border-blue);
            min-height: calc(100vh - 56px);
        }
        
        .sidebar .nav-link {
            color: var(--text-dark) !important;
            padding: 0.75rem 1rem;
            border-left: 3px solid transparent;
        }
        
        .sidebar .nav-link:hover {
            background-color: #e6f2ff;
            border-left-color: var(--primary-blue);
        }
        
        .sidebar .nav-link.active {
            background-color: #e6f2ff;
            border-left-color: var(--primary-blue);
            color: var(--primary-blue) !important;
            font-weight: 600;
        }
        
        /* Stats Cards */
        .stat-card {
            background: linear-gradient(135deg, var(--white) 0%, #f0f8ff 100%);
            border-left: 4px solid var(--primary-blue);
        }
        
        .stat-card h3 {
            color: var(--primary-blue);
        }
        
        /* Profile Picture */
        .profile-img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--white);
        }
        
        .profile-img-lg {
            width: 150px;
            height: 150px;
            border: 4px solid var(--primary-blue);
        }
        
        /* Pagination */
        .pagination .page-link {
            color: var(--primary-blue);
        }
        
        .pagination .page-item.active .page-link {
            background-color: var(--primary-blue);
            border-color: var(--primary-blue);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--off-white);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary-blue);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--dark-blue);
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-calendar-check me-2"></i>
                <strong>NFC Events</strong>
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% if current_user %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">
                            <i class="fas fa-home"></i> Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('events.list_events') }}">
                            <i class="fas fa-calendar-alt"></i> Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('forum.list_forums') }}">
                            <i class="fas fa-comments"></i> Forums
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('search') }}">
                            <i class="fas fa-search"></i> Search
                        </a>
                    </li>
                    {% endif %}
                </ul>
                
                <ul class="navbar-nav">
                    {% if current_user %}
                    <li class="nav-item position-relative">
                        <a class="nav-link" href="{{ url_for('messaging.inbox') }}">
                            <i class="fas fa-envelope"></i>
                            {% if unread_messages > 0 %}
                            <span class="badge">{{ unread_messages }}</span>
                            {% endif %}
                        </a>
                    </li>
                    <li class="nav-item position-relative">
                        <a class="nav-link" href="{{ url_for('notifications') }}">
                            <i class="fas fa-bell"></i>
                            {% if unread_notifications > 0 %}
                            <span class="badge">{{ unread_notifications }}</span>
                            {% endif %}
                        </a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" 
                           data-bs-toggle="dropdown">
                            {% if current_user.profile_picture %}
                            <img src="{{ url_for('static', filename=current_user.profile_picture) }}" 
                                 class="profile-img" alt="Profile">
                            {% else %}
                            <i class="fas fa-user-circle"></i>
                            {% endif %}
                            {{ current_user.full_name }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="{{ url_for('profile.view', user_id=current_user.id) }}">
                                    <i class="fas fa-user"></i> My Profile
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{{ url_for('profile.edit') }}">
                                    <i class="fas fa-edit"></i> Edit Profile
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{{ url_for('events.my_events') }}">
                                    <i class="fas fa-calendar"></i> My Events
                                </a>
                            </li>
                            {% if current_user.role == 'system_manager' %}
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="{{ url_for('system_manager.dashboard') }}">
                                    <i class="fas fa-cogs"></i> System Manager
                                </a>
                            </li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="{{ url_for('auth.change_password') }}">
                                    <i class="fas fa-key"></i> Change Password
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{{ url_for('auth.logout') }}">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </a>
                            </li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.login') }}">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.signup') }}">
                            <i class="fas fa-user-plus"></i> Sign Up
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Flash Messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    <i class="fas fa-info-circle me-2"></i>{{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    
    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <h5><i class="fas fa-calendar-check me-2"></i>NFC Events</h5>
                    <p class="text-white-50">Professional event management and networking platform.</p>
                </div>
                <div class="col-md-4 mb-3">
                    <h6>Quick Links</h6>
                    <ul class="list-unstyled">
                        <li><a href="{{ url_for('events.list_events') }}">Events</a></li>
                        <li><a href="{{ url_for('forum.list_forums') }}">Forums</a></li>
                        <li><a href="{{ url_for('search') }}">Search</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-3">
                    <h6>Contact</h6>
                    <p class="text-white-50">
                        <i class="fas fa-envelope me-2"></i> support@nfcevents.com<br>
                        <i class="fas fa-phone me-2"></i> +263 123 456 789
                    </p>
                </div>
            </div>
            <hr class="bg-white">
            <div class="text-center text-white-50">
                <small>&copy; 2026 NFC Event & Social Network. All rights reserved.</small>
            </div>
        </div>
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- jQuery (for AJAX) -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# ============================================================================
# AUTH TEMPLATES
# ============================================================================

LOGIN_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Login - NFC Events{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            <div class="card shadow-lg">
                <div class="card-header text-center py-3">
                    <h4 class="mb-0">
                        <i class="fas fa-sign-in-alt me-2"></i>Login
                    </h4>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="{{ url_for('auth.login') }}">
                        <div class="mb-3">
                            <label for="email" class="form-label">
                                <i class="fas fa-envelope"></i> Email Address
                            </label>
                            <input type="email" class="form-control" id="email" name="email" 
                                   placeholder="your.email@example.com" required autofocus>
                        </div>
                        
                        <div class="mb-3">
                            <label for="password" class="form-label">
                                <i class="fas fa-lock"></i> Password
                            </label>
                            <input type="password" class="form-control" id="password" name="password" 
                                   placeholder="Enter your password" required>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-sign-in-alt me-2"></i>Login
                            </button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <p class="mb-0">Don't have an account?</p>
                        <a href="{{ url_for('auth.signup') }}" class="btn btn-outline-primary mt-2">
                            <i class="fas fa-user-plus me-2"></i>Create Account
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Demo Credentials -->
            <div class="card mt-3">
                <div class="card-body">
                    <h6 class="text-muted">Demo Credentials:</h6>
                    <small class="text-muted">
                        <strong>System Manager:</strong> admin@nfcevents.com / admin123<br>
                        <strong>Regular User:</strong> user@nfcevents.com / user123
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

SIGNUP_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Sign Up - NFC Events{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5 mb-5">
        <div class="col-md-6">
            <div class="card shadow-lg">
                <div class="card-header text-center py-3">
                    <h4 class="mb-0">
                        <i class="fas fa-user-plus me-2"></i>Create Account
                    </h4>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="{{ url_for('auth.signup') }}">
                        <div class="row">
                            <div class="col-md-12 mb-3">
                                <label for="full_name" class="form-label">
                                    <i class="fas fa-user"></i> Full Name *
                                </label>
                                <input type="text" class="form-control" id="full_name" name="full_name" 
                                       placeholder="e.g., Thabo Ncube" required>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">
                                <i class="fas fa-envelope"></i> Email Address *
                            </label>
                            <input type="email" class="form-control" id="email" name="email" 
                                   placeholder="your.email@example.com" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="phone_number" class="form-label">
                                <i class="fas fa-phone"></i> Phone Number
                            </label>
                            <input type="tel" class="form-control" id="phone_number" name="phone_number" 
                                   placeholder="+263 123 456 789">
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="password" class="form-label">
                                    <i class="fas fa-lock"></i> Password *
                                </label>
                                <input type="password" class="form-control" id="password" name="password" 
                                       placeholder="Min. 6 characters" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="confirm_password" class="form-label">
                                    <i class="fas fa-lock"></i> Confirm Password *
                                </label>
                                <input type="password" class="form-control" id="confirm_password" 
                                       name="confirm_password" placeholder="Re-enter password" required>
                            </div>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-user-plus me-2"></i>Create Account
                            </button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <p class="mb-0">Already have an account?</p>
                        <a href="{{ url_for('auth.login') }}" class="btn btn-outline-primary mt-2">
                            <i class="fas fa-sign-in-alt me-2"></i>Login
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

CHANGE_PASSWORD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Change Password - NFC Events{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-key me-2"></i>Change Password
                    </h5>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('auth.change_password') }}">
                        <div class="mb-3">
                            <label for="current_password" class="form-label">Current Password</label>
                            <input type="password" class="form-control" id="current_password" 
                                   name="current_password" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="new_password" class="form-label">New Password</label>
                            <input type="password" class="form-control" id="new_password" 
                                   name="new_password" required>
                            <small class="text-muted">Minimum 6 characters</small>
                        </div>
                        
                        <div class="mb-3">
                            <label for="confirm_password" class="form-label">Confirm New Password</label>
                            <input type="password" class="form-control" id="confirm_password" 
                                   name="confirm_password" required>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-check me-2"></i>Change Password
                            </button>
                            <a href="{{ url_for('profile.view', user_id=current_user.id) }}" 
                               class="btn btn-outline-secondary">
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
# HOME TEMPLATE
# ============================================================================

HOME_TEMPLATE = """
{% extends "base.html" %}

{% block title %}Home - NFC Events{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Welcome Section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card stat-card">
                <div class="card-body">
                    <h2 class="mb-1">
                        <i class="fas fa-home me-2"></i>
                        Welcome back, {{ current_user.full_name }}!
                    </h2>
                    <p class="text-muted mb-0">
                        <i class="fas fa-calendar-day me-2"></i>
                        {{ "now"|datetime_format('%A, %B %d, %Y') }}
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Stats Row -->
    <div class="row mb-4">
        <div class="col-md-3 mb-3">
            <div class="card stat-card h-100">
                <div class="card-body text-center">
                    <i class="fas fa-calendar-check fa-3x text-primary mb-3"></i>
                    <h3 class="mb-0">{{ stats.total_events }}</h3>
                    <p class="text-muted mb-0">Total Events</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card h-100">
                <div class="card-body text-center">
                    <i class="fas fa-ticket-alt fa-3x text-primary mb-3"></i>
                    <h3 class="mb-0">{{ stats.my_registrations }}</h3>
                    <p class="text-muted mb-0">My Registrations</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card h-100">
                <div class="card-body text-center">
                    <i class="fas fa-comments fa-3x text-primary mb-3"></i>
                    <h3 class="mb-0">{{ stats.my_forums }}</h3>
                    <p class="text-muted mb-0">My Forums</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-3">
            <div class="card stat-card h-100">
                <div class="card-body text-center">
                    <i class="fas fa-users fa-3x text-primary mb-3"></i>
                    <h3 class="mb-0">{{ stats.followers }}</h3>
                    <p class="text-muted mb-0">Followers</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main Content Row -->
    <div class="row">
        <!-- Left Column - Events -->
        <div class="col-lg-8 mb-4">
            <!-- My Registered Events -->
            {% if my_events %}
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-calendar-check me-2"></i>My Upcoming Events
                    </h5>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        {% for event in my_events %}
                        <a href="{{ url_for('events.detail', event_id=event.id) }}" 
                           class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="mb-1">{{ event.title }}</h6>
                                    <p class="mb-1 text-muted small">
                                        <i class="fas fa-calendar me-1"></i>
                                        {{ event.start_date|datetime_format('%b %d, %Y at %I:%M %p') }}
                                    </p>
                                    <p class="mb-0 text-muted small">
                                        <i class="fas fa-map-marker-alt me-1"></i>
                                        {{ event.location }}
                                    </p>
                                </div>
                                <span class="badge bg-primary">{{ event.attendance_status }}</span>
                            </div>
                        </a>
                        {% endfor %}
                    </div>
                </div>
                <div class="card-footer text-center">
                    <a href="{{ url_for('events.list_events') }}" class="btn btn-sm btn-outline-primary">
                        View All Events <i class="fas fa-arrow-right ms-1"></i>
                    </a>
                </div>
            </div>
            {% endif %}
            
            <!-- Upcoming Events -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-calendar-alt me-2"></i>Upcoming Events
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        {% for event in upcoming_events %}
                        <div class="col-md-6 mb-3">
                            <div class="card h-100">
                                {% if event.cover_image %}
                                <img src="{{ url_for('static', filename=event.cover_image) }}" 
                                     class="card-img-top" style="height: 150px; object-fit: cover;" 
                                     alt="{{ event.title }}">
                                {% else %}
                                <div class="card-img-top bg-primary text-white d-flex align-items-center justify-content-center" 
                                     style="height: 150px;">
                                    <i class="fas fa-calendar-alt fa-3x"></i>
                                </div>
                                {% endif %}
                                <div class="card-body">
                                    <h6 class="card-title">{{ event.title }}</h6>
                                    <p class="card-text small text-muted">
                                        {{ event.description|truncate_words(15) }}
                                    </p>
                                    <p class="mb-1 small">
                                        <i class="fas fa-calendar me-1"></i>
                                        {{ event.start_date|datetime_format('%b %d, %Y') }}
                                    </p>
                                    <p class="mb-2 small">
                                        <i class="fas fa-users me-1"></i>
                                        {{ event.registration_count }} registered
                                    </p>
                                    <a href="{{ url_for('events.detail', event_id=event.id) }}" 
                                       class="btn btn-sm btn-primary w-100">
                                        View Details
                                    </a>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Right Column - Sidebar -->
        <div class="col-lg-4">
            <!-- Quick Actions -->
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-bolt me-2"></i>Quick Actions
                    </h6>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('events.create') }}" class="btn btn-primary">
                            <i class="fas fa-plus-circle me-2"></i>Create Event
                        </a>
                        <a href="{{ url_for('forum.create_forum') }}" class="btn btn-outline-primary">
                            <i class="fas fa-comments me-2"></i>Create Forum
                        </a>
                        <a href="{{ url_for('nfc.scanner_page') }}" class="btn btn-outline-primary">
                            <i class="fas fa-qrcode me-2"></i>NFC Scanner
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Active Forums -->
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-fire me-2"></i>Active Forums
                    </h6>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        {% for forum in active_forums[:5] %}
                        <a href="{{ url_for('forum.view', forum_id=forum.id) }}" 
                           class="list-group-item list-group-item-action">
                            <h6 class="mb-1">{{ forum.title }}</h6>
                            <small class="text-muted">
                                <i class="fas fa-users me-1"></i>{{ forum.member_count }} members
                                <i class="fas fa-comment ms-2 me-1"></i>{{ forum.post_count }} posts
                            </small>
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
            
            <!-- Recent Notifications -->
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-bell me-2"></i>Recent Notifications
                    </h6>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        {% for notif in notifications %}
                        <a href="{{ notif.link or '#' }}" 
                           class="list-group-item list-group-item-action {% if not notif.is_read %}bg-light{% endif %}">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">{{ notif.title }}</h6>
                                <small>{{ notif.created_at|timeago }}</small>
                            </div>
                            <p class="mb-0 small">{{ notif.message }}</p>
                        </a>
                        {% endfor %}
                    </div>
                </div>
                <div class="card-footer text-center">
                    <a href="{{ url_for('notifications') }}" class="btn btn-sm btn-outline-primary">
                        View All Notifications
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("📦 PART 4: Creating Templates (Base, Auth & Home)")
    
    print_section("Creating base template...")
    create_file('templates/base.html', BASE_TEMPLATE)
    
    print_section("Creating auth templates...")
    create_file('templates/auth/login.html', LOGIN_TEMPLATE)
    create_file('templates/auth/signup.html', SIGNUP_TEMPLATE)
    create_file('templates/auth/change_password.html', CHANGE_PASSWORD_TEMPLATE)
    
    print_section("Creating home template...")
    create_file('templates/home.html', HOME_TEMPLATE)
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 4 Complete - Base & Auth Templates created!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.CYAN}📋 Templates Created:{Colors.END}")
    print(f"  ✅ base.html - Blue & White theme")
    print(f"  ✅ auth/login.html")
    print(f"  ✅ auth/signup.html")
    print(f"  ✅ auth/change_password.html")
    print(f"  ✅ home.html - Dashboard")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 4A for Event & Profile templates{Colors.END}")

if __name__ == '__main__':
    main()