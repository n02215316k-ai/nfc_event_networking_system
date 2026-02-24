import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADDING NFC ENHANCEMENTS TO EXISTING DATABASE{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

try:
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'nfc_event_management')
    )
    cursor = conn.cursor()
    print(f"{Colors.GREEN}✓{Colors.END} Connected to database: {os.getenv('DB_NAME')}")

    # Add NFC columns to existing users table
    print(f"\n{Colors.CYAN}Enhancing users table...{Colors.END}")
    
    # Check which columns already exist
    cursor.execute("DESCRIBE users")
    existing_columns = [col[0] for col in cursor.fetchall()]
    
    columns_to_add = []
    
    if 'nfc_enabled' not in existing_columns:
        columns_to_add.append("ADD COLUMN nfc_enabled BOOLEAN DEFAULT TRUE")
    
    if 'last_nfc_scan' not in existing_columns:
        columns_to_add.append("ADD COLUMN last_nfc_scan TIMESTAMP NULL")
    
    if columns_to_add:
        sql = f"ALTER TABLE users {', '.join(columns_to_add)}"
        cursor.execute(sql)
        print(f"{Colors.GREEN}✓{Colors.END} Added NFC columns to users table: {', '.join([c.split()[2] for c in columns_to_add])}")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} NFC columns already exist in users table")

    # Generate NFC badge IDs for existing users without one
    print(f"\n{Colors.CYAN}Generating NFC badge IDs for existing users...{Colors.END}")
    
    cursor.execute("SELECT id, full_name FROM users WHERE nfc_badge_id IS NULL OR nfc_badge_id = ''")
    users_without_badges = cursor.fetchall()
    
    if users_without_badges:
        import uuid
        for user_id, full_name in users_without_badges:
            nfc_badge_id = f"NFC-{uuid.uuid4().hex[:12].upper()}"
            cursor.execute("UPDATE users SET nfc_badge_id = %s WHERE id = %s", (nfc_badge_id, user_id))
            print(f"  {Colors.GREEN}✓{Colors.END} {full_name}: {nfc_badge_id}")
        print(f"{Colors.GREEN}✓{Colors.END} Generated NFC badge IDs for {len(users_without_badges)} users")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} All users already have NFC badge IDs")

    # Enable NFC for all users by default
    cursor.execute("UPDATE users SET nfc_enabled = TRUE WHERE nfc_enabled IS NULL")
    
    # Commit all changes
    conn.commit()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ NFC DATABASE ENHANCEMENTS COMPLETE!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Summary of changes:{Colors.END}")
    print(f"  {Colors.GREEN}✓{Colors.END} Added/verified NFC columns to users table")
    print(f"  {Colors.GREEN}✓{Colors.END} Generated NFC badge IDs for users")
    print(f"  {Colors.GREEN}✓{Colors.END} Enabled NFC functionality for all users")
    print()

except mysql.connector.Error as e:
    print(f"\n{Colors.RED}✗ Database Error: {e}{Colors.END}\n")
    print(f"{Colors.YELLOW}Make sure:{Colors.END}")
    print(f"  - MySQL is running")
    print(f"  - Database '{os.getenv('DB_NAME')}' exists")
    print(f"  - Credentials in .env are correct")
    print()
except Exception as e:
    print(f"\n{Colors.RED}✗ Error: {e}{Colors.END}\n")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print(f"{Colors.CYAN}Database connection closed{Colors.END}\n")