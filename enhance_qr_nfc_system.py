import os
from database import get_db_connection

print("=" * 80)
print("🚀 ENHANCING QR/NFC SYSTEM")
print("=" * 80)

# ============================================================================
# PART 1: Database Schema Updates
# ============================================================================
print("\n📊 PART 1: Updating Database Schema")
print("-" * 80)

conn = get_db_connection()
cursor = conn.cursor()

try:
    # 1. Add qr_code_url to users table (if not exists)
    print("\n1. Checking users table...")
    cursor.execute("SHOW COLUMNS FROM users LIKE 'qr_code_url'")
    if not cursor.fetchone():
        print("  ✅ Adding qr_code_url column to users...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN qr_code_url VARCHAR(255) NULL AFTER profile_picture
        """)
        conn.commit()
        print("  ✅ Added qr_code_url column")
    else:
        print("  ℹ️  qr_code_url column already exists")
    
    # 2. Update scans table structure (enhance if needed)
    print("\n2. Checking scans table...")
    cursor.execute("SHOW COLUMNS FROM scans LIKE 'scan_data'")
    if not cursor.fetchone():
        print("  ✅ Adding scan_data column...")
        cursor.execute("""
            ALTER TABLE scans 
            ADD COLUMN scan_data TEXT NULL AFTER event_id,
            ADD COLUMN scan_method ENUM('nfc', 'qr', 'manual') DEFAULT 'manual' AFTER scan_data,
            ADD COLUMN scan_location VARCHAR(255) NULL AFTER scan_method
        """)
        conn.commit()
        print("  ✅ Enhanced scans table")
    else:
        print("  ℹ️  scans table already enhanced")
    
    # 3. Create scan_history table for detailed tracking
    print("\n3. Creating scan_history table...")
    cursor.execute("SHOW TABLES LIKE 'scan_history'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE scan_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scanner_id INT NOT NULL,
                scanned_user_id INT NOT NULL,
                scan_method ENUM('nfc', 'qr', 'manual') DEFAULT 'qr',
                scan_data TEXT NULL,
                profile_url VARCHAR(255) NULL,
                event_id INT NULL,
                scan_location VARCHAR(255) NULL,
                device_info VARCHAR(255) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (scanned_user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
                INDEX idx_scanner (scanner_id),
                INDEX idx_scanned (scanned_user_id),
                INDEX idx_created (created_at)
            )
        """)
        conn.commit()
        print("  ✅ Created scan_history table")
    else:
        print("  ℹ️  scan_history table already exists")
    
    print("\n✅ Database schema updated successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

# ============================================================================
# PART 2: Add QR Code Generation Utility
# ============================================================================
print("\n\n📦 PART 2: Creating QR Code Utility")
print("-" * 80)

qr_utility = '''
# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\utils\\qr_generator.py

import qrcode
import os
from io import BytesIO
import base64

def generate_profile_qr(user_id, base_url="http://localhost:5000"):
    """
    Generate QR code for user profile
    
    Args:
        user_id: User ID
        base_url: Base URL of the application
        
    Returns:
        tuple: (qr_code_path, qr_code_url)
    """
    # Create profile URL
    profile_url = f"{base_url}/profile/view/{user_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    qr_dir = "static/qr_codes"
    os.makedirs(qr_dir, exist_ok=True)
    
    filename = f"user_{user_id}_qr.png"
    filepath = os.path.join(qr_dir, filename)
    
    img.save(filepath)
    
    # Return both file path and URL path
    return filepath, f"/static/qr_codes/{filename}", profile_url


def generate_event_qr(event_id, base_url="http://localhost:5000"):
    """
    Generate QR code for event check-in
    
    Args:
        event_id: Event ID
        base_url: Base URL of the application
        
    Returns:
        tuple: (qr_code_path, qr_code_url, event_url)
    """
    # Create event URL
    event_url = f"{base_url}/events/{event_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(event_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    qr_dir = "static/qr_codes/events"
    os.makedirs(qr_dir, exist_ok=True)
    
    filename = f"event_{event_id}_qr.png"
    filepath = os.path.join(qr_dir, filename)
    
    img.save(filepath)
    
    return filepath, f"/static/qr_codes/events/{filename}", event_url


def generate_qr_base64(data):
    """
    Generate QR code as base64 string (for inline display)
    
    Args:
        data: Data to encode in QR
        
    Returns:
        str: Base64 encoded QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def verify_qr_data(qr_data, base_url="http://localhost:5000"):
    """
    Verify and extract information from QR code data
    
    Args:
        qr_data: Scanned QR code data
        base_url: Base URL of the application
        
    Returns:
        dict: Extracted information (type, id, url)
    """
    if not qr_data.startswith(base_url):
        return None
    
    # Remove base URL
    path = qr_data.replace(base_url, "")
    
    # Parse URL
    if "/profile/view/" in path:
        user_id = path.split("/profile/view/")[1].split("/")[0]
        return {
            'type': 'profile',
            'user_id': int(user_id),
            'url': qr_data
        }
    elif "/events/" in path:
        event_id = path.split("/events/")[1].split("/")[0]
        return {
            'type': 'event',
            'event_id': int(event_id),
            'url': qr_data
        }
    
    return None
'''

# Create utils directory
os.makedirs('utils', exist_ok=True)

with open('utils/qr_generator.py', 'w', encoding='utf-8') as f:
    f.write(qr_utility)

print("✅ Created utils/qr_generator.py")

# Create __init__.py
with open('utils/__init__.py', 'w', encoding='utf-8') as f:
    f.write("# Utils package\n")

print("✅ Created utils/__init__.py")

# ============================================================================
# PART 3: Enhance Profile Controller
# ============================================================================
print("\n\n📋 PART 3: Enhancing Profile Controller")
print("-" * 80)

profile_controller_path = "src/controllers/profile_controller.py"

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    profile_content = f.read()

# Add QR code routes
qr_routes = '''

# ============================================================================
# QR CODE ROUTES
# ============================================================================

@profile_bp.route('/qr-code')
@profile_bp.route('/qr')
def qr_code():
    """Display user's QR code"""
    if 'user_id' not in session:
        flash('Please login to view your QR code', 'error')
        return redirect(url_for('auth.login'))
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    # Generate QR code
    _, qr_url, profile_url = generate_profile_qr(session['user_id'])
    
    # Update user record with QR URL
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users SET qr_code_url = %s WHERE id = %s
    """, (profile_url, session['user_id']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return render_template('profile/qr_code.html',
                         qr_url=qr_url,
                         profile_url=profile_url)


@profile_bp.route('/generate-qr')
def generate_qr():
    """Generate/Regenerate QR code for user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    try:
        _, qr_url, profile_url = generate_profile_qr(session['user_id'])
        
        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET qr_code_url = %s WHERE id = %s
        """, (profile_url, session['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'qr_url': qr_url,
            'profile_url': profile_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/download-qr')
def download_qr():
    """Download QR code as image"""
    if 'user_id' not in session:
        flash('Please login', 'error')
        return redirect(url_for('auth.login'))
    
    from flask import send_file
    import os
    
    qr_path = f"static/qr_codes/user_{session['user_id']}_qr.png"
    
    if os.path.exists(qr_path):
        return send_file(qr_path, 
                        as_attachment=True,
                        download_name=f"my_profile_qr.png")
    else:
        flash('QR code not found. Generating...', 'info')
        return redirect(url_for('profile.qr_code'))
'''

# Check if QR routes already exist
if 'def qr_code(' not in profile_content:
    profile_content += qr_routes
    print("  ✅ Added QR code routes to profile_controller.py")
    
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.write(profile_content)
else:
    print("  ℹ️  QR code routes already exist")

# ============================================================================
# PART 4: Enhance NFC Controller
# ============================================================================
print("\n\n📋 PART 4: Enhancing NFC Controller")
print("-" * 80)

nfc_controller_path = "src/controllers/nfc_controller.py"

with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    nfc_content = f.read()

# Enhanced NFC routes
nfc_enhanced_routes = '''

# ============================================================================
# ENHANCED SCANNING ROUTES
# ============================================================================

@nfc_bp.route('/scan-profile', methods=['POST'])
def scan_profile():
    """Process QR/NFC scan of user profile"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from utils.qr_generator import verify_qr_data
    from database import get_db_connection
    
    data = request.get_json()
    scan_data = data.get('scan_data')
    scan_method = data.get('scan_method', 'qr')  # 'qr' or 'nfc'
    event_id = data.get('event_id')
    
    if not scan_data:
        return jsonify({'error': 'No scan data provided'}), 400
    
    # Verify QR data
    scan_info = verify_qr_data(scan_data)
    
    if not scan_info or scan_info['type'] != 'profile':
        return jsonify({'error': 'Invalid QR code'}), 400
    
    scanned_user_id = scan_info['user_id']
    
    # Prevent self-scan
    if scanned_user_id == session['user_id']:
        return jsonify({'error': 'Cannot scan your own profile'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get scanned user info
        cursor.execute("""
            SELECT id, full_name, email, profile_picture, institution, position
            FROM users WHERE id = %s
        """, (scanned_user_id,))
        
        scanned_user = cursor.fetchone()
        
        if not scanned_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Record scan in scan_history
        cursor.execute("""
            INSERT INTO scan_history 
            (scanner_id, scanned_user_id, scan_method, scan_data, 
             profile_url, event_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (session['user_id'], scanned_user_id, scan_method, 
              scan_data, scan_info['url'], event_id))
        
        scan_id = cursor.lastrowid
        
        # Also add to scans table for backwards compatibility
        cursor.execute("""
            INSERT INTO scans 
            (scanner_id, scanned_user_id, event_id, scan_data, scan_method, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (session['user_id'], scanned_user_id, event_id, scan_data, scan_method))
        
        # Create connection if doesn't exist
        cursor.execute("""
            SELECT id FROM connections 
            WHERE (user_id = %s AND connected_user_id = %s)
               OR (user_id = %s AND connected_user_id = %s)
        """, (session['user_id'], scanned_user_id, scanned_user_id, session['user_id']))
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO connections 
                (user_id, connected_user_id, connection_method, event_id, connected_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (session['user_id'], scanned_user_id, scan_method, event_id))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'scan_id': scan_id,
            'user': {
                'id': scanned_user['id'],
                'name': scanned_user['full_name'],
                'email': scanned_user['email'],
                'profile_picture': scanned_user['profile_picture'],
                'institution': scanned_user['institution'],
                'position': scanned_user['position'],
                'profile_url': scan_info['url']
            },
            'message': f'Successfully scanned {scanned_user["full_name"]}'
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@nfc_bp.route('/recent-scans')
def recent_scans():
    """View recent scans"""
    if 'user_id' not in session:
        flash('Please login to view scans', 'error')
        return redirect(url_for('auth.login'))
    
    from database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get recent scans with user details
    cursor.execute("""
        SELECT sh.*, 
               u.full_name, u.email, u.profile_picture, 
               u.institution, u.position,
               e.title as event_title
        FROM scan_history sh
        JOIN users u ON sh.scanned_user_id = u.id
        LEFT JOIN events e ON sh.event_id = e.id
        WHERE sh.scanner_id = %s
        ORDER BY sh.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    
    scans = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('nfc/recent_scans.html', scans=scans)


@nfc_bp.route('/scan-stats')
def scan_stats():
    """Get scan statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Total scans
    cursor.execute("""
        SELECT COUNT(*) as total FROM scan_history 
        WHERE scanner_id = %s
    """, (session['user_id'],))
    total = cursor.fetchone()['total']
    
    # Scans by method
    cursor.execute("""
        SELECT scan_method, COUNT(*) as count 
        FROM scan_history 
        WHERE scanner_id = %s
        GROUP BY scan_method
    """, (session['user_id'],))
    by_method = cursor.fetchall()
    
    # Recent scans (last 7 days)
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM scan_history 
        WHERE scanner_id = %s 
        AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    """, (session['user_id'],))
    recent = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': total,
        'by_method': by_method,
        'recent_7_days': recent
    })
'''

# Add enhanced routes if not exist
if 'def scan_profile(' not in nfc_content:
    nfc_content += nfc_enhanced_routes
    print("  ✅ Added enhanced scanning routes to nfc_controller.py")
    
    with open(nfc_controller_path, 'w', encoding='utf-8') as f:
        f.write(nfc_content)
else:
    print("  ℹ️  Enhanced scanning routes already exist")

# ============================================================================
# PART 5: Create Templates
# ============================================================================
print("\n\n🎨 PART 5: Creating/Updating Templates")
print("-" * 80)

# QR Code template
qr_code_template = '''{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4><i class="fas fa-qrcode"></i> My QR Code</h4>
                </div>
                <div class="card-body text-center">
                    <p class="lead">Share this QR code to connect with others!</p>
                    
                    <div class="my-4">
                        <img src="{{ qr_url }}" alt="My QR Code" class="img-fluid" style="max-width: 300px;">
                    </div>
                    
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        <strong>Profile URL:</strong><br>
                        <code>{{ profile_url }}</code>
                    </div>
                    
                    <div class="btn-group" role="group">
                        <a href="{{ url_for('profile.download_qr') }}" class="btn btn-success">
                            <i class="fas fa-download"></i> Download
                        </a>
                        <button onclick="regenerateQR()" class="btn btn-warning">
                            <i class="fas fa-sync"></i> Regenerate
                        </button>
                        <button onclick="shareQR()" class="btn btn-info">
                            <i class="fas fa-share"></i> Share
                        </button>
                    </div>
                    
                    <hr>
                    
                    <h5><i class="fas fa-mobile-alt"></i> How to Use</h5>
                    <div class="row text-left">
                        <div class="col-md-6">
                            <h6>For Others:</h6>
                            <ul>
                                <li>Scan this QR code with any QR scanner</li>
                                <li>It will open your profile</li>
                                <li>They can connect with you</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6>NFC Compatible:</h6>
                            <ul>
                                <li>Same URL works for NFC tags</li>
                                <li>Write URL to NFC tag</li>
                                <li>Tap phone to connect</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="text-center mt-3">
                <a href="{{ url_for('profile.my_profile') }}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Back to Profile
                </a>
                <a href="{{ url_for('nfc.scanner_page') }}" class="btn btn-primary">
                    <i class="fas fa-camera"></i> Scan Others
                </a>
            </div>
        </div>
    </div>
</div>

<script>
function regenerateQR() {
    fetch('/profile/generate-qr')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        });
}

function shareQR() {
    if (navigator.share) {
        navigator.share({
            title: 'My Profile',
            text: 'Connect with me!',
            url: '{{ profile_url }}'
        }).catch(err => console.error('Error sharing:', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText('{{ profile_url }}').then(() => {
            alert('Profile URL copied to clipboard!');
        });
    }
}
</script>
{% endblock %}
'''

os.makedirs('templates/profile', exist_ok=True)

with open('templates/profile/qr_code.html', 'w', encoding='utf-8') as f:
    f.write(qr_code_template)

print("  ✅ Created templates/profile/qr_code.html")

# Recent scans template
recent_scans_template = '''{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h4><i class="fas fa-history"></i> Recent Scans</h4>
        </div>
        <div class="card-body">
            {% if scans %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Person</th>
                            <th>Method</th>
                            <th>Event</th>
                            <th>When</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for scan in scans %}
                        <tr>
                            <td>
                                <a href="{{ scan.profile_url }}" class="text-decoration-none">
                                    {% if scan.profile_picture %}
                                    <img src="{{ url_for('static', filename=scan.profile_picture) }}" 
                                         class="rounded-circle" style="width: 30px; height: 30px;">
                                    {% else %}
                                    <div class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center"
                                         style="width: 30px; height: 30px;">
                                        {{ scan.full_name[0] if scan.full_name else 'U' }}
                                    </div>
                                    {% endif %}
                                    <strong>{{ scan.full_name }}</strong>
                                </a>
                                <br>
                                <small class="text-muted">
                                    {{ scan.position if scan.position else '' }}
                                    {{ ' @ ' + scan.institution if scan.institution else '' }}
                                </small>
                            </td>
                            <td>
                                {% if scan.scan_method == 'qr' %}
                                <span class="badge badge-info"><i class="fas fa-qrcode"></i> QR</span>
                                {% elif scan.scan_method == 'nfc' %}
                                <span class="badge badge-success"><i class="fas fa-wifi"></i> NFC</span>
                                {% else %}
                                <span class="badge badge-secondary"><i class="fas fa-hand-pointer"></i> Manual</span>
                                {% endif %}
                            </td>
                            <td>
                                {% if scan.event_title %}
                                <small>{{ scan.event_title }}</small>
                                {% else %}
                                <small class="text-muted">-</small>
                                {% endif %}
                            </td>
                            <td>
                                <small>{{ scan.created_at.strftime('%b %d, %Y %I:%M %p') }}</small>
                            </td>
                            <td>
                                <a href="{{ scan.profile_url }}" class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-user"></i> View
                                </a>
                                <a href="{{ url_for('messaging.compose') }}?recipient={{ scan.scanned_user_id }}" 
                                   class="btn btn-sm btn-outline-info">
                                    <i class="fas fa-envelope"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="text-center text-muted py-5">
                <i class="fas fa-qrcode fa-3x mb-3"></i>
                <h5>No Scans Yet</h5>
                <p>Start scanning QR codes or NFC tags to build your network!</p>
                <a href="{{ url_for('nfc.scanner_page') }}" class="btn btn-primary">
                    <i class="fas fa-camera"></i> Start Scanning
                </a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

os.makedirs('templates/nfc', exist_ok=True)

with open('templates/nfc/recent_scans.html', 'w', encoding='utf-8') as f:
    f.write(recent_scans_template)

print("  ✅ Created templates/nfc/recent_scans.html")

# Enhanced scanner page template
scanner_template = '''{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4><i class="fas fa-camera"></i> QR/NFC Scanner</h4>
                </div>
                <div class="card-body">
                    <div id="scanner-container" class="text-center mb-3">
                        <video id="qr-video" style="width: 100%; max-width: 500px; border: 2px solid #007bff; border-radius: 8px;"></video>
                    </div>
                    
                    <div class="form-group">
                        <label>Scan Method:</label>
                        <div class="btn-group btn-group-toggle d-flex" data-toggle="buttons">
                            <label class="btn btn-outline-primary active flex-fill">
                                <input type="radio" name="scan_method" value="qr" checked> 
                                <i class="fas fa-qrcode"></i> QR Code
                            </label>
                            <label class="btn btn-outline-success flex-fill">
                                <input type="radio" name="scan_method" value="nfc"> 
                                <i class="fas fa-wifi"></i> NFC
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Event (Optional):</label>
                        <select class="form-control" id="event-select">
                            <option value="">No Event</option>
                            {% for event in events %}
                            <option value="{{ event.id }}">{{ event.title }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div id="nfc-container" style="display: none;">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            <strong>NFC Mode:</strong> Bring your NFC-enabled device close to an NFC tag
                        </div>
                        <button onclick="startNFC()" class="btn btn-success btn-block">
                            <i class="fas fa-wifi"></i> Enable NFC Reading
                        </button>
                    </div>
                    
                    <div id="result-container" style="display: none;" class="alert alert-success mt-3">
                        <h5><i class="fas fa-check-circle"></i> Scan Successful!</h5>
                        <div id="scan-result"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5><i class="fas fa-info-circle"></i> Instructions</h5>
                </div>
                <div class="card-body">
                    <h6>QR Code Scanning:</h6>
                    <ol>
                        <li>Allow camera access</li>
                        <li>Point camera at QR code</li>
                        <li>Wait for automatic scan</li>
                    </ol>
                    
                    <hr>
                    
                    <h6>NFC Scanning:</h6>
                    <ol>
                        <li>Switch to NFC mode</li>
                        <li>Enable NFC on device</li>
                        <li>Tap NFC tag</li>
                    </ol>
                    
                    <hr>
                    
                    <div class="text-center">
                        <a href="{{ url_for('nfc.recent_scans') }}" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-history"></i> View Recent Scans
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="card mt-3">
                <div class="card-header bg-secondary text-white">
                    <h5><i class="fas fa-chart-bar"></i> Stats</h5>
                </div>
                <div class="card-body" id="stats-container">
                    <p class="text-center text-muted">Loading...</p>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/html5-qrcode"></script>
<script>
let html5QrCode = null;
let currentMethod = 'qr';

// Initialize QR Scanner
function initQRScanner() {
    html5QrCode = new Html5Qrcode("qr-video");
    
    html5QrCode.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        onScanSuccess,
        onScanError
    ).catch(err => {
        console.error("Error starting scanner:", err);
        alert("Camera access required for QR scanning");
    });
}

function onScanSuccess(decodedText, decodedResult) {
    // Stop scanning
    html5QrCode.stop();
    
    // Process scan
    processScan(decodedText, 'qr');
}

function onScanError(errorMessage) {
    // Ignore errors (happens frequently during scanning)
}

function processScan(scanData, method) {
    const eventId = document.getElementById('event-select').value;
    
    fetch('/nfc/scan-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scan_data: scanData,
            scan_method: method,
            event_id: eventId || null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayScanResult(data.user);
            loadStats();
        } else {
            alert('Error: ' + data.error);
            // Restart scanner
            setTimeout(() => initQRScanner(), 2000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Scan failed: ' + error);
        setTimeout(() => initQRScanner(), 2000);
    });
}

function displayScanResult(user) {
    const resultHTML = `
        <div class="media">
            ${user.profile_picture ? 
                `<img src="/static/${user.profile_picture}" class="mr-3 rounded-circle" style="width: 60px; height: 60px;">` :
                `<div class="mr-3 rounded-circle bg-primary text-white d-flex align-items-center justify-content-center" style="width: 60px; height: 60px; font-size: 24px;">${user.name[0]}</div>`
            }
            <div class="media-body">
                <h5>${user.name}</h5>
                <p class="mb-1">${user.position || ''} ${user.institution ? '@ ' + user.institution : ''}</p>
                <a href="${user.profile_url}" class="btn btn-sm btn-primary">View Profile</a>
                <a href="/messages/compose?recipient=${user.id}" class="btn btn-sm btn-info">Message</a>
            </div>
        </div>
    `;
    
    document.getElementById('scan-result').innerHTML = resultHTML;
    document.getElementById('result-container').style.display = 'block';
    
    // Restart scanner after 3 seconds
    setTimeout(() => {
        document.getElementById('result-container').style.display = 'none';
        initQRScanner();
    }, 3000);
}

// NFC Support
async function startNFC() {
    if ('NDEFReader' in window) {
        try {
            const ndef = new NDEFReader();
            await ndef.scan();
            
            ndef.addEventListener("reading", ({ message, serialNumber }) => {
                for (const record of message.records) {
                    if (record.recordType === "url") {
                        const decoder = new TextDecoder();
                        const url = decoder.decode(record.data);
                        processScan(url, 'nfc');
                    }
                }
            });
            
            alert('NFC scanning enabled. Tap an NFC tag.');
        } catch (error) {
            alert('NFC not available: ' + error);
        }
    } else {
        alert('NFC is not supported on this device/browser');
    }
}

// Scan method toggle
document.querySelectorAll('input[name="scan_method"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        currentMethod = e.target.value;
        
        if (currentMethod === 'qr') {
            document.getElementById('scanner-container').style.display = 'block';
            document.getElementById('nfc-container').style.display = 'none';
            initQRScanner();
        } else {
            document.getElementById('scanner-container').style.display = 'none';
            document.getElementById('nfc-container').style.display = 'block';
            if (html5QrCode) {
                html5QrCode.stop();
            }
        }
    });
});

