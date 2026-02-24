import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}INSTALLING LOGIN & LOGOUT ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Backup
with open('app.py.backup_auth', 'w', encoding='utf-8') as f:
    f.write(app_content)
print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup_auth\n")

AUTH_ROUTES = """

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''User login'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            import bcrypt
            from database import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Login successful
                session['user_id'] = user['id']
                session['full_name'] = user['full_name']
                session['email'] = user['email']
                session['role'] = user['role']
                
                flash(f'Welcome back, {user["full_name"]}!', 'success')
                
                # Redirect based on role
                if user['role'] == 'system_manager':
                    return redirect('/system/dashboard')
                elif user['role'] == 'event_admin':
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/dashboard')
            else:
                flash('Invalid email or password', 'danger')
                return redirect('/login')
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect('/login')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    '''User logout'''
    user_name = session.get('full_name', 'User')
    session.clear()
    flash(f'Goodbye, {user_name}! You have been logged out.', 'info')
    return redirect('/login')


@app.route('/forgot-password')
def forgot_password():
    '''Forgot password page (placeholder)'''
    flash('Password reset feature coming soon. Please contact admin.', 'info')
    return redirect('/login')

"""

# Check if routes already exist
if '@app.route(\'/login\'' in app_content:
    print(f"{Colors.YELLOW}⚠ Login route already exists!{Colors.END}")
    response = input(f"{Colors.YELLOW}Replace existing login route? (y/n): {Colors.END}")
    if response.lower() != 'y':
        print(f"{Colors.RED}Operation cancelled{Colors.END}")
        exit(0)
    # Remove old login route
    import re
    app_content = re.sub(r'@app\.route\(\'/login\'.*?\ndef login\(\):.*?(?=\n@app\.route|\nif __name__|$)', '', app_content, flags=re.DOTALL)

# Insert routes
if "if __name__ == '__main__':" in app_content:
    insertion_point = app_content.find("if __name__ == '__main__':")
    new_content = (
        app_content[:insertion_point] + 
        AUTH_ROUTES + 
        '\n\n' +
        app_content[insertion_point:]
    )
else:
    new_content = app_content + '\n\n' + AUTH_ROUTES

# Write
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ LOGIN & LOGOUT ROUTES INSTALLED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Routes added:{Colors.END}\n")
print(f"  {Colors.GREEN}✓{Colors.END} /login (GET, POST) - User authentication")
print(f"  {Colors.GREEN}✓{Colors.END} /logout - User logout")
print(f"  {Colors.GREEN}✓{Colors.END} /forgot-password - Password reset placeholder")

print(f"\n{Colors.BOLD}{Colors.CYAN}AUTHENTICATION SYSTEM READY!{Colors.END}\n")

print(f"{Colors.YELLOW}Features:{Colors.END}")
print(f"  • Secure password hashing (bcrypt)")
print(f"  • Session management")
print(f"  • Role-based redirects:")
print(f"    - system_manager → /system/dashboard")
print(f"    - event_admin → /admin/dashboard")
print(f"    - attendee → /dashboard")

print(f"\n{Colors.YELLOW}Restart your app:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")

print(f"{Colors.YELLOW}Test login at:{Colors.END}")
print(f"  {Colors.CYAN}http://localhost:5000/login{Colors.END}\n")