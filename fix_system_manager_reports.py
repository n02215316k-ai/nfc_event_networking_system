import os
import re

filepath = 'src/controllers/system_manager_controller.py'

print(f"\n🔧 Fixing system_manager_controller.py reports function...\n")

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the reports function
    reports_pattern = r'(@system_manager_bp\.route\(\'/reports\'\).*?def reports\(\):.*?)(return render_template\(\'system_manager/reports\.html\',)'
    
    # Check if stats is already being passed
    if "stats=" in content and "def reports():" in content:
        print("✓ Reports function already has stats parameter")
    else:
        # Find and replace the reports function
        new_reports_code = """@system_manager_bp.route('/reports')
@login_required
@system_manager_required
def reports():
    \"\"\"Generate system reports\"\"\"
    try:
        # Get statistics
        stats = {}
        
        # Total users
        user_count = db.select_one("SELECT COUNT(*) as count FROM users")
        stats['total_users'] = user_count['count'] if user_count else 0
        
        # Total events
        event_count = db.select_one("SELECT COUNT(*) as count FROM events")
        stats['total_events'] = event_count['count'] if event_count else 0
        
        # Total forums
        forum_count = db.select_one("SELECT COUNT(*) as count FROM forums")
        stats['total_forums'] = forum_count['count'] if forum_count else 0
        
        # Total NFC scans
        scan_count = db.select_one("SELECT COUNT(*) as count FROM nfc_scans")
        stats['total_scans'] = scan_count['count'] if scan_count else 0
        
        return render_template('system_manager/reports.html', stats=stats)
    
    except Exception as e:
        print(f"Reports error: {e}")
        flash('Error generating reports', 'error')
        return redirect(url_for('system_manager.dashboard'))
"""
        
        # Search for the reports function and replace it
        pattern = r'@system_manager_bp\.route\(\'/reports\'\).*?(?=@system_manager_bp\.route|$)'
        
        if '@system_manager_bp.route(\'/reports\')' in content:
            # Find the function
            lines = content.split('\n')
            new_lines = []
            skip_until_next_route = False
            i = 0
            
            while i < len(lines):
                line = lines[i]
                
                if "@system_manager_bp.route('/reports')" in line:
                    # Add the new function
                    new_lines.append(new_reports_code)
                    skip_until_next_route = True
                    i += 1
                    continue
                
                if skip_until_next_route:
                    # Skip until we find the next route or end
                    if '@system_manager_bp.route' in line or (i == len(lines) - 1):
                        skip_until_next_route = False
                        new_lines.append(line)
                    i += 1
                    continue
                
                new_lines.append(line)
                i += 1
            
            content = '\n'.join(new_lines)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ Fixed reports function in system_manager_controller.py")
        else:
            print("✗ Could not find reports route")
    
    print("\n✅ Done! Restart the app.\n")

except Exception as e:
    print(f"\n❌ Error: {e}\n")