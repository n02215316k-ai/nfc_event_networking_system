import os
import re
from pathlib import Path

print("=" * 80)
print("🔍 COMPLETE SYSTEM AUDIT - NFC Event Networking System")
print("=" * 80)

# ============================================================================
# PART 1: FILE STRUCTURE ANALYSIS
# ============================================================================
print("\n📁 PART 1: FILE STRUCTURE")
print("-" * 80)

structure = {
    'Controllers': [],
    'Templates': [],
    'Static Files': [],
    'Database': [],
    'Config': []
}

# Scan controllers
if os.path.exists('src/controllers'):
    for file in os.listdir('src/controllers'):
        if file.endswith('.py'):
            structure['Controllers'].append(f"src/controllers/{file}")

# Scan templates
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            structure['Templates'].append(os.path.join(root, file))

# Scan static
for root, dirs, files in os.walk('static'):
    for file in files:
        structure['Static Files'].append(os.path.join(root, file))

# Check main files
main_files = ['app.py', 'database.py', 'config.py']
for file in main_files:
    if os.path.exists(file):
        structure['Config'].append(file)

# Print structure
for category, files in structure.items():
    print(f"\n{category}: ({len(files)} files)")
    for file in sorted(files)[:10]:  # Show first 10
        print(f"  ✅ {file}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more")

# ============================================================================
# PART 2: BLUEPRINT ANALYSIS
# ============================================================================
print("\n\n📋 PART 2: BLUEPRINT ANALYSIS")
print("-" * 80)

blueprints = {}

# Analyze app.py
if os.path.exists('app.py'):
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Find blueprint registrations
    registrations = re.findall(
        r'app\.register_blueprint\((\w+).*?url_prefix=[\'"]([^\'"]+)[\'"]',
        app_content
    )
    
    print("\n🔗 Registered Blueprints in app.py:")
    for bp_var, prefix in registrations:
        print(f"  ✅ {bp_var:20} → {prefix}")
        blueprints[bp_var] = {'prefix': prefix, 'routes': []}

# Analyze each controller
for controller_file in structure['Controllers']:
    with open(controller_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find blueprint definition
    bp_match = re.search(r'(\w+_bp)\s*=\s*Blueprint\([\'"](\w+)[\'"]', content)
    if bp_match:
        bp_var = bp_match.group(1)
        bp_name = bp_match.group(2)
        
        # Find all routes
        routes = re.findall(
            r'@' + re.escape(bp_var) + r'\.route\([\'"]([^\'"]+)[\'"].*?\)\s*def\s+(\w+)\(',
            content
        )
        
        controller_name = os.path.basename(controller_file)
        print(f"\n📄 {controller_name}:")
        print(f"  Blueprint: {bp_name} (variable: {bp_var})")
        print(f"  Routes: {len(routes)}")
        
        for route_path, func_name in routes[:5]:
            endpoint = f"{bp_name}.{func_name}"
            print(f"    • {endpoint:40} → {route_path}")
        
        if len(routes) > 5:
            print(f"    ... and {len(routes) - 5} more routes")

# ============================================================================
# PART 3: TEMPLATE ANALYSIS
# ============================================================================
print("\n\n🎨 PART 3: TEMPLATE ANALYSIS")
print("-" * 80)

template_issues = []

for template_path in structure['Templates']:
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all url_for calls
    url_fors = re.findall(r"url_for\(['\"]([^'\"]+)['\"]", content)
    
    if url_fors:
        print(f"\n📄 {template_path}:")
        print(f"  Links found: {len(url_fors)}")
        
        # Check for common issues
        for endpoint in url_fors:
            # Check format
            if '.' not in endpoint and endpoint not in ['static', 'index']:
                template_issues.append({
                    'file': template_path,
                    'issue': f"Missing blueprint in endpoint: {endpoint}",
                    'endpoint': endpoint
                })
                print(f"    ⚠️  {endpoint} (missing blueprint prefix?)")
            else:
                print(f"    ✅ {endpoint}")

# ============================================================================
# PART 4: DATABASE SCHEMA CHECK
# ============================================================================
print("\n\n🗄️  PART 4: DATABASE SCHEMA")
print("-" * 80)

try:
    from database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = [list(row.values())[0] for row in cursor.fetchall()]
    
    print(f"\n📊 Database Tables: {len(tables)}")
    
    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = cursor.fetchall()
        
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        
        print(f"\n  📋 {table} ({count} records)")
        for col in columns[:5]:
            print(f"    • {col['Field']:20} {col['Type']}")
        if len(columns) > 5:
            print(f"    ... and {len(columns) - 5} more columns")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Database connection error: {e}")

# ============================================================================
# PART 5: ISSUES SUMMARY
# ============================================================================
print("\n\n⚠️  PART 5: ISSUES FOUND")
print("-" * 80)

if template_issues:
    print(f"\n🔴 Found {len(template_issues)} template issues:")
    for issue in template_issues[:10]:
        print(f"  • {issue['file']}")
        print(f"    Issue: {issue['issue']}")
else:
    print("\n✅ No template issues found!")

# ============================================================================
# PART 6: RECOMMENDATIONS
# ============================================================================
print("\n\n💡 PART 6: RECOMMENDATIONS")
print("-" * 80)

print("""
Based on the audit, here are the recommended actions:

1. 🔧 Fix Template Endpoints
   - Update url_for() calls to match actual blueprint names
   
2. 🗄️  Database Schema
   - Verify all tables have correct structure
   - Check for any missing foreign keys
   
3. 📝 Code Quality
   - Ensure all routes have proper error handling
   - Add missing docstrings
   
4. 🧪 Testing
   - Test all navigation links
   - Verify all forms submit correctly
   - Check authentication flows
""")

print("\n" + "=" * 80)
print("✅ AUDIT COMPLETE - Results saved above")
print("=" * 80)

# Save results to file
with open('audit_results.txt', 'w', encoding='utf-8') as f:
    f.write("System Audit Results\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total Controllers: {len(structure['Controllers'])}\n")
    f.write(f"Total Templates: {len(structure['Templates'])}\n")
    f.write(f"Template Issues: {len(template_issues)}\n")

print("\n📄 Full results saved to: audit_results.txt")