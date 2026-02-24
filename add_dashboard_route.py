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
print(f"{Colors.BOLD}{Colors.CYAN}ADDING DASHBOARD ROUTE TO APP.PY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read current app.py
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
except FileNotFoundError:
    print(f"{Colors.RED}❌ Error: app.py not found!{Colors.END}")
    exit(1)

# Check if dashboard route already exists
if '@app.route(\'/dashboard\')' in app_content or 'def dashboard():' in app_content:
    print(f"{Colors.YELLOW}⚠ Dashboard route already exists in app.py{Colors.END}")
    print(f"{Colors.GREEN}✓ No changes needed{Colors.END}\n")
    exit(0)

# Dashboard route code
DASHBOARD_ROUTE = """

# ============================================================================
# DASHBOARD ROUTE
# ============================================================================
@app.route('/dashboard')
def dashboard():
    '''User dashboard with stats and activity'''
    if 'user_id' not in session:
        flash('Please login to access dashboard', 'warning')
        return redirect('/login')
    
    from src.database.db import execute_query
    
    user_id = session.get('user_id')
    
    # Get user stats
    stats = {
        'registered_events': 0,
        'connections': 0,
        'scans': 0,
        'forum_posts': 0
    }
    
    # Get registered events count
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM event_registrations WHERE user_id = %s",
            (user_id,), fetch=True, fetchone=True
        )
        stats['registered_events'] = result['count'] if result else 0
    except Exception as e:
        print(f"Error getting registered events: {e}")
    
    # Get connections count
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM connections WHERE user_id = %s OR connected_user_id = %s",
            (user_id, user_id), fetch=True, fetchone=True
        )
        stats['connections'] = result['count'] if result else 0
    except Exception as e:
        print(f"Error getting connections: {e}")
    
    # Get scans count
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM nfc_scans WHERE scanner_id = %s OR scanned_user_id = %s",
            (user_id, user_id), fetch=True, fetchone=True
        )
        stats['scans'] = result['count'] if result else 0
    except Exception as e:
        print(f"Error getting scans: {e}")
    
    # Get forum posts count
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM forum_posts WHERE user_id = %s",
            (user_id,), fetch=True, fetchone=True
        )
        stats['forum_posts'] = result['count'] if result else 0
    except Exception as e:
        print(f"Error getting forum posts: {e}")
    
    # Get upcoming events user is registered for
    upcoming_events = []
    try:
        upcoming_events = execute_query(
            \"\"\"
            SELECT e.* FROM events e
            JOIN event_registrations er ON e.id = er.event_id
            WHERE er.user_id = %s AND e.event_date >= CURDATE()
            ORDER BY e.event_date ASC
            LIMIT 5
            \"\"\",
            (user_id,), fetch=True
        )
        if not upcoming_events:
            upcoming_events = []
    except Exception as e:
        print(f"Error getting upcoming events: {e}")
        upcoming_events = []
    
    # Recent activity (placeholder for now)
    recent_activity = [
        {
            'icon': 'calendar-check',
            'description': 'Welcome to your dashboard!',
            'time': 'Just now'
        }
    ]
    
    return render_template('dashboard.html', 
                         stats=stats,
                         upcoming_events=upcoming_events,
                         recent_activity=recent_activity)

"""

# Find a good place to insert (after login route)
# Look for the login route
login_pattern = r"(@app\.route\('/login'.*?\n(?:@.*?\n)*def login\(\):.*?(?=\n@app\.route|$))"
match = re.search(login_pattern, app_content, re.DOTALL)

if match:
    # Insert after login route
    insert_position = match.end()
    new_content = app_content[:insert_position] + DASHBOARD_ROUTE + app_content[insert_position:]
    print(f"{Colors.GREEN}✓{Colors.END} Found login route, inserting dashboard after it")
else:
    # Try to find after imports
    import_pattern = r"(from flask import.*?\n(?:from.*?\n)*)"
    match = re.search(import_pattern, app_content, re.DOTALL)
    
    if match:
        # Find first route after imports
        first_route_pattern = r"(@app\.route\()"
        first_route = re.search(first_route_pattern, app_content[match.end():])
        if first_route:
            insert_position = match.end() + first_route.start()
            new_content = app_content[:insert_position] + DASHBOARD_ROUTE + "\n" + app_content[insert_position:]
            print(f"{Colors.GREEN}✓{Colors.END} Inserting dashboard route before first route")
        else:
            # Append at end
            new_content = app_content + DASHBOARD_ROUTE
            print(f"{Colors.YELLOW}⚠{Colors.END} Adding dashboard route at end of file")
    else:
        # Last resort: append at end
        new_content = app_content + DASHBOARD_ROUTE
        print(f"{Colors.YELLOW}⚠{Colors.END} Adding dashboard route at end of file")

# Create backup
try:
    with open('app.py.backup', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup")
except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Could not create backup: {e}")

# Write new content
try:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"{Colors.GREEN}✓{Colors.END} Dashboard route added to app.py")
except Exception as e:
    print(f"{Colors.RED}❌ Error writing to app.py: {e}{Colors.END}")
    # Restore from backup if it exists
    if os.path.exists('app.py.backup'):
        with open('app.py.backup', 'r', encoding='utf-8') as f:
            backup = f.read()
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(backup)
        print(f"{Colors.YELLOW}⚠ Restored from backup{Colors.END}")
    exit(1)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ DASHBOARD ROUTE SUCCESSFULLY ADDED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Changes made:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} Added @app.route('/dashboard')")
print(f"  {Colors.GREEN}✓{Colors.END} Added dashboard() function")
print(f"  {Colors.GREEN}✓{Colors.END} Includes stats calculation")
print(f"  {Colors.GREEN}✓{Colors.END} Includes upcoming events")
print(f"  {Colors.GREEN}✓{Colors.END} Error handling included")

print(f"\n{Colors.CYAN}The dashboard route provides:{Colors.END}")
print(f"  • Registered events count")
print(f"  • Connections count")
print(f"  • NFC scans count")
print(f"  • Forum posts count")
print(f"  • List of upcoming events")
print(f"  • Recent activity feed")

print(f"\n{Colors.BOLD}{Colors.CYAN}Next steps:{Colors.END}")
print(f"  1. Restart your Flask app: {Colors.BOLD}python app.py{Colors.END}")
print(f"  2. Visit: {Colors.BOLD}http://localhost:5000/dashboard{Colors.END}")
print(f"  3. You should see your personalized dashboard!")

print(f"\n{Colors.YELLOW}Note:{Colors.END} If something goes wrong, restore from {Colors.BOLD}app.py.backup{Colors.END}\n")