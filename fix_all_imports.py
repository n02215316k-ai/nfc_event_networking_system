import os

print("=" * 80)
print("🔧 FIXING ALL MISSING IMPORTS")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# List of required imports
required_imports = {
    'secure_filename': 'from werkzeug.utils import secure_filename',
    'datetime': 'from datetime import datetime'
}

missing_imports = []

# Check which imports are missing
for import_name, import_statement in required_imports.items():
    if import_name not in content or import_statement not in content:
        missing_imports.append(import_statement)
        print(f"⚠️ Missing: {import_statement}")

if missing_imports:
    print(f"\n🔧 Adding {len(missing_imports)} missing import(s)...")
    
    lines = content.split('\n')
    
    # Find the last import line
    last_import_line = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            last_import_line = i
    
    # Add missing imports after the last import
    for import_statement in missing_imports:
        lines.insert(last_import_line + 1, import_statement)
        last_import_line += 1
        print(f"   ✅ Added: {import_statement}")
    
    content = '\n'.join(lines)
    
    # Write back
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ All imports added!")
else:
    print("✅ All required imports are present")

print("\n" + "=" * 80)
print("✅ IMPORT FIX COMPLETE!")
print("=" * 80)

print("\n🔄 Restart Flask:")
print("   Stop Flask (Ctrl+C)")
print("   python app.py")
print("\n   Upload should now work! 🎉")