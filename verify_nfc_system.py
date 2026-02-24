import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
print(f"{Colors.CYAN}NFC/QR SYSTEM VERIFICATION{Colors.END}")
print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")

# Check NFC Controller
nfc_controller = 'src/controllers/nfc_controller.py'
if os.path.exists(nfc_controller):
    with open(nfc_controller, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"{Colors.BLUE}📱 NFC Controller Features:{Colors.END}")
    print(f"  {Colors.GREEN}✓{Colors.END} File exists: {nfc_controller}")
    
    features = {
        'scan': 'def scan(' in content,
        'qr_scan': 'def qr_scan(' in content,
        'scanner_page': 'def scanner_page(' in content,
        'check_in': 'check_in' in content.lower(),
        'check_out': 'check_out' in content.lower(),
        'networking': 'network' in content.lower()
    }
    
    for feature, exists in features.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {feature}")
else:
    print(f"{Colors.RED}✗ NFC Controller not found{Colors.END}")

# Check database tables
print(f"\n{Colors.BLUE}🗄️  Database Tables Check:{Colors.END}")

db_file = 'database/schema.sql'
if os.path.exists(db_file):
    with open(db_file, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    tables = {
        'nfc_scans': 'CREATE TABLE nfc_scans' in schema or 'CREATE TABLE IF NOT EXISTS nfc_scans' in schema,
        'attendance': 'CREATE TABLE attendance' in schema or 'CREATE TABLE IF NOT EXISTS attendance' in schema,
        'event_registrations': 'CREATE TABLE event_registrations' in schema,
    }
    
    for table, exists in tables.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {table}")
else:
    print(f"{Colors.YELLOW}○ No schema.sql file found{Colors.END}")

# Check User Roles
print(f"\n{Colors.BLUE}👥 User Roles Check:{Colors.END}")

users_exist = False
if os.path.exists('src/models/user.py'):
    with open('src/models/user.py', 'r', encoding='utf-8') as f:
        user_content = f.read()
    
    roles = {
        'system_manager': 'system_manager' in user_content,
        'event_admin': 'event_admin' in user_content or 'event_creator' in user_content,
        'attendee': 'attendee' in user_content or 'user' in user_content
    }
    
    for role, exists in roles.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {role}")
    users_exist = True

# Check Event Controllers
print(f"\n{Colors.BLUE}📅 Event Management:{Colors.END}")

event_controller = 'src/controllers/events_controller.py'
if os.path.exists(event_controller):
    with open(event_controller, 'r', encoding='utf-8') as f:
        event_content = f.read()
    
    features = {
        'create_event': 'def create_event' in event_content,
        'register': 'def register' in event_content,
        'attendance_tracking': 'attendance' in event_content.lower(),
        'event_analytics': 'analytic' in event_content.lower()
    }
    
    for feature, exists in features.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {feature}")

# Summary
print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
print(f"{Colors.YELLOW}📋 TODO List to Complete System:{Colors.END}\n")

todos = [
    "Add Event Admin role to user model",
    "Implement NFC check-in/check-out logic",
    "Add QR code generation for events",
    "Create networking initiation on NFC scan",
    "Build Event Admin dashboard",
    "Add attendance reports for Event Admins",
    "Implement real-time attendance updates"
]

for i, todo in enumerate(todos, 1):
    print(f"  {i}. {todo}")

print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}\n")