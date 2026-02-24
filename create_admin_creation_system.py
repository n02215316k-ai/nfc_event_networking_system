import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING ADMIN CREATION SYSTEM{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

created_files = []

# Create directories
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('templates/system', exist_ok=True)

# ============================================================================
# 1. ADMIN CREATE USER PAGE
# ============================================================================
print(f"{Colors.CYAN}Creating admin/create_user.html...{Colors.END}")

ADMIN_CREATE_USER = """{% extends 'base.html' %}

{% block title %}Create User - Admin{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-user-plus me-2"></i>
                        Create New User
                    </h4>
                </div>
                <div class="card-body p-4">
                    
                    <form method="POST" action="/admin/users/create">
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Full Name *</label>
                                <input type="text" name="full_name" class="form-control" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Email *</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Password *</label>
                                <input type="password" name="password" class="form-control" 
                                       minlength="6" required>
                                <small class="text-muted">Minimum 6 characters</small>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Confirm Password *</label>
                                <input type="password" name="confirm_password" class="form-control" 
                                       minlength="6" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Role *</label>
                                <select name="role" class="form-select" required>
                                    <option value="attendee">Attendee (Regular User)</option>
                                    <option value="event_admin">Event Admin</option>
                                    {% if session.role == 'system_manager' %}
                                    <option value="system_manager">System Manager</option>
                                    {% endif %}
                                </select>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Phone</label>
                                <input type="tel" name="phone" class="form-control">
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Job Title</label>
                                <input type="text" name="job_title" class="form-control">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Company</label>
                                <input type="text" name="company" class="form-control">
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">NFC Badge ID</label>
                            <input type="text" name="nfc_badge_id" class="form-control" 
                                   placeholder="Optional - Auto-generated if empty">
                        </div>
                        
                        <hr>
                        
                        <div class="d-flex justify-content-between">
                            <a href="/admin/users" class="btn btn-secondary">
                                <i class="fas fa-arrow-left me-2"></i>
                                Cancel
                            </a>
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-user-plus me-2"></i>
                                Create User
                            </button>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/admin/create_user.html', 'w', encoding='utf-8') as f:
    f.write(ADMIN_CREATE_USER.strip())
created_files.append('templates/admin/create_user.html')

# ============================================================================
# 2. SYSTEM CREATE ADMIN PAGE
# ============================================================================
print(f"{Colors.CYAN}Creating system/create_admin.html...{Colors.END}")

SYSTEM_CREATE_ADMIN = """{% extends 'base.html' %}

{% block title %}Create Admin - System{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            
            <div class="card shadow-lg border-warning">
                <div class="card-header bg-warning text-dark">
                    <h4 class="mb-0">
                        <i class="fas fa-user-shield me-2"></i>
                        Quick Admin Creator
                    </h4>
                </div>
                <div class="card-body p-4">
                    
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        <strong>System Manager Access Required</strong>
                        <p class="mb-0 small">This will create a user with administrative privileges.</p>
                    </div>
                    
                    <form method="POST" action="/system/create-admin">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Full Name *</label>
                            <input type="text" name="full_name" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Email *</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Password *</label>
                            <input type="password" name="password" class="form-control" 
                                   minlength="6" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Admin Role *</label>
                            <select name="role" class="form-select" required>
                                <option value="event_admin">Event Admin</option>
                                <option value="system_manager">System Manager</option>
                            </select>
                            <small class="text-muted">
                                • Event Admin: Manage events<br>
                                • System Manager: Full system access
                            </small>
                        </div>
                        
                        <hr>
                        
                        <div class="d-flex justify-content-between">
                            <a href="/system/users" class="btn btn-secondary">
                                <i class="fas fa-arrow-left me-2"></i>
                                Cancel
                            </a>
                            <button type="submit" class="btn btn-warning btn-lg">
                                <i class="fas fa-user-shield me-2"></i>
                                Create Admin
                            </button>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/system/create_admin.html', 'w', encoding='utf-8') as f:
    f.write(SYSTEM_CREATE_ADMIN.strip())
created_files.append('templates/system/create_admin.html')

# ============================================================================
# 3. PUBLIC REGISTRATION PAGE
# ============================================================================
print(f"{Colors.CYAN}Creating register.html...{Colors.END}")

REGISTER_PAGE = """{% extends 'base.html' %}

{% block title %}Register - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0 text-center">
                        <i class="fas fa-user-plus me-2"></i>
                        Create Account
                    </h4>
                </div>
                <div class="card-body p-4">
                    
                    <form method="POST" action="/register" id="registerForm">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Full Name *</label>
                            <input type="text" name="full_name" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Email *</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Password *</label>
                            <input type="password" name="password" id="password" 
                                   class="form-control" minlength="6" required>
                            <small class="text-muted">Minimum 6 characters</small>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Confirm Password *</label>
                            <input type="password" name="confirm_password" id="confirm_password" 
                                   class="form-control" minlength="6" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Phone</label>
                            <input type="tel" name="phone" class="form-control">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Job Title</label>
                            <input type="text" name="job_title" class="form-control">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Company</label>
                            <input type="text" name="company" class="form-control">
                        </div>
                        
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="terms" required>
                            <label class="form-check-label" for="terms">
                                I agree to the <a href="/privacy" target="_blank">Terms & Privacy Policy</a> *
                            </label>
                        </div>
                        
                        <button type="submit" class="btn btn-success btn-lg w-100 mb-3">
                            <i class="fas fa-user-plus me-2"></i>
                            Create Account
                        </button>
                        
                        <p class="text-center text-muted mb-0">
                            Already have an account? 
                            <a href="/login" class="text-decoration-none">Login here</a>
                        </p>
                        
                    </form>
                    
                </div>
            </div>
            
        </div>
    </div>
</div>

<script>
document.getElementById('registerForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirm_password').value;
    
    if (password !== confirm) {
        e.preventDefault();
        alert('Passwords do not match!');
    }
});
</script>
{% endblock %}
"""

with open('templates/register.html', 'w', encoding='utf-8') as f:
    f.write(REGISTER_PAGE.strip())
created_files.append('templates/register.html')

# ============================================================================
# 4. SYSTEM USERS PAGE (was missing)
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
            <a href="/system/create-admin" class="btn btn-warning me-2">
                <i class="fas fa-user-shield me-2"></i>
                Quick Admin
            </a>
            <a href="/admin/users/create" class="btn btn-success">
                <i class="fas fa-user-plus me-2"></i>
                Create User
            </a>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card shadow-lg bg-primary text-white">
                <div class="card-body text-center">
                    <h6 class="text-uppercase">Total Users</h6>
                    <h2 class="mb-0">{{ users|length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-success text-white">
                <div class="card-body text-center">
                    <h6 class="text-uppercase">Attendees</h6>
                    <h2 class="mb-0">{{ users|selectattr('role', 'equalto', 'attendee')|list|length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-warning text-white">
                <div class="card-body text-center">
                    <h6 class="text-uppercase">Event Admins</h6>
                    <h2 class="mb-0">{{ users|selectattr('role', 'equalto', 'event_admin')|list|length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-lg bg-danger text-white">
                <div class="card-body text-center">
                    <h6 class="text-uppercase">System Managers</h6>
                    <h2 class="mb-0">{{ users|selectattr('role', 'equalto', 'system_manager')|list|length }}</h2>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card shadow-lg">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
                <i class="fas fa-list me-2"></i>
                All Users ({{ users|length }})
            </h5>
            <input type="text" id="searchUsers" class="form-control w-25" 
                   placeholder="🔍 Search users...">
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
# SUMMARY
# ============================================================================
print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL TEMPLATES CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Created {len(created_files)} template files:{Colors.END}")
for file in created_files:
    print(f"  {Colors.GREEN}✓{Colors.END} {file}")

print(f"\n{Colors.BOLD}{Colors.YELLOW}NEXT: RUN THE ROUTES INSTALLER{Colors.END}")
print(f"{Colors.YELLOW}This will add the corresponding routes to app.py{Colors.END}\n")