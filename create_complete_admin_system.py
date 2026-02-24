import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.cyan}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING COMPLETE ADMIN & SYSTEM MANAGER SECTIONS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

created_files = []

# Create directories
os.makedirs('src/controllers', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('templates/system', exist_ok=True)

# ============================================================================
# 1. SYSTEM CONTROLLER
# ============================================================================
print(f"{Colors.CYAN}Creating system_controller.py...{Colors.END}")

SYSTEM_CONTROLLER = """from flask import render_template, redirect, session, flash, request
from functools import wraps

def system_manager_required(f):
    '''Decorator to require system manager role'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect('/login')
        if session.get('role') != 'system_manager':
            flash('Access denied. System manager privileges required.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def get_all_users():
    '''Get all users from database'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(\"\"\"
            SELECT id, full_name, email, role, job_title, company, 
                   phone, created_at, nfc_badge_id
            FROM users 
            ORDER BY created_at DESC
        \"\"\")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Error getting users: {e}")
        return []

def get_system_stats():
    '''Get system-wide statistics'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        stats = {}
        
        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        stats['total_users'] = cursor.fetchone()['count']
        
        # Total events
        cursor.execute("SELECT COUNT(*) as count FROM events")
        stats['total_events'] = cursor.fetchone()['count']
        
        # Total connections
        cursor.execute("SELECT COUNT(*) as count FROM connections")
        stats['total_connections'] = cursor.fetchone()['count']
        
        # Total scans
        cursor.execute("SELECT COUNT(*) as count FROM nfc_scans")
        stats['total_scans'] = cursor.fetchone()['count']
        
        # Users by role
        cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
        stats['users_by_role'] = cursor.fetchall()
        
        # Recent activity (last 10 scans)
        cursor.execute(\"\"\"
            SELECT s.*, u1.full_name as scanner_name, u2.full_name as scanned_name
            FROM nfc_scans s
            LEFT JOIN users u1 ON s.scanner_id = u1.id
            LEFT JOIN users u2 ON s.scanned_user_id = u2.id
            ORDER BY s.scanned_at DESC
            LIMIT 10
        \"\"\")
        stats['recent_activity'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return stats
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return {
            'total_users': 0,
            'total_events': 0,
            'total_connections': 0,
            'total_scans': 0,
            'users_by_role': [],
            'recent_activity': []
        }

def update_user_role(user_id, new_role):
    '''Update user role'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating user role: {e}")
        return False

def delete_user(user_id):
    '''Delete user from system'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete related records first
        cursor.execute("DELETE FROM event_registrations WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM connections WHERE user_id = %s OR connected_user_id = %s", (user_id, user_id))
        cursor.execute("DELETE FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s", (user_id, user_id))
        cursor.execute("DELETE FROM forum_posts WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM messages WHERE sender_id = %s OR receiver_id = %s", (user_id, user_id))
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
"""

with open('src/controllers/system_controller.py', 'w', encoding='utf-8') as f:
    f.write(SYSTEM_CONTROLLER.strip())
created_files.append('src/controllers/system_controller.py')

# ============================================================================
# 2. ADMIN EVENTS TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating admin/events.html...{Colors.END}")

ADMIN_EVENTS = """{% extends 'base.html' %}

{% block title %}Event Management - Admin{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="display-5 fw-bold text-white">
            <i class="fas fa-calendar-alt me-3"></i>
            Event Management
        </h1>
        <a href="/events/create" class="btn btn-success btn-lg">
            <i class="fas fa-plus-circle me-2"></i>
            Create New Event
        </a>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card shadow-lg bg-primary text-white">
                <div class="card-body">
                    <h6 class="text-uppercase">Total Events</h6>
                    <h2 class="mb-0">{{ events|length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-success text-white">
                <div class="card-body">
                    <h6 class="text-uppercase">Upcoming</h6>
                    <h2 class="mb-0">{{ upcoming_count }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-info text-white">
                <div class="card-body">
                    <h6 class="text-uppercase">Total Registrations</h6>
                    <h2 class="mb-0">{{ total_registrations }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-warning text-white">
                <div class="card-body">
                    <h6 class="text-uppercase">Past Events</h6>
                    <h2 class="mb-0">{{ past_count }}</h2>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card shadow-lg">
        <div class="card-header bg-dark text-white">
            <h5 class="mb-0">
                <i class="fas fa-list me-2"></i>
                All Events
            </h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Registrations</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if events %}
                            {% for event in events %}
                            {% set is_dict = event is mapping %}
                            <tr>
                                <td>{{ event.id if not is_dict else event['id'] }}</td>
                                <td>
                                    <strong>{{ event.title if not is_dict else event['title'] }}</strong>
                                </td>
                                <td>
                                    {% set event_date = event.event_date if not is_dict else event.get('event_date') %}
                                    {% if event_date %}
                                        {{ event_date.strftime('%Y-%m-%d') if event_date is not string else event_date }}
                                    {% else %}
                                        TBD
                                    {% endif %}
                                </td>
                                <td>{{ event.location if not is_dict else event.get('location', 'TBD') }}</td>
                                <td>
                                    <span class="badge bg-primary">
                                        {{ event.attendee_count if not is_dict else event.get('attendee_count', 0) }}
                                    </span>
                                </td>
                                <td>
                                    {% if event_date and event_date >= now %}
                                        <span class="badge bg-success">Upcoming</span>
                                    {% else %}
                                        <span class="badge bg-secondary">Past</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="/events/{{ event.id if not is_dict else event['id'] }}" 
                                       class="btn btn-sm btn-info" title="View">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="/events/edit/{{ event.id if not is_dict else event['id'] }}" 
                                       class="btn btn-sm btn-warning" title="Edit">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <button onclick="deleteEvent({{ event.id if not is_dict else event['id'] }})" 
                                            class="btn btn-sm btn-danger" title="Delete">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="7" class="text-center py-5">
                                    <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
                                    <p class="text-muted">No events found</p>
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
</div>

<script>
function deleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
        fetch(`/admin/events/delete/${eventId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error deleting event: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error deleting event');
            console.error(error);
        });
    }
}
</script>
{% endblock %}
"""

with open('templates/admin/events.html', 'w', encoding='utf-8') as f:
    f.write(ADMIN_EVENTS.strip())
created_files.append('templates/admin/events.html')

# ============================================================================
# 3. ADMIN REPORTS TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating admin/reports.html...{Colors.END}")

ADMIN_REPORTS = """{% extends 'base.html' %}

{% block title %}Reports & Analytics - Admin{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    
    <h1 class="display-5 fw-bold text-white mb-4">
        <i class="fas fa-chart-bar me-3"></i>
        Reports & Analytics
    </h1>
    
    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card shadow-lg text-center">
                <div class="card-body">
                    <i class="fas fa-users fa-3x text-primary mb-3"></i>
                    <h6 class="text-uppercase text-muted">Total Users</h6>
                    <h2 class="fw-bold">{{ stats.total_users or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg text-center">
                <div class="card-body">
                    <i class="fas fa-calendar fa-3x text-success mb-3"></i>
                    <h6 class="text-uppercase text-muted">Total Events</h6>
                    <h2 class="fw-bold">{{ stats.total_events or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg text-center">
                <div class="card-body">
                    <i class="fas fa-handshake fa-3x text-info mb-3"></i>
                    <h6 class="text-uppercase text-muted">Connections</h6>
                    <h2 class="fw-bold">{{ stats.total_connections or 0 }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg text-center">
                <div class="card-body">
                    <i class="fas fa-qrcode fa-3x text-warning mb-3"></i>
                    <h6 class="text-uppercase text-muted">NFC Scans</h6>
                    <h2 class="fw-bold">{{ stats.total_scans or 0 }}</h2>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row g-4">
        <div class="col-lg-6">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-user-tag me-2"></i>
                        Users by Role
                    </h5>
                </div>
                <div class="card-body">
                    <canvas id="rolesChart" height="200"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-chart-line me-2"></i>
                        Event Registrations
                    </h5>
                </div>
                <div class="card-body">
                    <canvas id="registrationsChart" height="200"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-12">
            <div class="card shadow-lg">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-activity me-2"></i>
                        Recent Activity
                    </h5>
                </div>
                <div class="card-body">
                    {% if stats.recent_scans %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>Scanner</th>
                                        <th>Scanned User</th>
                                        <th>Type</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for scan in stats.recent_scans %}
                                    <tr>
                                        <td>{{ scan.scanned_at.strftime('%Y-%m-%d %H:%M') if scan.scanned_at else 'N/A' }}</td>
                                        <td>{{ scan.scanner_name or 'Unknown' }}</td>
                                        <td>{{ scan.scanned_name or 'Unknown' }}</td>
                                        <td>
                                            <span class="badge bg-primary">
                                                {{ scan.scan_type or 'NFC' }}
                                            </span>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted text-center py-4">No recent activity</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Roles Chart
const rolesCtx = document.getElementById('rolesChart').getContext('2d');
new Chart(rolesCtx, {
    type: 'doughnut',
    data: {
        labels: {{ stats.role_labels|tojson if stats.role_labels else '[]'|safe }},
        datasets: [{
            data: {{ stats.role_counts|tojson if stats.role_counts else '[]'|safe }},
            backgroundColor: ['#4F46E5', '#10B981', '#F59E0B']
        }]
    }
});

// Registrations Chart (placeholder)
const regCtx = document.getElementById('registrationsChart').getContext('2d');
new Chart(regCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Registrations',
            data: [12, 19, 8, 15, 22, 18],
            borderColor: '#10B981',
            tension: 0.4
        }]
    }
});
</script>
{% endblock %}
"""

with open('templates/admin/reports.html', 'w', encoding='utf-8') as f:
    f.write(ADMIN_REPORTS.strip())
created_files.append('templates/admin/reports.html')

# ============================================================================
# 4. SYSTEM USERS TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating system/users.html...{Colors.END}")

SYSTEM_USERS = """{% extends 'base.html' %}

{% block title %}User Management - System{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="display-5 fw-bold text-white">
            <i class="fas fa-users-cog me-3"></i>
            User Management
        </h1>
        <div>
            <input type="text" id="searchUsers" class="form-control" placeholder="🔍 Search users..." style="width: 300px;">
        </div>
    </div>
    
    <div class="card shadow-lg">
        <div class="card-header bg-dark text-white">
            <h5 class="mb-0">
                <i class="fas fa-list me-2"></i>
                All Users ({{ users|length }})
            </h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0" id="usersTable">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Company</th>
                            <th>NFC Badge</th>
                            <th>Joined</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if users %}
                            {% for user in users %}
                            <tr>
                                <td>{{ user.id or user['id'] }}</td>
                                <td>
                                    <strong>{{ user.full_name or user['full_name'] }}</strong>
                                    <br>
                                    <small class="text-muted">{{ user.job_title or user.get('job_title', 'N/A') }}</small>
                                </td>
                                <td>{{ user.email or user['email'] }}</td>
                                <td>
                                    <select class="form-select form-select-sm" 
                                            onchange="updateRole({{ user.id or user['id'] }}, this.value)">
                                        <option value="attendee" {{ 'selected' if (user.role or user['role']) == 'attendee' else '' }}>
                                            Attendee
                                        </option>
                                        <option value="event_admin" {{ 'selected' if (user.role or user['role']) == 'event_admin' else '' }}>
                                            Event Admin
                                        </option>
                                        <option value="system_manager" {{ 'selected' if (user.role or user['role']) == 'system_manager' else '' }}>
                                            System Manager
                                        </option>
                                    </select>
                                </td>
                                <td>{{ user.company or user.get('company', 'N/A') }}</td>
                                <td>
                                    <code>{{ user.nfc_badge_id or user.get('nfc_badge_id', 'Not assigned') }}</code>
                                </td>
                                <td>
                                    {% set created = user.created_at or user.get('created_at') %}
                                    {% if created %}
                                        {{ created.strftime('%Y-%m-%d') if created is not string else created[:10] }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </td>
                                <td>
                                    <button onclick="viewUser({{ user.id or user['id'] }})" 
                                            class="btn btn-sm btn-info" title="View">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button onclick="deleteUser({{ user.id or user['id'] }})" 
                                            class="btn btn-sm btn-danger" title="Delete">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="8" class="text-center py-5">
                                    <i class="fas fa-users-slash fa-3x text-muted mb-3"></i>
                                    <p class="text-muted">No users found</p>
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
</div>

<script>
// Search functionality
document.getElementById('searchUsers').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#usersTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});

function updateRole(userId, newRole) {
    if (confirm(`Change user role to ${newRole}?`)) {
        fetch('/system/users/update-role', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, role: newRole })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Role updated successfully');
            } else {
                alert('Error updating role: ' + data.message);
                location.reload();
            }
        })
        .catch(error => {
            alert('Error updating role');
            console.error(error);
            location.reload();
        });
    } else {
        location.reload();
    }
}

function viewUser(userId) {
    window.location.href = `/admin/users/${userId}`;
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user? All their data will be permanently removed.')) {
        fetch(`/system/users/delete/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('User deleted successfully');
                location.reload();
            } else {
                alert('Error deleting user: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error deleting user');
            console.error(error);
        });
    }
}
</script>
{% endblock %}
"""

with open('templates/system/users.html', 'w', encoding='utf-8') as f:
    f.write(SYSTEM_USERS.strip())
created_files.append('templates/system/users.html')

# ============================================================================
# 5. SYSTEM SETTINGS TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating system/settings.html...{Colors.END}")

SYSTEM_SETTINGS = """{% extends 'base.html' %}

{% block title %}System Settings{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    
    <h1 class="display-5 fw-bold text-white mb-4">
        <i class="fas fa-cogs me-3"></i>
        System Settings
    </h1>
    
    <div class="row g-4">
        <div class="col-lg-8">
            
            <div class="card shadow-lg mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-server me-2"></i>
                        General Settings
                    </h5>
                </div>
                <div class="card-body">
                    <form method="POST" action="/system/settings/update">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">System Name</label>
                            <input type="text" name="system_name" class="form-control" 
                                   value="Event Social Network" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Admin Email</label>
                            <input type="email" name="admin_email" class="form-control" 
                                   value="admin@eventsocial.net" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Max Upload Size (MB)</label>
                            <input type="number" name="max_upload_size" class="form-control" 
                                   value="5" min="1" max="50">
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="maintenanceMode" 
                                       name="maintenance_mode">
                                <label class="form-check-label" for="maintenanceMode">
                                    <strong>Maintenance Mode</strong>
                                    <br>
                                    <small class="text-muted">Temporarily disable access for regular users</small>
                                </label>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="allowRegistration" 
                                       name="allow_registration" checked>
                                <label class="form-check-label" for="allowRegistration">
                                    <strong>Allow New Registrations</strong>
                                    <br>
                                    <small class="text-muted">Enable/disable new user signups</small>
                                </label>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="emailNotifications" 
                                       name="email_notifications" checked>
                                <label class="form-check-label" for="emailNotifications">
                                    <strong>Email Notifications</strong>
                                    <br>
                                    <small class="text-muted">Send email notifications for events</small>
                                </label>
                            </div>
                        </div>
                        
                        <hr>
                        
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-save me-2"></i>
                            Save Settings
                        </button>
                        
                    </form>
                </div>
            </div>
            
            <div class="card shadow-lg">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Danger Zone
                    </h5>
                </div>
                <div class="card-body">
                    <h6 class="fw-bold">Clear System Cache</h6>
                    <p class="text-muted">Remove all cached data to improve performance</p>
                    <button class="btn btn-warning mb-3" onclick="clearCache()">
                        <i class="fas fa-broom me-2"></i>
                        Clear Cache
                    </button>
                    
                    <hr>
                    
                    <h6 class="fw-bold text-danger">Reset Database</h6>
                    <p class="text-muted">⚠️ This will delete ALL data. Use with extreme caution!</p>
                    <button class="btn btn-danger" onclick="resetDatabase()">
                        <i class="fas fa-database me-2"></i>
                        Reset Database
                    </button>
                </div>
            </div>
            
        </div>
        
        <div class="col-lg-4">
            
            <div class="card shadow-lg mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-info-circle me-2"></i>
                        System Information
                    </h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <strong>Version:</strong>
                        <p class="text-muted mb-0">1.0.0</p>
                    </div>
                    <div class="mb-3">
                        <strong>Database:</strong>
                        <p class="text-muted mb-0">MySQL</p>
                    </div>
                    <div class="mb-3">
                        <strong>Server Time:</strong>
                        <p class="text-muted mb-0">{{ now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
                    </div>
                    <div class="mb-3">
                        <strong>Python Version:</strong>
                        <p class="text-muted mb-0">3.11+</p>
                    </div>
                </div>
            </div>
            
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-database me-2"></i>
                        Database Status
                    </h5>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-between mb-2">
                        <span>Connection:</span>
                        <span class="badge bg-success">Active</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Tables:</span>
                        <span class="badge bg-info">10</span>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Size:</span>
                        <span class="badge bg-warning">2.5 MB</span>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
    
</div>

<script>
function clearCache() {
    if (confirm('Clear all system cache?')) {
        fetch('/system/settings/clear-cache', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Cache cleared successfully');
        })
        .catch(error => {
            alert('Error clearing cache');
            console.error(error);
        });
    }
}

function resetDatabase() {
    const confirmation = prompt('Type "RESET DATABASE" to confirm:');
    if (confirmation === 'RESET DATABASE') {
        alert('Database reset feature is disabled for safety. Please use database management tools.');
    }
}
</script>
{% endblock %}
"""

with open('templates/system/settings.html', 'w', encoding='utf-8') as f:
    f.write(SYSTEM_SETTINGS.strip())
created_files.append('templates/system/settings.html')

# ============================================================================
# 6. SYSTEM LOGS TEMPLATE
# ============================================================================
print(f"{Colors.CYAN}Creating system/logs.html...{Colors.END}")

SYSTEM_LOGS = """{% extends 'base.html' %}

{% block title %}System Logs{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="display-5 fw-bold text-white">
            <i class="fas fa-file-alt me-3"></i>
            System Logs
        </h1>
        <div>
            <button class="btn btn-warning me-2" onclick="downloadLogs()">
                <i class="fas fa-download me-2"></i>
                Download Logs
            </button>
            <button class="btn btn-danger" onclick="clearLogs()">
                <i class="fas fa-trash me-2"></i>
                Clear Logs
            </button>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-outline-light active" onclick="filterLogs('all')">
                    All Logs
                </button>
                <button type="button" class="btn btn-outline-light" onclick="filterLogs('info')">
                    <i class="fas fa-info-circle"></i> Info
                </button>
                <button type="button" class="btn btn-outline-light" onclick="filterLogs('warning')">
                    <i class="fas fa-exclamation-triangle"></i> Warning
                </button>
                <button type="button" class="btn btn-outline-light" onclick="filterLogs('error')">
                    <i class="fas fa-times-circle"></i> Error
                </button>
                <button type="button" class="btn btn-outline-light" onclick="filterLogs('success')">
                    <i class="fas fa-check-circle"></i> Success
                </button>
            </div>
        </div>
    </div>
    
    <div class="card shadow-lg">
        <div class="card-header bg-dark text-white">
            <h5 class="mb-0">
                <i class="fas fa-list me-2"></i>
                Recent Activity Logs
            </h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive" style="max-height: 600px; overflow-y: auto;">
                <table class="table table-hover mb-0" id="logsTable">
                    <thead class="table-light sticky-top">
                        <tr>
                            <th>Time</th>
                            <th>Level</th>
                            <th>User</th>
                            <th>Action</th>
                            <th>Details</th>
                            <th>IP Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if logs %}
                            {% for log in logs %}
                            <tr class="log-{{ log.level or 'info' }}">
                                <td>
                                    <small>{{ log.created_at.strftime('%Y-%m-%d %H:%M:%S') if log.created_at else 'N/A' }}</small>
                                </td>
                                <td>
                                    {% set level = log.level or 'info' %}
                                    {% if level == 'error' %}
                                        <span class="badge bg-danger">Error</span>
                                    {% elif level == 'warning' %}
                                        <span class="badge bg-warning">Warning</span>
                                    {% elif level == 'success' %}
                                        <span class="badge bg-success">Success</span>
                                    {% else %}
                                        <span class="badge bg-info">Info</span>
                                    {% endif %}
                                </td>
                                <td>{{ log.user_name or 'System' }}</td>
                                <td><strong>{{ log.action or 'N/A' }}</strong></td>
                                <td>{{ log.details or 'No details' }}</td>
                                <td><code>{{ log.ip_address or 'N/A' }}</code></td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="6" class="text-center py-5">
                                    <i class="fas fa-file-excel fa-3x text-muted mb-3"></i>
                                    <p class="text-muted">No logs available</p>
                                    <small class="text-muted">System activity will appear here</small>
                                </td>
                            </tr>
                        {% endif %}
                        
                        <!-- Sample logs for demonstration -->
                        <tr class="log-info">
                            <td><small>2026-02-23 12:30:15</small></td>
                            <td><span class="badge bg-info">Info</span></td>
                            <td>Admin User</td>
                            <td><strong>User Login</strong></td>
                            <td>Successful login from dashboard</td>
                            <td><code>127.0.0.1</code></td>
                        </tr>
                        <tr class="log-success">
                            <td><small>2026-02-23 12:28:45</small></td>
                            <td><span class="badge bg-success">Success</span></td>
                            <td>System</td>
                            <td><strong>Event Created</strong></td>
                            <td>New event "Tech Conference 2026" created</td>
                            <td><code>127.0.0.1</code></td>
                        </tr>
                        <tr class="log-warning">
                            <td><small>2026-02-23 12:25:30</small></td>
                            <td><span class="badge bg-warning">Warning</span></td>
                            <td>System</td>
                            <td><strong>High Memory Usage</strong></td>
                            <td>Memory usage at 85%</td>
                            <td><code>localhost</code></td>
                        </tr>
                        <tr class="log-info">
                            <td><small>2026-02-23 12:20:10</small></td>
                            <td><span class="badge bg-info">Info</span></td>
                            <td>John Doe</td>
                            <td><strong>Profile Updated</strong></td>
                            <td>User updated profile information</td>
                            <td><code>192.168.1.105</code></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
</div>

<script>
let currentFilter = 'all';

function filterLogs(level) {
    currentFilter = level;
    const rows = document.querySelectorAll('#logsTable tbody tr');
    
    // Update button states
    document.querySelectorAll('.btn-group button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    rows.forEach(row => {
        if (level === 'all') {
            row.style.display = '';
        } else {
            row.style.display = row.classList.contains(`log-${level}`) ? '' : 'none';
        }
    });
}

function downloadLogs() {
    // Implement log download
    alert('Downloading logs...');
    window.location.href = '/system/logs/download';
}

function clearLogs() {
    if (confirm('Are you sure you want to clear all logs? This cannot be undone.')) {
        fetch('/system/logs/clear', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Logs cleared successfully');
            location.reload();
        })
        .catch(error => {
            alert('Error clearing logs');
            console.error(error);
        });
    }
}

// Auto-refresh logs every 30 seconds
setInterval(() => {
    location.reload();
}, 30000);
</script>
{% endblock %}
"""

with open('templates/system/logs.html', 'w', encoding='utf-8') as f:
    f.write(SYSTEM_LOGS.strip())
created_files.append('templates/system/logs.html')

# ============================================================================
# SUMMARY
# ============================================================================
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL ADMIN & SYSTEM FILES CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Created {len(created_files)} files:{Colors.END}")
for file in created_files:
    print(f"  {Colors.GREEN}✓{Colors.END} {file}")

print(f"\n{Colors.BOLD}{Colors.YELLOW}NEXT STEP: ADD ROUTES TO APP.PY{Colors.END}")
print(f"{Colors.YELLOW}Run the route installer script next!{Colors.END}\n")