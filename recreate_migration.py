class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

print("=" * 80)
print(f"{Colors.CYAN}🔧 RECREATING MIGRATION FILE{Colors.END}")
print("=" * 80)

# The proper migration SQL
migration_sql = """-- Event Check-in Feature Migration
-- Database: nfc_event_social_network
-- Run this to add event check-in functionality

-- ============================================================================
-- 1. Create event_checkins table
-- ============================================================================
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

-- ============================================================================
-- 2. Add scan_url column to scan_history table
-- ============================================================================
-- Check if column exists first
SET @db_name = DATABASE();
SET @table_name = 'scan_history';
SET @column_name = 'scan_url';

SET @query = CONCAT(
    'ALTER TABLE ', @table_name, 
    ' ADD COLUMN IF NOT EXISTS ', @column_name, ' TEXT AFTER scan_data'
);

PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================================================
-- 3. Create indexes on scan_history for better performance
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_scanner ON scan_history(scanner_id);
CREATE INDEX IF NOT EXISTS idx_scanned_user ON scan_history(scanned_user_id);
CREATE INDEX IF NOT EXISTS idx_scan_date ON scan_history(created_at);

-- ============================================================================
-- 4. Verify migration
-- ============================================================================
SELECT 'Migration completed successfully!' AS Status;
SELECT 'event_checkins table created' AS Step1;
SELECT 'scan_history.scan_url column added' AS Step2;
SELECT 'Performance indexes created' AS Step3;
"""

# Write to file
print(f"\n{Colors.CYAN}📝 Writing migration file...{Colors.END}")

with open('migration_event_checkins.sql', 'w', encoding='utf-8') as f:
    f.write(migration_sql)

print(f"{Colors.GREEN}✓{Colors.END} Created: migration_event_checkins.sql")

# Verify file was created
import os
if os.path.exists('migration_event_checkins.sql'):
    file_size = os.path.getsize('migration_event_checkins.sql')
    print(f"{Colors.GREEN}✓{Colors.END} File size: {file_size} bytes")
    
    # Show content preview
    print(f"\n{Colors.CYAN}📋 Preview:{Colors.END}\n")
    with open('migration_event_checkins.sql', 'r', encoding='utf-8') as f:
        lines = f.readlines()[:10]
        for line in lines:
            print(f"  {line.rstrip()}")
    print(f"  ... ({len(open('migration_event_checkins.sql').readlines())} lines total)")
else:
    print(f"{Colors.RED}✗{Colors.END} Failed to create file!")

print("\n" + "=" * 80)
print(f"{Colors.GREEN}✅ MIGRATION FILE RECREATED!{Colors.END}")
print("=" * 80)

print(f"""
{Colors.CYAN}🚀 Next Steps:{Colors.END}

1. Run the migration:
   {Colors.GREEN}mysql -u root -p nfc_event_social_network < migration_event_checkins.sql{Colors.END}

2. Enter your MySQL password when prompted

3. Should see:
   • Migration completed successfully!
   • event_checkins table created
   • scan_history.scan_url column added
   • Performance indexes created

4. Verify tables exist:
   {Colors.GREEN}mysql -u root -p nfc_event_social_network -e "SHOW TABLES;"{Colors.END}

{Colors.CYAN}📍 File Location:{Colors.END}
   {os.path.abspath('migration_event_checkins.sql')}
""")

print("=" * 80)