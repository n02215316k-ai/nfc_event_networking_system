import os

print("=" * 80)
print("🎯 IMPROVING GUEST PROFILE VIEW EXPERIENCE")
print("=" * 80)

# ============================================================================
# Step 1: Update profile view template for better guest experience
# ============================================================================
print("\n🎨 Updating profile view template...")

profile_view_template = '''{% extends "base.html" %}

{% block title %}{{ user.full_name }} - Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Guest Alert Banner -->
    {% if not session.user_id %}
    <div class="alert alert-info alert-dismissible fade show" role="alert">
        <i class="fas fa-info-circle"></i> 
        <strong>Welcome!</strong> You're viewing this profile as a guest. 
        <a href="{{ url_for('auth.login') }}" class="alert-link">Login</a> or 
        <a href="{{ url_for('auth.register') }}" class="alert-link">Register</a> 
        to connect and send messages.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden>&times;</span>
        </button>
    </div>
    {% endif %}
    
    <div class="row">
        <!-- Profile Card -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    {% if user.profile_picture %}
                    <img src="{{ url_for('static', filename=user.profile_picture) }}" 
                         class="rounded-circle mb-3" 
                         style="width: 150px; height: 150px; object-fit: cover;"
                         alt="{{ user.full_name }}">
                    {% else %}
                    <div class="rounded-circle bg-primary text-white mx-auto mb-3 d-flex align-items-center justify-content-center"
                         style="width: 150px; height: 150px; font-size: 60px;">
                        {{ user.full_name[0].upper() if user.full_name else 'U' }}
                    </div>
                    {% endif %}
                    
                    <h3>{{ user.full_name }}</h3>
                    
                    {% if not session.user_id or not is_own_profile %}
                    <p class="text-muted">
                        <i class="fas fa-envelope"></i> {{ user.email }}
                    </p>
                    {% endif %}
                    
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
                            <!-- Own Profile Actions -->
                            <a href="{{ url_for('profile.edit') }}" class="btn btn-primary btn-block">
                                <i class="fas fa-edit"></i> Edit Profile
                            </a>
                            <a href="{{ url_for('profile.qr_code') }}" class="btn btn-info btn-block">
                                <i class="fas fa-qrcode"></i> My QR Code
                            </a>
                        {% elif session.user_id %}
                            <!-- Logged In User Actions -->
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
                                    class="btn btn-outline-primary btn-block" 
                                    id="connect-btn">
                                <i class="fas fa-user-plus"></i> Connect
                            </button>
                            {% endif %}
                        {% else %}
                            <!-- Guest User Actions -->
                            <div class="card bg-light mb-2">
                                <div class="card-body text-center py-3">
                                    <p class="mb-2">
                                        <i class="fas fa-lock"></i> 
                                        <strong>Connect with {{ user.full_name }}</strong>
                                    </p>
                                    <p class="small text-muted mb-3">
                                        Login or register to send messages and connect
                                    </p>
                                    <a href="{{ url_for('auth.login') }}?next={{ request.url }}" 
                                       class="btn btn-primary btn-sm">
                                        <i class="fas fa-sign-in-alt"></i> Login
                                    </a>
                                    <a href="{{ url_for('auth.register') }}?next={{ request.url }}" 
                                       class="btn btn-outline-primary btn-sm">
                                        <i class="fas fa-user-plus"></i> Register
                                    </a>
                                </div>
                            </div>
                            
                            <!-- Share Profile -->
                            <button onclick="shareProfile()" class="btn btn-outline-secondary btn-block">
                                <i class="fas fa-share-alt"></i> Share Profile
                            </button>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <!-- QR Code (Only for own profile) -->
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
                    <p class="text-muted text-center">
                        <i class="fas fa-info-circle"></i> 
                        {% if is_own_profile %}
                        Add a bio to your profile to tell others about yourself.
                        <a href="{{ url_for('profile.edit') }}">Edit Profile</a>
                        {% else %}
                        No bio available yet.
                        {% endif %}
                    </p>
                    {% endif %}
                </div>
            </div>
            
            <!-- Guest CTA (if not logged in) -->
            {% if not session.user_id %}
            <div class="card mt-3 border-primary">
                <div class="card-header bg-primary text-white">
                    <h5><i class="fas fa-star"></i> Join Our Network</h5>
                </div>
                <div class="card-body text-center">
                    <h5>Connect with {{ user.full_name }} and thousands of others</h5>
                    <p class="text-muted">
                        Create your profile, attend events, and build your professional network
                    </p>
                    <a href="{{ url_for('auth.register') }}?next={{ request.url }}" 
                       class="btn btn-primary btn-lg">
                        <i class="fas fa-rocket"></i> Get Started - It's Free!
                    </a>
                    <p class="mt-3 small">
                        Already have an account? 
                        <a href="{{ url_for('auth.login') }}?next={{ request.url }}">Login here</a>
                    </p>
                </div>
            </div>
            {% endif %}
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

function shareProfile() {
    const profileUrl = window.location.href;
    const userName = document.querySelector('h3').textContent;
    
    if (navigator.share) {
        navigator.share({
            title: userName + "'s Profile",
            text: 'Check out ' + userName + "'s profile",
            url: profileUrl
        }).then(() => {
            console.log('Shared successfully');
        }).catch(err => {
            console.error('Share failed:', err);
            copyToClipboard(profileUrl);
        });
    } else {
        copyToClipboard(profileUrl);
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Profile link copied to clipboard!');
    }).catch(err => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('Profile link copied to clipboard!');
    });
}
</script>
{% endblock %}
'''

