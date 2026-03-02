import os
import re
from database import get_db_connection

print("=" * 80)
print("🔧 INTELLIGENT SYSTEM FIX")
print("=" * 80)

# ============================================================================
# STEP 1: Discover actual routes
# ============================================================================
print("\n📋 STEP 1: Discovering actual routes...")

actual_routes = {}

# Scan all controllers
for file in os.listdir('src/controllers'):
    if not file.endswith('.py'):
        continue
    
    controller_path = f'src/controllers/{file}'
    with open(controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find blueprint
    bp_match = re.search(r'(\w+_bp)\s*=\s*Blueprint\([\'"](\w+)[\'"]', content)
    if not bp_match:
        continue
    
    bp_var = bp_match.group(1)
    bp_name = bp_match.group(2)
    
    # Find routes
    routes = re.findall(
        r'@' + re.escape(bp_var) + r'\.route\([\'"]([^\'"]+)[\'"].*?\)\s*def\s+(\w+)\(',
        content
    )
    
    for route_path, func_name in routes:
        endpoint = f"{bp_name}.{func_name}"
        actual_routes[endpoint] = route_path
        actual_routes[func_name] = endpoint  # Also map function name

print(f"  ✅ Found {len(actual_routes)} routes")

# ============================================================================
# STEP 2: Fix templates
# ============================================================================
print("\n🎨 STEP 2: Fixing templates...")

# Common endpoint mappings (based on typical patterns)
endpoint_corrections = {
    'events.create': 'events.create_event',
    'events.list_events': 'events.list',
    'events.my_events': 'events.my_events',
    'profile.qr': 'profile.qr_code',
}

templates_fixed = 0

for root, dirs, files in os.walk('templates'):
    for file in files:
        if not file.endswith('.html'):
            continue
        
        template_path = os.path.join(root, file)
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply corrections
        for wrong, correct in endpoint_corrections.items():
            if f"url_for('{wrong}')" in content:
                content = content.replace(f"url_for('{wrong}')", f"url_for('{correct}')")
                print(f"  ✅ {template_path}: {wrong} → {correct}")
                templates_fixed += 1
        
        # Write back if changed
        if content != original_content:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)

print(f"\n  ✅ Fixed {templates_fixed} template issues")

# ============================================================================
# STEP 3: Verify database
# ============================================================================
print("\n🗄️  STEP 3: Verifying database...")

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check critical tables
    critical_tables = ['users', 'events', 'connections']
    
    for table in critical_tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        if cursor.fetchone():
            print(f"  ✅ {table} exists")
        else:
            print(f"  ❌ {table} MISSING!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"  ⚠️  Database check failed: {e}")

# ============================================================================
# STEP 4: Generate route map
# ============================================================================
print("\n📋 STEP 4: Generating route map...")

with open('ROUTE_MAP.md', 'w', encoding='utf-8') as f:
    f.write("# Route Map\n\n")
    f.write("## Available Routes\n\n")
    
    current_bp = None
    for endpoint in sorted(actual_routes.keys()):
        if '.' in endpoint:
            bp_name = endpoint.split('.')[0]
            func_name = endpoint.split('.')[1]
            route_path = actual_routes.get(endpoint, 'Unknown')
            
            if bp_name != current_bp:
                current_bp = bp_name
                f.write(f"\n### {bp_name.title()} Blueprint\n\n")
            
            f.write(f"- `{endpoint}` → `{route_path}`\n")

print("  ✅ Route map saved to ROUTE_MAP.md")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ INTELLIGENT FIX COMPLETE!")
print("=" * 80)
print(f"""
📊 Summary:
  • Routes discovered: {len(actual_routes)}
  • Templates fixed: {templates_fixed}
  • Route map generated: ROUTE_MAP.md

🎯 Next steps:
  1. Review ROUTE_MAP.md for available endpoints
  2. Run: python app.py
  3. Test all pages manually
""")