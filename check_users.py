import mysql.connector
from tabulate import tabulate
import bcrypt

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}DATABASE USER CHECKER - NFC Event Management{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'nfc_event_management'
}

try:
    # Connect to database
    print(f"{Colors.CYAN}Connecting to database...{Colors.END}")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    print(f"{Colors.GREEN}✓ Connected successfully!{Colors.END}\n")
    
    # Get all users
    cursor.execute("""
        SELECT id, full_name, email, password, role, nfc_badge_id, 
               phone, job_title, company, created_at 
        FROM users 
        ORDER BY 
            CASE role 
                WHEN 'system_manager' THEN 1 
                WHEN 'event_admin' THEN 2 
                WHEN 'attendee' THEN 3 
            END,
            id
    """)
    
    users = cursor.fetchall()
    
    if not users:
        print(f"{Colors.RED}❌ No users found in database!{Colors.END}\n")
        exit(1)
    
    # ============================================================================
    # SUMMARY STATISTICS
    # ============================================================================
    total_users = len(users)
    system_managers = sum(1 for u in users if u['role'] == 'system_manager')
    event_admins = sum(1 for u in users if u['role'] == 'event_admin')
    attendees = sum(1 for u in users if u['role'] == 'attendee')
    
    print(f"{Colors.BOLD}{Colors.MAGENTA}📊 USER STATISTICS{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")
    
    stats_data = [
        [f"{Colors.BOLD}Total Users{Colors.END}", f"{Colors.CYAN}{total_users}{Colors.END}"],
        [f"{Colors.RED}System Managers{Colors.END}", f"{Colors.RED}{system_managers}{Colors.END}"],
        [f"{Colors.YELLOW}Event Admins{Colors.END}", f"{Colors.YELLOW}{event_admins}{Colors.END}"],
        [f"{Colors.GREEN}Attendees{Colors.END}", f"{Colors.GREEN}{attendees}{Colors.END}"],
    ]
    
    print(tabulate(stats_data, tablefmt='simple'))
    
    # ============================================================================
    # DETAILED USER LIST
    # ============================================================================
    print(f"\n{Colors.BOLD}{Colors.CYAN}👥 ALL USERS - DETAILED VIEW{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    for user in users:
        # Role coloring
        if user['role'] == 'system_manager':
            role_color = Colors.RED
            role_icon = "🔴"
        elif user['role'] == 'event_admin':
            role_color = Colors.YELLOW
            role_icon = "🟡"
        else:
            role_color = Colors.GREEN
            role_icon = "🟢"
        
        print(f"{Colors.BOLD}{'─'*80}{Colors.END}")
        print(f"{role_icon} {Colors.BOLD}User ID: {user['id']}{Colors.END}")
        print(f"{Colors.BOLD}{'─'*80}{Colors.END}")
        
        user_details = [
            ["Full Name", user['full_name']],
            ["Email", f"{Colors.CYAN}{user['email']}{Colors.END}"],
            ["Password (Hashed)", f"{Colors.YELLOW}{user['password'][:50]}...{Colors.END}"],
            ["Role", f"{role_color}{Colors.BOLD}{user['role'].upper()}{Colors.END}"],
            ["NFC Badge ID", user['nfc_badge_id'] or 'Not assigned'],
            ["Phone", user['phone'] or 'N/A'],
            ["Job Title", user['job_title'] or 'N/A'],
            ["Company", user['company'] or 'N/A'],
            ["Created", user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else 'N/A'],
        ]
        
        print(tabulate(user_details, tablefmt='simple'))
        print()
    
    # ============================================================================
    # COMPACT TABLE VIEW
    # ============================================================================
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}📋 COMPACT TABLE VIEW{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")
    
    table_data = []
    headers = [
        f"{Colors.BOLD}ID{Colors.END}",
        f"{Colors.BOLD}Name{Colors.END}",
        f"{Colors.BOLD}Email{Colors.END}",
        f"{Colors.BOLD}Role{Colors.END}",
        f"{Colors.BOLD}NFC Badge{Colors.END}"
    ]
    
    for user in users:
        if user['role'] == 'system_manager':
            role_display = f"{Colors.RED}SYSTEM_MANAGER{Colors.END}"
        elif user['role'] == 'event_admin':
            role_display = f"{Colors.YELLOW}EVENT_ADMIN{Colors.END}"
        else:
            role_display = f"{Colors.GREEN}ATTENDEE{Colors.END}"
        
        table_data.append([
            user['id'],
            user['full_name'][:20],
            user['email'][:30],
            role_display,
            user['nfc_badge_id'] or 'N/A'
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # ============================================================================
    # PASSWORD TEST UTILITY
    # ============================================================================
    print(f"\n{Colors.BOLD}{Colors.YELLOW}🔐 PASSWORD VERIFICATION UTILITY{Colors.END}")
    print(f"{Colors.YELLOW}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Test if a password matches a user account{Colors.END}\n")
    
    while True:
        test_choice = input(f"{Colors.BOLD}Do you want to test a password? (y/n): {Colors.END}").strip().lower()
        
        if test_choice != 'y':
            break
        
        test_email = input(f"\n{Colors.CYAN}Enter email to test: {Colors.END}").strip()
        test_password = input(f"{Colors.CYAN}Enter password to verify: {Colors.END}").strip()
        
        # Find user
        test_user = next((u for u in users if u['email'] == test_email), None)
        
        if not test_user:
            print(f"{Colors.RED}✗ Email not found!{Colors.END}\n")
            continue
        
        # Verify password
        try:
            if bcrypt.checkpw(test_password.encode('utf-8'), test_user['password'].encode('utf-8')):
                print(f"\n{Colors.GREEN}✓ PASSWORD CORRECT!{Colors.END}")
                print(f"{Colors.GREEN}User: {test_user['full_name']} ({test_user['role']}){Colors.END}\n")
            else:
                print(f"\n{Colors.RED}✗ PASSWORD INCORRECT!{Colors.END}\n")
        except Exception as e:
            print(f"\n{Colors.RED}✗ Error verifying password: {e}{Colors.END}\n")
    
    # ============================================================================
    # EXPORT OPTIONS
    # ============================================================================
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}💾 EXPORT OPTIONS{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")
    
    export_choice = input(f"{Colors.BOLD}Export users to CSV? (y/n): {Colors.END}").strip().lower()
    
    if export_choice == 'y':
        import csv
        from datetime import datetime
        
        filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'full_name', 'email', 'role', 'nfc_badge_id', 'phone', 
                         'job_title', 'company', 'created_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for user in users:
                user_copy = user.copy()
                user_copy.pop('password', None)  # Don't export passwords
                if user_copy['created_at']:
                    user_copy['created_at'] = user_copy['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow(user_copy)
        
        print(f"{Colors.GREEN}✓ Users exported to: {filename}{Colors.END}\n")
    
    # ============================================================================
    # ADMIN CREDENTIALS FOR LOGIN
    # ============================================================================
    print(f"\n{Colors.BOLD}{Colors.RED}🔑 ADMIN ACCOUNTS FOR LOGIN{Colors.END}")
    print(f"{Colors.RED}{'='*80}{Colors.END}\n")
    
    admins = [u for u in users if u['role'] in ['system_manager', 'event_admin']]
    
    if admins:
        print(f"{Colors.YELLOW}Copy these credentials to login:{Colors.END}\n")
        for admin in admins:
            role_label = "SYSTEM MANAGER" if admin['role'] == 'system_manager' else "EVENT ADMIN"
            print(f"{Colors.BOLD}{role_label}:{Colors.END}")
            print(f"  Email:    {Colors.CYAN}{admin['email']}{Colors.END}")
            print(f"  Password: {Colors.YELLOW}(Use the password you set during registration){Colors.END}")
            print(f"  Role:     {admin['role']}\n")
    else:
        print(f"{Colors.RED}No admin accounts found!{Colors.END}")
        print(f"{Colors.YELLOW}Run: python make_me_admin_standalone.py{Colors.END}\n")
    
    cursor.close()
    conn.close()
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ USER CHECK COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

except mysql.connector.Error as e:
    print(f"\n{Colors.RED}❌ Database Error:{Colors.END}")
    print(f"{Colors.RED}{str(e)}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Troubleshooting:{Colors.END}")
    print(f"  • Make sure MySQL is running (Start XAMPP/WAMP)")
    print(f"  • Check database name: 'nfc_event_management'")
    print(f"  • Verify credentials in script\n")

except ImportError:
    print(f"\n{Colors.YELLOW}Installing required package: tabulate{Colors.END}\n")
    import subprocess
    subprocess.check_call(['pip', 'install', 'tabulate'])
    print(f"\n{Colors.GREEN}✓ Package installed! Run the script again.{Colors.END}\n")

except Exception as e:
    print(f"\n{Colors.RED}❌ Error:{Colors.END}")
    print(f"{Colors.RED}{str(e)}{Colors.END}\n")
    import traceback
    traceback.print_exc()