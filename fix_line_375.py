import os

print("=" * 80)
print("🔧 FIXING LINE 375 IN PROFILE CONTROLLER")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"✅ Found profile controller with {len(lines)} lines")

# Show lines around 375
print("\n📋 Lines 370-380:")
for i in range(369, min(380, len(lines))):
    marker = ">>>" if i == 374 else "   "
    print(f"{marker} {i+1:4d} | {repr(lines[i])}")

# Remove line 375 (index 374) if it's an import statement
if lines[374].strip().startswith('import io'):
    print(f"\n🔧 Removing problematic line 375: {repr(lines[374])}")
    lines.pop(374)
    print("✅ Line removed!")

# Also check for any other misplaced imports in that area
removed_count = 0
i = 370
while i < min(len(lines), 385):
    line = lines[i]
    # If it's an import statement with indentation (not at module level)
    if (line.startswith('    import ') or line.startswith('\timport ')) and 'def ' not in lines[max(0, i-5):i]:
        print(f"🔧 Removing misplaced import at line {i+1}: {repr(line.strip())}")
        lines.pop(i)
        removed_count += 1
    else:
        i += 1

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ Fixed! Removed {removed_count + 1} problematic line(s)")
print(f"   New file has {len(lines)} lines")

# Verify imports are at the top
print("\n📋 Verifying imports at top of file:")
for i in range(min(30, len(lines))):
    if 'import' in lines[i].lower():
        print(f"   {i+1:3d} | {lines[i].strip()}")

print("\n" + "=" * 80)
print("✅ FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Try running Flask again:")
print("   python app.py")