from database import get_db_connection
from utils.qr_generator import generate_profile_qr
import sys

print("=" * 80)
print("🔄 REGENERATING QR CODES WITH CURRENT DOMAIN")
print("=" * 80)

# Get domain from command line or use default
if len(sys.argv) > 1:
    domain = sys.argv[1]
    print(f"\nℹ️  Using provided domain: {domain}")
else:
    domain = "http://localhost:5000"
    print(f"\nℹ️  Using default domain: {domain}")
    print("   💡 To use custom domain: python regenerate_all_qr_codes.py https://yourdomain.com")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

try:
    cursor.execute("SELECT id, full_name, email FROM users")
    users = cursor.fetchall()
    
    print(f"\n📊 Found {len(users)} users to process\n")
    
    success_count = 0
    error_count = 0
    
    for user in users:
        try:
            # Generate QR with specified domain
            _, qr_url, profile_url = generate_profile_qr(user['id'], base_url=domain)
            
            # Update database
            cursor.execute("""
                UPDATE users SET qr_code_url = %s WHERE id = %s
            """, (profile_url, user['id']))
            
            user_name = user['full_name'] if user['full_name'] else user['email']
            print(f"✅ {user_name:30} → {profile_url}")
            success_count += 1
            
        except Exception as e:
            user_name = user['full_name'] if user['full_name'] else user['email']
            print(f"❌ {user_name:30} → Error: {e}")
            error_count += 1
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print(f"✅ COMPLETE! Success: {success_count}, Errors: {error_count}")
    print("=" * 80)
    
    if success_count > 0:
        print(f"\n🎯 All QR codes now use: {domain}")
        print(f"   Test by visiting: {domain}/profile/qr")
        print("\n📝 QR codes have been saved to: static/qr_codes/")
        print("   Database qr_code_url field has been updated")

except Exception as e:
    print(f"\n❌ Database error: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()