// Load stats
function loadStats() {
    fetch('/nfc/scan-stats')
        .then(response => response.json())
        .then(data => {
            const statsHTML = `
                <div class="text-center">
                    <h3>${data.total}</h3>
                    <p class="text-muted">Total Scans</p>
                    <hr>
                    <p><i class="fas fa-qrcode"></i> QR: ${data.by_method.find(m => m.scan_method === 'qr')?.count || 0}</p>
                    <p><i class="fas fa-wifi"></i> NFC: ${data.by_method.find(m => m.scan_method === 'nfc')?.count || 0}</p>
                    <hr>
                    <p>Last 7 days: <strong>${data.recent_7_days}</strong></p>
                </div>
            `;
            document.getElementById('stats-container').innerHTML = statsHTML;
        });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initQRScanner();
    loadStats();
});
</script>
{% endblock %}
'''

with open('templates/nfc/scanner.html', 'w', encoding='utf-8') as f:
    f.write(scanner_template)

print("  ✅ Created/Updated templates/nfc/scanner.html")

# ============================================================================
# PART 6: Install Required Package
# ============================================================================
print("\n\n📦 PART 6: Required Python Packages")
print("-" * 80)

print("""
To complete the setup, install required packages:

    pip install qrcode[pil]

This package is needed for QR code generation.
""")

# ============================================================================
# PART 7: Generate QR codes for existing users
# ============================================================================
print("\n\n👥 PART 7: Generating QR Codes for Existing Users")
print("-" * 80)

generate_all_qr = '''
# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\generate_all_user_qr.py

