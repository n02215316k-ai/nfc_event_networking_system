base_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NFC Event Social Network{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-network-wired me-2"></i>NFC Events
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% if session.user_id %}
                        <!-- Common Links for All Users -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('index') }}">
                                <i class="fas fa-home me-1"></i>Home
                            </a>
                        </li>
                        
                        <!-- Events Menu -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="eventsDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-calendar me-1"></i>Events
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="eventsDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('events.list_events') }}">
                                    <i class="fas fa-list me-2"></i>Browse Events
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('events.my_events') }}">
                                    <i class="fas fa-ticket-alt me-2"></i>My Events
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('events.create_event') }}">
                                    <i class="fas fa-plus me-2"></i>Create Event
                                </a></li>
                            </ul>
                        </li>

                        <!-- Forums -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="forumsDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-comments me-1"></i>Forums
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="forumsDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('forum.list_forums') }}">
                                    <i class="fas fa-list me-2"></i>All Forums
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('forum.create_forum') }}">
                                    <i class="fas fa-plus me-2"></i>Create Forum
                                </a></li>
                            </ul>
                        </li>

                        <!-- NFC Features -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="nfcDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-qrcode me-1"></i>NFC
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="nfcDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('nfc.scanner_page') }}">
                                    <i class="fas fa-camera me-2"></i>Scan QR/NFC
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('nfc.my_connections') }}">
                                    <i class="fas fa-users me-2"></i>My Connections
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('nfc.recent_scans') }}">
                                    <i class="fas fa-history me-2"></i>Recent Scans
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('nfc.scan_stats') }}">
                                    <i class="fas fa-chart-bar me-2"></i>Statistics
                                </a></li>
                            </ul>
                        </li>

                        <!-- Event Admin Menu (Event Admins + System Managers) -->
                        {% if session.user_role in ['event_admin', 'system_manager'] %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle bg-success rounded" href="#" id="eventAdminDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-calendar-check me-1"></i>Event Admin
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="eventAdminDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('event_admin.dashboard') }}">
                                    <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                                </a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><h6 class="dropdown-header">Event Management</h6></li>
                                <li><a class="dropdown-item" href="{{ url_for('event_admin.networking_analytics') }}">
                                    <i class="fas fa-project-diagram me-2"></i>Networking Analytics
                                </a></li>
                            </ul>
                        </li>
                        {% endif %}

                        <!-- System Manager Menu (System Managers Only) -->
                        {% if session.user_role == 'system_manager' %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle bg-danger rounded" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user-shield me-1"></i>System Admin
                            </a>
                            <ul class="dropdown-menu dropdown-menu-lg" aria-labelledby="adminDropdown" style="min-width: 250px;">
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.dashboard') }}">
                                    <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                                </a></li>
                                <li><hr class="dropdown-divider"></li>
                                
                                <li><h6 class="dropdown-header"><i class="fas fa-users me-2"></i>User Management</h6></li>
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.users') }}">
                                    <i class="fas fa-list me-2"></i>All Users
                                </a></li>
                                
                                <li><hr class="dropdown-divider"></li>
                                
                                <li><h6 class="dropdown-header"><i class="fas fa-calendar me-2"></i>Events</h6></li>
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.events') }}">
                                    <i class="fas fa-calendar-alt me-2"></i>All Events
                                </a></li>
                                
                                <li><hr class="dropdown-divider"></li>
                                
                                <li><h6 class="dropdown-header"><i class="fas fa-check-circle me-2"></i>Verifications</h6></li>
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.verifications') }}">
                                    <i class="fas fa-tasks me-2"></i>Pending Verifications
                                </a></li>
                                
                                <li><hr class="dropdown-divider"></li>
                                
                                <li><h6 class="dropdown-header"><i class="fas fa-chart-line me-2"></i>Reports</h6></li>
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.reports') }}">
                                    <i class="fas fa-file-alt me-2"></i>System Reports
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.nfc_logs') }}">
                                    <i class="fas fa-qrcode me-2"></i>NFC Logs
                                </a></li>
                                
                                <li><hr class="dropdown-divider"></li>
                                
                                <li><a class="dropdown-item" href="{{ url_for('system_manager.settings') }}">
                                    <i class="fas fa-cog me-2"></i>Settings
                                </a></li>
                            </ul>
                        </li>
                        {% endif %}

                        <!-- Messages -->
                        <li class="nav-item">
                            <a class="nav-link position-relative" href="{{ url_for('messaging.inbox') }}">
                                <i class="fas fa-envelope me-1"></i>Messages
                                {% if session.unread_messages_count and session.unread_messages_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ session.unread_messages_count }}
                                </span>
                                {% endif %}
                            </a>
                        </li>

                    {% else %}
                        <!-- Guest Links -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('about') }}">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('help_page') }}">Help</a>
                        </li>
                    {% endif %}
                </ul>

                <!-- Right Side Menu -->
                <ul class="navbar-nav">
                    {% if session.user_id %}
                        <!-- Notifications -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle position-relative" href="#" id="notificationsDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-bell"></i>
                                {% if session.unread_notifications_count and session.unread_notifications_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ session.unread_notifications_count }}
                                </span>
                                {% endif %}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown" style="width: 320px; max-height: 400px; overflow-y: auto;">
                                <li><h6 class="dropdown-header">Notifications</h6></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-center small" href="{{ url_for('notifications') }}">
                                    <i class="fas fa-bell me-1"></i>View All Notifications
                                </a></li>
                            </ul>
                        </li>

                        <!-- User Profile -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user-circle me-1"></i>
                                {{ session.user_name|default('User') }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('profile.my_profile') }}">
                                    <i class="fas fa-user me-2"></i>My Profile
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('profile.qr_code') }}">
                                    <i class="fas fa-qrcode me-2"></i>My QR Code
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('profile.edit') }}">
                                    <i class="fas fa-edit me-2"></i>Edit Profile
                                </a></li>
                                <li><a class="dropdown-item" href="{{ url_for('auth.change_password') }}">
                                    <i class="fas fa-key me-2"></i>Change Password
                                </a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><span class="dropdown-item-text text-muted small">
                                    Role: <strong>{{ session.user_role|title }}</strong>
                                </span></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="{{ url_for('auth.logout') }}">
                                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                                </a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.login') }}">
                                <i class="fas fa-sign-in-alt me-1"></i>Login
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link btn btn-success text-white ms-2" href="{{ url_for('auth.register') }}">
                                <i class="fas fa-user-plus me-1"></i>Register
                            </a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="container mt-3">
                {% for category, message in messages %}
                <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                    <i class="fas fa-{{ 'exclamation-triangle' if category == 'error' else 'info-circle' }} me-2"></i>
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main class="mb-5">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center text-lg-start mt-auto">
        <div class="container p-4">
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-4 mb-md-0">
                    <h5 class="text-uppercase fw-bold">NFC Event Network</h5>
                    <p class="text-muted">Connect, Network, and Engage at Events</p>
                </div>
                <div class="col-lg-4 col-md-6 mb-4 mb-md-0">
                    <h5 class="text-uppercase fw-bold">Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="{{ url_for('about') }}" class="text-dark text-decoration-none">About</a></li>
                        <li><a href="{{ url_for('help_page') }}" class="text-dark text-decoration-none">Help</a></li>
                        <li><a href="{{ url_for('search') }}" class="text-dark text-decoration-none">Search</a></li>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-12 mb-4 mb-md-0">
                    <h5 class="text-uppercase fw-bold">Contact</h5>
                    <p class="text-muted mb-0">
                        <i class="fas fa-envelope me-2"></i>support@nfcevents.com
                    </p>
                </div>
            </div>
        </div>
        <div class="text-center p-3 bg-dark text-white">
            <small>© 2026 NFC Event Social Network. All rights reserved.</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# Write to file
with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base_html_content)

print("✅ base.html updated with role-based navigation!")