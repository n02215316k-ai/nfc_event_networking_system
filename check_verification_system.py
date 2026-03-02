import os

print("=" * 80)
print("🔍 CHECKING DOCUMENT VERIFICATION SYSTEM")
print("=" * 80)

# Check 1: Database - qualifications table
print("\n1️⃣ CHECKING DATABASE STRUCTURE")
print("-" * 80)

from database import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Check qualifications table structure
    cursor.execute("DESCRIBE qualifications")
    columns = cursor.fetchall()
    
    print("✅ Qualifications table structure:")
    for col in columns:
        print(f"   • {col['Field']}: {col['Type']}")
    
    # Check for verification_status field
    has_verification = any(col['Field'] == 'verification_status' for col in columns)
    has_document_path = any(col['Field'] == 'document_path' for col in columns)
    has_verifier = any(col['Field'] == 'verified_by' for col in columns)
    
    print(f"\n   Verification fields:")
    print(f"   {'✅' if has_verification else '❌'} verification_status")
    print(f"   {'✅' if has_document_path else '❌'} document_path")
    print(f"   {'✅' if has_verifier else '❌'} verified_by")
    
    # Check existing qualifications
    cursor.execute("SELECT COUNT(*) as count FROM qualifications")
    qual_count = cursor.fetchone()['count']
    print(f"\n   📊 Total qualifications: {qual_count}")
    
    if qual_count > 0:
        cursor.execute("""
            SELECT verification_status, COUNT(*) as count 
            FROM qualifications 
            GROUP BY verification_status
        """)
        status_counts = cursor.fetchall()
        print(f"\n   Status breakdown:")
        for status in status_counts:
            print(f"   • {status['verification_status']}: {status['count']}")
    
    cursor.close()
    conn.close()

# Check 2: Profile Controller - Add Qualification Route
print("\n\n2️⃣ CHECKING PROFILE CONTROLLER - QUALIFICATION SUBMISSION")
print("-" * 80)

profile_path = 'src/controllers/profile_controller.py'
with open(profile_path, 'r', encoding='utf-8') as f:
    profile_content = f.read()

if "def add_qualification" in profile_content:
    print("✅ add_qualification route exists")
    
    if "document_path" in profile_content:
        print("   ✅ Handles document uploads")
    else:
        print("   ⚠️ Might not handle document uploads")
    
    if "verification_status" in profile_content:
        print("   ✅ Sets verification_status")
    else:
        print("   ⚠️ Might not set verification_status")
else:
    print("❌ add_qualification route NOT found")

# Check 3: Template - Qualification Form
print("\n\n3️⃣ CHECKING PROFILE TEMPLATES")
print("-" * 80)

templates_to_check = [
    'templates/profile/edit.html',
    'templates/profile/view.html',
    'templates/profile/qualifications.html'
]

for template_path in templates_to_check:
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n✅ Found: {template_path}")
        
        if 'qualification' in content.lower():
            print(f"   ✅ Has qualification content")
        
        if 'document' in content.lower():
            print(f"   ✅ Has document upload field")
        
        if 'verification' in content.lower():
            print(f"   ✅ Shows verification status")
    else:
        print(f"\n⚠️ Missing: {template_path}")

# Check 4: System Manager Verification Interface
print("\n\n4️⃣ CHECKING SYSTEM MANAGER VERIFICATION INTERFACE")
print("-" * 80)

sys_manager_path = 'src/controllers/system_manager_controller.py'
if os.path.exists(sys_manager_path):
    with open(sys_manager_path, 'r', encoding='utf-8') as f:
        sys_content = f.read()
    
    print("✅ System manager controller exists")
    
    if "verify_qualification" in sys_content or "verification" in sys_content:
        print("   ✅ Has verification routes")
    else:
        print("   ⚠️ Might be missing verification routes")
else:
    print("⚠️ System manager controller not found")

# Check 5: Upload Folder Configuration
print("\n\n5️⃣ CHECKING UPLOAD CONFIGURATION")
print("-" * 80)

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

if "UPLOAD_FOLDER" in app_content:
    print("✅ UPLOAD_FOLDER configured")
else:
    print("⚠️ UPLOAD_FOLDER might not be configured")

# Check if upload directories exist
upload_dirs = [
    'uploads/qualifications',
    'uploads/profiles',
    'static/uploads/qualifications'
]

print("\n   Upload directories:")
for dir_path in upload_dirs:
    if os.path.exists(dir_path):
        print(f"   ✅ {dir_path}")
    else:
        print(f"   ⚠️ {dir_path} (not created yet)")

print("\n\n" + "=" * 80)
print("📋 DOCUMENT VERIFICATION FLOW SUMMARY")
print("=" * 80)

print("""
CURRENT FLOW:
1. User adds qualification via profile
2. User uploads document (PDF, JPG, PNG)
3. Status set to 'pending'
4. System Manager reviews documents
5. Manager approves/rejects with comments
6. User receives notification

MISSING COMPONENTS:
""")

# Identify missing components
missing = []

if not os.path.exists('templates/system_manager/verify_qualifications.html'):
    missing.append("System Manager verification interface template")

if 'def verify_qualification' not in (sys_content if os.path.exists(sys_manager_path) else ''):
    missing.append("Verification route in system manager controller")

if not os.path.exists('uploads/qualifications'):
    missing.append("Upload directory for qualification documents")

if missing:
    print("⚠️ Missing:")
    for item in missing:
        print(f"   • {item}")
else:
    print("✅ All components present!")

print("\n" + "=" * 80)
print("🔧 GENERATING COMPLETE VERIFICATION SYSTEM")
print("=" * 80)