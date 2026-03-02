import os

print("=" * 80)
print("🔍 CHECKING NFC CONTROLLER - EVENT DATA")
print("=" * 80)

nfc_controller_path = 'src/controllers/nfc_controller.py'

with open(nfc_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("✅ Found NFC controller")

# Check if scanner route passes events
if "def scanner" in content:
    print("\n✅ Found scanner function")
    
    # Find the scanner function
    scanner_start = content.find("def scanner")
    scanner_section = content[scanner_start:scanner_start+2000]
    
    print("\n📋 Current scanner function:")
    print("-" * 80)
    print(scanner_section[:1000])
    print("-" * 80)
    
    if "user_events" in scanner_section:
        print("\n✅ Scanner already queries user events")
    else:
        print("\n⚠️ Scanner is NOT querying user events!")
        print("   This is why events don't show up in the dropdown")
else:
    print("\n❌ Could not find scanner function")

print("\n" + "=" * 80)
print("🔧 FIXING NFC CONTROLLER...")
print("=" * 80)

# Find and update the scanner function
if "@nfc_bp.route('/scanner')" in content:
    # Find the scanner function
    lines = content.split('\n')
    scanner_line = None
    
    for i, line in enumerate(lines):
        if "@nfc_bp.route('/scanner')" in line:
            scanner_line = i
            break
    
    if scanner_line:
        print(f"✅ Found scanner route at line {scanner_line + 1}")
        
        # Find the render_template line
        render_line = None
        for i in range(scanner_line, min(scanner_line + 50, len(lines))):
            if "render_template" in lines[i] and "scanner.html" in lines[i]:
                render_line = i
                break
        
        if render_line:
            print(f"✅ Found render_template at line {render_line + 1}")
            print(f"\n   Current: {lines[render_line].strip()}")
            
            # Check if we need to add event query
            needs_event_query = True
            for i in range(scanner_line, render_line):
                if "user_events" in lines[i] or "events" in lines[i]:
                    needs_event_query = False
                    break
            
            if needs_event_query:
                print("\n🔧 Adding event query...")
                
                # Find where to insert the query (before render_template)
                indent = len(lines[render_line]) - len(lines[render_line].lstrip())
                
                event_query = f'''{' ' * indent}# Get user's events for check-in mode
{' ' * indent}user_events = execute_query(\'\'\'
{' ' * indent}    SELECT DISTINCT e.* FROM events e
{' ' * indent}    WHERE e.creator_id = %s OR e.id IN (
{' ' * indent}        SELECT event_id FROM event_registrations WHERE user_id = %s
{' ' * indent}    )
{' ' * indent}    ORDER BY e.start_date DESC
{' ' * indent}\'\'\', (session.get('user_id'), session.get('user_id')), fetch=True) or []
{' ' * indent}'''
                
                # Insert before render_template
                lines.insert(render_line, event_query)
                
                # Update render_template to include user_events
                render_line += 1  # Line shifted after insert
                if "user_events=" not in lines[render_line]:
                    # Add user_events to render_template
                    if lines[render_line].rstrip().endswith(')'):
                        lines[render_line] = lines[render_line].rstrip()[:-1] + ', user_events=user_events)'
                    else:
                        lines[render_line] = lines[render_line].rstrip() + ', user_events=user_events'
                
                # Write back
                new_content = '\n'.join(lines)
                with open(nfc_controller_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Added event query to scanner function!")
                print("\n📋 New scanner function includes:")
                print("   ✅ Query user's created events")
                print("   ✅ Query user's registered events")
                print("   ✅ Pass user_events to template")
                
            else:
                print("\n✅ Scanner already queries events")
        else:
            print("\n⚠️ Could not find render_template line")
    else:
        print("\n⚠️ Could not find scanner route")

print("\n" + "=" * 80)
print("✅ NFC CONTROLLER UPDATED!")
print("=" * 80)
print("\n🔄 Restart Flask:")
print("   python app.py")
print("\n   Your events should now appear in the scanner dropdown!")