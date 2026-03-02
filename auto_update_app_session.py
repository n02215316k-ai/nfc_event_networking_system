import re

# Read current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add context processor if not exists
context_processor_code = '''
# Context processor to make user info available in all templates
@app.context_processor
def inject_user():
    """Make user info available in all templates"""
    if 'user_id' in session:
        return {
            'current_user': {
                'id': session.get('user_id'),
                'full_name': session.get('user_name'),
                'email': session.get('user_email'),
                'role': session.get('user_role')
            }
        }
    return {'current_user': None}
'''

# Check if context processor already exists
if '@app.context_processor' not in content and 'inject_user' not in content:
    # Find a good place to insert (after imports, before routes)
    # Look for the first @app.route
    match = re.search(r'(@app\.route\()', content)
    if match:
        insert_pos = match.start()
        content = content[:insert_pos] + context_processor_code + '\n\n' + content[insert_pos:]
        print("✅ Added context processor to app.py")
    else:
        print("⚠️  Could not find @app.route - add context processor manually")
else:
    print("ℹ️  Context processor already exists")

# Update login route to store role in session
login_pattern = r"(session\['user_id'\]\s*=\s*user\['id'\])"
login_replacement = r"""\1
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']"""

if "session['user_role']" not in content:
    content = re.sub(login_pattern, login_replacement, content)
    print("✅ Updated login to store user role in session")
else:
    print("ℹ️  Session role storage already exists")

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ app.py updated successfully!")