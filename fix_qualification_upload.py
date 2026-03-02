import os

print("=" * 80)
print("🔧 FIXING QUALIFICATION UPLOAD ERROR")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if current_app is imported
if 'from flask import current_app' in content or 'import current_app' in content:
    print("✅ current_app is already imported")
else:
    print("⚠️ current_app is NOT imported - adding it...")
    
    # Find the imports section
    lines = content.split('\n')
    
    # Find the Flask import line
    for i, line in enumerate(lines):
        if line.startswith('from flask import'):
            # Add current_app to the import
            if 'current_app' not in line:
                # Add it to existing imports
                imports = line.replace('from flask import ', '').split(',')
                imports = [imp.strip() for imp in imports]
                imports.append('current_app')
                lines[i] = 'from flask import ' + ', '.join(sorted(imports))
                print(f"   ✅ Added current_app to imports at line {i+1}")
                break
    else:
        # If no Flask import found, add it after other imports
        for i, line in enumerate(lines):
            if line.startswith('from flask import') or line.startswith('import flask'):
                lines.insert(i+1, 'from flask import current_app')
                print(f"   ✅ Added import line at {i+2}")
                break
    
    content = '\n'.join(lines)

# Now fix the allowed_file usage
print("\n🔧 Fixing allowed_file function call...")

# Replace current_app.allowed_file with a proper implementation
if 'current_app.allowed_file' in content:
    print("   ⚠️ Found current_app.allowed_file - replacing with proper check...")
    
    # Replace with inline check
    content = content.replace(
        'current_app.allowed_file(file.filename)',
        "allowed_file(file.filename, {'pdf', 'png', 'jpg', 'jpeg'})"
    )
    print("   ✅ Replaced with allowed_file helper function")

# Check if allowed_file helper exists
if 'def allowed_file' not in content:
    print("\n🔧 Adding allowed_file helper function...")
    
    helper_function = '''
def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

'''
    
    # Add after imports, before first route
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '@profile_bp.route' in line:
            lines.insert(i, helper_function)
            print("   ✅ Added allowed_file helper function")
            break
    
    content = '\n'.join(lines)

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 80)
print("✅ FIX COMPLETE!")
print("=" * 80)

print("\n🔄 Restart Flask:")
print("   Stop current Flask (Ctrl+C)")
print("   python app.py")
print("\n   Then try uploading a document again!")