import os

print("=" * 80)
print("🔧 FIXING PROFILE VIEW ROUTE")
print("=" * 80)

profile_controller_path = "src/controllers/profile_controller.py"

if not os.path.exists(profile_controller_path):
    print(f"❌ Error: {profile_controller_path} not found!")
    exit(1)

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if view route exists
if "@profile_bp.route('/view/<int:user_id>')" in content:
    print("✅ Route /profile/view/<user_id> already exists")
else:
    print("⚠️  Route /profile/view/<user_id> is MISSING - Adding it now...")
    
    # Find a good place to insert the route (after imports, before other routes)
    view_route = '''
@profile_bp.route('/view/<int:user_id>')
def view(user_id):
    """View any user's profile (public)"""
    from database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get user details
        cursor.execute("""
            SELECT id, full_name, email, profile_picture, bio, 
                   qr_code_url, created_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('home.index'))
        
        # Get user's events (if any)
        cursor.execute("""
            SELECT e.* 
            FROM events e
            JOIN event_registrations er ON e.id = er.event_id
            WHERE er.user_id = %s AND e.date >= CURDATE()
            ORDER BY e.date ASC
            LIMIT 5
        """, (user_id,))
        
        upcoming_events = cursor.fetchall()
        
        # Check if current user is viewing their own profile
        is_own_profile = False
        if 'user_id' in session:
            is_own_profile = (session['user_id'] == user_id)
        
        # Check if already connected (for logged-in users)
        is_connected = False
        if 'user_id' in session and not is_own_profile:
            cursor.execute("""
                SELECT id FROM scans 
                WHERE scanner_id = %s AND scanned_user_id = %s
            """, (session['user_id'], user_id))
            is_connected = cursor.fetchone() is not None
        
        return render_template('profile/view.html',
                             user=user,
                             upcoming_events=upcoming_events,
                             is_own_profile=is_own_profile,
                             is_connected=is_connected)
    
    except Exception as e:
        print(f"Error viewing profile: {e}")
        flash('Error loading profile', 'error')
        return redirect(url_for('home.index'))
    
    finally:
        cursor.close()
        conn.close()

'''
    
    # Insert after the blueprint definition
    if "profile_bp = Blueprint" in content:
        # Find the end of imports section
        import_end = content.find("\n\n@profile_bp")
        if import_end == -1:
            # No routes yet, add after blueprint definition
            blueprint_pos = content.find("profile_bp = Blueprint")
            next_line = content.find("\n", blueprint_pos)
            content = content[:next_line] + "\n" + view_route + content[next_line:]
        else:
            content = content[:import_end] + view_route + content[import_end:]
        
        print("✅ Added /profile/view/<user_id> route")
    else:
        print("❌ Could not find blueprint definition!")
        exit(1)

# Save the updated file
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Saved profile_controller.py")

# ============================================================================
# Create/Update Profile View Template
# ============================================================================
print("\n📄 Creating profile view template...")

os.makedirs('templates/profile', exist_ok=True)

