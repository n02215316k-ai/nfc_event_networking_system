import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIX 2: DATABASE IMPORTS IN CONTROLLERS{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Database helper function
DB_HELPER = '''
# Database helper function
def execute_query(query, params=None, fetch=False, fetchone=False):
    """Execute database query with proper connection handling"""
    from database import get_db_connection
    
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

# Find all controller files
controllers = []
for root, dirs, files in os.walk('src/controllers'):
    for file in files:
        if file.endswith('_controller.py'):
            controllers.append(os.path.join(root, file))

print(f"{Colors.CYAN}Found {len(controllers)} controllers{Colors.END}\n")

fixed = 0
for controller in controllers:
    print(f"{Colors.CYAN}Processing: {controller}{Colors.END}")
    
    with open(controller, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove bad imports
    content = re.sub(r'from database\.db import db\n?', '', content)
    content = re.sub(r'from database import db\n?', '', content)
    
    # Replace db.execute_query with execute_query
    if 'db.execute_query' in content:
        content = content.replace('db.execute_query', 'execute_query')
    
    # Add helper function if not present
    if 'def execute_query' not in content and 'execute_query(' in content:
        # Find where to insert (after imports)
        import_end = 0
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                import_end = i + 1
            elif line.strip() and not line.startswith('#'):
                break
        
        # Insert helper
        lines.insert(import_end + 1, DB_HELPER)
        content = '\n'.join(lines)
    
    if content != original:
        # Backup
        with open(controller + '.backup_db', 'w', encoding='utf-8') as f:
            f.write(original)
        
        # Write fixed
        with open(controller, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"{Colors.GREEN}✓ Fixed database calls{Colors.END}\n")
        fixed += 1
    else:
        print(f"{Colors.YELLOW}No changes needed{Colors.END}\n")

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ Fixed {fixed} controllers{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")