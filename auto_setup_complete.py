import os
import sys

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def create_file(filepath, content):
    """Create a file with content"""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")

# ============================================================================
# ROOT FILES
# ============================================================================

ENV_EXAMPLE = """
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=nfc_event_social_network

# Flask Configuration
FLASK_SECRET_KEY=nfc-social-network-secret-key-2026-zimbabwe
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf,doc,docx

# NFC Configuration
NFC_ENABLED=True
NFC_READER_PORT=COM3
"""

GITIGNORE = """
__pycache__/
*.py[cod]
*$py.class
venv/
env/
.env
instance/
.vscode/
.idea/
static/uploads/*
!static/uploads/.gitkeep
*.db
*.sqlite
.DS_Store
Thumbs.db
*.log
"""

REQUIREMENTS = """
Flask==3.0.0
mysql-connector-python==8.2.0
Werkzeug==3.0.1
Jinja2==3.1.2
python-dotenv==1.0.0
Pillow==10.1.0
qrcode==7.4.2
"""

RUN_PY = """
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
    print("\\n📡 Server: http://localhost:5000")
    print("\\n👑 System Manager Login:")
    print("   Email: admin@eventsocial.zw")
    print("   Password: Admin@123")
    print("\\n⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!\\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
"""

README = """
# 🎟️ NFC Event & Social Network Management System

A comprehensive event management and social networking platform with NFC badge integration for Zimbabwe.

## ✨ Features

### Core Features
- ✅ NFC Badge Check-in/Check-out for Events
- ✅ NFC Badge Networking (Scan to view profiles)
- ✅ QR Code Backup for NFC
- ✅ Event Creation & Management
- ✅ Real-time Attendance Tracking
- ✅ Event Analytics Dashboard
- ✅ Auto-create Forum per Event

### User Management
- ✅ 3 User Roles: User, Event Manager, System Manager
- ✅ Complete User Profiles (Bio, Qualifications, Employment, Research Area)
- ✅ Followers/Following System
- ✅ Document Upload & Verification
- ✅ Direct Messaging

### Social Features
- ✅ Discussion Forums (Event-based & Independent)
- ✅ Forum Moderators
- ✅ Auto-join Forum on Event Check-in
- ✅ Search (Events, Forums, Users)

### Admin Features
- ✅ Event Manager: Manage own events, live stats
- ✅ System Manager: Verify documents, view all users, all events
- ✅ NFC Badge Assignment

## 🚀 Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your MySQL password
```

3. **Initialize Database**
```bash
python scripts/init_database.py
```

4. **Run Application**
```bash
python run.py
```

5. **Access**
- URL: http://localhost:5000
- System Manager: admin@eventsocial.zw / Admin@123

## 📁 Structure

```
nfc-event-social-network/
├── src/
│   ├── main.py
│   ├── config/database.py
│   └── controllers/
│       ├── auth_controller.py
│       ├── event_controller.py
│       ├── nfc_controller.py
│       ├── profile_controller.py
│       ├── messaging_controller.py
│       ├── forum_controller.py
│       └── system_manager_controller.py
├── templates/
├── static/
├── database/schema.sql
└── scripts/init_database.py
```

## 🏷️ NFC Badge Functionality

### Event Check-in/Check-out
1. Admin scans user's NFC badge → Check-in
2. Admin scans same badge again → Check-out
3. Admin scans again → Check-in (re-entry)

### Networking
- User scans another user's badge → View profile

## 🇿🇼 Made in Zimbabwe
"""

# ============================================================================
# DATABASE SCHEMA (Enhanced with ALL features)
# ============================================================================

