print("=" * 80)
print("🔍 CHECKING PROFILE DISPLAY ISSUES")
print("=" * 80)

# Check 1: Database - what fields exist in users table
print("\n1️⃣ CHECKING DATABASE SCHEMA")
print("-" * 80)

from database import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print("✅ Users table columns:")
    for col in columns:
        print(f"   • {col['Field']}: {col['Type']}")
    
    # Check sample user data
    cursor.execute("SELECT * FROM users LIMIT 1")
    sample_user = cursor.fetchone()
    
    if sample_user:
        print("\n📋 Sample user data:")
        for key, value in sample_user.items():
            if value:
                display_value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                print(f"   • {key}: {display_value}")
    
    cursor.close()
    conn.close()

# Check 2: Profile view template
print("\n\n2️⃣ CHECKING PROFILE VIEW TEMPLATE")
print("-" * 80)

view_template_path = 'templates/profile/view.html'
with open(view_template_path, 'r', encoding='utf-8') as f:
    template_content = f.read()

fields_to_check = ['bio', 'phone', 'location', 'company', 'job_title', 'linkedin', 'twitter', 'website']

print("✅ Profile fields in template:")
for field in fields_to_check:
    if field in template_content:
        print(f"   ✅ {field}")
    else:
        print(f"   ❌ {field} - MISSING")

