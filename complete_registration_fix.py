class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}COMPLETE REGISTRATION FIX{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_complete', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_complete{Colors.END}\n")

# Define the complete registration route
registration_route = '''@app.route('/register', methods=['GET', 'POST'])
def register():
    \'\'\'Public user registration\'\'\'
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number', '')
        current_employment = request.form.get('current_employment', '')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect('/register')

        try:
            import uuid
            from werkzeug.security import generate_password_hash
            from database import get_db_connection

            hashed = generate_password_hash(password)
            nfc_badge_id = str(uuid.uuid4())[:8].upper()

            conn = get_db_connection()
            cursor = conn.cursor()

            sql = "INSERT INTO users (full_name, email, password_hash, phone_number, current_employment, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, 'attendee', %s)"
            cursor.execute(sql, (full_name, email, hashed, phone_number, current_employment, nfc_badge_id))

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

'''

# Find the start of the registration route
import re

# Pattern to find registration route start
pattern = r"@app\.route\('/register',.*?\n.*?def register\(\):.*?\n(?:.*?\n){0,100}?(?=@app\.route|def \w+\(|$)"

# Replace the entire registration route
content = re.sub(pattern, registration_route, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ REGISTRATION COMPLETELY REWRITTEN!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}The registration route has been completely replaced{Colors.END}\n")

print(f"{Colors.BOLD}Try running Flask now:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")