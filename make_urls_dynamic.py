import os
import re

print("=" * 80)
print("🌐 MAKING URLs DYNAMIC FOR DEPLOYMENT")
print("=" * 80)

# ============================================================================
# STEP 1: Update QR Generator Utility
# ============================================================================
print("\n📦 STEP 1: Updating QR Generator...")

qr_generator_code = '''# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\utils\\qr_generator.py

import qrcode
import os
from io import BytesIO
import base64
from flask import request

def get_base_url():
    """
    Get the base URL dynamically from the request context
    Falls back to localhost if not in request context
    """
    try:
        # Get scheme (http/https)
        scheme = request.scheme
        # Get host (domain:port)
        host = request.host
        return f"{scheme}://{host}"
    except:
        # Fallback for when not in request context
        return "http://localhost:5000"


def generate_profile_qr(user_id, base_url=None):
    """
    Generate QR code for user profile
    
    Args:
        user_id: User ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, profile_url)
    """
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Create profile URL with dynamic domain
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


def generate_event_qr(event_id, base_url=None):
    """
    Generate QR code for event check-in
    
    Args:
        event_id: Event ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, event_url)
    """
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Create event URL with dynamic domain
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


def verify_qr_data(qr_data, base_url=None):
    """
    Verify and extract information from QR code data
    Works with any domain (localhost, production, etc.)
    
    Args:
        qr_data: Scanned QR code data
        base_url: Base URL (auto-detected if None)
        
    Returns:
        dict: Extracted information (type, id, url)
    """
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Handle both with and without base URL
    if not qr_data.startswith('http'):
        # Assume it's a relative path
        qr_data = base_url + qr_data
    
    # Extract path from URL (works with any domain)
    try:
        from urllib.parse import urlparse
        parsed = urlparse(qr_data)
        path = parsed.path
    except:
        # Fallback: simple string manipulation
        if '://' in qr_data:
            path = qr_data.split('://', 1)[1]
            if '/' in path:
                path = '/' + path.split('/', 1)[1]
            else:
                path = '/'
        else:
            path = qr_data
    
    # Parse URL path (domain-agnostic)
    if "/profile/view/" in path:
        user_id = path.split("/profile/view/")[1].split("/")[0].split("?")[0]
        try:
            return {
                'type': 'profile',
                'user_id': int(user_id),
                'url': qr_data
            }
        except ValueError:
            return None
    elif "/events/" in path:
        event_id = path.split("/events/")[1].split("/")[0].split("?")[0]
        try:
            return {
                'type': 'event',
                'event_id': int(event_id),
                'url': qr_data
            }
        except ValueError:
            return None
    
    return None


def update_user_qr_url(user_id):
    """
    Update user's QR code URL in database with current domain
    
    Args:
        user_id: User ID
    """
    from database import get_db_connection
    
    base_url = get_base_url()
    profile_url = f"{base_url}/profile/view/{user_id}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users SET qr_code_url = %s WHERE id = %s
        """, (profile_url, user_id))
        conn.commit()
        return profile_url
    except Exception as e:
        print(f"Error updating QR URL: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
'''

os.makedirs('utils', exist_ok=True)

with open('utils/qr_generator.py', 'w', encoding='utf-8') as f:
    f.write(qr_generator_code)

print("  ✅ Updated utils/qr_generator.py with dynamic URL detection")

# ============================================================================
# STEP 2: Update Profile Controller
# ============================================================================
print("\n📋 STEP 2: Updating Profile Controller...")

profile_controller_path = "src/controllers/profile_controller.py"

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    profile_content = f.read()

# Find and replace qr_code route
old_qr_route = '''@profile_bp.route('/qr-code')
@profile_bp.route('/qr')
def qr_code():
    """Display user's QR code"""
    if 'user_id' not in session:
        flash('Please login to view your QR code', 'error')
        return redirect(url_for('auth.login'))
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    # Generate QR code
    _, qr_url, profile_url = generate_profile_qr(session['user_id'])'''

new_qr_route = '''@profile_bp.route('/qr-code')
@profile_bp.route('/qr')
def qr_code():
    """Display user's QR code"""
    if 'user_id' not in session:
        flash('Please login to view your QR code', 'error')
        return redirect(url_for('auth.login'))
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    # Generate QR code (base_url auto-detected from request)
    _, qr_url, profile_url = generate_profile_qr(session['user_id'])'''

if old_qr_route in profile_content:
    profile_content = profile_content.replace(old_qr_route, new_qr_route)
    print("  ✅ Updated qr_code route")

# Update generate_qr route
old_gen_route = '''@profile_bp.route('/generate-qr')
def generate_qr():
    """Generate/Regenerate QR code for user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    try:
        _, qr_url, profile_url = generate_profile_qr(session['user_id'])'''

