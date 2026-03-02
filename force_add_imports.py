import os

print("=" * 80)
print("🔧 FORCE ADDING MISSING IMPORTS")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n📋 Current imports (first 20 lines):")
for i, line in enumerate(lines[:20], 1):
    if 'import' in line.lower():
        print(f"   {i:3d} | {line.rstrip()}")

# Check what's actually imported
has_datetime = any('from datetime import datetime' in line for line in lines)
has_secure_filename = any('from werkzeug.utils import secure_filename' in line for line in lines)

print(f"\n✅ Status:")
print(f"   datetime: {'✅ Found' if has_datetime else '❌ Missing'}")
print(f"   secure_filename: {'✅ Found' if has_secure_filename else '❌ Missing'}")

if not has_datetime or not has_secure_filename:
    print("\n🔧 Adding missing imports...")
    
    # Find where to insert (after the first import block)
    insert_position = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('#') and not line.startswith('from') and not line.startswith('import'):
            insert_position = i
            break
    
    imports_to_add = []
    if not has_datetime:
        imports_to_add.append('from datetime import datetime\n')
        print("   Adding: from datetime import datetime")
    
    if not has_secure_filename:
        imports_to_add.append('from werkzeug.utils import secure_filename\n')
        print("   Adding: from werkzeug.utils import secure_filename")
    
    # Insert the imports
    for import_line in reversed(imports_to_add):
        lines.insert(insert_position, import_line)
    
    # Write back
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\n✅ Imports added!")
    
    # Verify
    with open(profile_controller_path, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    print("\n✅ Verification:")
    print(f"   datetime in file: {'✅ Yes' if 'from datetime import datetime' in new_content else '❌ No'}")
    print(f"   secure_filename in file: {'✅ Yes' if 'from werkzeug.utils import secure_filename' in new_content else '❌ No'}")

else:
    print("\n✅ All imports already present!")

print("\n" + "=" * 80)
print("✅ FIX COMPLETE!")
print("=" * 80)

print("\n🔄 Now:")
print("   1. Stop Flask (Ctrl+C)")
print("   2. Restart: python app.py")
print("   3. Try upload again!")