import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}INSTALLING USER CREATION ROUTES{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Backup
with open('app.py.backup_creation', 'w', encoding='utf-8') as f:
    f.write(app_content)
print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup_creation\n")

CREATION_ROUTES = """

# ============================================================================
# USER CREATION & REGISTRATION ROUTES
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Public user registration'''
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone', '')
        job_title = request.form.get('job_title', '')
        company = request.form.get('company', '')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect('/register')
        
        try:
            import bcrypt
            import uuid
            from database import get_db_connection
            
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            nfc_badge_id = str(uuid.uuid4())[:8].upper()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (full_name, email, password, phone, job_title, company, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, %s, 'attendee', %s)"
            cursor.execute(sql, (full_name, email, hashed, phone, job_title, company, nfc_badge_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect('/login')
            
        except Exception as e:
            print(f"Registration error: {e}")
            if 'Duplicate entry' in str(e):
                flash('Email already registered', 'danger')
            else:
                flash('Error creating account. Please try again.', 'danger')
            return redirect('/register')
    
    return render_template('register.html')


@app.route('/admin/users/create', methods=['GET', 'POST'])
def admin_create_user():
    '''Admin creates new user'''
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'warning')
        return redirect('/login')
    
    if session.get('role') not in ['event_admin', 'system_manager']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect('/')
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        phone = request.form.get('phone', '')
        job_title = request.form.get('job_title', '')
        company = request.form.get('company', '')
        nfc_badge_id = request.form.get('nfc_badge_id', '')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect('/admin/users/create')
        
        if role == 'system_manager' and session.get('role') != 'system_manager':
            flash('Only system managers can create other system managers', 'danger')
            return redirect('/admin/users/create')
        
        try:
            import bcrypt
            import uuid
            from database import get_db_connection
            
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if not nfc_badge_id:
                nfc_badge_id = str(uuid.uuid4())[:8].upper()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (full_name, email, password, phone, job_title, company, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (full_name, email, hashed, phone, job_title, company, role, nfc_badge_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash(f'User created successfully with role: {role}', 'success')
            return redirect('/admin/users')
            
        except Exception as e:
            print(f"User creation error: {e}")
            if 'Duplicate entry' in str(e):
                flash('Email already exists', 'danger')
            else:
                flash('Error creating user. Please try again.', 'danger')
            return redirect('/admin/users/create')
    
    return render_template('admin/create_user.html')


@app.route('/system/create-admin', methods=['GET', 'POST'])
def system_create_admin():
    '''System manager quick admin creation'''
    if 'user_id' not in session:
        flash('Please login to access system panel', 'warning')
        return redirect('/login')
    
    if session.get('role') != 'system_manager':
        flash('Access denied. System manager privileges required.', 'danger')
        return redirect('/')
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        try:
            import bcrypt
            import uuid
            from database import get_db_connection
            
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            nfc_badge_id = str(uuid.uuid4())[:8].upper()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (full_name, email, password, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (full_name, email, hashed, role, nfc_badge_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash(f'{role.replace("_", " ").title()} created successfully!', 'success')
            return redirect('/system/users')
            
        except Exception as e:
            print(f"Admin creation error: {e}")
            if 'Duplicate entry' in str(e):
                flash('Email already exists', 'danger')
            else:
                flash('Error creating admin. Please try again.', 'danger')
            return redirect('/system/create-admin')
    
    return render_template('system/create_admin.html')

"""

# Insert routes
if "if __name__ == '__main__':" in app_content:
    insertion_point = app_content.find("if __name__ == '__main__':")
    new_content = (
        app_content[:insertion_point] + 
        CREATION_ROUTES + 
        '\n\n' +
        app_content[insertion_point:]
    )
else:
    new_content = app_content + '\n\n' + CREATION_ROUTES

# Write
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ USER CREATION ROUTES INSTALLED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Routes added:{Colors.END}\n")
print(f"  {Colors.GREEN}✓{Colors.END} /register - Public registration")
print(f"  {Colors.GREEN}✓{Colors.END} /admin/users/create - Admin creates users")
print(f"  {Colors.GREEN}✓{Colors.END} /system/create-admin - Quick admin creator")

print(f"\n{Colors.BOLD}{Colors.CYAN}COMPLETE ADMIN CREATION SYSTEM READY!{Colors.END}\n")

print(f"{Colors.YELLOW}Restart your app:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")

print(f"{Colors.YELLOW}Then access:{Colors.END}")
print(f"  • Public Registration: http://localhost:5000/register")
print(f"  • Admin Create User: http://localhost:5000/admin/users/create")
print(f"  • System Create Admin: http://localhost:5000/system/create-admin\n")