SCHEMA_SQL = """
-- NFC Event & Social Network Management System
-- Database Schema for Zimbabwe
-- Created: February 2026

-- ============================================================================
-- USERS TABLE (Enhanced with research_area)
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    profile_picture VARCHAR(500),
    biography TEXT,
    current_employment VARCHAR(255),
    current_research_area VARCHAR(255),
    role ENUM('user', 'event_manager', 'system_manager') DEFAULT 'user',
    is_verified BOOLEAN DEFAULT FALSE,
    nfc_badge_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_nfc_badge (nfc_badge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- EVENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category ENUM('technology', 'healthcare', 'education', 'business', 'research', 'other') DEFAULT 'other',
    location VARCHAR(255),
    venue VARCHAR(255),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    creator_id INT NOT NULL,
    status ENUM('draft', 'published', 'cancelled', 'completed') DEFAULT 'draft',
    max_attendees INT,
    current_attendees INT DEFAULT 0,
    cover_image VARCHAR(500),
    qr_code VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_creator (creator_id),
    INDEX idx_status (status),
    INDEX idx_start_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ATTENDANCE TABLE (Enhanced with scanner tracking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('registered', 'checked_in', 'checked_out') DEFAULT 'registered',
    check_in_time DATETIME,
    check_out_time DATETIME,
    check_in_method ENUM('nfc', 'qr', 'manual') DEFAULT 'manual',
    scanner_id INT,
    scanner_name VARCHAR(255),
    notes TEXT,
    
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_attendance (event_id, user_id),
    INDEX idx_event (event_id),
    INDEX idx_user (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ATTENDANCE LOGS (Track all check-in/check-out events)
-- ============================================================================
CREATE TABLE IF NOT EXISTS attendance_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    attendance_id INT NOT NULL,
    action ENUM('check_in', 'check_out') NOT NULL,
    scanner_id INT,
    scanner_name VARCHAR(255),
    scan_method ENUM('nfc', 'qr', 'manual') DEFAULT 'manual',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (attendance_id) REFERENCES attendance(id) ON DELETE CASCADE,
    FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_attendance (attendance_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- QUALIFICATIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS qualifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    qualification_type ENUM('certificate', 'diploma', 'degree', 'masters', 'phd', 'other') NOT NULL,
    institution VARCHAR(255) NOT NULL,
    field_of_study VARCHAR(255),
    year_obtained YEAR,
    document_path VARCHAR(500),
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    verified_by INT,
    verified_at DATETIME,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_status (verification_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MESSAGES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    parent_message_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_message_id) REFERENCES messages(id) ON DELETE CASCADE,
    INDEX idx_sender (sender_id),
    INDEX idx_recipient (recipient_id),
    INDEX idx_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- FORUMS TABLE (Enhanced with event linkage)
-- ============================================================================
CREATE TABLE IF NOT EXISTS forums (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creator_id INT NOT NULL,
    event_id INT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_creator (creator_id),
    INDEX idx_event (event_id),
    INDEX idx_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- FORUM POSTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS forum_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT NOT NULL,
    user_id INT NOT NULL,
    title VARCHAR(255),
    content TEXT NOT NULL,
    parent_post_id INT,
    attachment VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (forum_id) REFERENCES forums(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_post_id) REFERENCES forum_posts(id) ON DELETE CASCADE,
    INDEX idx_forum (forum_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- FORUM MEMBERS TABLE (Enhanced with moderator role)
-- ============================================================================
CREATE TABLE IF NOT EXISTS forum_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('member', 'moderator', 'admin') DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (forum_id) REFERENCES forums(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_membership (forum_id, user_id),
    INDEX idx_forum (forum_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- FOLLOWERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS followers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_follow (follower_id, following_id),
    INDEX idx_follower (follower_id),
    INDEX idx_following (following_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- NOTIFICATIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    link VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- NFC SCAN LOGS (Track all NFC scans)
-- ============================================================================
CREATE TABLE IF NOT EXISTS nfc_scan_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scanner_id INT NOT NULL,
    scanned_badge_id VARCHAR(50) NOT NULL,
    scanned_user_id INT,
    scan_type ENUM('event_checkin', 'event_checkout', 'networking') NOT NULL,
    event_id INT,
    success BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (scanner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scanned_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_scanner (scanner_id),
    INDEX idx_scanned_user (scanned_user_id),
    INDEX idx_event (event_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- VERIFICATION LOGS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS verification_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    qualification_id INT NOT NULL,
    verifier_id INT NOT NULL,
    action ENUM('verified', 'rejected') NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (qualification_id) REFERENCES qualifications(id) ON DELETE CASCADE,
    FOREIGN KEY (verifier_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_qualification (qualification_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# ============================================================================
# DATABASE INITIALIZATION SCRIPT
# ============================================================================

INIT_DATABASE_PY = """
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

