from database import get_db_connection
import os

print("=" * 80)
print("🔍 ANALYZING CURRENT QR/NFC IMPLEMENTATION")
print("=" * 80)

# ============================================================================
# Check current database structure
# ============================================================================
print("\n📊 DATABASE STRUCTURE:")
print("-" * 80)

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

# Check scans table
cursor.execute("SHOW COLUMNS FROM scans")
scan_columns = cursor.fetchall()

print("\n✅ 'scans' table columns:")
for col in scan_columns:
    print(f"  • {col['Field']:20} {col['Type']}")

# Check users table for QR data
cursor.execute("SHOW COLUMNS FROM users")
user_columns = cursor.fetchall()

print("\n✅ 'users' table columns:")
has_qr_code = False
for col in user_columns:
    if 'qr' in col['Field'].lower():
        print(f"  • {col['Field']:20} {col['Type']} ⭐")
        has_qr_code = True

if not has_qr_code:
    print("  ⚠️  No QR code field found in users table")

# Check events table for QR data
cursor.execute("SHOW COLUMNS FROM events")
event_columns = cursor.fetchall()

print("\n✅ 'events' table columns:")
for col in event_columns:
    if 'qr' in col['Field'].lower():
        print(f"  • {col['Field']:20} {col['Type']} ⭐")

# Check existing scans data
cursor.execute("SELECT COUNT(*) as count FROM scans")
scan_count = cursor.fetchone()['count']
print(f"\n📈 Current scans in database: {scan_count}")

if scan_count > 0:
    cursor.execute("SELECT * FROM scans LIMIT 1")
    sample_scan = cursor.fetchone()
    print("\n📝 Sample scan record:")
    for key, value in sample_scan.items():
        print(f"  • {key}: {value}")

cursor.close()
conn.close()

# ============================================================================
# Check existing QR code files
# ============================================================================
print("\n\n📁 QR CODE FILES:")
print("-" * 80)

if os.path.exists('static/qr_codes'):
    qr_files = os.listdir('static/qr_codes')
    print(f"\n✅ Found {len(qr_files)} QR code files:")
    for file in qr_files[:5]:
        print(f"  • {file}")
    if len(qr_files) > 5:
        print(f"  ... and {len(qr_files) - 5} more")
else:
    print("\n⚠️  QR codes directory doesn't exist")
    print("  Creating: static/qr_codes/")
    os.makedirs('static/qr_codes', exist_ok=True)

# ============================================================================
# Check current controllers
# ============================================================================
print("\n\n📋 CONTROLLER ANALYSIS:")
print("-" * 80)

controllers_to_check = {
    'nfc_controller.py': ['scan', 'scanner_page'],
    'profile_controller.py': ['view', 'qr_code', 'generate_qr'],
}

for controller, expected_routes in controllers_to_check.items():
    controller_path = f'src/controllers/{controller}'
    
    if os.path.exists(controller_path):
        with open(controller_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n✅ {controller}:")
        for route in expected_routes:
            if f"def {route}(" in content:
                print(f"  ✅ {route}() exists")
            else:
                print(f"  ❌ {route}() MISSING")
    else:
        print(f"\n⚠️  {controller} not found")

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE")
print("=" * 80)
print("\n📋 Next: Run enhance_qr_nfc_system.py to add features")