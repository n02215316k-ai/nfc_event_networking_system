import os
from dotenv import load_dotenv

load_dotenv()

from src.main import app

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 NFC Event & Social Network Management System")
    print("=" * 70)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Database: {os.getenv('DB_NAME', 'nfc_event_social_network')}")
    print("=" * 70)
    print("\n📡 Server: http://localhost:5000")
    print("\n👑 System Manager Login:")
    print("   Email: admin@eventsocial.zw")
    print("   Password: Admin@123")
    print("\n⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )