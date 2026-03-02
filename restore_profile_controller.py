import os

print("=" * 80)
print("🔧 FIXING PROFILE CONTROLLER INDENTATION")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

if os.path.exists(profile_controller_path):
    with open(profile_controller_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✅ Found profile controller with {len(lines)} lines")
    
    # Find the problem area (around line 377)
    print("\n📋 Checking lines 370-385...")
    for i in range(max(0, 370), min(len(lines), 385)):
        print(f"{i+1:4d} | {repr(lines[i])}")
    
    # Fix: Remove any incorrectly indented import statements in the middle of the file
    fixed_lines = []
    in_function = False
    
    for i, line in enumerate(lines):
        # Track if we're inside a function
        if line.strip().startswith('def '):
            in_function = True
        elif line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            in_function = False
        
        # Fix incorrectly placed imports in the middle of functions
        if in_function and line.strip().startswith('import ') and line.startswith('    import'):
            # This is likely the problem - import statement with wrong indentation
            print(f"\n⚠️  Found problematic import at line {i+1}: {line.strip()}")
            # Skip this line or move it to top
            continue
        
        fixed_lines.append(line)
    
    # Make sure all necessary imports are at the top
    import_section = []
    other_lines = []
    found_first_def = False
    
    for line in fixed_lines:
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            found_first_def = True
        
        if not found_first_def and (line.strip().startswith('import ') or line.strip().startswith('from ')):
            if line not in import_section:
                import_section.append(line)
        else:
            other_lines.append(line)
    
    # Ensure required imports are present
    required_imports = [
        'from io import BytesIO\n',
        'import base64\n',
        'import qrcode\n'
    ]
    
    for imp in required_imports:
        if imp not in import_section:
            # Add after other imports
            import_section.insert(len(import_section), imp)
    
    # Reconstruct file
    final_content = import_section + other_lines
    
    # Write back
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.writelines(final_content)
    
    print("\n✅ Fixed profile controller!")
    print(f"   Total imports: {len(import_section)}")
    print(f"   Total lines: {len(final_content)}")
    
    # Show the import section
    print("\n📋 Import section:")
    for imp in import_section[:15]:
        print(f"   {imp.strip()}")
    
else:
    print(f"❌ {profile_controller_path} not found")

print("\n" + "=" * 80)
print("✅ INDENTATION FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Try running Flask again:")
print("   python app.py")