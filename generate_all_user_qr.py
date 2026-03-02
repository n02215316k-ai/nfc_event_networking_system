
# filepath: c:\Users\lenovo\Downloads\nfc\generate_all_user_qr.py

from database import get_db_connection
from utils.qr_generator import generate_profile_qr

print("Generating QR codes for all users...")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT id, full_name FROM users")
users = cursor.fetchall()

for user in users:
    try:
        _, qr_url, profile_url = generate_profile_qr(user['id'])
        
        cursor.execute("""
            UPDATE users SET qr_code_url = %s WHERE id = %s
        """, (profile_url, user['id']))
        
        print(f"✅ Generated QR for: {user['full_name']} (ID: {user['id']})")
    except Exception as e:
        print(f"❌ Error for user {user['id']}: {e}")

conn.commit()
cursor.close()
conn.close()

print("\n✅ Complete! All users now have QR codes.")
