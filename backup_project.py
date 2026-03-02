import os
import shutil
import datetime
import zipfile

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

print("=" * 80)
print(f"{Colors.CYAN}💾 COMPLETE PROJECT BACKUP{Colors.END}")
print("=" * 80)

# ============================================================================
# Configuration
# ============================================================================
PROJECT_ROOT = os.getcwd()
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
BACKUP_DIR = f"backup_{TIMESTAMP}"
BACKUP_ZIP = f"nfc_backup_{TIMESTAMP}.zip"

# Files/folders to exclude from backup
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '.git',
    'venv',
    'env',
    '.venv',
    'node_modules',
    '*.log',
    '.DS_Store',
    'Thumbs.db',
    '.idea',
    '.vscode',
    '*.backup',
    'backup_*',
    'nfc_backup_*.zip'
]

# ============================================================================
# Helper Functions
# ============================================================================
def should_exclude(path):
    """Check if path should be excluded"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if path.endswith(pattern[1:]):
                return True
        elif pattern in path:
            return True
    return False

def get_dir_size(path):
    """Calculate directory size"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file() and not should_exclude(entry.path):
                total += entry.stat().st_size
            elif entry.is_dir() and not should_exclude(entry.path):
                total += get_dir_size(entry.path)
    except Exception:
        pass
    return total

def format_bytes(bytes_size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

# ============================================================================
# Step 1: Create Backup Directory
# ============================================================================
print(f"\n{Colors.CYAN}📁 Step 1: Creating backup directory...{Colors.END}")

try:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"{Colors.GREEN}✓{Colors.END} Created: {BACKUP_DIR}/")
except Exception as e:
    print(f"{Colors.RED}✗{Colors.END} Failed to create backup directory: {e}")
    exit(1)

# ============================================================================
# Step 2: Copy Project Files
# ============================================================================
print(f"\n{Colors.CYAN}📋 Step 2: Copying project files...{Colors.END}")

copied_files = 0
skipped_files = 0
total_size = 0

def copy_directory(src, dst):
    """Recursively copy directory"""
    global copied_files, skipped_files, total_size
    
    try:
        os.makedirs(dst, exist_ok=True)
        
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            
            # Skip excluded patterns
            if should_exclude(src_path):
                skipped_files += 1
                continue
            
            if os.path.isfile(src_path):
                try:
                    shutil.copy2(src_path, dst_path)
                    file_size = os.path.getsize(src_path)
                    total_size += file_size
                    copied_files += 1
                    
                    # Show progress for every 10 files
                    if copied_files % 10 == 0:
                        print(f"  Copied {copied_files} files... ({format_bytes(total_size)})")
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠{Colors.END} Failed to copy {src_path}: {e}")
                    skipped_files += 1
            
            elif os.path.isdir(src_path):
                copy_directory(src_path, dst_path)
    
    except Exception as e:
        print(f"{Colors.YELLOW}⚠{Colors.END} Error processing {src}: {e}")

# Start copying
copy_directory(PROJECT_ROOT, BACKUP_DIR)

print(f"{Colors.GREEN}✓{Colors.END} Copied {copied_files} files ({format_bytes(total_size)})")
print(f"{Colors.YELLOW}○{Colors.END} Skipped {skipped_files} files/folders")

# ============================================================================
# Step 3: Create Backup Manifest
# ============================================================================
print(f"\n{Colors.CYAN}📝 Step 3: Creating backup manifest...{Colors.END}")

manifest_content = f"""
NFC EVENT MANAGEMENT SYSTEM - BACKUP MANIFEST
============================================

Backup Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Backup Location: {os.path.abspath(BACKUP_DIR)}
Total Files: {copied_files}
Total Size: {format_bytes(total_size)}

BACKUP CONTENTS:
---------------
"""

# List all backed up files
for root, dirs, files in os.walk(BACKUP_DIR):
    # Remove excluded dirs
    dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
    
    level = root.replace(BACKUP_DIR, '').count(os.sep)
    indent = ' ' * 2 * level
    folder_name = os.path.basename(root)
    manifest_content += f"{indent}{folder_name}/\n"
    
    sub_indent = ' ' * 2 * (level + 1)
    for file in files:
        if not should_exclude(file):
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            manifest_content += f"{sub_indent}{file} ({format_bytes(file_size)})\n"

manifest_content += f"""

EXCLUDED PATTERNS:
-----------------
{chr(10).join(f"  - {pattern}" for pattern in EXCLUDE_PATTERNS)}

RESTORATION INSTRUCTIONS:
------------------------
1. Extract the backup ZIP file
2. Copy contents to your project directory
3. Run: pip install -r requirements.txt
4. Update database credentials in .env
5. Run: python app.py

IMPORTANT NOTES:
---------------
• This backup does NOT include:
  - Virtual environment (venv/)
  - Git repository (.git/)
  - Python cache (__pycache__/)
  - User uploads (may need separate backup)
  - Database (needs separate MySQL dump)

• To backup database separately:
  mysqldump -u root -p nfc_db > backup_{TIMESTAMP}_database.sql

• To restore database:
  mysql -u root -p nfc_db < backup_{TIMESTAMP}_database.sql
"""

manifest_path = os.path.join(BACKUP_DIR, 'BACKUP_MANIFEST.txt')
with open(manifest_path, 'w', encoding='utf-8') as f:
    f.write(manifest_content)

print(f"{Colors.GREEN}✓{Colors.END} Created backup manifest")

# ============================================================================
# Step 4: Create Database Backup Script
# ============================================================================
print(f"\n{Colors.CYAN}🗄️ Step 4: Creating database backup script...{Colors.END}")

db_backup_script = f"""@echo off
REM Database Backup Script
REM Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo ========================================
echo DATABASE BACKUP
echo ========================================
echo.

set TIMESTAMP={TIMESTAMP}
set DB_NAME=nfc_db
set BACKUP_FILE=backup_%TIMESTAMP%_database.sql

echo Backing up database: %DB_NAME%
echo Output file: %BACKUP_FILE%
echo.

REM Update with your MySQL credentials
set MYSQL_USER=root
set /p MYSQL_PASSWORD=Enter MySQL password: 

mysqldump -u %MYSQL_USER% -p%MYSQL_PASSWORD% %DB_NAME% > %BACKUP_FILE%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Database backed up successfully!
    echo File: %BACKUP_FILE%
) else (
    echo.
    echo [ERROR] Database backup failed!
)

pause
"""

db_script_path = os.path.join(BACKUP_DIR, 'backup_database.bat')
with open(db_script_path, 'w', encoding='utf-8') as f:
    f.write(db_backup_script)

print(f"{Colors.GREEN}✓{Colors.END} Created database backup script: backup_database.bat")

# ============================================================================
# Step 5: Create Restoration Script
# ============================================================================
print(f"\n{Colors.CYAN}♻️ Step 5: Creating restoration script...{Colors.END}")

