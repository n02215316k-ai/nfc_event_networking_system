import re

print("=" * 80)
print("🔧 REMOVING DUPLICATE FUNCTIONS FROM PROFILE CONTROLLER")
print("=" * 80)

profile_path = "src/controllers/profile_controller.py"

with open(profile_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all function definitions
functions = re.findall(r'@profile_bp\.route.*?\ndef (\w+)\(', content, re.DOTALL)

print(f"\n📊 Found {len(functions)} route functions")
print("Functions:", functions)

# Count occurrences
from collections import Counter
func_counts = Counter(functions)

duplicates = {name: count for name, count in func_counts.items() if count > 1}

if duplicates:
    print(f"\n⚠️  DUPLICATES FOUND: {duplicates}")
    
    for func_name, count in duplicates.items():
        print(f"\n🔍 Finding all {count} instances of {func_name}()...")
        
        # Find all complete function blocks for this name
        pattern = rf'(@profile_bp\.route.*?(?=@profile_bp\.route|$))'
        blocks = re.findall(pattern, content, re.DOTALL)
        
        matching_blocks = []
        for block in blocks:
            if f'def {func_name}(' in block:
                matching_blocks.append(block)
        
        print(f"   Found {len(matching_blocks)} code blocks")
        
        if len(matching_blocks) > 1:
            print(f"\n   Keeping the LAST occurrence (most complete)")
            print(f"   Removing {len(matching_blocks) - 1} duplicate(s)")
            
            # Remove all but the last occurrence
            for i, block in enumerate(matching_blocks[:-1]):
                print(f"   ❌ Removing duplicate {i+1}")
                content = content.replace(block, '', 1)
    
    # Save cleaned content
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Removed duplicate functions")

else:
    print("\n✅ No duplicates found (but error says otherwise...)")
    print("   Searching more carefully...")
    
    # Look for the specific function mentioned in error
    pattern = r'(@profile_bp\.route.*?def view_user_profile\(.*?(?=\n@profile_bp\.route|\nclass |\Z))'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if len(matches) > 1:
        print(f"\n⚠️  Found {len(matches)} view_user_profile blocks!")
        print("   Keeping only the last one...")
        
        for match in matches[:-1]:
            content = content.replace(match, '', 1)
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Cleaned up duplicates")

print("\n" + "=" * 80)
print("✅ PROFILE CONTROLLER CLEANED")
print("=" * 80)

print("\n🚀 Now try: python app.py")