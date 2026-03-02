import os
import re

print("=" * 80)
print("🔍 DEEP SEARCH FOR DUPLICATE FUNCTIONS")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n1️⃣ SEARCHING FOR ALL delete_qualification DEFINITIONS")
print("-" * 80)

delete_qual_found = []
for i, line in enumerate(lines):
    if 'def delete_qualification' in line:
        delete_qual_found.append(i + 1)
        print(f"   Line {i+1}: {line.strip()}")
        # Show 3 lines before (decorators)
        if i >= 3:
            for j in range(max(0, i-3), i):
                print(f"   Line {j+1}: {lines[j].strip()}")

print(f"\n   Total found: {len(delete_qual_found)}")

print("\n2️⃣ SEARCHING FOR ALL qualifications DEFINITIONS")
print("-" * 80)

qual_found = []
for i, line in enumerate(lines):
    if 'def qualifications(' in line:
        qual_found.append(i + 1)
        print(f"   Line {i+1}: {line.strip()}")
        if i >= 3:
            for j in range(max(0, i-3), i):
                print(f"   Line {j+1}: {lines[j].strip()}")

print(f"\n   Total found: {len(qual_found)}")

print("\n3️⃣ CHECKING IF PROFILE_BP IS IMPORTED TWICE")
print("-" * 80)

import_found = []
for i, line in enumerate(lines):
    if 'profile_bp' in line and 'Blueprint' in line:
        import_found.append(i + 1)
        print(f"   Line {i+1}: {line.strip()}")

print(f"\n   Total blueprint definitions: {len(import_found)}")

# Now let's manually remove all duplicates by rewriting the file
print("\n" + "=" * 80)
print("🔧 COMPLETE FILE CLEANUP")
print("=" * 80)

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all function definitions
all_functions = re.findall(r'@profile_bp\.route.*?\ndef\s+(\w+)', content, re.DOTALL)
print(f"\n📋 All route functions found: {set(all_functions)}")

# Check for duplicates
from collections import Counter
function_counts = Counter(all_functions)
duplicates = {func: count for func, count in function_counts.items() if count > 1}

if duplicates:
    print(f"\n⚠️ DUPLICATES DETECTED:")
    for func, count in duplicates.items():
        print(f"   • {func}: appears {count} times")
    
    print("\n🔧 Removing ALL duplicate function definitions...")
    
    # Strategy: Keep first occurrence, remove all others
    seen_functions = set()
    new_lines = []
    skip_mode = False
    skip_function = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a function definition
        if line.strip().startswith('def '):
            func_match = re.match(r'\s*def\s+(\w+)', line)
            if func_match:
                func_name = func_match.group(1)
                
                if func_name in seen_functions:
                    # This is a duplicate - skip it
                    print(f"   ⚠️ Skipping duplicate: {func_name} at line {i+1}")
                    skip_mode = True
                    skip_function = func_name
                    
                    # Also remove decorators above (go back and remove last few lines if they're decorators)
                    while new_lines and new_lines[-1].strip().startswith('@'):
                        removed = new_lines.pop()
                        print(f"      Removed decorator: {removed.strip()}")
                    
                    i += 1
                    continue
                else:
                    seen_functions.add(func_name)
                    skip_mode = False
                    print(f"   ✅ Keeping first: {func_name} at line {i+1}")
        
        # Skip lines if we're in skip mode
        if skip_mode:
            # Continue skipping until we hit next function or decorator at same indentation
            if line.strip().startswith('@') and not line.strip().startswith('   '):
                skip_mode = False
            elif line.strip().startswith('def ') and not line.strip().startswith('   '):
                skip_mode = False
                # Don't skip this line, process it
                continue
            else:
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    # Write the cleaned file
    with open(profile_controller_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n✅ File cleaned and rewritten!")

else:
    print("\n✅ No duplicate functions found")

print("\n" + "=" * 80)
print("📊 VERIFICATION")
print("=" * 80)

# Re-read and verify
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    final_content = f.read()

final_functions = re.findall(r'def\s+(\w+)', final_content)
final_counts = Counter(final_functions)

print(f"\n   Final function counts:")
for func, count in sorted(final_counts.items()):
    status = "✅" if count == 1 else "⚠️"
    print(f"   {status} {func}: {count}")

print("\n" + "=" * 80)
print("✅ CLEANUP COMPLETE - Now try: python app.py")
print("=" * 80)