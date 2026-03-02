import os

print("=" * 80)
print("🔧 SURGICAL FIX - CORRECTING PROFILE CONTROLLER")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("✅ File loaded")

# The problem: Lines 374-376 have wrong indentation
# Line 374: "from src.controllers.nfc_controller import generate_user_nfc_code, generate_event_qr_code"
# Line 375: "from io import BytesIO"  
# Line 376: "import base64"

# These should be at the function level (4 spaces), not module level (0 spaces)

# Fix: Remove the duplicate imports from line 374-376 
# (they're already at the top of the file)

# Find and remove lines 374-376
lines = content.split('\n')

print(f"\n🔍 Current line 374: {repr(lines[373][:80])}")
print(f"   Current line 375: {repr(lines[374][:80])}")
print(f"   Current line 376: {repr(lines[375][:80])}")

# Remove the problematic import lines (they're duplicates anyway)
if 'from src.controllers.nfc_controller' in lines[373]:
    print("\n🔧 Removing line 374 (duplicate import)")
    lines.pop(373)

if 'from io import BytesIO' in lines[373]:  # Index shifted after first pop
    print("🔧 Removing line 375 (duplicate import)")
    lines.pop(373)

if 'import base64' in lines[373]:  # Index shifted again
    print("🔧 Removing line 376 (duplicate import)")
    lines.pop(373)

# Reconstruct file
new_content = '\n'.join(lines)

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ Fixed! New file has {len(lines)} lines")

# Verify the fix
print("\n📋 Verifying my_nfc function (should start around line 371):")
for i in range(370, min(380, len(lines))):
    print(f"{i+1:4d} | {lines[i][:80]}")

# Make sure imports are at top
print("\n📋 Import section at top of file:")
for i in range(min(20, len(lines))):
    if 'import' in lines[i]:
        print(f"{i+1:3d} | {lines[i].strip()}")

print("\n" + "=" * 80)
print("✅ SURGICAL FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Try running Flask:")
print("   python app.py")