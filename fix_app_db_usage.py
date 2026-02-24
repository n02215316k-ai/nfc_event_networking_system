class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING db USAGE IN app.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_db_fix', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_db_fix{Colors.END}\n")

original = content

# Add helper function at the top after imports
helper_function = '''
# Database helper function
def execute_query(query, params=None, fetch=False, fetchone=False):
    """Execute database query with proper connection handling"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchone() if fetchone else cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid if cursor.lastrowid else True
        
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.close()
        return None

'''

# Find where to insert (after imports, before first route)
import re

# Find the first @app.route
first_route = re.search(r'\n@app\.route', content)

if first_route and 'def execute_query' not in content:
    # Insert helper function before first route
    insert_pos = first_route.start()
    content = content[:insert_pos] + '\n' + helper_function + content[insert_pos:]
    print(f"{Colors.GREEN}✓ Added execute_query helper function{Colors.END}")

# Replace db.execute_query with execute_query
content = content.replace('db.execute_query(', 'execute_query(')

if content != original:
    # Write fixed content
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓ Replaced db.execute_query with execute_query{Colors.END}\n")
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ app.py FIXED!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Changes made:{Colors.END}")
    print(f"  • Added execute_query() helper function")
    print(f"  • Replaced db.execute_query() calls\n")
    
    print(f"{Colors.BOLD}Now restart Flask:{Colors.END}")
    print(f"  {Colors.CYAN}python app.py{Colors.END}\n")
else:
    print(f"{Colors.YELLOW}No changes needed{Colors.END}\n")