import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'

try:
    print(f"\n{Colors.CYAN}Updating notifications table...{Colors.END}\n")
    
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'nfc_event_management')
    )
    
    cursor = connection.cursor()
    
    # Add notification_type column if it doesn't exist
    try:
        cursor.execute("""
            ALTER TABLE notifications 
            ADD COLUMN notification_type VARCHAR(50) DEFAULT 'general' AFTER user_id
        """)
        print(f"{Colors.GREEN}✓{Colors.END} Added notification_type column")
    except mysql.connector.Error as e:
        if "Duplicate column name" in str(e):
            print(f"{Colors.YELLOW}○{Colors.END} notification_type column already exists")
        else:
            print(f"{Colors.RED}✗{Colors.END} Error: {e}")
    
    # Create default avatar if missing
    avatar_dir = 'static/uploads'
    os.makedirs(avatar_dir, exist_ok=True)
    
    default_avatar_path = os.path.join(avatar_dir, 'default-avatar.png')
    if not os.path.exists(default_avatar_path):
        print(f"\n{Colors.YELLOW}Creating default avatar...{Colors.END}")
        # Create a simple colored square as default avatar
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (200, 200), color='#6c757d')
            d = ImageDraw.Draw(img)
            
            # Draw a circle
            d.ellipse([50, 50, 150, 150], fill='#ffffff', outline='#dee2e6', width=3)
            
            # Draw user icon (simple representation)
            d.ellipse([85, 70, 115, 100], fill='#6c757d')  # Head
            d.ellipse([70, 110, 130, 170], fill='#6c757d')  # Body
            
            img.save(default_avatar_path)
            print(f"{Colors.GREEN}✓{Colors.END} Created default avatar")
        except ImportError:
            # If PIL not available, create a simple text file placeholder
            with open(default_avatar_path.replace('.png', '.txt'), 'w') as f:
                f.write('Default Avatar Placeholder')
            print(f"{Colors.YELLOW}○{Colors.END} PIL not available, install: pip install Pillow")
    else:
        print(f"{Colors.GREEN}✓{Colors.END} Default avatar exists")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"\n{Colors.GREEN}✅ Database update complete!{Colors.END}\n")

except Exception as e:
    print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}\n")