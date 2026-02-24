import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def create_file(filepath, content):
    dirname = os.path.dirname(filepath)
    if dirname:  # Only create directory if path has a directory component
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

# Create a test routes file to verify everything works
TEST_ROUTES = """
# Add these test routes to app.py to verify NFC functionality

@app.route('/test-nfc')
def test_nfc():
    '''Test NFC routes'''
    return '''
    <h1>NFC Routes Test</h1>
    <ul>
        <li><a href="/nfc/scanner">Scanner Page</a></li>
        <li><a href="/profile/my-nfc">My QR Code</a></li>
        <li><a href="/event-admin/dashboard">Event Admin Dashboard</a></li>
    </ul>
    '''
"""

print(f"\n{Colors.CYAN}Creating test routes file...{Colors.END}\n")
create_file('test_routes.txt', TEST_ROUTES)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}SETUP COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

print(f"{Colors.CYAN}NEXT STEPS:{Colors.END}\n")
print(f"1. {Colors.YELLOW}Update base.html navigation:{Colors.END}")
print(f"   Open: NAVIGATION_UPDATE_INSTRUCTIONS.txt")
print(f"   Follow the instructions to update templates/base.html\n")

print(f"2. {Colors.YELLOW}Restart the app:{Colors.END}")
print(f"   python app.py\n")

print(f"3. {Colors.YELLOW}Test the new features directly:{Colors.END}")
print(f"   {Colors.GREEN}✓{Colors.END} Home: http://localhost:5000/")
print(f"   {Colors.GREEN}✓{Colors.END} Scanner: http://localhost:5000/nfc/scanner")
print(f"   {Colors.GREEN}✓{Colors.END} My QR Code: http://localhost:5000/profile/my-nfc")
print(f"   {Colors.GREEN}✓{Colors.END} Event Admin: http://localhost:5000/event-admin/dashboard")
print(f"   {Colors.GREEN}✓{Colors.END} Test Page: http://localhost:5000/test-nfc\n")

print(f"{Colors.BOLD}{Colors.YELLOW}You should now see a NEW homepage with big colorful cards!{Colors.END}\n")
print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")