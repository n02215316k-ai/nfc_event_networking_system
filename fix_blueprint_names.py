print("=" * 80)
print("🔧 FIXING BLUEPRINT NAMES IN TEMPLATE")
print("=" * 80)

view_template_path = 'templates/profile/view.html'

with open(view_template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the blueprint name
if "url_for('messages.compose'" in content:
    content = content.replace("url_for('messages.compose'", "url_for('messaging.compose'")
    print("✅ Fixed: messages.compose → messaging.compose")

# Also check if messaging blueprint exists and has compose route
import os
if os.path.exists('src/controllers/messaging_controller.py'):
    with open('src/controllers/messaging_controller.py', 'r') as f:
        messaging_content = f.read()
    
    if 'def compose' in messaging_content:
        print("✅ messaging.compose route exists")
    else:
        print("⚠️ messaging.compose route might be missing")
        # Remove the message button if route doesn't exist
        content = content.replace(
            '''<a href="{{ url_for('messaging.compose', recipient_id=user.id) }}" class="btn btn-outline-primary">
                            <i class="fas fa-envelope me-2"></i>Message
                        </a>''',
            '''<!-- Message functionality coming soon -->'''
        )
        print("   Removed message button temporarily")
else:
    print("⚠️ messaging_controller.py not found")
    # Remove the message button
    content = content.replace(
        '''<a href="{{ url_for('messaging.compose', recipient_id=user.id) }}" class="btn btn-outline-primary">
                            <i class="fas fa-envelope me-2"></i>Message
                        </a>''',
        '''<!-- Message functionality coming soon -->'''
    )
    print("   Removed message button temporarily")

# Write back
with open(view_template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Template fixed!")
print("\n🔄 Refresh the profile page - it should work now!")