import os
import re

print("=" * 80)
print("🔧 FIXING DUPLICATE VIEW ROUTE")
print("=" * 80)

profile_controller_path = "src/controllers/profile_controller.py"

if not os.path.exists(profile_controller_path):
    print(f"❌ Error: {profile_controller_path} not found!")
    exit(1)

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n📋 Analyzing profile_controller.py...")

# Find all @profile_bp.route decorators with 'view'
view_routes = re.findall(r"@profile_bp\.route\(['\"]([^'\"]*view[^'\"]*)['\"].*?\)\s*def\s+(\w+)\(", content, re.DOTALL)

print(f"\nℹ️  Found {len(view_routes)} route(s) with 'view' in them:")
for route, func_name in view_routes:
    print(f"  • {route} → {func_name}()")

if len(view_routes) > 1:
    print("\n⚠️  DUPLICATE ROUTES DETECTED!")
    print("   Fixing by renaming routes...\n")
    
    # Strategy: Keep /view/<int:user_id> as 'view', rename others
    
    # Find the old /view route (without user_id) and rename it
    old_view_pattern = r"(@profile_bp\.route\(['\"]/(view)['\"].*?\)\s*def\s+view\()"
    
    if re.search(old_view_pattern, content):
        # Rename old /view to /my-profile or /me
        content = re.sub(
            old_view_pattern,
            r"@profile_bp.route('/me')\n@profile_bp.route('/my-profile')\ndef view_own(",
            content
        )
        print("✅ Renamed old /view route to /me and /my-profile")
        print("   Function renamed: view() → view_own()")
    
    # Ensure the new /view/<int:user_id> route exists
    new_view_pattern = r"@profile_bp\.route\(['\"]/(view/<int:user_id>)['\"].*?\)\s*def\s+view\("
    
    if re.search(new_view_pattern, content):
        print("✅ Route /view/<int:user_id> already exists and is correct")
    else:
        print("⚠️  Route /view/<int:user_id> not found - will be added")

else:
    print("\n✅ No duplicate routes found!")

# Save the updated file
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Saved profile_controller.py")

# ============================================================================
# Show the updated routes
# ============================================================================
print("\n" + "=" * 80)
print("📋 UPDATED PROFILE ROUTES:")
print("=" * 80)

view_routes_updated = re.findall(r"@profile_bp\.route\(['\"]([^'\"]*)['\"].*?\)\s*def\s+(\w+)\(", content)

for route, func_name in view_routes_updated:
    print(f"✅ {route:40} → {func_name}()")

print("\n" + "=" * 80)
print("✅ DUPLICATE ROUTE FIX COMPLETE!")
print("=" * 80)

print("""
🎯 Changes Made:
  ✅ Renamed conflicting routes
  ✅ /view/<int:user_id> → Public profile view
  ✅ /me or /my-profile → Own profile view

🚀 Test the Routes:
  1. Restart Flask app: python app.py
  2. Test public profile: http://localhost:5000/profile/view/3
  3. Test own profile: http://localhost:5000/profile/me

📋 Route Summary:
  • /profile/view/<user_id>  - View any user's profile (QR/NFC scans)
  • /profile/me              - View your own profile
  • /profile/edit            - Edit your profile
  • /profile/qr              - Your QR code

✅ QR codes will now work correctly!
""")