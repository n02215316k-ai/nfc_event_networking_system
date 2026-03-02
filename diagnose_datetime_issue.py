print("=" * 80)
print("🔍 DIAGNOSING DATETIME IMPORT ISSUE")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n📋 ALL imports in file:")
print("-" * 80)
for i, line in enumerate(lines, 1):
    if 'import' in line.lower() and not line.strip().startswith('#'):
        print(f"Line {i:3d}: {line.rstrip()}")
    if i > 50:  # Only check first 50 lines
        break

print("\n🔍 Searching for 'datetime' usage:")
print("-" * 80)
for i, line in enumerate(lines, 1):
    if 'datetime' in line.lower():
        print(f"Line {i:3d}: {line.rstrip()}")

print("\n" + "=" * 80)
print("🔧 SOLUTION: Add explicit import at top of file")
print("=" * 80)

# Insert at the very top after the first import line
new_lines = []
import_added = False

for i, line in enumerate(lines):
    new_lines.append(line)
    # Add after the first import line
    if not import_added and ('from flask import' in line or 'import flask' in line):
        # Check if datetime is already imported in next few lines
        has_datetime_import = any('from datetime import datetime' in lines[j] for j in range(i, min(i+10, len(lines))))
        
        if not has_datetime_import:
            new_lines.append('from datetime import datetime\n')
            print("✅ Added 'from datetime import datetime' after line", i+1)
            import_added = True

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\n✅ File updated!")
print("\n🔄 STOP Flask (Ctrl+C) and restart: python app.py")