import re

print("=" * 80)
print("🔧 FIXING EVENT CREATION ERROR")
print("=" * 80)

# Read the event controller
with open('src/controllers/event_controller.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the execute_query with return_lastrowid
# Pattern 1: return_lastrowid=True
old_pattern1 = r"execute_query\((.*?)\)"
new_pattern1 = r"execute_query(\1, fetch=False)"

# Pattern 2: More complex cases
fixes_applied = 0

# Method 1: Replace specific problematic calls
if "return_lastrowid=True" in content:
    # Fix: Replace return_lastrowid with proper implementation
    content = re.sub(
        r'event_id\s*=\s*execute_query\((.*?)\s*,\s*return_lastrowid=True\)',
        r'execute_query(\1, fetch=False)\n        # Get the last inserted ID\n        event_id = execute_query("SELECT LAST_INSERT_ID() as id", fetch=True, fetchone=True)[\'id\']',
        content,
        flags=re.DOTALL
    )
    fixes_applied += 1
    print("✅ Fixed return_lastrowid in event creation")

# Write back
with open('src/controllers/event_controller.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Applied {fixes_applied} fixes to event_controller.py")

# Also update db_utils.py to support lastrowid properly
print("\n📝 Checking db_utils.py...")

try:
    with open('src/utils/db_utils.py', 'r', encoding='utf-8') as f:
        db_content = f.read()
    
    # Check if execute_query returns lastrowid
    if 'lastrowid' not in db_content or 'return_lastrowid' not in db_content:
        print("ℹ️  Adding lastrowid support to execute_query...")
        
        # Find the execute_query function and update it
        updated_db_content = db_content.replace(
            "def execute_query(query, params=None, fetch=False, fetchone=False):",
            "def execute_query(query, params=None, fetch=False, fetchone=False, return_lastrowid=False):"
        )
        
        # Add lastrowid return logic
        updated_db_content = updated_db_content.replace(
            """            conn.commit()
            return True""",
            """            conn.commit()
            if return_lastrowid:
                return cursor.lastrowid
            return True"""
        )
        
        with open('src/utils/db_utils.py', 'w', encoding='utf-8') as f:
            f.write(updated_db_content)
        
        print("✅ Updated db_utils.py to support return_lastrowid")
    else:
        print("✅ db_utils.py already supports lastrowid")
        
except FileNotFoundError:
    print("⚠️  Could not find db_utils.py")

print("\n" + "=" * 80)
print("✅ EVENT CREATION FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Restart Flask:")
print("  python app.py")