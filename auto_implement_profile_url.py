import os
import re

print("=" * 80)
print("🚀 AUTO-IMPLEMENTING PROFILE URL & NFC FEATURE")
print("=" * 80)

# ==================== STEP 1: Update Profile Controller ====================
print("\n1️⃣ Updating profile controller...")

profile_controller_path = 'src/controllers/profile_controller.py'

if os.path.exists(profile_controller_path):
    with open(profile_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already implemented
    if 'profile_url' in content and 'request.url_root' in content:
        print("   ✅ Profile URL feature already implemented")
    else:
        print("   🔧 Adding profile URL generation...")
        
        # Add imports at the top if not present
        if 'from io import BytesIO' not in content:
            content = content.replace(
                'import qrcode',
                'import qrcode\nfrom io import BytesIO\nimport base64'
            )
        
        # Find the view_user_profile function
        if 'def view_user_profile' in content:
            # Find where we return render_template
            pattern = r"(def view_user_profile.*?)(return render_template\('profile/view\.html')"
            
            url_generation_code = '''
    # Generate dynamic profile URL
    profile_url = request.url_root.rstrip('/') + url_for('profile.view_user_profile', user_id=user['id'])
    nfc_data = f"USER:{user['id']}|URL:{profile_url}"
    
    # Generate QR code with profile URL
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    '''
            
            # Insert before return render_template
            content = re.sub(
                pattern,
                r'\1' + url_generation_code + r'\2',
                content,
                flags=re.DOTALL
            )
            
            # Update render_template to include new variables
            content = content.replace(
                "return render_template('profile/view.html', user=user",
                "return render_template('profile/view.html', user=user, profile_url=profile_url, nfc_data=nfc_data, qr_code=qr_code_base64"
            )
            
            with open(profile_controller_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Profile controller updated!")
        else:
            print("   ⚠️  Could not find view_user_profile function")
else:
    print(f"   ❌ {profile_controller_path} not found")

# ==================== STEP 2: Update Profile Template ====================
print("\n2️⃣ Updating profile template...")

profile_template_path = 'templates/profile/view.html'

if os.path.exists(profile_template_path):
    with open(profile_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has share section
    if 'Share Profile' in content and 'profile-url' in content:
        print("   ✅ Profile template already has share section")
    else:
        print("   🔧 Adding share profile section...")
        
        share_section = '''
<!-- Share Profile Section -->
<div class="card mt-4">
    <div class="card-header">
        <h5 class="mb-0"><i class="fas fa-share-alt me-2"></i>Share Your Profile</h5>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-6">
                <!-- Shareable URL -->
                <div class="mb-3">
                    <label class="form-label fw-bold">Profile URL</label>
                    <div class="input-group">
                        <input type="text" class="form-control" id="profile-url" 
                               value="{{ profile_url }}" readonly>
                        <button class="btn btn-outline-primary" onclick="copyProfileURL()">
                            <i class="fas fa-copy"></i> Copy
                        </button>
                    </div>
                    <small class="text-muted">
                        <i class="fas fa-info-circle"></i> Share this link to connect with others
                    </small>
                </div>
                
                <!-- NFC Data (hidden) -->
                <input type="hidden" id="nfc-data" value="{{ nfc_data }}">
                
                <!-- NFC Write Button (if supported) -->
                <div class="d-grid gap-2">
                    <button class="btn btn-info" onclick="writeNFC()" id="nfc-write-btn">
                        <i class="fas fa-wifi me-2"></i>Write to NFC Tag
                    </button>
                </div>
            </div>
            
            <div class="col-md-6">
                <!-- QR Code -->
                <div class="text-center">
                    <h6 class="mb-3">Your QR Code</h6>
                    <img src="data:image/png;base64,{{ qr_code }}" 
                         alt="Profile QR Code" 
                         class="img-fluid border rounded shadow-sm p-2 bg-white"
                         style="max-width: 250px;">
                    <p class="text-muted mt-2 small">
                        <i class="fas fa-qrcode"></i> 
                        Scan to view profile or connect
                    </p>
                    <button class="btn btn-primary btn-sm" onclick="downloadQR()">
                        <i class="fas fa-download me-2"></i>Download QR Code
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Copy profile URL to clipboard
function copyProfileURL() {
    const urlInput = document.getElementById('profile-url');
    urlInput.select();
    urlInput.setSelectionRange(0, 99999); // For mobile
    
    try {
        document.execCommand('copy');
        alert('✅ Profile URL copied to clipboard!');
    } catch (err) {
        // Fallback for modern browsers
        navigator.clipboard.writeText(urlInput.value).then(() => {
            alert('✅ Profile URL copied to clipboard!');
        }).catch(() => {
            alert('❌ Could not copy to clipboard');
        });
    }
}

// Download QR code
function downloadQR() {
    const img = document.querySelector('img[alt="Profile QR Code"]');
    const link = document.createElement('a');
    link.download = 'profile-qr-code.png';
    link.href = img.src;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    alert('✅ QR code downloaded!');
}

// Write to NFC tag (if supported)
async function writeNFC() {
    const nfcBtn = document.getElementById('nfc-write-btn');
    
    if ('NDEFWriter' in window) {
        try {
            const ndef = new NDEFWriter();
            const nfcData = document.getElementById('nfc-data').value;
            
            nfcBtn.disabled = true;
            nfcBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Hold NFC tag near device...';
            
            await ndef.write({
                records: [{ recordType: "text", data: nfcData }]
            });
            
            nfcBtn.innerHTML = '<i class="fas fa-check me-2"></i>NFC Tag Written!';
            nfcBtn.classList.remove('btn-info');
            nfcBtn.classList.add('btn-success');
            
            setTimeout(() => {
                nfcBtn.disabled = false;
                nfcBtn.innerHTML = '<i class="fas fa-wifi me-2"></i>Write to NFC Tag';
                nfcBtn.classList.remove('btn-success');
                nfcBtn.classList.add('btn-info');
            }, 3000);
            
        } catch (error) {
            console.error('NFC write error:', error);
            nfcBtn.disabled = false;
            nfcBtn.innerHTML = '<i class="fas fa-wifi me-2"></i>Write to NFC Tag';
            alert('❌ Could not write to NFC tag: ' + error.message);
        }
    } else {
        alert('❌ NFC not supported on this device');
    }
}

// Check NFC support on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!('NDEFWriter' in window)) {
        const nfcBtn = document.getElementById('nfc-write-btn');
        nfcBtn.disabled = true;
        nfcBtn.innerHTML = '<i class="fas fa-times me-2"></i>NFC Not Supported';
        nfcBtn.title = 'Your device or browser does not support NFC writing';
    }
});
</script>
'''
        
        # Insert before {% endblock %}
        if '{% endblock %}' in content:
            content = content.replace('{% endblock %}', share_section + '\n{% endblock %}')
            
            with open(profile_template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Profile template updated!")
        else:
            print("   ⚠️  Could not find {% endblock %} in template")
else:
    print(f"   ❌ {profile_template_path} not found")

# ==================== STEP 3: Update Scanner ====================
print("\n3️⃣ Updating scanner to handle all URL formats...")

scanner_path = 'templates/nfc/scanner.html'

if os.path.exists(scanner_path):
    with open(scanner_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and update processScan function
    if 'function processScan' in content:
        # Replace the userId extraction logic
        old_pattern = r'(function processScan\(scannedData, method\) \{.*?let userId = null;.*?)(if \(!userId\))'
        
        new_extraction = '''
    // Extract user ID from multiple formats
    
    // Format 1: Full profile URL (http://domain.com/profile/user/123)
    if (scannedData.includes('/profile/user/')) {
        const match = scannedData.match(/\\/profile\\/user\\/(\\d+)/);
        if (match) userId = match[1];
    }
    // Format 2: NFC data format (USER:123|URL:...)
    else if (scannedData.includes('USER:')) {
        const parts = scannedData.split('|');
        userId = parts[0].replace('USER:', '').trim();
    }
    // Format 3: Simple numeric ID
    else if (!isNaN(scannedData)) {
        userId = scannedData;
    }
    // Format 4: Any URL containing /user/ or /profile/
    else if (scannedData.includes('http')) {
        const match = scannedData.match(/\\/(user|profile)\\/?(\\d+)/);
        if (match) userId = match[2];
    }
    // Format 5: Just extract any number
    else {
        const match = scannedData.match(/\\d+/);
        if (match) userId = match[0];
    }
    
    '''
        
        content = re.sub(old_pattern, r'\1' + new_extraction + r'\2', content, flags=re.DOTALL)
        
        with open(scanner_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Scanner updated to handle all URL formats!")
    else:
        print("   ⚠️  Could not find processScan function")
else:
    print(f"   ❌ {scanner_path} not found")

print("\n" + "=" * 80)
print("✅ AUTO-IMPLEMENTATION COMPLETE!")
print("=" * 80)

print("\n📋 What was implemented:")
print("  ✅ Dynamic profile URL generation (adapts to any domain)")
print("  ✅ QR code with embedded profile URL")
print("  ✅ NFC data format: USER:ID|URL:...")
print("  ✅ Copy URL to clipboard button")
print("  ✅ Download QR code button")
print("  ✅ Write to NFC tag button (if supported)")
print("  ✅ Scanner handles: URLs, USER:ID, plain IDs")

print("\n🎯 Features:")
print("  • Works on localhost:5000 (development)")
print("  • Works on any production domain")
print("  • QR codes are portable (contain full URL)")
print("  • NFC tags contain full profile data")
print("  • Scanner auto-detects format")

print("\n🔄 Restart Flask:")
print("  python app.py")

print("\n🧪 Test it:")
print("  1. Go to your profile page")
print("  2. Scroll down to 'Share Your Profile' section")
print("  3. See your dynamic URL and QR code")
print("  4. Copy URL or download QR code")
print("  5. Scan the QR code with scanner - should work!")

print("\n💡 The URL will automatically be:")
print("  • http://localhost:5000/profile/user/123 (development)")
print("  • https://yourdomain.com/profile/user/123 (production)")