os.makedirs('templates/profile', exist_ok=True)

with open('templates/profile/view.html', 'w', encoding='utf-8') as f:
    f.write(profile_view_template)

print("  ✅ Updated templates/profile/view.html with guest-friendly features")

# ============================================================================
# Step 2: Add analytics tracking for guest views
# ============================================================================
print("\n📊 Adding guest view tracking...")

tracking_code = """
# Add to profile_controller.py in view_user_profile function

# Track profile view
try:
    cursor.execute('''
        INSERT INTO profile_views (user_id, viewer_id, view_date, is_guest)
        VALUES (%s, %s, NOW(), %s)
    ''', (user_id, session.get('user_id'), not bool(session.get('user_id'))))
    conn.commit()
except:
    # Table might not exist yet - ignore for now
    pass
"""

print("  📝 Tracking code ready (optional feature)")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ GUEST PROFILE VIEW IMPROVED!")
print("=" * 80)

print("""
🎯 What Non-Logged-In Users Now See:

✅ FULL ACCESS TO:
  • User's profile picture
  • Name and bio
  • Upcoming events
  • Member since date

✅ HELPFUL PROMPTS:
  • Info banner explaining they're viewing as guest
  • Login/Register buttons prominently displayed
  • "Join Our Network" call-to-action card
  • Share profile button (works without login)

❌ DISABLED (Login Required):
  • Send Message button (shows "Login to Connect")
  • Connect button (shows login prompt)
  • View connection status

🎨 User Experience:

1. Guest scans QR/NFC → Profile loads ✅
2. Sees profile info clearly ✅
3. Blue banner: "Login or Register to connect" ✅
4. Can click Login (returns to profile after login) ✅
5. Can click Register (returns to profile after signup) ✅
6. Can share profile link ✅

🔗 Smart Redirects:
  • Login link includes: ?next=/profile/view/7
  • After login, returns to the profile they were viewing
  • Seamless experience!

🚀 Next Steps:
  1. Restart app: python app.py
  2. Test as guest: Open incognito window
  3. Visit: http://localhost:5000/profile/view/7
  4. See the improved guest experience!

📊 Optional: Add Profile View Tracking
  • Track how many guests view profiles
  • Track conversion: guest → registered user
  • Analytics for popular profiles
""")