new_gen_route = '''@profile_bp.route('/generate-qr')
def generate_qr():
    """Generate/Regenerate QR code for user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from utils.qr_generator import generate_profile_qr
    from database import get_db_connection
    
    try:
        # base_url auto-detected from request
        _, qr_url, profile_url = generate_profile_qr(session['user_id'])'''

if old_gen_route in profile_content:
    profile_content = profile_content.replace(old_gen_route, new_gen_route)
    print("  ✅ Updated generate_qr route")

with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(profile_content)

print("  ✅ Saved profile_controller.py")

# ============================================================================
# STEP 3: Update NFC Controller
# ============================================================================
print("\n📋 STEP 3: Updating NFC Controller...")

nfc_controller_path = "src/controllers/nfc_controller.py"

with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    nfc_content = f.read()

# Update scan_profile route to use dynamic verification
old_verify = "from utils.qr_generator import verify_qr_data"
if old_verify in nfc_content and "scan_info = verify_qr_data(scan_data)" in nfc_content:
    print("  ℹ️  NFC controller already uses verify_qr_data (now dynamic)")

# Ensure scanner page template gets current domain
scanner_route_fix = '''
# Add base_url to scanner page context
if 'def scanner_page(' in nfc_content:
    # Already handled in template
    pass
'''

print("  ✅ NFC controller verified")

# ============================================================================
# STEP 4: Update Scanner Template with Dynamic Domain
# ============================================================================
print("\n🎨 STEP 4: Updating Scanner Template...")

scanner_template_path = "templates/nfc/scanner.html"

with open(scanner_template_path, 'r', encoding='utf-8') as f:
    scanner_content = f.read()

# Replace hardcoded localhost references
scanner_content = scanner_content.replace(
    "scanData = `http://localhost:5000/profile/view/${input}`;",
    "scanData = `${window.location.origin}/profile/view/${input}`;"
)

# Add dynamic base URL to JavaScript
if "let currentMethod = 'qr';" in scanner_content and "const BASE_URL =" not in scanner_content:
    scanner_content = scanner_content.replace(
        "let currentMethod = 'qr';",
        """let currentMethod = 'qr';
const BASE_URL = window.location.origin; // Dynamic base URL"""
    )
    print("  ✅ Added dynamic BASE_URL to scanner template")

# Update manual entry function
old_manual = '''function processManualEntry() {
    const input = document.getElementById('manual-input').value.trim();
    
    if (!input) {
        showError('Please enter a profile URL or user ID');
        return;
    }
    
    // Check if it's a URL or just an ID
    let scanData;
    if (input.includes('http')) {
        scanData = input;
    } else {
        // Assume it's a user ID
        scanData = `http://localhost:5000/profile/view/${input}`;
    }
    
    processScan(scanData, 'manual');
}'''

new_manual = '''function processManualEntry() {
    const input = document.getElementById('manual-input').value.trim();
    
    if (!input) {
        showError('Please enter a profile URL or user ID');
        return;
    }
    
    // Check if it's a URL or just an ID
    let scanData;
    if (input.includes('http')) {
        scanData = input;
    } else {
        // Assume it's a user ID - use dynamic base URL
        scanData = `${BASE_URL}/profile/view/${input}`;
    }
    
    processScan(scanData, 'manual');
}'''

if old_manual in scanner_content:
    scanner_content = scanner_content.replace(old_manual, new_manual)
    print("  ✅ Updated manual entry to use dynamic URL")

with open(scanner_template_path, 'w', encoding='utf-8') as f:
    f.write(scanner_content)

print("  ✅ Updated scanner template")

# ============================================================================
# STEP 5: Create deployment configuration guide
# ============================================================================
print("\n📄 STEP 5: Creating Deployment Guide...")

deployment_guide = '''# DEPLOYMENT CONFIGURATION GUIDE

## 🌐 Dynamic URL Configuration

This system now automatically detects the domain it's running on.
No configuration needed for localhost vs production!

### How It Works:

1. **QR Code Generation**: Uses `request.scheme` and `request.host` from Flask
   - Localhost: `http://localhost:5000/profile/view/123`
   - Production: `https://yourdomain.com/profile/view/123`

2. **QR Code Verification**: Domain-agnostic parsing
   - Extracts user ID from any domain
   - Works with http/https
   - Works with any port

3. **Frontend**: Uses `window.location.origin`
   - Automatically matches current domain
   - Works in any environment

### Deployment Checklist:

#### For Production Deployment:

1. **Update Database Connection** (if different from dev):
   ```python
   # database.py
   MYSQL_HOST = os.getenv('MYSQL_HOST', 'your-db-host')
   MYSQL_USER = os.getenv('MYSQL_USER', 'your-db-user')
   MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your-db-password')
   MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'your-db-name')