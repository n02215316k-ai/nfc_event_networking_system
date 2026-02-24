import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING NFC NETWORKING & CHECK-IN TABLES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

try:
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'nfc_event_management')
    )
    cursor = conn.cursor()
    print(f"{Colors.GREEN}✓{Colors.END} Connected to database: {os.getenv('DB_NAME')}\n")

    # 1. Connections table for networking
    print(f"{Colors.CYAN}Creating connections table...{Colors.END}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            connected_user_id INT NOT NULL,
            connection_method ENUM('nfc', 'qr', 'manual') DEFAULT 'qr',
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (connected_user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_connection (user_id, connected_user_id),
            INDEX idx_user (user_id),
            INDEX idx_connected_user (connected_user_id),
            INDEX idx_method (connection_method)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print(f"{Colors.GREEN}✓{Colors.END} Created connections table")

    # 2. Networking logs
    print(f"{Colors.CYAN}Creating networking_logs table...{Colors.END}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS networking_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            scanner_id INT NOT NULL,
            scanned_user_id INT NOT NULL,
            scan_method ENUM('nfc', 'qr') DEFAULT 'qr',
            event_id INT NULL,
            scan_location VARCHAR(255) NULL,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (scanned_user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
            INDEX idx_scanner (scanner_id),
            INDEX idx_scanned (scanned_user_id),
            INDEX idx_event (event_id),
            INDEX idx_time (scanned_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print(f"{Colors.GREEN}✓{Colors.END} Created networking_logs table")

    # 3. Event check-ins (enhanced)
    print(f"{Colors.CYAN}Creating event_checkins table...{Colors.END}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_checkins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_id INT NOT NULL,
            user_id INT NOT NULL,
            checked_in_at TIMESTAMP NULL,
            checked_out_at TIMESTAMP NULL,
            checked_in_by INT NULL,
            checked_out_by INT NULL,
            check_in_method ENUM('nfc', 'qr', 'manual') DEFAULT 'qr',
            check_out_method ENUM('nfc', 'qr', 'manual') DEFAULT 'qr',
            scan_method VARCHAR(20) DEFAULT 'qr',
            duration_minutes INT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (checked_out_by) REFERENCES users(id) ON DELETE SET NULL,
            INDEX idx_event_user (event_id, user_id),
            INDEX idx_checkin_time (checked_in_at),
            INDEX idx_user (user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print(f"{Colors.GREEN}✓{Colors.END} Created event_checkins table")

    # 4. Admin check-in logs for auditing
    print(f"{Colors.CYAN}Creating admin_checkin_logs table...{Colors.END}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_checkin_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_id INT NOT NULL,
            admin_id INT NOT NULL,
            attendee_id INT NOT NULL,
            action ENUM('checked_in', 'checked_out', 'manual_override') NOT NULL,
            scan_method ENUM('nfc', 'qr', 'manual') DEFAULT 'qr',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (attendee_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_event_time (event_id, timestamp),
            INDEX idx_admin (admin_id),
            INDEX idx_attendee (attendee_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print(f"{Colors.GREEN}✓{Colors.END} Created admin_checkin_logs table")

    # 5. NFC device registrations (for tracking authorized NFC devices)
    print(f"{Colors.CYAN}Creating nfc_devices table...{Colors.END}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nfc_devices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            device_name VARCHAR(255) NULL,
            device_id VARCHAR(100) UNIQUE NOT NULL,
            device_type ENUM('phone', 'tablet', 'badge', 'reader') DEFAULT 'phone',
            is_active BOOLEAN DEFAULT TRUE,
            last_used TIMESTAMP NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user (user_id),
            INDEX idx_device_id (device_id),
            INDEX idx_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print(f"{Colors.GREEN}✓{Colors.END} Created nfc_devices table")

    # Commit all changes
    conn.commit()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ NFC TABLES CREATED SUCCESSFULLY!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Created tables:{Colors.END}")
    print(f"  {Colors.GREEN}✓{Colors.END} connections - User networking connections")
    print(f"  {Colors.GREEN}✓{Colors.END} networking_logs - Scan activity logs")
    print(f"  {Colors.GREEN}✓{Colors.END} event_checkins - Event attendance tracking")
    print(f"  {Colors.GREEN}✓{Colors.END} admin_checkin_logs - Admin action audit trail")
    print(f"  {Colors.GREEN}✓{Colors.END} nfc_devices - Authorized NFC devices")
    print()
    
    print(f"{Colors.YELLOW}Next steps:{Colors.END}")
    print(f"  1. Run: python app.py")
    print(f"  2. Visit: http://localhost:5000/nfc/scanner")
    print(f"  3. Test NFC scanning functionality")
    print()

except mysql.connector.Error as e:
    print(f"\n{Colors.RED}✗ Database Error: {e}{Colors.END}\n")
    print(f"{Colors.YELLOW}Make sure:{Colors.END}")
    print(f"  - MySQL is running")
    print(f"  - Database '{os.getenv('DB_NAME')}' exists")
    print(f"  - Credentials in .env are correct")
    print()
except Exception as e:
    print(f"\n{Colors.RED}✗ Error: {e}{Colors.END}\n")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print(f"{Colors.CYAN}Database connection closed{Colors.END}\n")