from database import get_db_connection
from utils.qr_generator import generate_profile_qr

print("Generating QR codes for all users...")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT id, full_name FROM users")
users = cursor.fetchall()

for user in users:
    try:
        _, qr_url, profile_url = generate_profile_qr(user['id'])
        
        cursor.execute("""
            UPDATE users SET qr_code_url = %s WHERE id = %s
        """, (profile_url, user['id']))
        
        print(f"✅ Generated QR for: {user['full_name']} (ID: {user['id']})")
    except Exception as e:
        print(f"❌ Error for user {user['id']}: {e}")

conn.commit()
cursor.close()
conn.close()

print("\\n✅ Complete! All users now have QR codes.")
'''

with open('generate_all_user_qr.py', 'w', encoding='utf-8') as f:
    f.write(generate_all_qr)

print("  ✅ Created generate_all_user_qr.py")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "=" * 80)
print("✅ QR/NFC SYSTEM ENHANCEMENT COMPLETE!")
print("=" * 80)

print("""
📊 Summary of Changes:

DATABASE:
  ✅ Added qr_code_url to users table
  ✅ Enhanced scans table with scan_data, scan_method
  ✅ Created scan_history table for detailed tracking

CODE:
  ✅ Created utils/qr_generator.py (QR generation utility)
  ✅ Enhanced profile_controller.py (QR code routes)
  ✅ Enhanced nfc_controller.py (scanning routes)

TEMPLATES:
  ✅ Created profile/qr_code.html (display QR)
  ✅ Created nfc/scanner.html (enhanced scanner)
  ✅ Created nfc/recent_scans.html (scan history)

FEATURES:
  ✅ Unified QR/NFC data (URL to profile)
  ✅ Recent scans tracking with profile links
  ✅ QR code generation for all users
  ✅ Enhanced scanner with QR & NFC support
  ✅ Scan statistics and history
  ✅ Connection creation on scan

🎯 Next Steps:

1. Install required package:
   pip install qrcode[pil]

2. Generate QR codes for existing users:
   python generate_all_user_qr.py

3. Start the application:
   python app.py

4. Test the features:
   • Visit /profile/qr to see your QR code
   • Visit /nfc/scanner to scan others
   • Visit /nfc/recent-scans to see history

📱 QR Code URLs:
   Each QR code contains: http://localhost:5000/profile/view/<user_id>
   This works for both QR codes and NFC tags!

🔗 New Routes:
   /profile/qr                 - View your QR code
   /profile/generate-qr        - Regenerate QR code
   /profile/download-qr        - Download QR as image
   /nfc/scanner                - Enhanced scanner page
   /nfc/scan-profile           - Process scan (API)
   /nfc/recent-scans          - View scan history
   /nfc/scan-stats            - Get statistics (API)
""")

print("\n🚀 Run: python enhance_qr_nfc_system.py")
print("   Then: pip install qrcode[pil]")
print("   Then: python generate_all_user_qr.py")
print("   Then: python app.py")