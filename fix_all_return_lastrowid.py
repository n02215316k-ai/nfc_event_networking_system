import os
import re

print("=" * 80)
print("🔍 SEARCHING AND FIXING ALL return_lastrowid CALLS")
print("=" * 80)

# Search all Python files for return_lastrowid
found_files = []

for root, dirs, files in os.walk('.'):
    # Skip venv and cache
    if 'venv' in root or '__pycache__' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'return_lastrowid' in content:
                    found_files.append(filepath)
                    print(f"\n📁 Found in: {filepath}")
                    
                    # Show the lines
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'return_lastrowid' in line:
                            print(f"   Line {i}: {line.strip()}")
            
            except Exception as e:
                pass

if not found_files:
    print("\n✅ No files with return_lastrowid found!")
else:
    print(f"\n🔧 Found {len(found_files)} file(s) with return_lastrowid")
    print("\n" + "=" * 80)
    print("FIXING FILES...")
    print("=" * 80)
    
    for filepath in found_files:
        print(f"\n📝 Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern 1: Simple replacement - remove the parameter
        content = re.sub(
            r',\s*return_lastrowid\s*=\s*True',
            '',
            content
        )
        
        # Pattern 2: If it's the only parameter
        content = re.sub(
            r'\(\s*return_lastrowid\s*=\s*True\s*\)',
            '()',
            content
        )
        
        # Pattern 3: Variable assignment with return_lastrowid
        # Find: something = execute_query(...)
        # Replace with: execute_query(...) then SELECT LAST_INSERT_ID()
        
        pattern = r'(\s*)(\w+)\s*=\s*execute_query\((.*?)\s*,\s*return_lastrowid\s*=\s*True\s*\)'
        
        def replace_with_last_insert(match):
            indent = match.group(1)
            var_name = match.group(2)
            query_params = match.group(3)
            
            # Return the fixed code
            return f'''{indent}execute_query({query_params}, fetch=False)
{indent}{var_name} = execute_query("SELECT LAST_INSERT_ID() as id", fetch=True, fetchone=True)["id"]'''
        
        content = re.sub(pattern, replace_with_last_insert, content, flags=re.DOTALL)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Fixed!")
        else:
            print(f"   ℹ️  No changes needed")

print("\n" + "=" * 80)
print("✅ ALL FILES PROCESSED")
print("=" * 80)

# Also check db_utils.py to ensure it has the support
print("\n📋 Checking db_utils.py implementation...")

if os.path.exists('db_utils.py'):
    with open('db_utils.py', 'r', encoding='utf-8') as f:
        db_content = f.read()
    
    if 'return_lastrowid' in db_content:
        if 'cursor.lastrowid' in db_content:
            print("   ✅ db_utils.py has full lastrowid support")
        else:
            print("   ⚠️  db_utils.py has parameter but not implementation")
            print("   🔧 Adding implementation...")
            
            # Add the implementation
            db_content = db_content.replace(
                "        else:\n            conn.commit()\n            return True",
                """        else:
            conn.commit()
            if return_lastrowid:
                return cursor.lastrowid
            return True"""
            )
            
            with open('db_utils.py', 'w', encoding='utf-8') as f:
                f.write(db_content)
            
            print("   ✅ Implementation added!")
    else:
        print("   ⚠️  db_utils.py missing return_lastrowid parameter")
        print("   🔧 Adding parameter to function signature...")
        
        db_content = db_content.replace(
            'def execute_query(query, params=None, fetch=False, fetchone=False):',
            'def execute_query(query, params=None, fetch=False, fetchone=False, return_lastrowid=False):'
        )
        
        # Add return logic
        db_content = db_content.replace(
            "        else:\n            conn.commit()\n            return True",
            """        else:
            conn.commit()
            if return_lastrowid:
                return cursor.lastrowid
            return True"""
        )
        
        with open('db_utils.py', 'w', encoding='utf-8') as f:
            f.write(db_content)
        
        print("   ✅ Full support added!")
else:
    print("   ❌ db_utils.py not found!")

print("\n" + "=" * 80)
print("🎉 ALL FIXES COMPLETE!")
print("=" * 80)
print("\n🔄 Restart Flask and test:")
print("   python app.py")