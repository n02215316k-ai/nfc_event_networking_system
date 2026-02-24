import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
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

def admin_required(f):
    '''Decorator to require admin role (event_admin or system_manager)'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect('/login')
        if session.get('role') not in ['event_admin', 'system_manager']:
            flash('Access denied. Admin privileges required.', 'danger')
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
        role_data = cursor.fetchall()
        stats['users_by_role'] = role_data
        stats['role_labels'] = [r['role'] for r in role_data]
        stats['role_counts'] = [r['count'] for r in role_data]
        
        # Recent scans
        cursor.execute(\"\"\"
            SELECT s.*, u1.full_name as scanner_name, u2.full_name as scanned_name
            FROM nfc_scans s
            LEFT JOIN users u1 ON s.scanner_id = u1.id
            LEFT JOIN users u2 ON s.scanned_user_id = u2.id
            ORDER BY s.scanned_at DESC
            LIMIT 10
        \"\"\")
        stats['recent_scans'] = cursor.fetchall()
        
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
            'role_labels': [],
            'role_counts': [],
            'recent_scans': []
        }

def get_all_events():
    '''Get all events from database'''
    try:
        from database import get_db_connection
        from datetime import datetime
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(\"\"\"
            SELECT e.*, 
                   COUNT(DISTINCT er.user_id) as attendee_count
            FROM events e
            LEFT JOIN event_registrations er ON e.id = er.event_id
            GROUP BY e.id
            ORDER BY e.event_date DESC
        \"\"\")
        events = cursor.fetchall()
        
        # Count upcoming and past events
        now = datetime.now().date()
        upcoming_count = sum(1 for e in events if e.get('event_date') and e['event_date'] >= now)
        past_count = len(events) - upcoming_count
        
        # Total registrations
        cursor.execute("SELECT COUNT(*) as count FROM event_registrations")
        total_registrations = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return {
            'events': events,
            'upcoming_count': upcoming_count,
            'past_count': past_count,
            'total_registrations': total_registrations
        }
    except Exception as e:
        print(f"Error getting events: {e}")
        return {
            'events': [],
            'upcoming_count': 0,
            'past_count': 0,
            'total_registrations': 0
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

def delete_event(event_id):
    '''Delete event from system'''
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete related records
        cursor.execute("DELETE FROM event_registrations WHERE event_id = %s", (event_id,))
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting event: {e}")
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
                alert('Event deleted successfully');
                location.reload();
            } else {
                alert('Error deleting event: ' + (data.message || 'Unknown error'));
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

# Continue with other templates (reports, system/users, settings, logs)
# Due to character limit, I'll create the remaining files in the next part

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ CORE ADMIN FILES CREATED (Part 1){Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Created {len(created_files)} files so far:{Colors.END}")
for file in created_files:
    print(f"  {Colors.GREEN}✓{Colors.END} {file}")

print(f"\n{Colors.YELLOW}Creating remaining templates...{Colors.END}\n")

# [Continuing with remaining templates - truncated for response size]