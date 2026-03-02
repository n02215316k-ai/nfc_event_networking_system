import os

print("=" * 80)
print("🔍 CHECKING DOCUMENT UPLOAD FUNCTIONALITY")
print("=" * 80)

# Check 1: Profile controller - add_qualification route
print("\n1️⃣ CHECKING add_qualification ROUTE")
print("-" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    profile_content = f.read()

if 'def add_qualification' in profile_content:
    print("✅ add_qualification route exists")
    
    # Check if it handles file uploads
    if 'request.files' in profile_content and 'document' in profile_content:
        print("   ✅ Handles file uploads")
    else:
        print("   ❌ Does NOT handle file uploads properly")
    
    # Show the function
    import re
    match = re.search(r'@profile_bp\.route.*?add.*qualification.*?\ndef add_qualification.*?(?=\n@|\nclass |\Z)', 
                     profile_content, re.DOTALL)
    if match:
        lines = match.group(0).split('\n')[:30]  # Show first 30 lines
        print("\n   Current implementation (first 30 lines):")
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d} | {line}")
else:
    print("❌ add_qualification route NOT found")

# Check 2: Upload directory configuration
print("\n\n2️⃣ CHECKING UPLOAD DIRECTORIES")
print("-" * 80)

upload_dirs = [
    'uploads/qualifications',
    'static/uploads/qualifications',
    'uploads'
]

for dir_path in upload_dirs:
    if os.path.exists(dir_path):
        file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
        print(f"   ✅ {dir_path} (contains {file_count} files)")
    else:
        print(f"   ❌ {dir_path} (does not exist)")

# Check 3: File upload form in templates
print("\n\n3️⃣ CHECKING TEMPLATES FOR UPLOAD FORMS")
print("-" * 80)

template_files = [
    'templates/profile/qualifications.html',
    'templates/profile/edit.html',
    'templates/profile/view.html'
]

for template_path in template_files:
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        print(f"\n   {template_path}:")
        
        if 'enctype="multipart/form-data"' in template_content:
            print(f"      ✅ Has multipart form for file uploads")
        else:
            print(f"      ⚠️ Missing multipart/form-data encoding")
        
        if 'type="file"' in template_content:
            print(f"      ✅ Has file input field")
        else:
            print(f"      ❌ No file input field")
        
        if 'accept=' in template_content:
            accept_match = re.search(r'accept="([^"]+)"', template_content)
            if accept_match:
                print(f"      ✅ Accepts: {accept_match.group(1)}")
    else:
        print(f"\n   ❌ {template_path} does not exist")

print("\n\n" + "=" * 80)
print("📋 DOCUMENT UPLOAD FLOW")
print("=" * 80)

print("""
CURRENT FLOW (if implemented):
1. User goes to /profile/qualifications
2. Clicks "Add Qualification" button
3. Modal opens with form
4. User fills in:
   - Qualification type (dropdown)
   - Field of study (text)
   - Institution name (text)
   - Year obtained (number)
   - Document file (file upload)
5. User clicks "Submit for Verification"
6. File is uploaded to server
7. Record saved to database with status='pending'
8. System manager reviews and verifies

SUPPORTED FILE TYPES:
- PDF documents (.pdf)
- Images (.jpg, .jpeg, .png)
- Maximum size: 5MB
""")

print("\n" + "=" * 80)
print("🔧 CHECKING IF UPLOAD FUNCTIONALITY NEEDS TO BE ADDED")
print("=" * 80)

needs_fix = False

if 'def add_qualification' not in profile_content:
    print("❌ add_qualification route missing")
    needs_fix = True
elif 'request.files' not in profile_content:
    print("❌ File upload handling missing in add_qualification")
    needs_fix = True
else:
    print("✅ add_qualification route appears complete")

if not os.path.exists('uploads/qualifications'):
    print("⚠️ Upload directory missing")
    needs_fix = True

if needs_fix:
    print("\n🔧 Creating complete upload implementation...")
    print("   Run: python create_complete_upload_system.py")
else:
    print("\n✅ Upload system appears to be implemented!")
    print("\n📝 HOW TO USE:")
    print("   1. Go to: http://localhost:5000/profile/qualifications")
    print("   2. Click 'Add Qualification'")
    print("   3. Fill form and select document file")
    print("   4. Click 'Submit for Verification'")
    print("   5. File will be uploaded and saved")