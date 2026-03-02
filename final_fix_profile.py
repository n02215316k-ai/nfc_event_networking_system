import os

print("=" * 80)
print("🔧 FINAL FIX - CORRECTING PROFILE CONTROLLER")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"✅ File loaded with {len(lines)} lines")

# Show the problem area
print("\n📋 Lines 370-380 (BEFORE FIX):")
for i in range(369, min(380, len(lines))):
    indent = len(lines[i]) - len(lines[i].lstrip())
    print(f"{i+1:4d} [{indent:2d}sp] {repr(lines[i].rstrip())}")

# The problem: Lines 372-373 are imports that should be removed
# Line 372: "    from src.controllers.nfc_controller import..."
# Line 373: "from io import BytesIO" (no indentation - WRONG!)

# These imports are already at the top, so we delete them
print("\n🔧 Removing duplicate/misplaced imports...")

# Remove line 373 first (the one with no indentation)
if 'from io import BytesIO' in lines[372] and not lines[372].startswith(' '):
    print(f"   Removing line 373: {repr(lines[372].strip())}")
    lines.pop(372)

# Remove line 372 (now at index 371 after previous pop)
if 'from src.controllers.nfc_controller' in lines[371]:
    print(f"   Removing line 372: {repr(lines[371].strip())}")
    lines.pop(371)

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ Fixed! New file has {len(lines)} lines")

# Show the fixed area
print("\n📋 Lines 370-380 (AFTER FIX):")
for i in range(369, min(380, len(lines))):
    indent = len(lines[i]) - len(lines[i].lstrip())
    print(f"{i+1:4d} [{indent:2d}sp] {lines[i].rstrip()[:70]}")

print("\n" + "=" * 80)
print("✅ FINAL FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Try running Flask:")
print("   python app.py")