restore_script = f"""@echo off
REM Project Restoration Script
REM Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo ========================================
echo PROJECT RESTORATION
echo ========================================
echo.

echo This script will help you restore the NFC project from backup.
echo.
echo Prerequisites:
echo   - Python 3.8+ installed
echo   - MySQL Server installed and running
echo   - Git installed (optional)
echo.

pause

REM Step 1: Create virtual environment
echo.
echo Step 1: Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created

REM Step 2: Activate and install dependencies
echo.
echo Step 2: Installing dependencies...
call venv\\Scripts\\activate.bat
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed

REM Step 3: Environment configuration
echo.
echo Step 3: Configuring environment...
if not exist .env (
    copy .env.example .env
    echo [INFO] Created .env file - PLEASE UPDATE with your database credentials
    notepad .env
)

REM Step 4: Database setup
echo.
echo Step 4: Database setup
echo.
echo Option 1: Restore from backup SQL file
echo Option 2: Run fresh database setup
echo.
set /p DB_OPTION=Choose option (1 or 2): 

if "%DB_OPTION%"=="1" (
    set /p SQL_FILE=Enter SQL backup file path: 
    set /p DB_USER=Enter MySQL username: 
    set /p DB_PASS=Enter MySQL password: 
    mysql -u %DB_USER% -p%DB_PASS% nfc_db < "%SQL_FILE%"
    echo [SUCCESS] Database restored from backup
) else (
    echo Run: mysql -u root -p nfc_db < database_schema.sql
    echo Then press any key to continue...
    pause
)

REM Step 5: Create required directories
echo.
echo Step 5: Creating required directories...
if not exist static\\uploads mkdir static\\uploads
if not exist static\\qr_codes mkdir static\\qr_codes
if not exist static\\qr_codes\\events mkdir static\\qr_codes\\events
if not exist logs mkdir logs
echo [SUCCESS] Directories created

REM Step 6: Test the application
echo.
echo Step 6: Starting application in test mode...
echo.
echo The application will start in a few seconds.
echo Press Ctrl+C to stop when you're done testing.
echo.
timeout /t 3
python app.py

echo.
echo ========================================
echo RESTORATION COMPLETE!
echo ========================================
echo.
echo Next steps:
echo   1. Update .env with your settings
echo   2. Run: python app.py
echo   3. Visit: http://localhost:5000
echo.
pause
"""

restore_script_path = os.path.join(BACKUP_DIR, 'RESTORE.bat')
with open(restore_script_path, 'w', encoding='utf-8') as f:
    f.write(restore_script)

print(f"{Colors.GREEN}✓{Colors.END} Created restoration script: RESTORE.bat")

# ============================================================================
# Step 6: Create ZIP Archive
# ============================================================================
print(f"\n{Colors.CYAN}📦 Step 6: Creating ZIP archive...{Colors.END}")

try:
    with zipfile.ZipFile(BACKUP_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BACKUP_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, os.path.dirname(BACKUP_DIR))
                zipf.write(file_path, arc_name)
                print(f"  Adding: {arc_name}")
    
    zip_size = os.path.getsize(BACKUP_ZIP)
    print(f"{Colors.GREEN}✓{Colors.END} Created ZIP archive: {BACKUP_ZIP} ({format_bytes(zip_size)})")
except Exception as e:
    print(f"{Colors.RED}✗{Colors.END} Failed to create ZIP: {e}")

# ============================================================================
# Step 7: Create Quick Info File
# ============================================================================
print(f"\n{Colors.CYAN}📄 Step 7: Creating backup info file...{Colors.END}")

info_content = f"""
╔════════════════════════════════════════════════════════════════╗
║           NFC EVENT MANAGEMENT - BACKUP INFORMATION           ║
╚════════════════════════════════════════════════════════════════╝

📅 Backup Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📦 Backup Size: {format_bytes(total_size)}
📁 Total Files: {copied_files}
🗜️  ZIP Archive: {BACKUP_ZIP} ({format_bytes(os.path.getsize(BACKUP_ZIP))})

═══════════════════════════════════════════════════════════════

📋 BACKUP CONTENTS:

✅ Source Code:
   • Python controllers
   • Templates (HTML)
   • Static files (CSS, JS)
   • Configuration files

✅ Scripts:
   • Database backup script (backup_database.bat)
   • Restoration script (RESTORE.bat)
   • Backup manifest (BACKUP_MANIFEST.txt)

❌ NOT INCLUDED (backup separately):
   • Database (run backup_database.bat)
   • Virtual environment (venv/)
   • User uploads (static/uploads/*)
   • Generated QR codes (static/qr_codes/*)
   • Git repository (.git/)

═══════════════════════════════════════════════════════════════

🔄 QUICK RESTORATION:

1. Extract {BACKUP_ZIP}
2. Run: RESTORE.bat
3. Follow on-screen instructions

OR MANUAL RESTORATION:

1. Extract ZIP to project folder
2. Create virtual environment: python -m venv venv
3. Activate: venv\\Scripts\\activate
4. Install: pip install -r requirements.txt
5. Configure: Update .env with database credentials
6. Restore DB: mysql -u root -p nfc_db < backup_database.sql
7. Start: python app.py

═══════════════════════════════════════════════════════════════

📦 BACKUP DATABASE SEPARATELY:

Windows:
  cd {BACKUP_DIR}
  backup_database.bat

Linux/Mac:
  mysqldump -u root -p nfc_db > backup_{TIMESTAMP}_database.sql

═══════════════════════════════════════════════════════════════

💾 STORAGE RECOMMENDATIONS:

✅ Keep this backup in at least 2 locations:
   • External hard drive
   • Cloud storage (Google Drive, Dropbox, etc.)
   • Network storage (NAS)

✅ Test restoration periodically

✅ Create new backups before major changes

═══════════════════════════════════════════════════════════════

📞 NEED HELP?

Refer to:
  • BACKUP_MANIFEST.txt (complete file list)
  • RESTORE.bat (automated restoration)
  • README.md (project documentation)

═══════════════════════════════════════════════════════════════
"""

