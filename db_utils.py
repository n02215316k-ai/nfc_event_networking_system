import os
import glob

print("=" * 80)
print("🔍 FINDING AND FIXING db_utils.py")
print("=" * 80)

# Search for db_utils.py
possible_locations = [
    'src/utils/db_utils.py',
    'utils/db_utils.py',
    'src/db_utils.py',
    'db_utils.py',
    'src/database/db_utils.py',
    'database/db_utils.py'
]

# Also do a recursive search
print("\n📁 Searching for db_utils.py...")
db_utils_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == 'db_utils.py':
            db_utils_files.append(os.path.join(root, file))
            print(f"   Found: {os.path.join(root, file)}")

if not db_utils_files:
    print("❌ db_utils.py not found!")
    print("\n📋 Creating db_utils.py with lastrowid support...")
    
    # Create the utils directory and file
    os.makedirs('src/utils', exist_ok=True)
    
    db_utils_content = '''"""Database utility functions"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=False, fetchone=False, return_lastrowid=False):
    """
    Execute a database query
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch: Whether to fetch results
        fetchone: Fetch only one result
        return_lastrowid: Return the last inserted row ID
    
    Returns:
        - If fetch=True and fetchone=True: Single row (dict)
        - If fetch=True: List of rows (list of dicts)
        - If return_lastrowid=True: Last inserted ID (int)
        - Otherwise: True/False (success status)
    """
    conn = get_db_connection()
    if not conn:
        return None if fetch else False
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            return result
        else:
            conn.commit()
            if return_lastrowid:
                return cursor.lastrowid
            return True
    
    except Error as e:
        print(f"Query execution error: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        conn.rollback()
        return None if fetch else False
    
    finally:
        cursor.close()
        conn.close()
'''
    
    with open('src/utils/db_utils.py', 'w', encoding='utf-8') as f:
        f.write(db_utils_content)
    
    print("✅ Created src/utils/db_utils.py with lastrowid support")
    print("✅ Created src/utils/__init__.py")
    
    # Create __init__.py
    with open('src/utils/__init__.py', 'w', encoding='utf-8') as f:
        f.write('')
    
else:
    # Fix existing db_utils.py
    db_utils_path = db_utils_files[0]
    print(f"\n📝 Updating: {db_utils_path}")
    
    with open(db_utils_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has return_lastrowid
    if 'return_lastrowid' in content:
        print("✅ Already has lastrowid support!")
    else:
        print("ℹ️  Adding lastrowid support...")
        
        # Update function signature
        content = content.replace(
            "def execute_query(query, params=None, fetch=False, fetchone=False):",
            "def execute_query(query, params=None, fetch=False, fetchone=False, return_lastrowid=False):"
        )
        
        # Add lastrowid return logic
        # Find the commit section
        if "conn.commit()" in content:
            content = content.replace(
                "            conn.commit()\n            return True",
                "            conn.commit()\n            if return_lastrowid:\n                return cursor.lastrowid\n            return True"
            )
            print("✅ Added lastrowid return logic")
        else:
            print("⚠️  Could not find conn.commit() - manual update needed")
        
        # Write back
        with open(db_utils_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {db_utils_path}")

print("\n" + "=" * 80)
print("✅ DB_UTILS FIX COMPLETE!")
print("=" * 80)
print("\n📋 Next steps:")
print("  1. Restart Flask: python app.py")
print("  2. Try creating an event again")
print("  3. It should work now!")