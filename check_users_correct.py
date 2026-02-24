import mysql.connector
from werkzeug.security import check_password_hash

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}NFC EVENT MANAGEMENT - USER CHECKER{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'nfc_event_management'
}

try:
    print(f"{Colors.CYAN}Connecting to database...{Colors.END}")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    print(f"{Colors.GREEN}✓ Connected successfully!{Colors.END}\n")
    
    cursor.execute("""
        SELECT id, email, password_hash, full_name, phone_number, 
               current_employment, current_research_area, role, 
               is_verified, nfc_badge_id, nfc_enabled, 
               created_at, updated_at, last_nfc_scan
        FROM users 
        ORDER BY 
            CASE role 
                WHEN 'system_manager' THEN 1 
                WHEN 'event_admin' THEN 2 
                WHEN 'attendee' THEN 3 
                ELSE 4
            END, id
    """)
    
    users = cursor.fetchall()
    
    if not users:
        print(f"{Colors.RED}❌ No users found in database!{Colors.END}\n")
        exit(1)
    
    # Statistics
    total_users = len(users)
    system_managers = sum(1 for u in users if u['role'] == 'system_manager')
    event_admins = sum(1 for u in users if u['role'] == 'event_admin')
    attendees = sum(1 for u in users if u['role'] == 'attendee')
    no_role = sum(1 for u in users if not u['role'])
    
    print(f"{Colors.BOLD}{Colors.MAGENTA}📊 USER STATISTICS{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")
    print(f"  Total Users:        {Colors.CYAN}{total_users}{Colors.END}")
    print(f"  System Managers:    {Colors.RED}{system_managers}{Colors.END}")
    print(f"  Event Admins:       {Colors.YELLOW}{event_admins}{Colors.END}")
    print(f"  Attendees:          {Colors.GREEN}{attendees}{Colors.END}")
    if no_role > 0:
        print(f"  No Role Assigned:   {Colors.YELLOW}{no_role}{Colors.END}")
    
    # Detailed view
    print(f"\n{Colors.BOLD}{Colors.CYAN}👥 ALL USERS - DETAILED VIEW{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    for i, user in enumerate(users, 1):
        role = user['role'] or 'NO_ROLE'
        
        if role == 'system_manager':
            role_color = Colors.RED
            role_icon = "🔴"
        elif role == 'event_admin':
            role_color = Colors.YELLOW
            role_icon = "🟡"
        elif role == 'attendee':
            role_color = Colors.GREEN
            role_icon = "🟢"
        else:
            role_color = Colors.YELLOW
            role_icon = "⚪"
        
        print(f"{Colors.BOLD}{'─'*80}{Colors.END}")
        print(f"{role_icon} {Colors.BOLD}User #{i} - ID: {user['id']}{Colors.END}")
        print(f"{Colors.BOLD}{'─'*80}{Colors.END}")
        print(f"  Full Name:        {user['full_name']}")
        print(f"  Email:            {Colors.CYAN}{user['email']}{Colors.END}")
        print(f"  Password Hash:    {Colors.YELLOW}{user['password_hash'][:45]}...{Colors.END}")
        print(f"  Role:             {role_color}{Colors.BOLD}{role.upper()}{Colors.END}")
        print(f"  NFC Badge ID:     {user['nfc_badge_id'] or 'Not assigned'}")
        print(f"  NFC Enabled:      {'✓ Yes' if user['nfc_enabled'] else '✗ No'}")
        print(f"  Verified:         {'✓ Yes' if user['is_verified'] else '✗ No'}")
        print(f"  Phone:            {user['phone_number'] or 'N/A'}")
        print(f"  Employment:       {user['current_employment'] or 'N/A'}")
        print(f"  Research Area:    {user['current_research_area'] or 'N/A'}")
        if user['created_at']:
            print(f"  Created:          {user['created_at']}")
        if user['last_nfc_scan']:
            print(f"  Last NFC Scan:    {user['last_nfc_scan']}")
        print()
    
    # Compact table
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}📋 COMPACT TABLE VIEW{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")
    print(f"{Colors.BOLD}{'ID':<5} {'Name':<25} {'Email':<30} {'Role':<20}{Colors.END}")
    print(f"{'-'*80}")
    
    for user in users:
        role = user['role'] or 'NO_ROLE'
        
        if role == 'system_manager':
            role_display = f"{Colors.RED}SYSTEM_MANAGER{Colors.END}"
        elif role == 'event_admin':
            role_display = f"{Colors.YELLOW}EVENT_ADMIN{Colors.END}"
        elif role == 'attendee':
            role_display = f"{Colors.GREEN}ATTENDEE{Colors.END}"
        else:
            role_display = f"{Colors.YELLOW}NO_ROLE{Colors.END}"
        
        name = user['full_name'][:24]
        email = user['email'][:29]
        print(f"{user['id']:<5} {name:<25} {email:<30} {role_display}")
    
    # Password verification
    print(f"\n{Colors.BOLD}{Colors.YELLOW}🔐 PASSWORD VERIFICATION UTILITY{Colors.END}")
    print(f"{Colors.YELLOW}{'='*80}{Colors.END}\n")
    print(f"{Colors.CYAN}Test if a password matches a user account{Colors.END}")
    print(f"{Colors.YELLOW}(Your passwords are hashed with scrypt){Colors.END}\n")
    
    while True:
        test_choice = input(f"{Colors.BOLD}Test a password? (y/n): {Colors.END}").strip().lower()
        if test_choice != 'y':
            break
        
        test_email = input(f"\n{Colors.CYAN}Enter email: {Colors.END}").strip()
        test_password = input(f"{Colors.CYAN}Enter password: {Colors.END}").strip()
        
        test_user = next((u for u in users if u['email'] == test_email), None)
        
        if not test_user:
            print(f"{Colors.RED}✗ Email not found!{Colors.END}\n")
            continue
        
        try:
            if check_password_hash(test_user['password_hash'], test_password):
                print(f"\n{Colors.GREEN}{'='*80}{Colors.END}")
                print(f"{Colors.GREEN}{Colors.BOLD}✓ PASSWORD CORRECT!{Colors.END}")
                print(f"{Colors.GREEN}{'='*80}{Colors.END}")
                print(f"{Colors.GREEN}User: {test_user['full_name']}{Colors.END}")
                print(f"{Colors.GREEN}Role: {test_user['role'] or 'NO_ROLE'}{Colors.END}\n")
            else:
                print(f"\n{Colors.RED}✗ PASSWORD INCORRECT!{Colors.END}\n")
        except Exception as e:
            print(f"\n{Colors.RED}✗ Error verifying password: {e}{Colors.END}\n")
    
    # Admin accounts
    print(f"\n{Colors.BOLD}{Colors.RED}🔑 ADMIN ACCOUNTS FOR LOGIN{Colors.END}")
    print(f"{Colors.RED}{'='*80}{Colors.END}\n")
    
    admins = [u for u in users if u['role'] in ['system_manager', 'event_admin']]
    
    if admins:
        print(f"{Colors.YELLOW}Use these credentials to login:{Colors.END}\n")
        for admin in admins:
            role_label = "SYSTEM MANAGER" if admin['role'] == 'system_manager' else "EVENT ADMIN"
            print(f"{Colors.BOLD}{role_label}:{Colors.END}")
            print(f"  Email:        {Colors.CYAN}{admin['email']}{Colors.END}")
            print(f"  NFC Badge:    {admin['nfc_badge_id']}")
            print(f"  Password:     {Colors.YELLOW}(Use the password you set){Colors.END}\n")
    else:
        print(f"{Colors.RED}No admin accounts found!{Colors.END}\n")
    
    # Users without roles
    no_role_users = [u for u in users if not u['role']]
    
    if no_role_users:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ USERS WITHOUT ROLES{Colors.END}")
        print(f"{Colors.YELLOW}{'='*80}{Colors.END}\n")
        print(f"{Colors.YELLOW}These users need roles assigned:{Colors.END}\n")
        
        for user in no_role_users:
            print(f"  • {user['full_name']} ({user['email']}) - ID: {user['id']}")
        
        print(f"\n{Colors.CYAN}To assign roles, run:{Colors.END}")
        print(f"  {Colors.CYAN}python make_me_admin_standalone.py{Colors.END}\n")
    
    cursor.close()
    conn.close()
    
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ USER CHECK COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

except Exception as e:
    print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}\n")
    import traceback
    traceback.print_exc()