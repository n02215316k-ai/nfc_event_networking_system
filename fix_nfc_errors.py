import os
import shutil

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing NFC Errors...{Colors.END}\n")

# 1. Add functions to nfc_controller.py
NFC_FUNCTIONS = """

import qrcode
import io
import base64
from datetime import datetime

def generate_user_nfc_code(user_id, email):
    '''Generate QR code for user networking (NFC backup)'''
    try:
        # Format: "user:{user_id}:{email}"
        qr_data = f"user:{user_id}:{email}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating user QR code: {e}")
        return None

def generate_event_qr_code(event_id, user_id):
    '''Generate QR code for event check-in (NFC backup)'''
    try:
        # Format: "event:{event_id}:{user_id}"
        qr_data = f"event:{event_id}:{user_id}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating event QR code: {e}")
        return None
"""

nfc_controller_path = 'src/controllers/nfc_controller.py'
if os.path.exists(nfc_controller_path):
    with open(nfc_controller_path, 'a', encoding='utf-8') as f:
        f.write(NFC_FUNCTIONS)
    print(f"{Colors.GREEN}✓{Colors.END} Added QR generation functions to nfc_controller.py")
else:
    print(f"{Colors.YELLOW}⚠{Colors.END} nfc_controller.py not found")

# 2. Fix connections.html template
connections_template_path = 'templates/nfc/connections.html'
if os.path.exists(connections_template_path):
    with open(connections_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the datetimeformat filter
    content = content.replace(
        "{{ conn.connected_at|datetimeformat }}",
        "{{ conn.connected_at.strftime('%Y-%m-%d %H:%M') if conn.connected_at else 'N/A' }}"
    )
    
    with open(connections_template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Fixed connections.html template")
else:
    print(f"{Colors.YELLOW}⚠{Colors.END} connections.html not found")

print(f"\n{Colors.GREEN}✅ Fixes applied!{Colors.END}")
print(f"\n{Colors.CYAN}Next steps:{Colors.END}")
print(f"  1. Install qrcode: pip install qrcode[pil]")
print(f"  2. Restart app: python app.py")
print(f"  3. Test: http://localhost:5000/profile/my-nfc")
print(f"  4. Test: http://localhost:5000/nfc/my-connections\n")