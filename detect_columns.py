import mysql.connector

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}DETECTING DATABASE STRUCTURE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'nfc_event_management'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print(f"{Colors.GREEN}✓ Connected to database: nfc_event_management{Colors.END}\n")
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print(f"{Colors.BOLD}Tables in database:{Colors.END}\n")
    for table in tables:
        print(f"  • {table[0]}")
    
    # Check users table structure
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}USERS TABLE STRUCTURE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.END}\n")
    
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print(f"{Colors.BOLD}{'Column Name':<30} {'Type':<20} {'Null':<10} {'Key':<10}{Colors.END}")
    print(f"{'-'*80}")
    
    column_names = []
    for col in columns:
        column_names.append(col[0])
        print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {col[3]:<10}")
    
    # Show sample data
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}SAMPLE USER DATA (First 3 users){Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    cursor.execute("SELECT * FROM users LIMIT 3")
    users = cursor.fetchall()
    
    if users:
        for i, user in enumerate(users, 1):
            print(f"{Colors.BOLD}User {i}:{Colors.END}")
            for j, value in enumerate(user):
                col_name = column_names[j]
                # Truncate long values
                display_value = str(value)[:60] if value else 'NULL'
                print(f"  {col_name:<25} = {display_value}")
            print()
    else:
        print(f"{Colors.RED}No users found in database{Colors.END}\n")
    
    # Generate correct SQL
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}GENERATING CORRECT SQL QUERY{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Use this SELECT query for your users:{Colors.END}\n")
    
    # Build SELECT statement
    select_fields = ', '.join(column_names)
    print(f"{Colors.CYAN}SELECT {select_fields} FROM users{Colors.END}\n")
    
    # Detect password column
    password_col = None
    for col in column_names:
        if 'pass' in col.lower():
            password_col = col
            break
    
    if password_col:
        print(f"{Colors.GREEN}✓ Password column found: {Colors.BOLD}{password_col}{Colors.END}\n")
    else:
        print(f"{Colors.RED}✗ No password column found!{Colors.END}\n")
    
    # Detect email column
    email_col = None
    for col in column_names:
        if 'email' in col.lower() or 'mail' in col.lower():
            email_col = col
            break
    
    if email_col:
        print(f"{Colors.GREEN}✓ Email column found: {Colors.BOLD}{email_col}{Colors.END}\n")
    else:
        print(f"{Colors.RED}✗ No email column found!{Colors.END}\n")
    
    # Detect role column
    role_col = None
    for col in column_names:
        if 'role' in col.lower() or 'type' in col.lower():
            role_col = col
            break
    
    if role_col:
        print(f"{Colors.GREEN}✓ Role column found: {Colors.BOLD}{role_col}{Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}⚠ No role column found{Colors.END}\n")
    
    cursor.close()
    conn.close()
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ DETECTION COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Next: I'll create a custom check_users script based on your actual columns{Colors.END}\n")

except Exception as e:
    print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}\n")
    import traceback
    traceback.print_exc()