import mysql.connector

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}MAKE USER ADMIN/SYSTEM MANAGER{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change if you have a password
    'database': 'event_social_network'
}

print(f"{Colors.YELLOW}Enter your MySQL credentials:{Colors.END}\n")

# Get database credentials
db_host = input(f"Host (default: localhost): ").strip() or 'localhost'
db_user = input(f"Username (default: root): ").strip() or 'root'
db_pass = input(f"Password (press Enter if none): ").strip()
db_name = input(f"Database (default: event_social_network): ").strip() or 'event_social_network'

print()

try:
    # Connect to database
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    
    cursor = conn.cursor(dictionary=True)
    
    print(f"{Colors.GREEN}✓ Connected to database!{Colors.END}\n")
    
    # Show all users
    print(f"{Colors.CYAN}Available users:{Colors.END}\n")
    cursor.execute("SELECT id, full_name, email, role FROM users ORDER BY id")
    users = cursor.fetchall()
    
    if not users:
        print(f"{Colors.RED}No users found in database!{Colors.END}")
        print(f"{Colors.YELLOW}Please register a user first at: http://localhost:5000/register{Colors.END}\n")
        exit(1)
    
    # Display users in a table
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Current Role':<20}")
    print(f"{'-'*85}")
    for user in users:
        role_color = Colors.RED if user['role'] == 'system_manager' else (Colors.YELLOW if user['role'] == 'event_admin' else Colors.CYAN)
        print(f"{user['id']:<5} {user['full_name']:<25} {user['email']:<30} {role_color}{user['role']:<20}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Available roles:{Colors.END}")
    print(f"  1. {Colors.CYAN}attendee{Colors.END}        - Regular user (default)")
    print(f"  2. {Colors.YELLOW}event_admin{Colors.END}     - Can manage events")
    print(f"  3. {Colors.RED}system_manager{Colors.END}  - Full system access\n")
    
    # Get user choice
    try:
        user_id = int(input(f"{Colors.BOLD}Enter user ID to promote: {Colors.END}"))
    except ValueError:
        print(f"{Colors.RED}Invalid ID!{Colors.END}")
        cursor.close()
        conn.close()
        exit(1)
    
    # Verify user exists
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    selected_user = cursor.fetchone()
    
    if not selected_user:
        print(f"{Colors.RED}User ID {user_id} not found!{Colors.END}")
        cursor.close()
        conn.close()
        exit(1)
    
    print(f"\n{Colors.GREEN}Selected user:{Colors.END}")
    print(f"  ID:    {selected_user['id']}")
    print(f"  Name:  {selected_user['full_name']}")
    print(f"  Email: {selected_user['email']}")
    print(f"  Current Role: {selected_user['role']}\n")
    
    # Choose new role
    print(f"{Colors.BOLD}Select new role:{Colors.END}")
    print(f"  1. Event Admin (manage events, users)")
    print(f"  2. System Manager (full system access)")
    print(f"  3. Attendee (regular user)\n")
    
    role_choice = input(f"{Colors.BOLD}Enter choice (1-3): {Colors.END}").strip()
    
    role_map = {
        '1': 'event_admin',
        '2': 'system_manager',
        '3': 'attendee'
    }
    
    if role_choice not in role_map:
        print(f"{Colors.RED}Invalid choice!{Colors.END}")
        cursor.close()
        conn.close()
        exit(1)
    
    new_role = role_map[role_choice]
    
    # Confirm
    print(f"\n{Colors.YELLOW}⚠ CONFIRM:{Colors.END}")
    print(f"  Change {Colors.BOLD}{selected_user['full_name']}{Colors.END} ({selected_user['email']})")
    print(f"  From: {Colors.CYAN}{selected_user['role']}{Colors.END}")
    print(f"  To:   {Colors.GREEN}{new_role}{Colors.END}\n")
    
    confirm = input(f"{Colors.BOLD}Type 'yes' to confirm: {Colors.END}").strip().lower()
    
    if confirm != 'yes':
        print(f"\n{Colors.RED}Operation cancelled{Colors.END}")
        cursor.close()
        conn.close()
        exit(0)
    
    # Update role
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ ROLE UPDATED SUCCESSFULLY!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Updated user:{Colors.END}")
    print(f"  Name:  {selected_user['full_name']}")
    print(f"  Email: {selected_user['email']}")
    print(f"  Role:  {Colors.BOLD}{Colors.GREEN}{new_role}{Colors.END}\n")
    
    if new_role == 'system_manager':
        print(f"{Colors.BOLD}{Colors.YELLOW}System Manager Access Granted:{Colors.END}")
        print(f"  {Colors.GREEN}✓{Colors.END} System Dashboard:     http://localhost:5000/system")
        print(f"  {Colors.GREEN}✓{Colors.END} User Management:      http://localhost:5000/system/users")
        print(f"  {Colors.GREEN}✓{Colors.END} Create Admin:         http://localhost:5000/system/create-admin")
        print(f"  {Colors.GREEN}✓{Colors.END} System Settings:      http://localhost:5000/system/settings")
        print(f"  {Colors.GREEN}✓{Colors.END} System Logs:          http://localhost:5000/system/logs")
        print(f"  {Colors.GREEN}✓{Colors.END} Admin Dashboard:      http://localhost:5000/admin")
        print(f"  {Colors.GREEN}✓{Colors.END} Event Management:     http://localhost:5000/admin/events")
        print(f"  {Colors.GREEN}✓{Colors.END} Create Users:         http://localhost:5000/admin/users/create")
    elif new_role == 'event_admin':
        print(f"{Colors.BOLD}{Colors.YELLOW}Event Admin Access Granted:{Colors.END}")
        print(f"  {Colors.GREEN}✓{Colors.END} Admin Dashboard:      http://localhost:5000/admin")
        print(f"  {Colors.GREEN}✓{Colors.END} Event Management:     http://localhost:5000/admin/events")
        print(f"  {Colors.GREEN}✓{Colors.END} User Management:      http://localhost:5000/admin/users")
        print(f"  {Colors.GREEN}✓{Colors.END} Create Users:         http://localhost:5000/admin/users/create")
        print(f"  {Colors.GREEN}✓{Colors.END} Reports & Analytics:  http://localhost:5000/admin/reports")
    else:
        print(f"{Colors.YELLOW}Regular user access (no admin privileges){Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}Next steps:{Colors.END}")
    print(f"  1. {Colors.YELLOW}Logout{Colors.END} from the application (if logged in)")
    print(f"  2. {Colors.YELLOW}Login again{Colors.END} with the updated account")
    print(f"  3. {Colors.YELLOW}Access admin panels{Colors.END} with new privileges\n")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"\n{Colors.RED}❌ Database Error:{Colors.END}")
    print(f"{Colors.RED}{str(e)}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Common issues:{Colors.END}")
    print(f"  • Wrong MySQL credentials")
    print(f"  • Database doesn't exist")
    print(f"  • MySQL server not running\n")
    
    print(f"{Colors.CYAN}Try running MySQL:{Colors.END}")
    print(f"  • Start XAMPP/WAMP")
    print(f"  • Or: mysql -u root -p\n")

except Exception as e:
    print(f"\n{Colors.RED}❌ Unexpected Error:{Colors.END}")
    print(f"{Colors.RED}{str(e)}{Colors.END}\n")
    import traceback
    traceback.print_exc()