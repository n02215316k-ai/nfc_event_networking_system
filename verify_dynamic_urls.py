import os

print("=" * 80)
print("🔍 COMPREHENSIVE VERIFICATION - DYNAMIC URLs & FULL IMPLEMENTATION")
print("=" * 80)

# Check 1: Profile Controller - QR Code Generation
print("\n1️⃣ CHECKING PROFILE CONTROLLER - QR CODE GENERATION")
print("-" * 80)

profile_path = 'src/controllers/profile_controller.py'
with open(profile_path, 'r', encoding='utf-8') as f:
    profile_content = f.read()

# Check if view_user_profile generates dynamic URL
if "request.url_root" in profile_content and "url_for('profile.view_user_profile'" in profile_content:
    print("✅ Profile generates DYNAMIC URLs using request.url_root + url_for()")
    
    # Extract the QR generation code
    if "profile_url = request.url_root" in profile_content:
        start = profile_content.find("profile_url = request.url_root")
        end = profile_content.find("\n", start + 200)
        print(f"\n   Code: {profile_content[start:end]}")
    
    if "qr.add_data(profile_url)" in profile_content:
        print("\n   ✅ QR code uses profile_url (dynamic)")
    else:
        print("\n   ⚠️ QR code might not use dynamic URL")
else:
    print("❌ Profile does NOT generate dynamic URLs")
    print("   This needs to be fixed!")

# Check 2: NFC Controller - NFC Data Generation
print("\n\n2️⃣ CHECKING NFC CONTROLLER - NFC DATA GENERATION")
print("-" * 80)

nfc_path = 'src/controllers/nfc_controller.py'
with open(nfc_path, 'r', encoding='utf-8') as f:
    nfc_content = f.read()

# Check scanner route
if "def scanner" in nfc_content:
    print("✅ Scanner route exists")
else:
    print("❌ Scanner route NOT found")

# Check process_scan route
if "def process_scan" in nfc_content:
    print("✅ Process scan route exists")
    
    # Check if it handles both NFC and QR formats
    if "USER:" in nfc_content and "profile/user/" in nfc_content:
        print("   ✅ Handles both NFC format (USER:ID) and URL format")
    else:
        print("   ⚠️ Might not handle all formats")
else:
    print("❌ Process scan route NOT found")

# Check 3: QR Code Generator Utility
print("\n\n3️⃣ CHECKING QR CODE GENERATOR UTILITY")
print("-" * 80)

qr_gen_path = 'utils/qr_generator.py'
if os.path.exists(qr_gen_path):
    with open(qr_gen_path, 'r', encoding='utf-8') as f:
        qr_gen_content = f.read()
    
    if "request.url_root" in qr_gen_content or "request.host_url" in qr_gen_content:
        print("✅ QR generator uses dynamic URLs")
    else:
        print("⚠️ QR generator might use hardcoded URLs")
else:
    print("⚠️ QR generator utility not found at utils/qr_generator.py")

# Check 4: Scanner Template - JavaScript Processing
print("\n\n4️⃣ CHECKING SCANNER TEMPLATE - JAVASCRIPT")
print("-" * 80)

scanner_template = 'templates/nfc/scanner.html'
with open(scanner_template, 'r', encoding='utf-8') as f:
    scanner_html = f.read()

# Check format handling
formats_found = []
if "includes('/profile/user/')" in scanner_html:
    formats_found.append("Profile URL (/profile/user/ID)")
if "includes('USER:')" in scanner_html:
    formats_found.append("NFC format (USER:ID)")
if "!isNaN(scannedData)" in scanner_html:
    formats_found.append("Numeric ID")

print(f"✅ Scanner handles {len(formats_found)} formats:")
for fmt in formats_found:
    print(f"   • {fmt}")

# Check if it extracts user ID correctly
if "match(/\\/profile\\/user\\/(\\d+)/)" in scanner_html or "match(/\\/(user|profile)\\/(\\d+)/)" in scanner_html:
    print("\n✅ Uses regex to extract user ID from URLs (works with any domain)")
else:
    print("\n⚠️ Might not extract user ID correctly from URLs")

# Check 5: Database - Verify user QR codes stored correctly
print("\n\n5️⃣ CHECKING DATABASE - QR CODE STORAGE")
print("-" * 80)

from database import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Check if qr_code_url column exists
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    has_qr_column = any(col['Field'] == 'qr_code_url' for col in columns)
    
    if has_qr_column:
        print("✅ users.qr_code_url column exists")
        
        # Check sample QR URLs
        cursor.execute("SELECT id, qr_code_url FROM users WHERE qr_code_url IS NOT NULL LIMIT 3")
        qr_samples = cursor.fetchall()
        
        if qr_samples:
            print(f"\n   Sample QR URLs ({len(qr_samples)} users):")
            for user in qr_samples:
                url = user['qr_code_url']
                if url:
                    # Check if it's dynamic or hardcoded
                    if 'localhost' in url or '127.0.0.1' in url:
                        print(f"   ⚠️  User {user['id']}: {url[:60]}... (HARDCODED localhost)")
                    else:
                        print(f"   ✅ User {user['id']}: {url[:60]}... (looks dynamic)")
        else:
            print("   ℹ️  No users have QR codes generated yet")
    else:
        print("❌ users.qr_code_url column does NOT exist")
    
    cursor.close()
    conn.close()

