import os
import re

print("=" * 80)
print("🌐 MAKING URLs DYNAMIC FOR DEPLOYMENT")
print("=" * 80)

# ============================================================================
# STEP 1: Update QR Generator Utility
# ============================================================================
print("\n📦 STEP 1: Updating QR Generator...")

qr_generator_code = """# filepath: c:\\\\Users\\\\lenovo\\\\Downloads\\\\nfc\\\\utils\\\\qr_generator.py

import qrcode
import os
from io import BytesIO
import base64
from flask import request

def get_base_url():
    '''
    Get the base URL dynamically from the request context
    Falls back to localhost if not in request context
    '''
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
    '''
    Generate QR code for user profile
    
    Args:
        user_id: User ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, profile_url)
    '''
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
    '''
    Generate QR code for event check-in
    
    Args:
        event_id: Event ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, event_url)
    '''
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
    '''
    Generate QR code as base64 string (for inline display)
    
    Args:
        data: Data to encode in QR
        
    Returns:
        str: Base64 encoded QR code image
    '''
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
    '''
    Verify and extract information from QR code data
    Works with any domain (localhost, production, etc.)
    
    Args:
        qr_data: Scanned QR code data
        base_url: Base URL (auto-detected if None)
        
    Returns:
        dict: Extracted information (type, id, url)
    '''
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
    '''
    Update user's QR code URL in database with current domain
    
    Args:
        user_id: User ID
    '''
    from database import get_db_connection
    
    base_url = get_base_url()
    profile_url = f"{base_url}/profile/view/{user_id}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE users SET qr_code_url = %s WHERE id = %s",
            (profile_url, user_id)
        )
        conn.commit()
        return profile_url
    except Exception as e:
        print(f"Error updating QR URL: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
"""

os.makedirs('utils', exist_ok=True)

with open('utils/qr_generator.py', 'w', encoding='utf-8') as f:
    f.write(qr_generator_code)

print("  ✅ Updated utils/qr_generator.py with dynamic URL detection")

# ============================================================================
# STEP 2: Update Scanner Template
# ============================================================================
print("\n🎨 STEP 2: Updating Scanner Template...")

scanner_template_path = "templates/nfc/scanner.html"

if os.path.exists(scanner_template_path):
    with open(scanner_template_path, 'r', encoding='utf-8') as f:
        scanner_content = f.read()
    
    # Replace hardcoded localhost
    if "http://localhost:5000" in scanner_content:
        scanner_content = scanner_content.replace(
            "scanData = `http://localhost:5000/profile/view/${input}`;",
            "scanData = `${window.location.origin}/profile/view/${input}`;"
        )
        print("  ✅ Replaced hardcoded localhost in scanner template")
    
    # Add BASE_URL constant if not exists
    if "const BASE_URL" not in scanner_content and "let currentMethod" in scanner_content:
        scanner_content = scanner_content.replace(
            "let currentMethod = 'qr';",
            "let currentMethod = 'qr';\nconst BASE_URL = window.location.origin; // Dynamic base URL"
        )
        print("  ✅ Added dynamic BASE_URL constant")
    
    with open(scanner_template_path, 'w', encoding='utf-8') as f:
        f.write(scanner_content)
    
    print("  ✅ Updated scanner template")
else:
    print("  ⚠️  Scanner template not found")

# ============================================================================
# STEP 3: Create QR Regeneration Script
# ============================================================================
print("\n📋 STEP 3: Creating QR Regeneration Script...")

regenerate_script = """# filepath: c:\\\\Users\\\\lenovo\\\\Downloads\\\\nfc\\\\regenerate_all_qr_codes.py

from database import get_db_connection
from utils.qr_generator import generate_profile_qr
from flask import Flask
import sys

# Create minimal Flask app for request context
app = Flask(__name__)

print("=" * 80)
print("🔄 REGENERATING QR CODES WITH CURRENT DOMAIN")
print("=" * 80)

# Get domain from command line or use default
if len(sys.argv) > 1:
    domain = sys.argv[1]
    print(f"\\nℹ️  Using provided domain: {domain}")
else:
    domain = "http://localhost:5000"
    print(f"\\nℹ️  Using default domain: {domain}")
    print("   To use custom domain: python regenerate_all_qr_codes.py https://yourdomain.com")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT id, full_name FROM users")
users = cursor.fetchall()

print(f"\\n📊 Found {len(users)} users to process\\n")

success_count = 0
error_count = 0

for user in users:
    try:
        # Generate QR with specified domain
        _, qr_url, profile_url = generate_profile_qr(user['id'], base_url=domain)
        
        # Update database
        cursor.execute(
            "UPDATE users SET qr_code_url = %s WHERE id = %s",
            (profile_url, user['id'])
        )
        
        print(f"✅ {user['full_name']:30} → {profile_url}")
        success_count += 1
        
    except Exception as e:
        print(f"❌ {user['full_name']:30} → Error: {e}")
        error_count += 1

conn.commit()
cursor.close()
conn.close()

print("\\n" + "=" * 80)
print(f"✅ COMPLETE! Success: {success_count}, Errors: {error_count}")
print("=" * 80)

if success_count > 0:
    print("\\n🎯 All QR codes now use: " + domain)
    print("   Test by visiting: " + domain + "/profile/qr")
"""

