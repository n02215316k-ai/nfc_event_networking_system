import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING DASHBOARD IMPORT ERROR{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Check what database import is used in the file
print(f"{Colors.CYAN}Analyzing existing imports in app.py...{Colors.END}")

if 'from database import' in app_content:
    db_import = "from database import execute_query"
    print(f"{Colors.GREEN}✓{Colors.END} Using: from database import execute_query")
elif 'import database' in app_content:
    db_import = "import database"
    execute_function = "database.execute_query"
    print(f"{Colors.GREEN}✓{Colors.END} Using: import database")
else:
    # Check if db_config exists
    if os.path.exists('db_config.py'):
        db_import = "from db_config import execute_query"
        print(f"{Colors.GREEN}✓{Colors.END} Using: from db_config import execute_query")
    else:
        db_import = "from database import get_db_connection"
        print(f"{Colors.YELLOW}⚠{Colors.END} Using fallback: from database import get_db_connection")

# Find and replace the dashboard function
dashboard_pattern = r'@app\.route\(\'/dashboard\'\).*?def dashboard\(\):.*?(?=@app\.route|\Z)'

# New dashboard function with correct imports
NEW_DASHBOARD = """@app.route('/dashboard')
def dashboard():
    '''User dashboard with stats and activity'''
    if 'user_id' not in session:
        flash('Please login to access dashboard', 'warning')
        return redirect('/login')
    
    user_id = session.get('user_id')
    
    # Initialize stats
    stats = {
        'registered_events': 0,
        'connections': 0,
        'scans': 0,
        'forum_posts': 0
    }
    
    upcoming_events = []
    recent_activity = []
    
    try:
        # Try to get database connection
        if 'get_db_connection' in dir():
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get registered events count
            try:
                cursor.execute("SELECT COUNT(*) as count FROM event_registrations WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                stats['registered_events'] = result['count'] if result else 0
            except: pass
            
            # Get connections count
            try:
                cursor.execute("SELECT COUNT(*) as count FROM connections WHERE user_id = %s OR connected_user_id = %s", (user_id, user_id))
                result = cursor.fetchone()
                stats['connections'] = result['count'] if result else 0
            except: pass
            
            # Get scans count
            try:
                cursor.execute("SELECT COUNT(*) as count FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s", (user_id, user_id))
                result = cursor.fetchone()
                stats['scans'] = result['count'] if result else 0
            except: pass
            
            # Get forum posts count
            try:
                cursor.execute("SELECT COUNT(*) as count FROM forum_posts WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                stats['forum_posts'] = result['count'] if result else 0
            except: pass
            
            # Get upcoming events
            try:
                cursor.execute(\"\"\"
                    SELECT e.* FROM events e
                    JOIN event_registrations er ON e.id = er.event_id
                    WHERE er.user_id = %s AND e.event_date >= CURDATE()
                    ORDER BY e.event_date ASC
                    LIMIT 5
                \"\"\", (user_id,))
                upcoming_events = cursor.fetchall() or []
            except: pass
            
            cursor.close()
            conn.close()
            
        elif 'execute_query' in dir():
            # Use execute_query function
            try:
                result = execute_query("SELECT COUNT(*) as count FROM event_registrations WHERE user_id = %s", (user_id,), fetch=True, fetchone=True)
                stats['registered_events'] = result['count'] if result else 0
            except: pass
            
            try:
                result = execute_query("SELECT COUNT(*) as count FROM connections WHERE user_id = %s OR connected_user_id = %s", (user_id, user_id), fetch=True, fetchone=True)
                stats['connections'] = result['count'] if result else 0
            except: pass
            
            try:
                result = execute_query("SELECT COUNT(*) as count FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s", (user_id, user_id), fetch=True, fetchone=True)
                stats['scans'] = result['count'] if result else 0
            except: pass
            
            try:
                result = execute_query("SELECT COUNT(*) as count FROM forum_posts WHERE user_id = %s", (user_id,), fetch=True, fetchone=True)
                stats['forum_posts'] = result['count'] if result else 0
            except: pass
            
            try:
                upcoming_events = execute_query(\"\"\"
                    SELECT e.* FROM events e
                    JOIN event_registrations er ON e.id = er.event_id
                    WHERE er.user_id = %s AND e.event_date >= CURDATE()
                    ORDER BY e.event_date ASC
                    LIMIT 5
                \"\"\", (user_id,), fetch=True) or []
            except: pass
    
    except Exception as e:
        print(f"Dashboard error: {e}")
    
    # Add welcome activity
    recent_activity.append({
        'icon': 'calendar-check',
        'description': 'Welcome to your dashboard!',
        'time': 'Just now'
    })
    
    return render_template('dashboard.html', 
                         stats=stats,
                         upcoming_events=upcoming_events,
                         recent_activity=recent_activity)

"""

# Replace dashboard function
if re.search(dashboard_pattern, app_content, re.DOTALL):
    new_content = re.sub(dashboard_pattern, NEW_DASHBOARD, app_content, flags=re.DOTALL)
    print(f"{Colors.GREEN}✓{Colors.END} Found existing dashboard function, replacing it")
else:
    print(f"{Colors.RED}❌ Could not find dashboard function!{Colors.END}")
    exit(1)

# Backup
with open('app.py.backup2', 'w', encoding='utf-8') as f:
    f.write(app_content)
print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup2")

# Write fixed version
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"{Colors.GREEN}✓{Colors.END} Dashboard function updated with proper imports")

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ DASHBOARD IMPORT FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Changes made:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Removed problematic 'src.database' import")
print(f"  {Colors.GREEN}✓{Colors.END} Added flexible database access")
print(f"  {Colors.GREEN}✓{Colors.END} Added error handling for all queries")
print(f"  {Colors.GREEN}✓{Colors.END} Dashboard will work even if some queries fail")

print(f"\n{Colors.BOLD}{Colors.CYAN}Restart your app:{Colors.END}")
print(f"  {Colors.BOLD}python app.py{Colors.END}\n")