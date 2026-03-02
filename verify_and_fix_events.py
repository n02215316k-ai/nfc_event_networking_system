import os

print("=" * 80)
print("🔍 VERIFYING EVENTS IN DATABASE")
print("=" * 80)

# First, let's check if events exist
from database import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Check all events
    cursor.execute("SELECT * FROM events ORDER BY created_at DESC LIMIT 5")
    all_events = cursor.fetchall()
    
    print(f"\n📊 Total events in database: {len(all_events)}")
    if all_events:
        print("\n✅ Events found:")
        for event in all_events:
            print(f"   • ID: {event['id']} | {event['title']} | Creator: {event.get('creator_id', 'N/A')}")
    else:
        print("\n⚠️ NO EVENTS FOUND in database!")
        print("   You need to create an event first")
    
    # Check event_registrations table
    cursor.execute("SELECT * FROM event_registrations LIMIT 5")
    registrations = cursor.fetchall()
    print(f"\n📊 Event registrations: {len(registrations)}")
    
    cursor.close()
    conn.close()
else:
    print("❌ Could not connect to database")

print("\n" + "=" * 80)
print("🔧 FIXING NFC CONTROLLER EVENT QUERY")
print("=" * 80)

nfc_controller_path = 'src/controllers/nfc_controller.py'

with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if execute_query is imported
if "from database import" not in content and "def execute_query" not in content:
    print("⚠️ execute_query function not found!")
    print("   Adding database helper import...")
    
    # Add at the top after other imports
    lines = content.split('\n')
    import_added = False
    for i, line in enumerate(lines):
        if line.startswith('from flask import'):
            lines.insert(i + 1, 'from database import get_db_connection')
            import_added = True
            break
    
    if import_added:
        content = '\n'.join(lines)
        print("✅ Added database import")

# Find the scanner function and add/update event query
if "@nfc_bp.route('/scanner')" in content:
    lines = content.split('\n')
    scanner_line = None
    
    for i, line in enumerate(lines):
        if "@nfc_bp.route('/scanner')" in line:
            scanner_line = i
            break
    
    if scanner_line:
        # Find render_template
        render_line = None
        for i in range(scanner_line, min(scanner_line + 100, len(lines))):
            if "render_template" in lines[i] and "scanner.html" in lines[i]:
                render_line = i
                break
        
        if render_line:
            # Check if event query exists
            has_event_query = False
            for i in range(scanner_line, render_line):
                if "user_events" in lines[i]:
                    has_event_query = True
                    break
            
            if not has_event_query:
                print("\n🔧 Adding event query to scanner...")
                
                # Get indentation
                indent = "    "
                
                # Create event query using direct database connection
                event_query_code = f'''
{indent}# Get user's events for check-in mode
{indent}user_events = []
{indent}if 'user_id' in session:
{indent}    conn = get_db_connection()
{indent}    if conn:
{indent}        cursor = conn.cursor(dictionary=True)
{indent}        cursor.execute(\'\'\'
{indent}            SELECT DISTINCT e.* FROM events e
{indent}            WHERE e.creator_id = %s 
{indent}            OR e.id IN (
{indent}                SELECT event_id FROM event_registrations WHERE user_id = %s
{indent}            )
{indent}            ORDER BY e.start_date DESC
{indent}        \'\'\', (session['user_id'], session['user_id']))
{indent}        user_events = cursor.fetchall()
{indent}        cursor.close()
{indent}        conn.close()
'''
                
                # Insert before render_template
                lines.insert(render_line, event_query_code)
                render_line += 1
                
                # Update render_template
                if "user_events=" not in lines[render_line]:
                    lines[render_line] = lines[render_line].rstrip()
                    if lines[render_line].endswith(')'):
                        lines[render_line] = lines[render_line][:-1] + ',\n' + indent + '                         user_events=user_events)'
                    else:
                        lines[render_line] += ', user_events=user_events'
                
                content = '\n'.join(lines)
                print("✅ Added event query!")
            else:
                print("\n✅ Event query already exists")
                
        else:
            print("⚠️ Could not find render_template")
    else:
        print("⚠️ Could not find scanner route")

# Write back
with open(nfc_controller_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 80)
print("✅ NFC CONTROLLER UPDATED!")
print("=" * 80)

print("\n📋 Next steps:")
print("   1. Restart Flask: python app.py")
print("   2. Create an event if you haven't:")
print("      • Go to: http://localhost:5000/events/create")
print("      • Fill in event details")
print("      • Click 'Create Event'")
print("   3. Go to scanner: http://localhost:5000/nfc/scanner")
print("   4. Select 'Check-In/Out' mode")
print("   5. Your events should appear in dropdown!")

print("\n💡 If events still don't show:")
print("   • Make sure you're logged in")
print("   • Check that you created the event with your account")
print("   • Verify event status is 'published' not 'draft'")