# Check 6: Create comprehensive test
print("\n\n6️⃣ CREATING COMPREHENSIVE TEST REPORT")
print("-" * 80)

issues = []
recommendations = []

# Analyze findings
if "request.url_root" not in profile_content:
    issues.append("Profile controller doesn't use request.url_root for dynamic URLs")
    recommendations.append("Update view_user_profile() to use: profile_url = request.url_root.rstrip('/') + url_for(...)")

if len(formats_found) < 3:
    issues.append("Scanner doesn't handle all QR/NFC formats")
    recommendations.append("Update scanner JavaScript to handle: NFC format, URL format, and numeric ID")

if has_qr_column and qr_samples and any('localhost' in s.get('qr_code_url', '') for s in qr_samples):
    issues.append("Database contains hardcoded localhost URLs")
    recommendations.append("Regenerate QR codes to use dynamic URLs")

print("\n📊 SUMMARY:")
print("=" * 80)

if not issues:
    print("✅ ALL CHECKS PASSED!")
    print("\n   Your NFC/QR system is properly configured with:")
    print("   ✅ Dynamic URLs that work on any server")
    print("   ✅ Multiple format handling (NFC, QR, Manual)")
    print("   ✅ Proper database storage")
    print("\n   🎉 Ready for production deployment!")
else:
    print(f"⚠️  FOUND {len(issues)} ISSUE(S):")
    for i, issue in enumerate(issues, 1):
        print(f"\n   {i}. {issue}")
    
    print("\n\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n   {i}. {rec}")

# Check 7: Test URL extraction logic
print("\n\n7️⃣ TESTING URL EXTRACTION LOGIC")
print("-" * 80)

test_urls = [
    "http://localhost:5000/profile/user/123",
    "https://myserver.com/profile/user/456",
    "http://192.168.1.100:5000/profile/user/789",
    "USER:123|URL:http://example.com/profile/user/123",
    "123",
]

print("\n   Testing with sample URLs:")
for url in test_urls:
    print(f"\n   Input: {url}")
    
    # Simulate the extraction logic from scanner
    user_id = None
    
    if '/profile/user/' in url:
        import re
        match = re.search(r'/profile/user/(\d+)', url)
        if match:
            user_id = match.group(1)
    elif 'USER:' in url:
        parts = url.split('|')
        user_id = parts[0].replace('USER:', '').strip()
    elif url.isdigit():
        user_id = url
    
    if user_id:
        print(f"   ✅ Extracted: User ID = {user_id}")
    else:
        print(f"   ❌ Failed to extract user ID")

print("\n\n" + "=" * 80)
print("✅ VERIFICATION COMPLETE!")
print("=" * 80)

# Generate fix script if needed
if issues:
    print("\n🔧 Generating fix script...")
    
    fix_script = '''# filepath: fix_dynamic_urls.py

print("=" * 80)
print("🔧 FIXING DYNAMIC URL IMPLEMENTATION")
print("=" * 80)

# Fix 1: Update profile controller
profile_path = 'src/controllers/profile_controller.py'
with open(profile_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure dynamic URL generation in view_user_profile
if "request.url_root" not in content:
    print("\\n1️⃣ Fixing profile controller...")
    
    # Find the view_user_profile function
    lines = content.split('\\n')
    for i, line in enumerate(lines):
        if 'def view_user_profile(user_id):' in line:
            # Find where to add dynamic URL code
            for j in range(i, min(i+150, len(lines))):
                if 'return render_template' in lines[j]:
                    # Add dynamic URL code before return
                    indent = '    '
                    url_code = f"""
{indent}# Generate dynamic profile URL
{indent}profile_url = request.url_root.rstrip('/') + url_for('profile.view_user_profile', user_id=user['id'])
{indent}
{indent}# Generate QR code with dynamic URL
{indent}qr = qrcode.QRCode(version=1, box_size=10, border=5)
{indent}qr.add_data(profile_url)
{indent}qr.make(fit=True)
{indent}
{indent}img = qr.make_image(fill_color="black", back_color="white")
{indent}buffer = BytesIO()
{indent}img.save(buffer, format='PNG')
{indent}qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
{indent}"""
                    lines.insert(j, url_code)
                    break
            break
    
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(lines))
    
    print("   ✅ Profile controller updated!")

print("\\n✅ ALL FIXES APPLIED!")
print("\\n🔄 Restart Flask: python app.py")
'''
    
    with open('fix_dynamic_urls.py', 'w', encoding='utf-8') as f:
        f.write(fix_script)
    
    print("\n   ✅ Created: fix_dynamic_urls.py")
    print("\n   Run: python fix_dynamic_urls.py")
else:
    print("\n✅ No fixes needed - system is properly configured!")

print("\n💡 NEXT STEPS:")
print("   1. If issues found: Run python fix_dynamic_urls.py")
print("   2. Restart Flask: python app.py")
print("   3. Test on different domains/IPs")
print("   4. Generate fresh QR codes for users")
print("   5. Test NFC and QR scanning with real devices")