import os
import glob

print("=" * 80)
print("🔧 FIXING TEMPLATE ROUTE ERRORS")
print("=" * 80)

# Define all route fixes needed
route_fixes = {
    "url_for('events.list')": "url_for('events.list_events')",
    "url_for('profile.view'": "url_for('profile.view_user_profile'",
    'url_for("events.list")': 'url_for("events.list_events")',
    'url_for("profile.view"': 'url_for("profile.view_user_profile"',
}

# Find all HTML templates
templates = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            templates.append(os.path.join(root, file))

print(f"\n📁 Found {len(templates)} template files")

fixed_count = 0
files_modified = []

# Fix each template
for template_path in templates:
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        for old_route, new_route in route_fixes.items():
            if old_route in content:
                content = content.replace(old_route, new_route)
                fixed_count += 1
                files_modified.append(template_path)
                print(f"  ✅ Fixed: {template_path}")
                print(f"     {old_route} → {new_route}")
        
        # Write back if changed
        if content != original_content:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    except Exception as e:
        print(f"  ❌ Error in {template_path}: {e}")

print(f"\n✅ Fixed {fixed_count} route references in {len(set(files_modified))} files")

# Create missing settings.html template
settings_html = '''{% extends "base.html" %}

{% block title %}System Settings - NFC Event Network{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="fas fa-cog me-2"></i>System Settings</h2>
                <a href="{{ url_for('system_manager.dashboard') }}" class="btn btn-outline-secondary">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>

            <!-- Settings Form -->
            <div class="card">
                <div class="card-body">
                    <form method="POST">
                        <h5 class="card-title mb-4">General Settings</h5>
                        
                        <div class="mb-3">
                            <label for="site_name" class="form-label">Site Name</label>
                            <input type="text" class="form-control" id="site_name" name="site_name" 
                                   value="NFC Event Social Network">
                        </div>

                        <div class="mb-3">
                            <label for="site_email" class="form-label">System Email</label>
                            <input type="email" class="form-control" id="site_email" name="site_email" 
                                   value="admin@nfcevents.com">
                        </div>

                        <div class="mb-3">
                            <label for="max_events_per_user" class="form-label">Max Events Per User</label>
                            <input type="number" class="form-control" id="max_events_per_user" 
                                   name="max_events_per_user" value="10">
                        </div>

                        <hr class="my-4">

                        <h5 class="card-title mb-4">Event Settings</h5>

                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="require_event_approval" 
                                   name="require_event_approval" checked>
                            <label class="form-check-label" for="require_event_approval">
                                Require admin approval for new events
                            </label>
                        </div>

                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="allow_public_registration" 
                                   name="allow_public_registration" checked>
                            <label class="form-check-label" for="allow_public_registration">
                                Allow public user registration
                            </label>
                        </div>

                        <hr class="my-4">

                        <h5 class="card-title mb-4">NFC Settings</h5>

                        <div class="mb-3">
                            <label for="nfc_scan_cooldown" class="form-label">NFC Scan Cooldown (seconds)</label>
                            <input type="number" class="form-control" id="nfc_scan_cooldown" 
                                   name="nfc_scan_cooldown" value="30">
                            <small class="text-muted">Minimum time between scans of the same user</small>
                        </div>

                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="enable_qr_codes" 
                                   name="enable_qr_codes" checked>
                            <label class="form-check-label" for="enable_qr_codes">
                                Enable QR code generation
                            </label>
                        </div>

                        <hr class="my-4">

                        <h5 class="card-title mb-4">Security Settings</h5>

                        <div class="mb-3">
                            <label for="session_timeout" class="form-label">Session Timeout (minutes)</label>
                            <input type="number" class="form-control" id="session_timeout" 
                                   name="session_timeout" value="60">
                        </div>

                        <div class="mb-3">
                            <label for="password_min_length" class="form-label">Minimum Password Length</label>
                            <input type="number" class="form-control" id="password_min_length" 
                                   name="password_min_length" value="8">
                        </div>

                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="require_email_verification" 
                                   name="require_email_verification">
                            <label class="form-check-label" for="require_email_verification">
                                Require email verification for new accounts
                            </label>
                        </div>

                        <hr class="my-4">

                        <div class="d-flex justify-content-end gap-2">
                            <button type="reset" class="btn btn-outline-secondary">
                                <i class="fas fa-undo me-2"></i>Reset
                            </button>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Save Settings
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- System Information -->
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title mb-4">System Information</h5>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th width="30%">Platform</th>
                                <td>Flask / Python 3.11</td>
                            </tr>
                            <tr>
                                <th>Database</th>
                                <td>MySQL</td>
                            </tr>
                            <tr>
                                <th>Version</th>
                                <td>1.0.0</td>
                            </tr>
                            <tr>
                                <th>Last Updated</th>
                                <td>{{ now().strftime('%Y-%m-%d %H:%M:%S') }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Maintenance Actions -->
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title mb-4">Maintenance</h5>
                    <div class="d-flex gap-2 flex-wrap">
                        <button class="btn btn-warning" onclick="return confirm('Clear cache?')">
                            <i class="fas fa-broom me-2"></i>Clear Cache
                        </button>
                        <button class="btn btn-info">
                            <i class="fas fa-database me-2"></i>Backup Database
                        </button>
                        <button class="btn btn-secondary">
                            <i class="fas fa-sync me-2"></i>Run Diagnostics
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Create the settings template
os.makedirs('templates/system_manager', exist_ok=True)
settings_path = 'templates/system_manager/settings.html'

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(settings_html)

print(f"\n✅ Created missing template: {settings_path}")

print("\n" + "=" * 80)
print("✅ ALL TEMPLATE FIXES COMPLETE!")
print("=" * 80)
print("\n📋 What was fixed:")
print("  ✅ events.list → events.list_events")
print("  ✅ profile.view → profile.view_user_profile")
print("  ✅ Created system_manager/settings.html")
print("\n🔄 Restart Flask and test:")
print("  python app.py")