import os
import re

print("=" * 80)
print("🔍 CHECKING AND FIXING IMPORTS")
print("=" * 80)

# Find where db_utils.py exists
db_utils_locations = []
for root, dirs, files in os.walk('.'):
    if 'db_utils.py' in files:
        db_utils_locations.append(os.path.join(root, 'db_utils.py'))

print(f"\n📁 Found db_utils.py in {len(db_utils_locations)} location(s):")
for loc in db_utils_locations:
    print(f"   {loc}")

# Find all Python files that import db_utils
print("\n📝 Checking imports in Python files...")
import_issues = []

for root, dirs, files in os.walk('.'):
    # Skip virtual environments and cache
    if 'venv' in root or '__pycache__' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for db_utils imports
                if 'from db_utils import' in content or 'import db_utils' in content:
                    print(f"   ✅ {filepath} - imports db_utils correctly")
                
                elif 'from src.utils.db_utils import' in content:
                    print(f"   ⚠️  {filepath} - imports from src.utils.db_utils (may not exist)")
                    import_issues.append((filepath, 'src.utils.db_utils'))
                
                elif 'from utils.db_utils import' in content:
                    print(f"   ⚠️  {filepath} - imports from utils.db_utils (may not exist)")
                    import_issues.append((filepath, 'utils.db_utils'))
            
            except Exception as e:
                pass

# Fix import issues
if import_issues:
    print(f"\n🔧 Found {len(import_issues)} import issues. Fixing...")
    
    for filepath, old_import in import_issues:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace incorrect imports
        content = content.replace(
            f'from {old_import} import',
            'from db_utils import'
        )
        content = content.replace(
            f'import {old_import}',
            'import db_utils'
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Fixed: {filepath}")
else:
    print("\n✅ No import issues found!")

# Check if event_controller.py has the fixed code
print("\n📋 Checking event_controller.py fix...")
event_controller_path = 'src/controllers/event_controller.py'

if os.path.exists(event_controller_path):
    with open(event_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'LAST_INSERT_ID()' in content:
        print("   ✅ Event creation uses LAST_INSERT_ID() - Good!")
    elif 'return_lastrowid=True' in content:
        print("   ⚠️  Still has return_lastrowid=True")
        print("   ℹ️  But db_utils.py supports it now, so it should work!")
    else:
        print("   ❓ Cannot determine event creation method")
else:
    print(f"   ❌ {event_controller_path} not found")

print("\n" + "=" * 80)
print("✅ IMPORT CHECK COMPLETE!")
print("=" * 80)
print("\n🔄 Now restart Flask and test event creation:")
print("   python app.py")