# Check 3: Profile controller - view_user_profile route
print("\n\n3️⃣ CHECKING PROFILE CONTROLLER")
print("-" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    controller_content = f.read()

if 'def view_user_profile' in controller_content:
    print("✅ view_user_profile route exists")
    
    # Check if it fetches all user data
    if 'SELECT * FROM users' in controller_content:
        print("   ✅ Fetches all user columns")
    else:
        print("   ⚠️ Might not fetch all columns")
else:
    print("❌ view_user_profile route NOT found")

print("\n\n" + "=" * 80)
print("🔧 CREATING COMPLETE PROFILE VIEW")
print("=" * 80)

# Now let's create/update the profile view template
complete_profile_template = '''{% extends "base.html" %}

{% block title %}{{ user.full_name }} - Profile{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Left Column - Profile Card -->
        <div class="col-md-4">
            <div class="card shadow mb-4">
                <div class="card-body text-center">
                    <!-- Profile Photo -->
                    {% if user.profile_photo %}
                    <img src="{{ url_for('static', filename=user.profile_photo) }}" 
                         class="rounded-circle mb-3" 
                         style="width: 150px; height: 150px; object-fit: cover;" 
                         alt="Profile Photo">
                    {% else %}
                    <div class="rounded-circle bg-primary text-white d-inline-flex align-items-center justify-content-center mb-3" 
                         style="width: 150px; height: 150px; font-size: 48px;">
                        {{ user.full_name[0].upper() }}
                    </div>
                    {% endif %}
                    
                    <!-- Name & Role -->
                    <h4 class="mb-1">{{ user.full_name }}</h4>
                    {% if user.job_title %}
                    <p class="text-muted mb-1">{{ user.job_title }}</p>
                    {% endif %}
                    {% if user.company %}
                    <p class="text-muted mb-3">@ {{ user.company }}</p>
                    {% endif %}
                    
                    <!-- Location -->
                    {% if user.location %}
                    <p class="mb-2">
                        <i class="fas fa-map-marker-alt me-2"></i>{{ user.location }}
                    </p>
                    {% endif %}
                    
                    <!-- Verification Badge -->
                    {% if user.has_verified_qualification %}
                    <span class="badge bg-success mb-3">
                        <i class="fas fa-check-circle"></i> Verified Professional
                    </span>
                    {% endif %}
                    
                    <!-- Action Buttons -->
                    <div class="d-grid gap-2 mt-3">
                        {% if session.user_id == user.id %}
                        <a href="{{ url_for('profile.edit_profile') }}" class="btn btn-primary">
                            <i class="fas fa-edit me-2"></i>Edit Profile
                        </a>
                        <a href="{{ url_for('profile.qualifications') }}" class="btn btn-outline-primary">
                            <i class="fas fa-certificate me-2"></i>My Qualifications
                        </a>
                        {% else %}
                        <button class="btn btn-primary" onclick="followUser({{ user.id }})">
                            <i class="fas fa-user-plus me-2"></i>Follow
                        </button>
                        <a href="{{ url_for('messages.compose', recipient_id=user.id) }}" class="btn btn-outline-primary">
                            <i class="fas fa-envelope me-2"></i>Message
                        </a>
                        {% endif %}
                    </div>
                    
                    <!-- Stats -->
                    <div class="row text-center mt-4">
                        <div class="col-4">
                            <h5 class="mb-0">{{ followers_count }}</h5>
                            <small class="text-muted">Followers</small>
                        </div>
                        <div class="col-4">
                            <h5 class="mb-0">{{ following_count }}</h5>
                            <small class="text-muted">Following</small>
                        </div>
                        <div class="col-4">
                            <h5 class="mb-0">{{ events_count }}</h5>
                            <small class="text-muted">Events</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Contact Info Card -->
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-address-card me-2"></i>Contact Information</h6>
                </div>
                <div class="card-body">
                    <div class="mb-2">
                        <i class="fas fa-envelope me-2 text-primary"></i>
                        <a href="mailto:{{ user.email }}">{{ user.email }}</a>
                    </div>
                    
                    {% if user.phone %}
                    <div class="mb-2">
                        <i class="fas fa-phone me-2 text-primary"></i>
                        <a href="tel:{{ user.phone }}">{{ user.phone }}</a>
                    </div>
                    {% endif %}
                    
                    {% if user.website %}
                    <div class="mb-2">
                        <i class="fas fa-globe me-2 text-primary"></i>
                        <a href="{{ user.website }}" target="_blank">Website</a>
                    </div>
                    {% endif %}
                    
                    {% if user.linkedin %}
                    <div class="mb-2">
                        <i class="fab fa-linkedin me-2 text-primary"></i>
                        <a href="{{ user.linkedin }}" target="_blank">LinkedIn</a>
                    </div>
                    {% endif %}
                    
                    {% if user.twitter %}
                    <div class="mb-2">
                        <i class="fab fa-twitter me-2 text-primary"></i>
                        <a href="{{ user.twitter }}" target="_blank">Twitter</a>
                    </div>
                    {% endif %}
                </div>
            </div>
            
            <!-- QR Code Card -->
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-qrcode me-2"></i>My QR Code</h6>
                </div>
                <div class="card-body text-center">
                    <img src="data:image/png;base64,{{ qr_code_base64 }}" 
                         class="img-fluid" 
                         alt="QR Code"
                         style="max-width: 200px;">
                    <p class="text-muted small mt-2">Scan to view profile</p>
                </div>
            </div>
        </div>
        
        <!-- Right Column - Content -->
        <div class="col-md-8">
            
            <!-- Bio Section -->
            {% if user.bio %}
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-user me-2"></i>About</h6>
                </div>
                <div class="card-body">
                    <p class="mb-0">{{ user.bio }}</p>
                </div>
            </div>
            {% endif %}
            
            <!-- Qualifications Section -->
            {% if qualifications %}
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-graduation-cap me-2"></i>Qualifications</h6>
                </div>
                <div class="card-body">
                    {% for qual in qualifications %}
                    <div class="mb-3 pb-3 {% if not loop.last %}border-bottom{% endif %}">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="mb-1">
                                    {{ qual.qualification_type|title }} in {{ qual.field_of_study }}
                                </h6>
                                <p class="text-muted mb-1">{{ qual.institution }} • {{ qual.year_obtained }}</p>
                            </div>
                            {% if qual.verification_status == 'verified' %}
                            <span class="badge bg-success">
                                <i class="fas fa-check-circle"></i> Verified
                            </span>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Skills Section -->
            {% if user.skills %}
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-tools me-2"></i>Skills</h6>
                </div>
                <div class="card-body">
                    {% set skills_list = user.skills.split(',') %}
                    {% for skill in skills_list %}
                    <span class="badge bg-secondary me-2 mb-2">{{ skill.strip() }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Interests Section -->
            {% if user.interests %}
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-heart me-2"></i>Interests</h6>
                </div>
                <div class="card-body">
                    {% set interests_list = user.interests.split(',') %}
                    {% for interest in interests_list %}
                    <span class="badge bg-info me-2 mb-2">{{ interest.strip() }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Recent Activity / Posts (if implemented) -->
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-clock me-2"></i>Recent Activity</h6>
                </div>
                <div class="card-body">
                    <p class="text-muted">Member since {{ user.created_at.strftime('%B %Y') }}</p>
                </div>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
'''

with open(view_template_path, 'w', encoding='utf-8') as f:
    f.write(complete_profile_template)

print("✅ Created complete profile view template!")
print("\n📋 Now displays:")
print("   ✅ Profile photo")
print("   ✅ Bio")
print("   ✅ Job title & company")
print("   ✅ Location")
print("   ✅ Phone, email, website")
print("   ✅ Social links (LinkedIn, Twitter)")
print("   ✅ QR code")
print("   ✅ Qualifications with verification badges")
print("   ✅ Skills & interests")
print("   ✅ Follower stats")

print("\n🔄 Restart Flask and visit profile page to see all information!")