import os
import sys

print("=" * 80)
print("🚀 AUTO-UPDATING NAVIGATION FOR ALL USER ROLES")
print("=" * 80)

scripts = [
    'auto_update_navigation.py',
    'auto_update_app_session.py',
    'auto_fix_home_routes.py'
]

for script in scripts:
    print(f"\n▶️  Running {script}...")
    try:
        exec(open(script).read())
        print(f"✅ {script} completed!")
    except Exception as e:
        print(f"❌ Error in {script}: {e}")

print("\n" + "=" * 80)
print("✅ ALL UPDATES COMPLETE!")
print("=" * 80)
print("\n📋 Next steps:")
print("  1. Restart your Flask app: python app.py")
print("  2. Login with different user roles to test")
print("  3. System Manager will see all admin menus")
print("  4. Event Admin will see event management menus")
print("  5. Attendees will see standard user menus")
print("\n🎉 Done! Refresh your browser.")