info_path = os.path.join(BACKUP_DIR, 'BACKUP_INFO.txt')
with open(info_path, 'w', encoding='utf-8') as f:
    f.write(info_content)

# Also create a copy in the project root
with open(f'BACKUP_INFO_{TIMESTAMP}.txt', 'w', encoding='utf-8') as f:
    f.write(info_content)

print(f"{Colors.GREEN}✓{Colors.END} Created backup info files")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print(f"{Colors.GREEN}✅ BACKUP COMPLETE!{Colors.END}")
print("=" * 80)

print(f"""
{Colors.CYAN}📊 BACKUP SUMMARY:{Colors.END}

✅ Backup Folder:     {BACKUP_DIR}/
✅ ZIP Archive:       {BACKUP_ZIP} ({format_bytes(os.path.getsize(BACKUP_ZIP))})
✅ Files Backed Up:   {copied_files}
✅ Total Size:        {format_bytes(total_size)}
✅ Skipped:           {skipped_files} files/folders

{Colors.CYAN}📁 BACKUP FILES CREATED:{Colors.END}

1. {BACKUP_ZIP}
   └─ Complete project backup (compressed)

2. {BACKUP_DIR}/
   ├─ BACKUP_INFO.txt          (Quick reference)
   ├─ BACKUP_MANIFEST.txt      (Complete file list)
   ├─ RESTORE.bat              (Restoration script)
   ├─ backup_database.bat      (Database backup script)
   └─ [All project files]

3. BACKUP_INFO_{TIMESTAMP}.txt (Copy in project root)

{Colors.CYAN}🗄️  NEXT: BACKUP DATABASE{Colors.END}

Run the database backup:
  cd {BACKUP_DIR}
  backup_database.bat

Or manually:
  mysqldump -u root -p nfc_db > backup_{TIMESTAMP}_database.sql

{Colors.CYAN}💾 STORAGE RECOMMENDATIONS:{Colors.END}

1. Copy {BACKUP_ZIP} to:
   • External hard drive
   • Cloud storage (Google Drive, OneDrive, Dropbox)
   • Network storage

2. Keep database backup separately

3. Test restoration to ensure backup works

{Colors.CYAN}🔄 TO RESTORE THIS BACKUP:{Colors.END}

1. Extract: {BACKUP_ZIP}
2. Run:     RESTORE.bat
3. Follow:  On-screen instructions

{Colors.GREEN}✅ Your project is now safely backed up!{Colors.END}
""")

# Open backup folder
print(f"\n{Colors.CYAN}📂 Opening backup folder...{Colors.END}")
try:
    os.startfile(BACKUP_DIR)
except Exception:
    print(f"Open manually: {os.path.abspath(BACKUP_DIR)}")

print("\n" + "=" * 80)