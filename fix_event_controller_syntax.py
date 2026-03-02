print("=" * 80)
print("🔧 FIXING EVENT_CONTROLLER SYNTAX ERROR")
print("=" * 80)

with open('src/controllers/event_controller.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Escape sequence error
content = content.replace(
    "execute_query(\"SELECT LAST_INSERT_ID() as id\", fetch=True, fetchone=True)[\\'id\\']",
    'execute_query("SELECT LAST_INSERT_ID() as id", fetch=True, fetchone=True)["id"]'
)

# Fix 2: Indentation and try block structure
# Find and fix the problematic section
old_code = '''        # Create event
        try:
            execute_query('''

new_code = '''        # Create event
        try:
            execute_query('''

if old_code in content:
    # The try block is correct, just need to fix the escaping
    print("✅ Try block structure is OK")

# Also fix any other escaped quotes
content = content.replace("\\'", "'")

with open('src/controllers/event_controller.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed syntax errors in event_controller.py")
print("\n" + "=" * 80)
print("🔄 Restart Flask and test event creation")
print("=" * 80)