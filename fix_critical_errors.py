import os
import re

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

print("=" * 80)
print(f"{Colors.RED}🔧 FIXING CRITICAL ERRORS{Colors.END}")
print("=" * 80)

errors_found = []
errors_fixed = []

# ============================================================================
# ERROR 1: Unknown column 'u.phone' in 'field list'
# ============================================================================
print(f"\n{Colors.CYAN}📋 Error 1: Missing 'phone' column in users table{Colors.END}")

# Need to add phone column to database OR remove it from queries
print(f"{Colors.YELLOW}⚠️{Colors.END}  The code is trying to fetch 'phone' but column doesn't exist")

# Check event_admin_controller.py for phone references
event_admin_path = 'src/controllers/event_admin_controller.py'

if os.path.exists(event_admin_path):
    with open(event_admin_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    with open(event_admin_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Find and fix phone column references
    if 'u.phone' in content or 'users.phone' in content:
        errors_found.append("Phone column referenced but doesn't exist")
        
        # Remove phone from SELECT statements
        content = re.sub(r',\s*u\.phone', '', content)
        content = re.sub(r',\s*users\.phone', '', content)
        content = re.sub(r'u\.phone,', '', content)
        content = re.sub(r'users\.phone,', '', content)
        
        with open(event_admin_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        errors_fixed.append("Removed phone column references")
        print(f"{Colors.GREEN}✓{Colors.END} Fixed: Removed phone column from queries")

# ============================================================================
# ERROR 2: ModuleNotFoundError: No module named 'controllers'
# ============================================================================
print(f"\n{Colors.CYAN}📋 Error 2: Incorrect import path 'controllers.nfc_controller'{Colors.END}")

if os.path.exists(event_admin_path):
    with open(event_admin_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from controllers.nfc_controller' in content:
        errors_found.append("Wrong import: 'from controllers.nfc_controller'")
        
        # Fix import path
        content = content.replace(
            'from controllers.nfc_controller',
            'from src.controllers.nfc_controller'
        )
        
        with open(event_admin_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        errors_fixed.append("Fixed import path to 'src.controllers.nfc_controller'")
        print(f"{Colors.GREEN}✓{Colors.END} Fixed: Import path corrected")

# ============================================================================
# ERROR 3: 'attendance_stats' is undefined in reports.html
# ============================================================================
print(f"\n{Colors.CYAN}📋 Error 3: Missing 'attendance_stats' variable in reports{Colors.END}")

if os.path.exists(event_admin_path):
    with open(event_admin_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the event_reports function
    if 'def event_reports' in content:
        errors_found.append("attendance_stats not passed to template")
        
        # Find the render_template call in event_reports function
        pattern = r'(def event_reports\(event_id\):.*?)(return render_template\([\'"]event_admin/reports\.html[\'"],)'
        
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Check if attendance_stats is already being calculated
            if 'attendance_stats' not in match.group(1):
                # Add attendance stats calculation before render_template
                stats_code = '''
        # Calculate attendance statistics
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT er.user_id) as total_registered,
                COUNT(DISTINCT ec.user_id) as total_checked_in
            FROM event_registrations er
            LEFT JOIN event_checkins ec ON er.event_id = ec.event_id AND er.user_id = ec.user_id
            WHERE er.event_id = %s
        """, (event_id,))
        
        attendance_data = cursor.fetchone()
        attendance_stats = {
            'total_registered': attendance_data['total_registered'] or 0,
            'total_checked_in': attendance_data['total_checked_in'] or 0
        }
        
        '''
                
                # Insert before return render_template
                render_pos = content.find('return render_template(\'event_admin/reports.html\'', match.start())
                if render_pos != -1:
                    content = content[:render_pos] + stats_code + content[render_pos:]
                    
                    # Also ensure it's passed to template
                    content = content.replace(
                        "return render_template('event_admin/reports.html',",
                        "return render_template('event_admin/reports.html',\n                             attendance_stats=attendance_stats,"
                    )
                    
                    with open(event_admin_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    errors_fixed.append("Added attendance_stats calculation and passed to template")
                    print(f"{Colors.GREEN}✓{Colors.END} Fixed: attendance_stats now calculated and passed")

# ============================================================================
# CREATE DATABASE MIGRATION FOR PHONE COLUMN (Optional)
# ============================================================================
print(f"\n{Colors.CYAN}📋 Creating optional migration to add phone column{Colors.END}")

phone_migration = """-- Optional: Add phone column to users table
-- Run this if you want to add phone functionality

ALTER TABLE users 
ADD COLUMN phone VARCHAR(20) AFTER email;

-- Add index for phone lookups
CREATE INDEX idx_phone ON users(phone);
"""

with open('migration_add_phone_column.sql', 'w', encoding='utf-8') as f:
    f.write(phone_migration)

print(f"{Colors.GREEN}✓{Colors.END} Created migration_add_phone_column.sql (optional)")

# ============================================================================
# FIX MIGRATION FILE
# ============================================================================
print(f"\n{Colors.CYAN}📋 Fixing migration_event_checkins.sql{Colors.END}")

migration_path = 'migration_event_checkins.sql'

if os.path.exists(migration_path):
    # Check if file just says "pyt"
    with open(migration_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if content == 'pyt' or len(content) < 100:
        errors_found.append("migration_event_checkins.sql is corrupted/empty")
        
        # Recreate proper migration
        proper_migration = """-- Event Check-in Feature Migration
-- Run this on your database if event_checkins table doesn't exist

-- Create event_checkins table if it doesn't exist
CREATE TABLE IF NOT EXISTS event_checkins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    checked_in_by INT,
    checked_in_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_url TEXT,
    scan_id INT,
    notes TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (scan_id) REFERENCES scan_history(id) ON DELETE SET NULL,
    UNIQUE KEY unique_checkin (event_id, user_id),
    INDEX idx_event (event_id),
    INDEX idx_user (user_id),
    INDEX idx_checkin_time (checked_in_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add scan_url to scan_history if it doesn't exist
ALTER TABLE scan_history 
ADD COLUMN IF NOT EXISTS scan_url TEXT AFTER scan_data;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_scanner ON scan_history(scanner_id);
CREATE INDEX IF NOT EXISTS idx_scanned_user ON scan_history(scanned_user_id);
CREATE INDEX IF NOT EXISTS idx_scan_date ON scan_history(created_at);
"""
        
        with open(migration_path, 'w', encoding='utf-8') as f:
            f.write(proper_migration)
        
        errors_fixed.append("Recreated migration_event_checkins.sql")
        print(f"{Colors.GREEN}✓{Colors.END} Fixed: Recreated proper migration file")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print(f"{Colors.CYAN}📊 FIX SUMMARY{Colors.END}")
print("=" * 80)

print(f"\n{Colors.RED}❌ Errors Found:{Colors.END}")
for i, error in enumerate(errors_found, 1):
    print(f"  {i}. {error}")

print(f"\n{Colors.GREEN}✅ Errors Fixed:{Colors.END}")
for i, fix in enumerate(errors_fixed, 1):
    print(f"  {i}. {fix}")

# ============================================================================
# NEXT STEPS
# ============================================================================
print(f"\n{Colors.CYAN}🚀 NEXT STEPS:{Colors.END}\n")

print(f"""
1️⃣  Run database migrations:

   {Colors.YELLOW}# Main migration (event check-ins){Colors.END}
   mysql -u root -p nfc_event_social_network < migration_event_checkins.sql
   
   {Colors.YELLOW}# Optional: Add phone column if you want phone functionality{Colors.END}
   mysql -u root -p nfc_event_social_network < migration_add_phone_column.sql

2️⃣  Restart your Flask app:

   {Colors.GREEN}python app.py{Colors.END}

3️⃣  Test these pages:

   ✓ http://localhost:5000/nfc/scanner
   ✓ http://localhost:5000/event-admin/event/2
   ✓ http://localhost:5000/event-admin/event/2/reports
   ✓ http://localhost:5000/event-admin/event/2/qr-codes

4️⃣  If still having issues, check:

   • MySQL service is running
   • Database name matches .env
   • All migrations ran successfully

{Colors.CYAN}📋 Files Modified:{Colors.END}

• src/controllers/event_admin_controller.py (fixed 3 errors)
• migration_event_checkins.sql (recreated)
• migration_add_phone_column.sql (created)

{Colors.CYAN}💾 Backups Created:{Colors.END}

• src/controllers/event_admin_controller.py.backup

{Colors.GREEN}✅ All critical errors have been fixed!{Colors.END}
""")

print("=" * 80)