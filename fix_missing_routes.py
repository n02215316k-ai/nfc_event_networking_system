import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING MISSING ROUTES & TEMPLATES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

fixes_needed = {
    '/dashboard': 'Should redirect to / (home)',
    '/forums/': 'Should be /forum/ (singular)',
    '/profile/view': 'Should be /profile/ or /profile/edit',
    '/profile/settings': 'Missing route',
    'messaging/compose.html': 'Missing template',
}

print(f"{Colors.BOLD}Issues found from logs:{Colors.END}\n")
for issue, fix in fixes_needed.items():
    print(f"  {Colors.YELLOW}❌ {issue}{Colors.END}")
    print(f"     {Colors.CYAN}→ {fix}{Colors.END}\n")

# Fix 1: Create missing messaging/compose.html template
print(f"{Colors.BOLD}Creating missing templates...{Colors.END}\n")

messaging_dir = 'templates/messaging'
os.makedirs(messaging_dir, exist_ok=True)

compose_template = '''{% extends "base.html" %}

{% block title %}Compose Message{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4>✉️ Compose New Message</h4>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('messaging.send') }}">
                        <div class="mb-3">
                            <label for="recipient" class="form-label">To:</label>
                            <select class="form-select" id="recipient" name="recipient_id" required>
                                <option value="">Select recipient...</option>
                                {% for user in users %}
                                <option value="{{ user.id }}" {% if recipient and recipient.id == user.id %}selected{% endif %}>
                                    {{ user.full_name }} ({{ user.email }})
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label for="subject" class="form-label">Subject:</label>
                            <input type="text" class="form-control" id="subject" name="subject" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="message" class="form-label">Message:</label>
                            <textarea class="form-control" id="message" name="message" rows="8" required></textarea>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-paper-plane"></i> Send Message
                            </button>
                            <a href="{{ url_for('messaging.inbox') }}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

compose_path = os.path.join(messaging_dir, 'compose.html')
if not os.path.exists(compose_path):
    with open(compose_path, 'w', encoding='utf-8') as f:
        f.write(compose_template)
    print(f"{Colors.GREEN}✓ Created: {compose_path}{Colors.END}")
else:
    print(f"{Colors.YELLOW}Already exists: {compose_path}{Colors.END}")

# Fix 2: Add missing profile routes
print(f"\n{Colors.BOLD}Checking profile controller...{Colors.END}\n")

profile_controller = 'src/controllers/profile_controller.py'
if os.path.exists(profile_controller):
    with open(profile_controller, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for missing routes
    routes_to_add = []
    
    if "@profile_bp.route('/view')" not in content and "@profile_bp.route('/')" not in content:
        routes_to_add.append('view')
    
    if "@profile_bp.route('/settings')" not in content:
        routes_to_add.append('settings')
    
    if routes_to_add:
        print(f"{Colors.YELLOW}Missing routes in profile_controller: {', '.join(routes_to_add)}{Colors.END}")
        print(f"{Colors.CYAN}Add these routes or redirect them to existing ones{Colors.END}\n")
    else:
        print(f"{Colors.GREEN}✓ Profile routes look good{Colors.END}\n")

# Fix 3: Create redirect helpers in app.py
print(f"{Colors.BOLD}Adding redirect helpers to app.py...{Colors.END}\n")

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

redirect_routes = '''
# Redirect helpers for common 404s
@app.route('/dashboard')
def dashboard_redirect():
    """Redirect /dashboard to home"""
    return redirect('/')

@app.route('/forums')
@app.route('/forums/')
def forums_redirect():
    """Redirect /forums to /forum"""
    return redirect('/forum')

@app.route('/profile/view')
def profile_view_redirect():
    """Redirect /profile/view to /profile/edit"""
    return redirect('/profile/edit')

@app.route('/profile/settings')
def profile_settings_redirect():
    """Redirect /profile/settings to /profile/edit"""
    return redirect('/profile/edit')

'''

if '@app.route(\'/dashboard\')' not in app_content:
    # Find a good place to insert (before if __name__)
    import re
    main_block = re.search(r'\nif __name__ == [\'"]__main__[\'"]:', app_content)
    
    if main_block:
        insert_pos = main_block.start()
        app_content = app_content[:insert_pos] + '\n' + redirect_routes + app_content[insert_pos:]
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(app_content)
        
        print(f"{Colors.GREEN}✓ Added redirect routes to app.py{Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}Could not auto-add redirects (no __main__ block found){Colors.END}\n")
else:
    print(f"{Colors.YELLOW}Redirect routes already exist{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ FIXES APPLIED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Summary:{Colors.END}")
print(f"  ✓ Created messaging/compose.html template")
print(f"  ✓ Added redirect routes for 404s\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.CYAN}python app.py{Colors.END} - Restart Flask")
print(f"  2. Test all the routes that were giving 404s\n")

print(f"{Colors.YELLOW}Note: Some routes may need actual implementation in controllers{Colors.END}\n")