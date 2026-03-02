import os

print("=" * 80)
print("🔍 CHECKING PROFILE URL & NFC DATA FEATURE")
print("=" * 80)

# Check 1: Profile controller
print("\n1️⃣ Checking profile controller...")
profile_controller_path = 'src/controllers/profile_controller.py'

if os.path.exists(profile_controller_path):
    with open(profile_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'request.host_url' in content or 'request.url_root' in content:
        print("   ✅ Profile controller generates dynamic URLs")
    else:
        print("   ⚠️  Profile controller may not generate dynamic URLs")
    
    if 'qr_code' in content or 'qrcode' in content:
        print("   ✅ Profile has QR code generation")
    else:
        print("   ❌ Profile missing QR code generation")
else:
    print(f"   ❌ {profile_controller_path} not found")

# Check 2: Profile template
print("\n2️⃣ Checking profile template...")
profile_template_path = 'templates/profile/view.html'

if os.path.exists(profile_template_path):
    with open(profile_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'profile_url' in content or 'shareable' in content:
        print("   ✅ Profile template shows shareable URL")
    else:
        print("   ⚠️  Profile template may not show shareable URL")
    
    if 'qr' in content.lower():
        print("   ✅ Profile template shows QR code")
    else:
        print("   ❌ Profile template missing QR code display")
else:
    print(f"   ❌ {profile_template_path} not found")

# Check 3: NFC data format
print("\n3️⃣ Checking NFC data format...")
nfc_controller_path = 'src/controllers/nfc_controller.py'

if os.path.exists(nfc_controller_path):
    with open(nfc_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'profile_url' in content or 'url_for' in content:
        print("   ✅ NFC controller uses profile URLs")
    else:
        print("   ⚠️  NFC controller may use simple IDs")

# Now let's create/update the complete feature
print("\n" + "=" * 80)
print("🔧 ADDING COMPLETE PROFILE URL + NFC FEATURE")
print("=" * 80)

# Update profile controller to generate shareable URLs
print("\n📝 Updating profile controller...")

profile_fix = '''
# Add this to your profile view function

from flask import request, url_for

# In the view_user_profile function, add:
profile_url = request.url_root.rstrip('/') + url_for('profile.view_user_profile', user_id=user['id'])
nfc_data = f"USER:{user['id']}|URL:{profile_url}"

# Generate QR code with the profile URL
import qrcode
from io import BytesIO
import base64

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(profile_url)  # Use full URL
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
buffer = BytesIO()
img.save(buffer, format='PNG')
qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

# Pass to template:
# profile_url=profile_url, nfc_data=nfc_data, qr_code=qr_code_base64
'''

with open('profile_url_implementation.txt', 'w', encoding='utf-8') as f:
    f.write(profile_fix)

print("   ✅ Created profile_url_implementation.txt with instructions")

# Create enhanced profile template
print("\n📝 Creating enhanced profile template snippet...")

profile_template_snippet = '''
<!-- Add this to your profile template -->

<div class="card mt-4">
    <div class="card-header">
        <h5><i class="fas fa-share-alt me-2"></i>Share Profile</h5>
    </div>
    <div class="card-body">
        <!-- Shareable URL -->
        <div class="mb-4">
            <label class="form-label">Your Profile URL</label>
            <div class="input-group">
                <input type="text" class="form-control" id="profile-url" 
                       value="{{ profile_url }}" readonly>
                <button class="btn btn-outline-secondary" onclick="copyProfileURL()">
                    <i class="fas fa-copy"></i> Copy
                </button>
            </div>
            <small class="text-muted">Share this link to connect with others</small>
        </div>

        <!-- QR Code -->
        <div class="text-center">
            <h6>Your QR Code</h6>
            <img src="data:image/png;base64,{{ qr_code }}" 
                 alt="Profile QR Code" 
                 class="img-fluid border rounded p-2"
                 style="max-width: 300px;">
            <p class="text-muted mt-2">
                <i class="fas fa-info-circle"></i> 
                Scan this code or tap your NFC-enabled device
            </p>
            <button class="btn btn-primary" onclick="downloadQR()">
                <i class="fas fa-download me-2"></i>Download QR Code
            </button>
        </div>

        <!-- NFC Data (hidden) -->
        <input type="hidden" id="nfc-data" value="{{ nfc_data }}">
    </div>
</div>

<script>
function copyProfileURL() {
    const urlInput = document.getElementById('profile-url');
    urlInput.select();
    document.execCommand('copy');
    alert('Profile URL copied to clipboard!');
}

function downloadQR() {
    const img = document.querySelector('img[alt="Profile QR Code"]');
    const link = document.createElement('a');
    link.download = 'my-profile-qr.png';
    link.href = img.src;
    link.click();
}

// NFC Write Function (if supported)
async function writeNFC() {
    if ('NDEFReader' in window) {
        try {
            const ndef = new NDEFWriter();
            const nfcData = document.getElementById('nfc-data').value;
            
            await ndef.write({
                records: [{ recordType: "text", data: nfcData }]
            });
            
            alert('NFC tag written successfully!');
        } catch (error) {
            console.error('NFC write error:', error);
            alert('Could not write to NFC tag: ' + error.message);
        }
    } else {
        alert('NFC not supported on this device');
    }
}
</script>
'''

with open('profile_template_snippet.html', 'w', encoding='utf-8') as f:
    f.write(profile_template_snippet)

print("   ✅ Created profile_template_snippet.html")

# Update scanner to handle both formats
print("\n📝 Updating scanner to handle URL and ID formats...")

scanner_update = '''
// Update the processScan function in scanner.html to handle both formats:

function processScan(scannedData, method) {
    let userId = null;
    
    // Format 1: Full URL (https://domain.com/profile/user/123)
    if (scannedData.includes('/profile/user/')) {
        userId = scannedData.split('/profile/user/')[1].split('?')[0];
    }
    // Format 2: USER:123|URL:...
    else if (scannedData.includes('USER:')) {
        const parts = scannedData.split('|');
        userId = parts[0].split('USER:')[1];
    }
    // Format 3: Just the ID
    else if (!isNaN(scannedData)) {
        userId = scannedData;
    }
    // Format 4: Try to extract ID from any URL
    else if (scannedData.includes('http')) {
        const match = scannedData.match(/\\/(\\d+)(?:\\?|$)/);
        if (match) userId = match[1];
    }
    
    if (!userId) {
        showScanResult('danger', 'Invalid scan data format');
        return;
    }
    
    // Rest of the processing code...
}
'''

with open('scanner_url_handling.js', 'w', encoding='utf-8') as f:
    f.write(scanner_update)

print("   ✅ Created scanner_url_handling.js")

print("\n" + "=" * 80)
print("✅ PROFILE URL FEATURE IMPLEMENTATION GUIDE CREATED!")
print("=" * 80)

print("\n📋 What the feature does:")
print("  ✅ Generates dynamic profile URL based on current domain")
print("  ✅ URL format: https://yourdomain.com/profile/user/123")
print("  ✅ QR code contains the full URL")
print("  ✅ NFC data contains: USER:123|URL:https://...")
print("  ✅ Scanner accepts: URL, USER:ID, or plain ID")
print("  ✅ Works on any domain (localhost, production, etc.)")

print("\n📁 Files created:")
print("  1. profile_url_implementation.txt - Backend code")
print("  2. profile_template_snippet.html - Frontend template")
print("  3. scanner_url_handling.js - Scanner updates")

print("\n🔧 To implement:")
print("  1. Add code from profile_url_implementation.txt to profile controller")
print("  2. Add HTML from profile_template_snippet.html to profile template")
print("  3. Update scanner processScan() with code from scanner_url_handling.js")

print("\n💡 The system will automatically:")
print("  - Use localhost:5000 during development")
print("  - Use your production domain when deployed")
print("  - Generate unique QR codes for each user")
print("  - Handle multiple scan formats")