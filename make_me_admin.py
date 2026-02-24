import mysql.connector
from getpass import getpass

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

try:
    from database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 
    # Show all users
    print(f"{Colors.CYAN}Available users:{Colors.END}\n")
    cursor.execute("SELECT id, full_name, email, role FROM users ORDER BY id")
    users = cursor.fetchall()
    
    if not users:
        print(f"{Colors.RED}No users found in database!{Colors.END}")
        print(f"{Colors.YELLOW}Please register a user first at: http://localhost:5000/register{Colors.END}\n")
        exit(1)
    
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Current Role':<20}")
    print(f"{'-'*80}")
    for user in users:
        print(f"{user['id']:<5} {user['full_name']:<25} {user['email']:<30} {user['role']:<20}")
    
    print(f"\n{Colors.BOLD}Available roles:{Colors.END}")
    print(f"  1. {Colors.CYAN}attendee{Colors.END}        - Regular user (default)")
    print(f"  2. {Colors.YELLOW}event_admin{Colors.END}     - Can manage events")
    print(f"  3. {Colors.RED}system_manager{Colors.END}  - Full system access\n")
    
    # Get user choice
    try:
        user_id = int(input(f"{Colors.BOLD}Enter user ID to promote: {Colors.END}"))
    except ValueError:
        print(f"{Colors.RED}Invalid ID!{Colors.END}")
        exit(1)
    
    # Verify user exists
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    selected_user = cursor.fetchone()
    
    if not selected_user:
        print(f"{Colors.RED}User ID {user_id} not found!{Colors.END}")
        exit(1)
    
    print(f"\n{Colors.GREEN}Selected user:{Colors.END}")
    print(f"  Name: {selected_user['full_name']}")
    print(f"  Email: {selected_user['email']}")
    print(f"  Current Role: {selected_user['role']}\n")
    
    # Choose new role
    print(f"{Colors.BOLD}Select new role:{Colors.END}")
    print(f"  1. Event Admin")
    print(f"  2. System Manager")
    print(f"  3. Attendee (regular user)\n")
    
    role_choice = input(f"{Colors.BOLD}Enter choice (1-3): {Colors.END}").strip()
    
    role_map = {
        '1': 'event_admin',
        '2': 'system_manager',
        '3': 'attendee'
    }
    
    if role_choice not in role_map:
        print(f"{Colors.RED}Invalid choice!{Colors.END}")
        exit(1)
    
    new_role = role_map[role_choice]
    
    # Confirm
    print(f"\n{Colors.YELLOW}⚠ CONFIRM:{Colors.END}")
    print(f"  Change {selected_user['full_name']} ({selected_user['email']})")
    print(f"  From: {selected_user['role']}")
    print(f"  To:   {new_role}\n")
    
    confirm = input(f"{Colors.BOLD}Proceed? (yes/no): {Colors.END}").strip().lower()
    
    if confirm != 'yes':
        print(f"{Colors.RED}Operation cancelled{Colors.END}")
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
    print(f"  Role:  {Colors.BOLD}{new_role}{Colors.END}\n")
    
    if new_role == 'system_manager':
        print(f"{Colors.YELLOW}Access granted to:{Colors.END}")
        print(f"  • System Dashboard: http://localhost:5000/system")
        print(f"  • User Management:  http://localhost:5000/system/users")
        print(f"  • Create Admin:     http://localhost:5000/system/create-admin")
        print(f"  • System Settings:  http://localhost:5000/system/settings")
        print(f"  • System Logs:      http://localhost:5000/system/logs")
    elif new_role == 'event_admin':
        print(f"{Colors.YELLOW}Access granted to:{Colors.END}")
        print(f"  • Admin Dashboard:  http://localhost:5000/admin")
        print(f"  • Event Management: http://localhost:5000/admin/events")
        print(f"  • User Management:  http://localhost:5000/admin/users")
        print(f"  • Create User:      http://localhost:5000/admin/users/create")
        print(f"  • Reports:          http://localhost:5000/admin/reports")
    
    print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
    print(f"  1. Logout and login again")
    print(f"  2. Access admin panels with new privileges\n")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
    import traceback
    traceback.print_exc()