# Ndebele/Zimbabwean names for sample data
NDEBELE_NAMES = [
    ("Nkosiyethu", "Dube"),
    ("Thembinkosi", "Ncube"),
    ("Nomusa", "Moyo"),
    ("Siphiwe", "Khumalo"),
    ("Mandla", "Ndlovu"),
    ("Zanele", "Sibanda"),
    ("Mbuso", "Mpofu"),
    ("Lindiwe", "Nkomo")
]

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )

def initialize_database():
    print("=" * 70)
    print("🗄️  NFC Event & Social Network - Database Setup")
    print("=" * 70)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create database
        db_name = os.getenv('DB_NAME', 'nfc_event_social_network')
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"\\n✓ Database '{db_name}' created")
        
        cursor.execute(f"USE {db_name}")
        
        # Execute schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        statements = [s.strip() for s in schema_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print("✓ Database schema created")
        
        # Create System Manager with Ndebele name
        admin_email = "admin@eventsocial.zw"
        admin_password = "Admin@123"
        admin_name = "Mandla Ndlovu"
        password_hash = generate_password_hash(admin_password)
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role, is_verified, 
                             current_employment, current_research_area, biography)
            VALUES (%s, %s, %s, 'system_manager', TRUE, 
                    'System Administrator', 'Digital Identity Systems',
                    'System Manager for NFC Event & Social Network Platform')
        ''', (admin_email, password_hash, admin_name))
        admin_id = cursor.lastrowid
        conn.commit()
        
        print(f"\\n✓ System Manager created:")
        print(f"  📧 Email: {admin_email}")
        print(f"  🔑 Password: {admin_password}")
        print(f"  👤 Name: {admin_name}")
        
        # Create sample users with Ndebele names
        print("\\n📝 Creating sample users...")
        sample_users = []
        
        for i, (first, last) in enumerate(NDEBELE_NAMES[:6]):
            email = f"{first.lower()}.{last.lower()}@eventsocial.zw"
            full_name = f"{first} {last}"
            role = 'event_manager' if i < 2 else 'user'
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, role, 
                                 current_employment, current_research_area, biography)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                email,
                generate_password_hash('password123'),
                full_name,
                role,
                f"{'Event Coordinator' if role == 'event_manager' else 'Researcher'} at University of Zimbabwe",
                f"{'Event Management' if role == 'event_manager' else 'Technology & Innovation'}",
                f"Passionate about community development and technology in Zimbabwe."
            ))
            
            user_id = cursor.lastrowid
            sample_users.append({
                'id': user_id,
                'name': full_name,
                'email': email,
                'role': role
            })
            
            # Assign NFC badge
            nfc_badge = f"NFC{str(user_id).zfill(6)}"
            cursor.execute("UPDATE users SET nfc_badge_id = %s WHERE id = %s", (nfc_badge, user_id))
        
        conn.commit()
        print(f"  ✓ Created {len(sample_users)} sample users")
        
        # Create sample events
        print("\\n📅 Creating sample events...")
        event_ids = []
        
        events_data = [
            ("Zimbabwe Tech Summit 2026", "Annual technology conference bringing together innovators across Zimbabwe", 
             "technology", "Harare", "Rainbow Towers Hotel"),
            ("Healthcare Innovation Workshop", "Exploring digital health solutions for rural communities",
             "healthcare", "Bulawayo", "Bulawayo Conference Centre"),
            ("Education Technology Symposium", "Transforming education through technology in Zimbabwe",
             "education", "Harare", "University of Zimbabwe")
        ]
        
        from datetime import datetime, timedelta
        
        for i, (title, desc, cat, loc, venue) in enumerate(events_data):
            start_date = datetime.now() + timedelta(days=15 + i*7)
            end_date = start_date + timedelta(hours=8)
            creator_id = sample_users[i % 2]['id']  # Rotate between event managers
            
            cursor.execute('''
                INSERT INTO events (title, description, category, location, venue,
                                  start_date, end_date, creator_id, status, max_attendees)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'published', %s)
            ''', (title, desc, cat, loc, venue, start_date, end_date, creator_id, 150))
            
            event_id = cursor.lastrowid
            event_ids.append(event_id)
            
            # Create forum for event
            cursor.execute('''
                INSERT INTO forums (title, description, creator_id, event_id, is_public)
                VALUES (%s, %s, %s, %s, TRUE)
            ''', (f"{title} - Discussion Forum", f"Forum for {title}", creator_id, event_id))
            
            forum_id = cursor.lastrowid
            
            # Add creator as forum admin
            cursor.execute('''
                INSERT INTO forum_members (forum_id, user_id, role)
                VALUES (%s, %s, 'admin')
            ''', (forum_id, creator_id))
        
        conn.commit()
        print(f"  ✓ Created {len(event_ids)} events with forums")
        
        # Create independent forum
        cursor.execute('''
            INSERT INTO forums (title, description, creator_id, is_public)
            VALUES ('Zimbabwe Developers Community', 
                    'A community for developers and tech enthusiasts in Zimbabwe',
                    %s, TRUE)
        ''', (sample_users[0]['id'],))
        
        forum_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO forum_members (forum_id, user_id, role)
            VALUES (%s, %s, 'admin')
        ''', (forum_id, sample_users[0]['id']))
        
        conn.commit()
        print("  ✓ Created independent forum")
        
        print("\\n" + "=" * 70)
        print("✅ Database initialization complete!")
        print("=" * 70)
        
        print("\\n📝 Sample Accounts:")
        print(f"\\n👑 System Manager:")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        
        print(f"\\n🎫 Event Managers:")
        for user in sample_users[:2]:
            print(f"   {user['name']}: {user['email']} / password123")
        
        print(f"\\n👤 Regular Users:")
        for user in sample_users[2:4]:
            print(f"   {user['name']}: {user['email']} / password123")
        
        print("\\n⚠️  CHANGE ALL PASSWORDS AFTER FIRST LOGIN!")
        
        print("\\n📋 Next steps:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your MySQL password")
        print("3. Run: python run.py")
        print("4. Visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print_header("🚀 NFC Event & Social Network - Complete Auto Setup")
    
    print_section("Creating root configuration files...")
    create_file('.env.example', ENV_EXAMPLE)
    create_file('.gitignore', GITIGNORE)
    create_file('requirements.txt', REQUIREMENTS)
    create_file('run.py', RUN_PY)
    create_file('README.md', README)
    
    print_section("Creating database files...")
    create_file('database/schema.sql', SCHEMA_SQL)
    create_file('scripts/init_database.py', INIT_DATABASE_PY)
    
    # Create upload directories
    print_section("Creating upload directories...")
    os.makedirs('static/uploads/profiles', exist_ok=True)
    os.makedirs('static/uploads/qualifications', exist_ok=True)
    os.makedirs('static/uploads/events', exist_ok=True)
    os.makedirs('static/uploads/forums', exist_ok=True)
    
    # Create .gitkeep files
    for folder in ['profiles', 'qualifications', 'events', 'forums']:
        with open(f'static/uploads/{folder}/.gitkeep', 'w') as f:
            f.write('')
    
    print(f"{Colors.GREEN}✓{Colors.END} Created upload directories")
    
    print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
    print(f"{Colors.GREEN}✅ Part 1 Complete - Base files created!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}📋 Next: Run part 2 script to create source code{Colors.END}")

if __name__ == '__main__':
    main()