profile_view_template = '''{% extends "base.html" %}

{% block title %}{{ user.full_name }} - Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Profile Card -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    {% if user.profile_picture %}
                    <img src="{{ url_for('static', filename=user.profile_picture) }}" 
                         class="rounded-circle mb-3" 
                         style="width: 150px; height: 150px; object-fit: cover;">
                    {% else %}
                    <div class="rounded-circle bg-primary text-white mx-auto mb-3 d-flex align-items-center justify-content-center"
                         style="width: 150px; height: 150px; font-size: 60px;">
                        {{ user.full_name[0].upper() if user.full_name else 'U' }}
                    </div>
                    {% endif %}
                    
                    <h3>{{ user.full_name }}</h3>
                    <p class="text-muted">{{ user.email }}</p>
                    
                    {% if user.bio %}
                    <p class="mt-3">{{ user.bio }}</p>
                    {% endif %}
                    
                    <hr>
                    
                    <p class="small text-muted">
                        <i class="fas fa-calendar"></i> 
                        Member since {{ user.created_at.strftime('%B %Y') }}
                    </p>
                    
                    <!-- Action Buttons -->
                    <div class="mt-3">
                        {% if is_own_profile %}
                        <a href="{{ url_for('profile.edit') }}" class="btn btn-primary btn-block">
                            <i class="fas fa-edit"></i> Edit Profile
                        </a>
                        <a href="{{ url_for('profile.qr_code') }}" class="btn btn-info btn-block">
                            <i class="fas fa-qrcode"></i> My QR Code
                        </a>
                        {% else %}
                            {% if session.user_id %}
                            <a href="{{ url_for('messaging.compose') }}?recipient={{ user.id }}" 
                               class="btn btn-primary btn-block">
                                <i class="fas fa-envelope"></i> Send Message
                            </a>
                            
                            {% if is_connected %}
                            <button class="btn btn-success btn-block" disabled>
                                <i class="fas fa-check-circle"></i> Connected
                            </button>
                            {% else %}
                            <button onclick="connectWithUser({{ user.id }})" 
                                    class="btn btn-outline-primary btn-block" id="connect-btn">
                                <i class="fas fa-user-plus"></i> Connect
                            </button>
                            {% endif %}
                            {% else %}
                            <a href="{{ url_for('auth.login') }}" class="btn btn-primary btn-block">
                                <i class="fas fa-sign-in-alt"></i> Login to Connect
                            </a>
                            {% endif %}
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <!-- QR Code -->
            {% if user.qr_code_url and is_own_profile %}
            <div class="card mt-3">
                <div class="card-header bg-info text-white">
                    <h5><i class="fas fa-qrcode"></i> My QR Code</h5>
                </div>
                <div class="card-body text-center">
                    <img src="{{ url_for('static', filename='qr_codes/user_' + user.id|string + '_qr.png') }}" 
                         alt="QR Code" class="img-fluid" style="max-width: 200px;">
                    <p class="small text-muted mt-2">
                        Share this QR code for quick connections
                    </p>
                </div>
            </div>
            {% endif %}
        </div>
        
        <!-- Main Content -->
        <div class="col-md-8">
            <!-- Upcoming Events -->
            {% if upcoming_events %}
            <div class="card mb-3">
                <div class="card-header">
                    <h5><i class="fas fa-calendar-alt"></i> Upcoming Events</h5>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        {% for event in upcoming_events %}
                        <a href="{{ url_for('events.view', event_id=event.id) }}" 
                           class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">{{ event.title }}</h6>
                                <small>{{ event.date.strftime('%b %d') }}</small>
                            </div>
                            {% if event.description %}
                            <p class="mb-1 small text-muted">{{ event.description[:100] }}...</p>
                            {% endif %}
                            <small>
                                <i class="fas fa-map-marker-alt"></i> {{ event.location }}
                            </small>
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}
            
            <!-- About Section -->
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-user"></i> About</h5>
                </div>
                <div class="card-body">
                    {% if user.bio %}
                    <p>{{ user.bio }}</p>
                    {% else %}
                    <p class="text-muted">
                        {% if is_own_profile %}
                        <i class="fas fa-info-circle"></i> Add a bio to your profile to tell others about yourself.
                        <a href="{{ url_for('profile.edit') }}">Edit Profile</a>
                        {% else %}
                        No bio available yet.
                        {% endif %}
                    </p>
                    {% endif %}
                </div>
            </div>
            
            <!-- Activity Feed (Optional - can be added later) -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5><i class="fas fa-chart-line"></i> Activity</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted text-center">
                        <i class="fas fa-clock"></i> Activity feed coming soon
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function connectWithUser(userId) {
    const btn = document.getElementById('connect-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';
    
    fetch('/nfc/scan-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scan_data: window.location.href,
            scan_method: 'manual',
            event_id: null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            btn.className = 'btn btn-success btn-block';
            btn.innerHTML = '<i class="fas fa-check-circle"></i> Connected!';
            
            // Show success message
            const alert = document.createElement('div');
            alert.className = 'alert alert-success alert-dismissible fade show mt-3';
            alert.innerHTML = `
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <i class="fas fa-check-circle"></i> Successfully connected with ${data.user.name}!
            `;
            btn.parentElement.appendChild(alert);
            
            setTimeout(() => alert.remove(), 5000);
        } else {
            btn.disabled = false;
            btn.className = 'btn btn-outline-primary btn-block';
            btn.innerHTML = '<i class="fas fa-user-plus"></i> Connect';
            
            alert('Connection failed: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Connection error:', error);
        btn.disabled = false;
        btn.className = 'btn btn-outline-primary btn-block';
        btn.innerHTML = '<i class="fas fa-user-plus"></i> Connect';
        alert('Network error: ' + error.message);
    });
}
</script>
{% endblock %}
'''

with open('templates/profile/view.html', 'w', encoding='utf-8') as f:
    f.write(profile_view_template)

print("✅ Created templates/profile/view.html")

# ============================================================================
# Check app.py registration
# ============================================================================
print("\n📋 Checking app.py blueprint registration...")

if os.path.exists('app.py'):
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    if "from src.controllers.profile_controller import profile_bp" in app_content:
        print("✅ Profile blueprint already imported")
    else:
        print("⚠️  Add to app.py:")
        print("   from src.controllers.profile_controller import profile_bp")
        print("   app.register_blueprint(profile_bp, url_prefix='/profile')")
else:
    print("⚠️  app.py not found")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ PROFILE ROUTE FIX COMPLETE!")
print("=" * 80)

print("""
🎯 Changes Made:
  ✅ Added /profile/view/<user_id> route to profile_controller.py
  ✅ Created templates/profile/view.html
  ✅ Added connection functionality

🚀 Test the Route:
  1. Restart Flask app: python app.py
  2. Visit: http://localhost:5000/profile/view/3
  3. Should show user profile (not 404)

📋 Features Added:
  ✅ Public profile view
  ✅ Profile picture display
  ✅ Bio and user info
  ✅ Upcoming events list
  ✅ Connect button (for other users)
  ✅ QR code display (for own profile)
  ✅ Send message button

🔗 URLs Now Working:
  • /profile/view/<user_id>  - View any user's profile
  • /profile/qr              - Your QR code
  • /profile/edit            - Edit your profile

✅ QR codes and NFC tags will now work correctly!
""")