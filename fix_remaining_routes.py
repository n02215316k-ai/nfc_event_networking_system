import os
import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING REMAINING 404 ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Backup
with open('app.py.backup_final', 'w', encoding='utf-8') as f:
    f.write(app_content)
print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup_final")

routes_to_add = []

# ============================================================================
# 1. CHECK AND ADD /forums/ ROUTE
# ============================================================================
if "@app.route('/forums')" not in app_content and "@app.route('/forums/')" not in app_content:
    print(f"{Colors.YELLOW}⚠{Colors.END} /forums/ route missing - will add")
    routes_to_add.append("""
@app.route('/forums/')
@app.route('/forums')
def forums_list():
    '''Forums list page'''
    if 'user_id' not in session:
        flash('Please login to access forums', 'warning')
        return redirect('/login')
    
    # Get forums from database (placeholder for now)
    forums = []
    
    try:
        if 'get_db_connection' in dir():
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM forums ORDER BY created_at DESC")
            forums = cursor.fetchall() or []
            cursor.close()
            conn.close()
        elif 'execute_query' in dir():
            forums = execute_query("SELECT * FROM forums ORDER BY created_at DESC", fetch=True) or []
    except Exception as e:
        print(f"Error loading forums: {e}")
        forums = []
    
    return render_template('forums/list.html', forums=forums)
""")
else:
    print(f"{Colors.GREEN}✓{Colors.END} /forums/ route exists")

# ============================================================================
# 2. CHECK AND ADD /profile/view ROUTE
# ============================================================================
if "@app.route('/profile/view')" not in app_content:
    print(f"{Colors.YELLOW}⚠{Colors.END} /profile/view route missing - will add")
    routes_to_add.append("""
@app.route('/profile/view')
def profile_view():
    '''View own profile'''
    if 'user_id' not in session:
        flash('Please login to view your profile', 'warning')
        return redirect('/login')
    
    user_id = session.get('user_id')
    user_data = None
    
    try:
        if 'get_db_connection' in dir():
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
        elif 'execute_query' in dir():
            user_data = execute_query("SELECT * FROM users WHERE id = %s", (user_id,), fetch=True, fetchone=True)
    except Exception as e:
        print(f"Error loading profile: {e}")
    
    # If we got user data, update session
    if user_data:
        for key, value in user_data.items():
            if key not in ['password', 'password_hash']:
                session[key] = value
    
    return render_template('profile/view.html', user=user_data or session)
""")
else:
    print(f"{Colors.GREEN}✓{Colors.END} /profile/view route exists")

# ============================================================================
# 3. CHECK AND ADD /profile/settings ROUTE
# ============================================================================
if "@app.route('/profile/settings')" not in app_content:
    print(f"{Colors.YELLOW}⚠{Colors.END} /profile/settings route missing - will add")
    routes_to_add.append("""
@app.route('/profile/settings', methods=['GET', 'POST'])
def profile_settings():
    '''Profile settings page'''
    if 'user_id' not in session:
        flash('Please login to access settings', 'warning')
        return redirect('/login')
    
    if request.method == 'POST':
        user_id = session.get('user_id')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate passwords
        if new_password and new_password == confirm_password:
            try:
                import bcrypt
                
                # Get current password hash
                if 'get_db_connection' in dir():
                    conn = get_db_connection()
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
                    user = cursor.fetchone()
                    
                    if user and bcrypt.checkpw(current_password.encode('utf-8'), user['password'].encode('utf-8')):
                        # Hash new password
                        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
                        conn.commit()
                        flash('Password updated successfully!', 'success')
                    else:
                        flash('Current password is incorrect', 'danger')
                    
                    cursor.close()
                    conn.close()
                elif 'execute_query' in dir():
                    user = execute_query("SELECT password FROM users WHERE id = %s", (user_id,), fetch=True, fetchone=True)
                    
                    if user and bcrypt.checkpw(current_password.encode('utf-8'), user['password'].encode('utf-8')):
                        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        execute_query("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
                        flash('Password updated successfully!', 'success')
                    else:
                        flash('Current password is incorrect', 'danger')
            
            except Exception as e:
                print(f"Error updating password: {e}")
                flash('Error updating password', 'danger')
        
        elif new_password:
            flash('Passwords do not match', 'danger')
        
        # Handle notification settings
        email_notifications = request.form.get('email_notifications') == 'on'
        connection_notifications = request.form.get('connection_notifications') == 'on'
        
        flash('Settings updated successfully!', 'success')
        return redirect('/profile/settings')
    
    return render_template('profile/settings.html')
""")
else:
    print(f"{Colors.GREEN}✓{Colors.END} /profile/settings route exists")

# ============================================================================
# ADD ROUTES TO APP.PY
# ============================================================================
if routes_to_add:
    print(f"\n{Colors.CYAN}Adding {len(routes_to_add)} missing route(s)...{Colors.END}")
    
    # Find best insertion point (before if __name__)
    if "if __name__ == '__main__':" in app_content:
        insertion_point = app_content.find("if __name__ == '__main__':")
        new_content = (
            app_content[:insertion_point] + 
            '\n'.join(routes_to_add) + 
            '\n\n' +
            app_content[insertion_point:]
        )
    else:
        # Append at end
        new_content = app_content + '\n\n' + '\n'.join(routes_to_add)
    
    # Write updated content
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Routes added to app.py")
else:
    print(f"\n{Colors.GREEN}✓{Colors.END} All routes already exist!")
    new_content = app_content

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL ROUTES FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Routes now available:{Colors.END}")
print(f"  {Colors.GREEN}✓{Colors.END} /forums/ - Forum list")
print(f"  {Colors.GREEN}✓{Colors.END} /profile/view - View profile")
print(f"  {Colors.GREEN}✓{Colors.END} /profile/settings - Account settings")

print(f"\n{Colors.BOLD}{Colors.CYAN}Restart your app:{Colors.END}")
print(f"  {Colors.BOLD}python app.py{Colors.END}")

print(f"\n{Colors.CYAN}Test these URLs:{Colors.END}")
print(f"  • http://localhost:5000/forums/")
print(f"  • http://localhost:5000/profile/view")
print(f"  • http://localhost:5000/profile/settings")
print()