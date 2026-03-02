print("=" * 80)
print("🔧 ADDING ALL MISSING IMPORTS")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = f.readlines()

# Reset file pointer
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n📋 Current imports:")
for i, line in enumerate(lines[:15], 1):
    if 'import' in line.lower():
        print(f"   {line.rstrip()}")

# Required imports
required_imports = {
    'os': 'import os',
    'datetime': 'from datetime import datetime'
}

# Check what's missing
missing = []
for name, import_statement in required_imports.items():
    if import_statement not in content and name not in [line.split()[-1] for line in lines if 'import' in line]:
        missing.append(import_statement)
        print(f"\n⚠️ Missing: {import_statement}")

if missing:
    print(f"\n🔧 Adding {len(missing)} import(s)...")
    
    # Add after the first Flask import
    new_lines = []
    added = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        if not added and 'from flask import' in line:
            for import_stmt in missing:
                new_lines.append(import_stmt + '\n')
                print(f"   ✅ Added: {import_stmt}")
            added = True
    
    # Write back
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n✅ All imports added!")
else:
    print("\n✅ All imports already present")

print("\n" + "=" * 80)
print("🔄 STOP Flask (Ctrl+C) and restart:")
print("   python app.py")
print("=" * 80)