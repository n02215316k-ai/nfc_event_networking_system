import os

print("=" * 80)
print("🔧 FIXING INDENTATION ERROR")
print("=" * 80)

event_admin_path = 'src/controllers/event_admin_controller.py'

if os.path.exists(event_admin_path):
    # Backup first
    with open(event_admin_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    with open(event_admin_path + '.backup2', 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print("✓ Backup created: event_admin_controller.py.backup2")
    
    # Read lines
    lines = original_content.split('\n')
    
    # Find the problematic area around line 321
    print(f"\nLooking for indentation error around line 321...")
    
    fixed = False
    for i in range(310, min(340, len(lines))):
        line = lines[i]
        
        # Find the cursor.execute that's causing trouble
        if 'cursor.execute("""' in line:
            # Check if it's incorrectly indented
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            
            # Look back to find the function definition
            for j in range(i-1, max(0, i-30), -1):
                if 'def ' in lines[j] and lines[j].strip().startswith('def '):
                    func_indent = len(lines[j]) - len(lines[j].lstrip())
                    correct_indent = func_indent + 4
                    
                    if current_indent != correct_indent:
                        print(f"✗ Line {i+1}: Incorrect indent ({current_indent} spaces)")
                        print(f"  Should be: {correct_indent} spaces")
                        print(f"  Function at line {j+1}: {lines[j].strip()[:50]}")
                        
                        # Fix the line
                        lines[i] = ' ' * correct_indent + stripped
                        
                        # Also fix following lines in the SQL block
                        for k in range(i+1, min(i+20, len(lines))):
                            if '"""' in lines[k] and lines[k].strip() == '"""':
                                # End of SQL block
                                lines[k] = ' ' * correct_indent + lines[k].lstrip()
                                break
                            elif lines[k].strip():  # Non-empty line
                                # SQL content should be indented further
                                lines[k] = ' ' * (correct_indent + 4) + lines[k].lstrip()
                        
                        fixed = True
                        print(f"✓ Fixed indentation")
                    break
    
    if fixed:
        # Write back
        new_content = '\n'.join(lines)
        with open(event_admin_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("\n✅ File fixed and saved!")
        print("\nNow run: python app.py")
    else:
        print("\n⚠️  Could not auto-fix.")
        print("\nPlease manually check line 321 in:")
        print(f"  {event_admin_path}")
        print("\nLook for cursor.execute and ensure it's aligned with other")
        print("statements inside the same function (4 spaces from 'def')")

else:
    print(f"✗ File not found: {event_admin_path}")

print("=" * 80)