import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

def create_file(filepath, content):
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

# System Manager Users Template
USERS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Manage Users - System Manager{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-users me-2"></i>Manage Users</h2>
    <div class="card mt-3">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Joined</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in all_users %}
                        <tr>
                            <td>{{ user.id }}</td>
                            <td>{{ user.full_name }}</td>
                            <td>{{ user.email }}</td>
                            <td><span class="badge bg-{{ 'danger' if user.role == 'system_manager' else 'primary' }}">{{ user.role }}</span></td>
                            <td><span class="badge bg-{{ 'success' if user.is_verified else 'warning' }}">{{ 'Verified' if user.is_verified else 'Pending' }}</span></td>
                            <td>{{ user.created_at|datetime_format('%Y-%m-%d') }}</td>
                            <td>
                                <a href="{{ url_for('system_manager.edit_user', user_id=user.id) }}" class="btn btn-sm btn-primary">Edit</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# System Manager Events Template
EVENTS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Manage Events - System Manager{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-calendar me-2"></i>Manage Events</h2>
    <div class="card mt-3">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Creator</th>
                            <th>Date</th>
                            <th>Status</th>
                            <th>Registrations</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for event in all_events %}
                        <tr>
                            <td>{{ event.id }}</td>
                            <td>{{ event.title }}</td>
                            <td>{{ event.creator_name }}</td>
                            <td>{{ event.start_date|datetime_format('%Y-%m-%d') }}</td>
                            <td><span class="badge bg-{{ 'success' if event.status == 'published' else 'secondary' }}">{{ event.status }}</span></td>
                            <td>{{ event.registration_count }}</td>
                            <td>
                                <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-sm btn-primary">View</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# System Manager Verifications Template
VERIFICATIONS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Qualification Verifications - System Manager{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-certificate me-2"></i>Qualification Verifications</h2>
    <div class="card mt-3">
        <div class="card-body">
            {% if pending_qualifications %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Qualification</th>
                            <th>Institution</th>
                            <th>Year</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for qual in pending_qualifications %}
                        <tr>
                            <td>{{ qual.user_name }}</td>
                            <td>{{ qual.qualification }}</td>
                            <td>{{ qual.institution }}</td>
                            <td>{{ qual.year }}</td>
                            <td><span class="badge bg-warning">Pending</span></td>
                            <td>
                                <form method="POST" action="{{ url_for('system_manager.verify_qualification', qual_id=qual.id) }}" class="d-inline">
                                    <button type="submit" class="btn btn-sm btn-success">Verify</button>
                                </form>
                                <form method="POST" action="{{ url_for('system_manager.reject_qualification', qual_id=qual.id) }}" class="d-inline">
                                    <button type="submit" class="btn btn-sm btn-danger">Reject</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <p class="text-muted">No pending verifications.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

# System Manager Reports Template
REPORTS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Reports - System Manager{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-chart-bar me-2"></i>System Reports</h2>
    
    <div class="row mt-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5>Total Users</h5>
                    <h2>{{ stats.total_users or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5>Total Events</h5>
                    <h2>{{ stats.total_events or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5>Total Forums</h5>
                    <h2>{{ stats.total_forums or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <h5>NFC Scans</h5>
                    <h2>{{ stats.total_scans or 0 }}</h2>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

print(f"\n{Colors.CYAN}Creating system manager templates...{Colors.END}\n")

create_file('templates/system_manager/users.html', USERS_TEMPLATE)
create_file('templates/system_manager/events.html', EVENTS_TEMPLATE)
create_file('templates/system_manager/verifications.html', VERIFICATIONS_TEMPLATE)
create_file('templates/system_manager/reports.html', REPORTS_TEMPLATE)

print(f"\n{Colors.GREEN}✅ All system manager templates created!{Colors.END}\n")