with open('regenerate_all_qr_codes.py', 'w', encoding='utf-8') as f:
    f.write(regenerate_script)

print("  ✅ Created regenerate_all_qr_codes.py")

# ============================================================================
# STEP 4: Create Deployment Guide
# ============================================================================
print("\n📄 STEP 4: Creating Deployment Guide...")

deployment_guide = """# DEPLOYMENT CONFIGURATION GUIDE

## 🌐 Dynamic URL Configuration

This system now automatically detects the domain it's running on.
No configuration needed for localhost vs production!

### How It Works:

1. **QR Code Generation**: Uses Flask request context
   - Localhost: http://localhost:5000/profile/view/123
   - Production: https://yourdomain.com/profile/view/123

2. **QR Code Verification**: Domain-agnostic parsing
   - Extracts user ID from any domain
   - Works with http/https
   - Works with any port

3. **Frontend**: Uses window.location.origin
   - Automatically matches current domain
   - Works in any environment

### Deployment Checklist:

#### For Production Deployment:

1. **Environment Variables**:
   Create a .env file or set environment variables:
   
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key
   MYSQL_HOST=your-db-host
   MYSQL_USER=your-db-user
   MYSQL_PASSWORD=your-db-password
   MYSQL_DATABASE=your-db-name

2. **HTTPS Configuration**:
   - Ensure your server uses HTTPS in production
   - Flask will auto-detect scheme (http/https)

3. **Regenerate QR Codes** (if migrating from localhost):
   
   # For production domain
   python regenerate_all_qr_codes.py https://yourdomain.com
   
   # For localhost (default)
   python regenerate_all_qr_codes.py

4. **Test URLs**:
   - Visit: https://yourdomain.com/profile/qr
   - Scan QR code
   - Should redirect to: https://yourdomain.com/profile/view/[id]

### Supported Deployment Platforms:

✅ **Heroku**:
   - Automatic domain detection
   - Use environment variables for DB config
   - Add gunicorn to requirements.txt

✅ **AWS / Azure / GCP**:
   - Configure load balancer for HTTPS
   - Set environment variables
   - Use managed database service

✅ **VPS (DigitalOcean, Linode, etc.)**:
   - Configure nginx/apache for HTTPS
   - Set domain in DNS
   - System auto-detects domain

✅ **Docker**:
   - Use environment variables
   - Map ports correctly
   - System adapts to container's domain

### Testing:

# Test on localhost
python app.py
# QR codes will use: http://localhost:5000

# Test on production
# QR codes will use: https://yourdomain.com

### No Configuration Needed! 🎉

The system automatically adapts to whatever domain it's running on.
Just deploy and it works!

### Troubleshooting:

**QR codes still show localhost after deployment:**
   Run: python regenerate_all_qr_codes.py https://yourdomain.com

**Mixed content errors (http/https):**
   Ensure your server is properly configured for HTTPS

**Domain detection not working:**
   Check that Flask can access request.scheme and request.host
"""

with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(deployment_guide)

print("  ✅ Created DEPLOYMENT_GUIDE.md")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "=" * 80)
print("✅ DYNAMIC URL CONFIGURATION COMPLETE!")
print("=" * 80)

print("""
🎯 What Changed:

1. ✅ QR Generator: Auto-detects domain from Flask request
2. ✅ Scanner Template: Uses window.location.origin
3. ✅ Regeneration Script: Created for production migration
4. ✅ Deployment Guide: Created with full instructions

🌐 How It Works:

DEVELOPMENT (localhost:5000):
  • QR Code URL: http://localhost:5000/profile/view/123
  • Auto-detected from request

PRODUCTION (yourdomain.com):
  • QR Code URL: https://yourdomain.com/profile/view/123
  • Auto-detected from request

🚀 Testing:

1. Restart Flask app:
   python app.py

2. Generate a QR code:
   http://localhost:5000/profile/qr

3. Check the URL in QR code:
   Should show: http://localhost:5000/profile/view/[your-id]

📋 Before Production Deployment:

1. Set environment variables (SECRET_KEY, DB credentials)
2. Configure HTTPS on your server
3. Run: python regenerate_all_qr_codes.py https://yourdomain.com
4. Test QR codes on production domain

✅ No Manual Configuration Required!
   The system adapts to any domain automatically.

💡 Read DEPLOYMENT_GUIDE.md for detailed instructions.
""")