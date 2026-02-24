import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}NFC SETUP VERIFICATION{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'nfc_event_management')
    )
    cursor = conn.cursor()
    
    print(f"{Colors.GREEN}✓{Colors.END} Connected to database: {Colors.BOLD}{os.getenv('DB_NAME')}{Colors.END}\n")
    
    # Check existing tables
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking Existing Tables:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    cursor.execute("SHOW TABLES")
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    print(f"{Colors.YELLOW}Current tables in database:{Colors.END}")
    for table in existing_tables:
        print(f"  • {table}")
    
    # Check NFC-specific tables
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking NFC Tables:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    nfc_tables = {
        'connections': 'User networking connections',
        'networking_logs': 'NFC/QR scan activity logs',
        'event_checkins': 'Event check-in/out tracking',
        'admin_checkin_logs': 'Admin action audit trail',
        'nfc_scans': 'NFC scan logging',
        'nfc_scan_logs': 'Detailed NFC scan logs',
        'nfc_devices': 'Authorized NFC devices'
    }
    
    missing_tables = []
    for table, description in nfc_tables.items():
        if table in existing_tables:
            print(f"  {Colors.GREEN}✓{Colors.END} {table:20} - {description}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {table:20} - {description} {Colors.RED}(MISSING){Colors.END}")
            missing_tables.append(table)
    
    # Check users table NFC columns
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking Users Table NFC Columns:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    cursor.execute("DESCRIBE users")
    user_columns = [col[0] for col in cursor.fetchall()]
    
    nfc_user_columns = {
        'nfc_badge_id': 'Unique NFC badge identifier',
        'nfc_enabled': 'NFC functionality enabled',
        'last_nfc_scan': 'Last NFC scan timestamp'
    }
    
    missing_user_columns = []
    for col, description in nfc_user_columns.items():
        if col in user_columns:
            print(f"  {Colors.GREEN}✓{Colors.END} {col:20} - {description}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {col:20} - {description} {Colors.RED}(MISSING){Colors.END}")
            missing_user_columns.append(col)
    
    # Check attendance table NFC columns
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking Attendance Table NFC Columns:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    if 'attendance' in existing_tables:
        cursor.execute("DESCRIBE attendance")
        att_columns = [col[0] for col in cursor.fetchall()]
        
        nfc_att_columns = {
            'check_in_method': 'Check-in method (NFC/QR/Manual)',
            'check_out_method': 'Check-out method (NFC/QR/Manual)'
        }
        
        missing_att_columns = []
        for col, description in nfc_att_columns.items():
            if col in att_columns:
                print(f"  {Colors.GREEN}✓{Colors.END} {col:20} - {description}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {col:20} - {description} {Colors.RED}(MISSING){Colors.END}")
                missing_att_columns.append(col)
    else:
        print(f"  {Colors.YELLOW}○{Colors.END} Attendance table not found")
        missing_att_columns = []
    
    # Check if users have NFC badge IDs
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking NFC Badge IDs:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    if 'nfc_badge_id' in user_columns:
        cursor.execute("SELECT COUNT(*) FROM users WHERE nfc_badge_id IS NOT NULL AND nfc_badge_id != ''")
        badge_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        if badge_count == total_users and badge_count > 0:
            print(f"  {Colors.GREEN}✓{Colors.END} {badge_count}/{total_users} users have NFC badge IDs")
        elif badge_count > 0:
            print(f"  {Colors.YELLOW}●{Colors.END} {badge_count}/{total_users} users have NFC badge IDs")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {badge_count}/{total_users} users have NFC badge IDs")
    else:
        print(f"  {Colors.RED}✗{Colors.END} NFC badge ID column not yet added")
    
    # Check NFC controller file
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking NFC Controller Files:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    controller_path = 'src/controllers/nfc_controller.py'
    if os.path.exists(controller_path):
        print(f"  {Colors.GREEN}✓{Colors.END} {controller_path}")
    else:
        print(f"  {Colors.RED}✗{Colors.END} {controller_path} {Colors.RED}(MISSING){Colors.END}")
    
    # Check NFC templates
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Checking NFC Templates:{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    templates = {
        'templates/nfc/scanner.html': 'NFC/QR Scanner page',
        'templates/nfc/checkin_log.html': 'Real-time check-in dashboard',
        'templates/nfc/connections.html': 'My connections page'
    }
    
    missing_templates = []
    for template, description in templates.items():
        if os.path.exists(template):
            print(f"  {Colors.GREEN}✓{Colors.END} {template:35} - {description}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {template:35} - {description} {Colors.RED}(MISSING){Colors.END}")
            missing_templates.append(template)
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    all_good = True
    
    if missing_tables:
        all_good = False
        print(f"{Colors.YELLOW}Missing NFC Tables ({len(missing_tables)}):{Colors.END}")
        for table in missing_tables:
            print(f"  • {table}")
        print(f"\n{Colors.YELLOW}→ Run: python create_nfc_tables_migration.py{Colors.END}\n")
    else:
        print(f"{Colors.GREEN}✓ All NFC tables exist!{Colors.END}\n")
    
    if missing_user_columns or (missing_att_columns if 'attendance' in existing_tables else False):
        all_good = False
        print(f"{Colors.YELLOW}Missing NFC Columns:{Colors.END}")
        if missing_user_columns:
            print(f"  Users table: {', '.join(missing_user_columns)}")
        if missing_att_columns and 'attendance' in existing_tables:
            print(f"  Attendance table: {', '.join(missing_att_columns)}")
        print(f"\n{Colors.YELLOW}→ Run: python fix_nfc_database.py{Colors.END}\n")
    else:
        print(f"{Colors.GREEN}✓ All NFC columns exist!{Colors.END}\n")
    
    if badge_count == 0 and 'nfc_badge_id' in user_columns:
        all_good = False
        print(f"{Colors.YELLOW}No users have NFC badge IDs{Colors.END}")
        print(f"{Colors.YELLOW}→ Run: python fix_nfc_database.py{Colors.END}\n")
    
    if not os.path.exists(controller_path):
        all_good = False
        print(f"{Colors.YELLOW}NFC controller missing{Colors.END}")
        print(f"{Colors.YELLOW}→ Run: python fix_enhance_nfc_logic.py{Colors.END}\n")
    
    if missing_templates:
        all_good = False
        print(f"{Colors.YELLOW}Missing NFC templates ({len(missing_templates)}):{Colors.END}")
        for template in missing_templates:
            print(f"  • {template}")
        print(f"\n{Colors.YELLOW}→ Run the template creation scripts{Colors.END}\n")
    
    if all_good:
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}✅ NFC SYSTEM FULLY SET UP!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
        print(f"{Colors.CYAN}You can now:{Colors.END}")
        print(f"  1. Run: {Colors.BOLD}python app.py{Colors.END}")
        print(f"  2. Visit: {Colors.BOLD}http://localhost:5000/nfc/scanner{Colors.END}")
        print(f"  3. Test: {Colors.BOLD}http://localhost:5000/profile/my-nfc{Colors.END}")
        print(f"  4. View connections: {Colors.BOLD}http://localhost:5000/nfc/my-connections{Colors.END}")
        print()
    else:
        print(f"{Colors.YELLOW}Follow the instructions above to complete setup{Colors.END}\n")
    
except mysql.connector.Error as e:
    print(f"\n{Colors.RED}✗ Database Error: {e}{Colors.END}\n")
    print(f"{Colors.YELLOW}Make sure:{Colors.END}")
    print(f"  - MySQL is running")
    print(f"  - Database exists: {os.getenv('DB_NAME', 'nfc_event_management')}")
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