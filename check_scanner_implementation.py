import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}NFC SCANNER IMPLEMENTATION CHECK{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Check scanner template
scanner_path = 'templates/nfc/scanner.html'
print(f"{Colors.CYAN}Checking scanner template...{Colors.END}")

if os.path.exists(scanner_path):
    with open(scanner_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"{Colors.GREEN}✓{Colors.END} Scanner template exists\n")
    
    # Check for key features
    features = {
        'Camera QR scanning': 'html5-qrcode' in content or 'jsQR' in content,
        'NFC scanning button': 'Start NFC Scan' in content or 'nfcScan' in content,
        'Manual input': 'manual' in content.lower() and 'input' in content.lower(),
        'Scan processing': '/nfc/scan' in content or 'processScan' in content,
        'Camera preview': 'video' in content or 'reader' in content,
        'Result display': 'result' in content.lower() or 'success' in content.lower()
    }
    
    print(f"{Colors.CYAN}Features found:{Colors.END}")
    for feature, found in features.items():
        if found:
            print(f"  {Colors.GREEN}✓{Colors.END} {feature}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {feature} {Colors.RED}(MISSING){Colors.END}")
    
    # Check scanner modes
    print(f"\n{Colors.CYAN}Scanner modes:{Colors.END}")
    has_networking = 'networking' in content.lower()
    has_checkin = 'check-in' in content.lower() or 'checkin' in content.lower()
    
    if has_networking:
        print(f"  {Colors.GREEN}✓{Colors.END} Networking mode (scan other attendees)")
    else:
        print(f"  {Colors.RED}✗{Colors.END} Networking mode (MISSING)")
    
    if has_checkin:
        print(f"  {Colors.GREEN}✓{Colors.END} Check-in mode (admin attendance tracking)")
    else:
        print(f"  {Colors.RED}✗{Colors.END} Check-in mode (MISSING)")

else:
    print(f"{Colors.RED}✗{Colors.END} Scanner template NOT FOUND\n")

# Check NFC controller
print(f"\n{Colors.CYAN}Checking NFC controller...{Colors.END}")
controller_path = 'src/controllers/nfc_controller.py'

if os.path.exists(controller_path):
    with open(controller_path, 'r', encoding='utf-8') as f:
        controller_content = f.read()
    
    print(f"{Colors.GREEN}✓{Colors.END} NFC controller exists\n")
    
    # Check routes
    routes = {
        '/nfc/scanner': '@nfc_bp.route(\'/scanner\')' in controller_content,
        '/nfc/scan (POST)': '@nfc_bp.route(\'/scan\'' in controller_content and 'POST' in controller_content,
        '/nfc/my-connections': '@nfc_bp.route(\'/my-connections\')' in controller_content,
        'process_scan function': 'def process_scan' in controller_content,
        'handle_networking_scan': 'def handle_networking_scan' in controller_content,
        'handle_checkin_scan': 'def handle_checkin_scan' in controller_content
    }
    
    print(f"{Colors.CYAN}Routes & Functions:{Colors.END}")
    for route, found in routes.items():
        if found:
            print(f"  {Colors.GREEN}✓{Colors.END} {route}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {route} {Colors.RED}(MISSING){Colors.END}")
else:
    print(f"{Colors.RED}✗{Colors.END} NFC controller NOT FOUND\n")

# Check static files
print(f"\n{Colors.CYAN}Checking required JavaScript libraries...{Colors.END}")

js_libs = {
    'static/js/html5-qrcode.min.js': 'HTML5 QR Code Scanner',
    'static/js/scanner.js': 'Custom scanner logic'
}

for path, description in js_libs.items():
    if os.path.exists(path):
        print(f"  {Colors.GREEN}✓{Colors.END} {description}")
    else:
        print(f"  {Colors.YELLOW}○{Colors.END} {description} (using CDN is OK)")

# Summary
print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}SUMMARY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

if os.path.exists(scanner_path) and os.path.exists(controller_path):
    print(f"{Colors.GREEN}Scanner is implemented!{Colors.END}\n")
    print(f"{Colors.CYAN}How to use:{Colors.END}")
    print(f"  1. Visit: {Colors.BOLD}http://localhost:5000/nfc/scanner{Colors.END}")
    print(f"  2. Allow camera access when prompted")
    print(f"  3. Point camera at QR code OR click 'Start NFC Scan'")
    print(f"  4. QR codes are generated at: {Colors.BOLD}http://localhost:5000/profile/my-nfc{Colors.END}")
    print()
else:
    print(f"{Colors.RED}Scanner is NOT fully implemented{Colors.END}\n")
    print(f"{Colors.YELLOW}Missing components need to be created{Colors.END}\n")

print()