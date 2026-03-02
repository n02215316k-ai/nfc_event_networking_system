import os
import re

print("=" * 80)
print("🔧 PROPER FIX - RESTORING STRUCTURE WITHOUT LOSING FUNCTIONALITY")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

# Read current content
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"Current file: {len(lines)} lines")

# Find the function that contains line 375-376
print("\n🔍 Finding the function structure...")

# Look backwards from line 375 to find the function definition
function_start = None
for i in range(374, max(0, 374-100), -1):
    if lines[i].strip().startswith('def '):
        function_start = i
        print(f"   Found function at line {i+1}: {lines[i].strip()}")
        break

if not function_start:
    print("   ❌ Could not find function definition")
    exit(1)

# Get the proper indentation level for this function
function_indent = 0
for i in range(function_start + 1, min(function_start + 20, len(lines))):
    line = lines[i]
    if line.strip() and not line.strip().startswith('#'):
        function_indent = len(line) - len(line.lstrip())
        print(f"   Function body indent: {function_indent} spaces")
        break

# Now fix all lines from 375 onwards that lost indentation
print(f"\n🔧 Fixing indentation from line 375...")

# Find where this broken section ends (next function definition or decorator)
section_end = None
for i in range(374, min(len(lines), 500)):
    line = lines[i].strip()
    # Look for next function/route that's properly indented
    if i > 380 and (line.startswith('@') or (line.startswith('def ') and not lines[i].startswith(' '))):
        section_end = i
        print(f"   Broken section ends at line {i+1}")
        break

if not section_end:
    section_end = min(len(lines), 450)

# Fix the indentation
fixed_count = 0
for i in range(374, section_end):
    line = lines[i]
    stripped = line.strip()
    
    # Skip empty lines and comments
    if not stripped or stripped.startswith('#'):
        continue
    
    # Skip lines that are function definitions or decorators at module level
    if not line.startswith(' ') and (stripped.startswith(('def ', 'class ', '@profile_bp', '@login_required'))):
        continue
    
    # Get current indentation
    current_indent = len(line) - len(line.lstrip())
    
    # If line has wrong indentation (0 or less than function_indent)
    if current_indent < function_indent and stripped:
        # Re-indent to function level
        lines[i] = ' ' * function_indent + stripped
        print(f"   Fixed line {i+1}: {stripped[:60]}...")
        fixed_count += 1

print(f"\n✅ Fixed {fixed_count} lines")

# Reconstruct the file
new_content = '\n'.join(lines)

# Write back
with open(profile_controller_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ File updated: {len(lines)} lines")

# Show the fixed section
print("\n📋 Fixed section (lines 370-390):")
for i in range(369, min(390, len(lines))):
    indent_level = (len(lines[i]) - len(lines[i].lstrip())) // 4
    indent_marker = '│   ' * indent_level
    print(f"{i+1:4d} {indent_marker}{lines[i].strip()[:70]}")

print("\n" + "=" * 80)
print("✅ PROPER FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Try running Flask:")
print("   python app.py")