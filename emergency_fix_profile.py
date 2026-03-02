import os

print("=" * 80)
print("🚨 EMERGENCY FIX - RESTORING PROFILE CONTROLLER")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

# Read current content
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Current file: {len(lines)} lines")

# Find the problematic section (lines that lost indentation)
# These lines should be inside a function but are at module level

# Option 1: Find all lines between line 375-400 that have no indentation
# and remove them or comment them out temporarily

print("\n🔧 Commenting out problematic lines...")

for i in range(374, min(len(lines), 400)):
    line = lines[i]
    stripped = line.strip()
    
    # If line has content but no indentation (and it's not a function/class def)
    if stripped and not line.startswith((' ', '\t')) and not stripped.startswith(('def ', 'class ', '@', '#')):
        lines[i] = '# TEMP_DISABLED: ' + line
        print(f"   Disabled line {i+1}: {stripped[:60]}")

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Problematic lines commented out")
print("\n🔄 Try running Flask:")
print("   python app.py")
print("\n⚠️  The profile URL feature may not work until we properly fix the function")