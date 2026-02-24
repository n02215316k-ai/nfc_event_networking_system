import os
import re

print("\n" + "="*70)
print("UPDATING BASE TEMPLATE")
print("="*70 + "\n")

base_template = 'templates/base.html'

if os.path.exists(base_template):
    with open(base_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    with open(base_template + '.backup_nav', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Replace old navbar with include
    # Find existing navbar
    navbar_pattern = r'<nav class="navbar[^>]*>.*?</nav>'
    
    if re.search(navbar_pattern, content, re.DOTALL):
        new_nav = '{% include "partials/navigation.html" %}'
        content = re.sub(navbar_pattern, new_nav, content, flags=re.DOTALL, count=1)
        
        with open(base_template, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Updated base.html with dynamic navigation\n")
    else:
        print("⚠ Could not find navbar in base.html")
        print("  Manually add: {% include \"partials/navigation.html\" %}\n")
else:
    print("❌ base.html not found\n")