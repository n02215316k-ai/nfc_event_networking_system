import os

print("=" * 80)
print("🔧 FIXING DUPLICATE ROUTE DEFINITIONS")
print("=" * 80)

profile_controller_path = 'src/controllers/profile_controller.py'

with open(profile_controller_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of delete_qualification
import re
delete_qual_matches = list(re.finditer(r'@profile_bp\.route\([\'"]\/delete-qualification', content))
qualifications_route_matches = list(re.finditer(r'@profile_bp\.route\([\'"]\/qualifications[\'"]', content))

print(f"\n📊 Found {len(delete_qual_matches)} delete_qualification route(s)")
print(f"📊 Found {len(qualifications_route_matches)} qualifications route(s)")

if len(delete_qual_matches) > 1:
    print("\n⚠️ DUPLICATE delete_qualification routes found!")
    print("   Removing duplicates...")
    
    # Split content into lines
    lines = content.split('\n')
    
    # Find line numbers of all delete_qualification definitions
    delete_qual_lines = []
    for i, line in enumerate(lines):
        if "@profile_bp.route('/delete-qualification" in line or '@profile_bp.route("/delete-qualification' in line:
            delete_qual_lines.append(i)
    
    if len(delete_qual_lines) > 1:
        # Keep only the first occurrence, remove others
        # Find the end of each function (next @profile_bp or end of file)
        functions_to_remove = []
        
        for line_num in delete_qual_lines[1:]:  # Skip first, remove others
            # Find the end of this function
            start = line_num
            end = start + 1
            indent_level = len(lines[start + 1]) - len(lines[start + 1].lstrip())
            
            # Find where function ends (next decorator or same/less indentation)
            while end < len(lines):
                if lines[end].strip() and not lines[end].startswith(' ' * indent_level):
                    if lines[end].startswith('@') or (lines[end].strip() and len(lines[end]) - len(lines[end].lstrip()) < indent_level):
                        break
                end += 1
            
            functions_to_remove.append((start, end))
            print(f"   Found duplicate at lines {start+1} to {end+1}")
        
        # Remove duplicates from end to beginning to maintain line numbers
        for start, end in reversed(functions_to_remove):
            del lines[start:end]
            print(f"   ✅ Removed duplicate function (lines {start+1}-{end+1})")
        
        # Write back
        content = '\n'.join(lines)
        with open(profile_controller_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n✅ Duplicate routes removed!")

if len(qualifications_route_matches) > 1:
    print("\n⚠️ DUPLICATE qualifications routes found!")
    print("   Removing duplicates...")
    
    lines = content.split('\n')
    qual_lines = []
    
    for i, line in enumerate(lines):
        if "@profile_bp.route('/qualifications')" in line or '@profile_bp.route("/qualifications")' in line:
            qual_lines.append(i)
    
    if len(qual_lines) > 1:
        functions_to_remove = []
        
        for line_num in qual_lines[1:]:
            start = line_num
            end = start + 1
            
            while end < len(lines):
                if lines[end].strip().startswith('@profile_bp') or (end > start + 50):
                    break
                end += 1
            
            functions_to_remove.append((start, end))
        
        for start, end in reversed(functions_to_remove):
            del lines[start:end]
            print(f"   ✅ Removed duplicate qualifications route")
        
        content = '\n'.join(lines)
        with open(profile_controller_path, 'w', encoding='utf-8') as f:
            f.write(content)

# Re-read to verify
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    final_content = f.read()

final_delete_matches = len(list(re.finditer(r'@profile_bp\.route\([\'"]\/delete-qualification', final_content)))
final_qual_matches = len(list(re.finditer(r'@profile_bp\.route\([\'"]\/qualifications[\'"]', final_content)))

print("\n" + "=" * 80)
print("📊 FINAL COUNT:")
print("=" * 80)
print(f"   delete_qualification routes: {final_delete_matches}")
print(f"   qualifications routes: {final_qual_matches}")

if final_delete_matches == 1 and final_qual_matches == 1:
    print("\n✅ ALL DUPLICATES REMOVED!")
    print("\n🔄 Now restart Flask:")
    print("   python app.py")
else:
    print("\n⚠️ Manual intervention needed")
    print("   Please check src/controllers/profile_controller.py")

print("\n" + "=" * 80)