print("=" * 80)
print("🔧 FIXING EVENT_CONTROLLER COMPLETE STRUCTURE")
print("=" * 80)

with open('src/controllers/event_controller.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the problematic try block (around line 156-164)
fixed = False
for i in range(len(lines)):
    if i < len(lines) - 20 and '# Create event' in lines[i] and 'try:' in lines[i+1]:
        print(f"Found problem area at line {i+1}")
        
        # Find the end of the INSERT query
        insert_end = i + 1
        while insert_end < len(lines) and 'fetch=False)' not in lines[insert_end]:
            insert_end += 1
        
        if insert_end < len(lines):
            # Get indentation
            indent = '            '  # 12 spaces for inside try block
            
            # Check if next lines are properly indented
            if insert_end + 1 < len(lines) and lines[insert_end + 1].strip().startswith('# Get the last'):
                # Fix the indentation and add except block
                
                # Find where the try block should end (before except)
                try_end = insert_end + 1
                
                # Look for the next unindented line or except/finally
                while try_end < len(lines):
                    stripped = lines[try_end].strip()
                    if stripped and not lines[try_end].startswith('            ') and not stripped.startswith('#'):
                        if 'except' not in stripped and 'finally' not in stripped:
                            # Need to add except before this line
                            break
                    try_end += 1
                
                # Find where to insert except block (look for flash or return after event creation)
                except_insert_pos = try_end
                for j in range(insert_end, min(insert_end + 50, len(lines))):
                    if 'flash(' in lines[j] or 'return redirect' in lines[j]:
                        except_insert_pos = j
                        break
                
                # Add proper indentation to lines between INSERT and except
                for j in range(insert_end + 1, except_insert_pos):
                    if lines[j].strip() and not lines[j].startswith(indent):
                        if lines[j].startswith('        '):
                            # Already has some indentation, add more
                            lines[j] = '    ' + lines[j]
                
                # Insert except block if not present
                if except_insert_pos < len(lines) and 'except' not in lines[except_insert_pos]:
                    except_block = '''        except Exception as e:
            print(f"Event creation error: {e}")
            flash('Error creating event. Please try again.', 'error')
            return render_template('events/create.html')
        
'''
                    lines.insert(except_insert_pos, except_block)
                
                fixed = True
                print(f"✅ Fixed try-except block structure")
                break

if not fixed:
    print("⚠️ Could not auto-fix. Applying manual fix...")
    
    # Read again
    with open('src/controllers/event_controller.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the problematic section with correct code
    old_pattern = '''        # Create event
        try:
            execute_query('''
    
    # Find and replace the entire try block
    if old_pattern in content:
        # Split at the try block
        parts = content.split(old_pattern, 1)
        before = parts[0]
        after_parts = parts[1].split('flash(', 1)
        
        # Reconstruct with proper structure
        new_try_block = '''        # Create event
        try:
            execute_query('''
        
        content = before + new_try_block + after_parts[0]
        
        # Add proper except before flash
        content = content + '''
        except Exception as e:
            print(f"Event creation error: {e}")
            flash('Error creating event. Please try again.', 'error')
            return render_template('events/create.html')
        
        flash(''' + after_parts[1]
        
        lines = content.split('\n')

# Write back
with open('src/controllers/event_controller.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Fixed event_controller.py structure")
print("\n" + "=" * 80)
print("🔄 Now restart Flask:")
print("   python app.py")
print("=" * 80)