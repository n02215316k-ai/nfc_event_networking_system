import os

print("=" * 80)
print("🔍 DEBUGGING NFC SCANNER - WHY NO EVENTS?")
print("=" * 80)

# First verify events exist in database
from database import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Get current user ID from session (you're logged in as user with ID)
    print("\n1️⃣ Checking events in database...")
    cursor.execute("SELECT id, title, creator_id, status FROM events")
    all_events = cursor.fetchall()
    
    print(f"\n   Found {len(all_events)} events:")
    for event in all_events:
        print(f"   • Event ID: {event['id']} | {event['title']}")
        print(f"     Creator: {event['creator_id']} | Status: {event['status']}")
    
    cursor.close()
    conn.close()

# Now check the NFC controller
print("\n2️⃣ Checking NFC controller scanner function...")

nfc_controller_path = 'src/controllers/nfc_controller.py'

with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find scanner function
if "@nfc_bp.route('/scanner')" in content:
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if "@nfc_bp.route('/scanner')" in line:
            # Show 30 lines after the route decorator
            print(f"\n   Scanner function (lines {i+1} to {i+30}):")
            print("   " + "-" * 70)
            for j in range(i, min(i+30, len(lines))):
                print(f"   {j+1:4d} | {lines[j]}")
            print("   " + "-" * 70)
            break

print("\n3️⃣ Checking if user_events is in render_template...")
if "render_template('nfc/scanner.html'" in content:
    # Find what variables are passed
    match_start = content.find("render_template('nfc/scanner.html'")
    match_end = content.find(")", match_start) + 1
    render_call = content[match_start:match_end]
    
    print(f"\n   Current render_template call:")
    print(f"   {render_call}")
    
    if "user_events" in render_call:
        print("\n   ✅ user_events IS being passed")
    else:
        print("\n   ❌ user_events is NOT being passed!")
        print("\n   This is the problem!")

print("\n" + "=" * 80)
print("🔧 NOW FIXING THE NFC CONTROLLER...")
print("=" * 80)

# Read the file again
with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find scanner function and fix it
scanner_line = None
for i, line in enumerate(lines):
    if "@nfc_bp.route('/scanner')" in line:
        scanner_line = i
        break

if scanner_line:
    # Find the render_template line
    render_line = None
    for i in range(scanner_line, min(scanner_line + 50, len(lines))):
        if "render_template" in lines[i] and "scanner.html" in lines[i]:
            render_line = i
            break
    
    if render_line:
        # Check if event query exists before render_template
        has_event_query = False
        for i in range(scanner_line, render_line):
            if "user_events" in lines[i] and "=" in lines[i]:
                has_event_query = True
                break
        
        if not has_event_query:
            print("\n🔧 Adding event query before render_template...")
            
            indent = "    "
            event_query = f"{indent}# Get user's events for check-in mode\n"
            event_query += f"{indent}user_events = []\n"
            event_query += f"{indent}if 'user_id' in session:\n"
            event_query += f"{indent}    conn = get_db_connection()\n"
            event_query += f"{indent}    if conn:\n"
            event_query += f"{indent}        cursor = conn.cursor(dictionary=True)\n"
            event_query += f"{indent}        cursor.execute(\"\"\"\n"
            event_query += f"{indent}            SELECT DISTINCT e.* FROM events e\n"
            event_query += f"{indent}            WHERE e.creator_id = %s\n"
            event_query += f"{indent}            OR e.id IN (\n"
            event_query += f"{indent}                SELECT event_id FROM event_registrations WHERE user_id = %s\n"
            event_query += f"{indent}            )\n"
            event_query += f"{indent}            ORDER BY e.start_date DESC\n"
            event_query += f"{indent}        \"\"\", (session['user_id'], session['user_id']))\n"
            event_query += f"{indent}        user_events = cursor.fetchall()\n"
            event_query += f"{indent}        cursor.close()\n"
            event_query += f"{indent}        conn.close()\n"
            event_query += f"{indent}\n"
            
            lines.insert(render_line, event_query)
            render_line += 1
            print("   ✅ Event query added!")
        
        # Update render_template to include user_events
        if "user_events=" not in lines[render_line]:
            print("🔧 Adding user_events to render_template...")
            
            # Find the closing parenthesis
            if lines[render_line].rstrip().endswith(')'):
                lines[render_line] = lines[render_line].rstrip()[:-1] + ', user_events=user_events)\n'
            else:
                lines[render_line] = lines[render_line].rstrip() + ', user_events=user_events\n'
            
            print("   ✅ user_events added to render_template!")
        
        # Write back
        with open(nfc_controller_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("\n✅ NFC CONTROLLER FIXED!")
    else:
        print("\n⚠️ Could not find render_template")
else:
    print("\n⚠️ Could not find scanner route")

print("\n" + "=" * 80)
print("✅ FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Restart Flask:")
print("   python app.py")
print("\n   Then refresh the scanner page!")
print("   Your events should now appear in the dropdown! 🎉")