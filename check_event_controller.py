import os

print("=" * 80)
print("🔍 CHECKING EVENT_CONTROLLER.PY")
print("=" * 80)

event_controller_path = 'src/controllers/event_controller.py'

if os.path.exists(event_controller_path):
    with open(event_controller_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n✅ Found: {event_controller_path}")
    print("\n📋 Searching for event creation code...\n")
    
    # Find the event creation section
    for i, line in enumerate(lines, 1):
        if 'INSERT INTO events' in line:
            # Show context around INSERT
            start = max(0, i - 5)
            end = min(len(lines), i + 20)
            
            print(f"   Lines {start+1}-{end}:")
            print("   " + "-" * 70)
            for j in range(start, end):
                marker = ">>>" if j == i-1 else "   "
                print(f"{marker} {j+1:4d} | {lines[j].rstrip()}")
            print("   " + "-" * 70)
            break
    
    # Check for the problematic patterns
    content = ''.join(lines)
    
    print("\n📊 Analysis:")
    if 'LAST_INSERT_ID()' in content:
        print("   ✅ Uses LAST_INSERT_ID() method - Should work!")
    
    if 'return_lastrowid=True' in content:
        print("   ⚠️  Found return_lastrowid=True")
        
        # Check if db_utils supports it
        if os.path.exists('db_utils.py'):
            with open('db_utils.py', 'r', encoding='utf-8') as f:
                db_content = f.read()
            
            if 'return_lastrowid' in db_content and 'cursor.lastrowid' in db_content:
                print("   ✅ db_utils.py DOES support return_lastrowid - Should work!")
            else:
                print("   ❌ db_utils.py DOES NOT support return_lastrowid - Will fail!")
                print("\n   🔧 Fix needed in db_utils.py")
    
    if 'execute_query' not in content:
        print("   ❌ No execute_query found - Different database method?")
    
else:
    print(f"❌ {event_controller_path} not found!")
    
    # Try to find it
    print("\n🔍 Searching for event_controller.py...")
    for root, dirs, files in os.walk('.'):
        if 'event_controller.py' in files:
            print(f"   Found: {os.path.join(root, files[0])}")

print("\n" + "=" * 80)