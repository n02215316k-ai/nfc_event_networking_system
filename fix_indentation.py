class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING INDENTATION IN app.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Backup
with open('app.py.backup_indent', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_indent{Colors.END}\n")

# Find and fix the registration route (around line 852-897)
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Find the registration route
    if "@app.route('/register'" in line:
        print(f"{Colors.CYAN}Found registration route at line {i+1}{Colors.END}")
        
        # Write the route decorator and function definition
        fixed_lines.append(line)  # @app.route
        i += 1
        fixed_lines.append(lines[i])  # def register():
        i += 1
        fixed_lines.append(lines[i])  # '''Public user registration'''
        i += 1
        fixed_lines.append(lines[i])  # if request.method == 'POST':
        i += 1
        
        # Now write the corrected registration logic
        fixed_lines.append("        full_name = request.form.get('full_name')\n")
        fixed_lines.append("        email = request.form.get('email')\n")
        fixed_lines.append("        password = request.form.get('password')\n")
        fixed_lines.append("        confirm_password = request.form.get('confirm_password')\n")
        fixed_lines.append("        phone_number = request.form.get('phone_number', '')\n")
        fixed_lines.append("        current_employment = request.form.get('current_employment', '')\n")
        fixed_lines.append("\n")
        fixed_lines.append("        if password != confirm_password:\n")
        fixed_lines.append("            flash('Passwords do not match', 'danger')\n")
        fixed_lines.append("            return redirect('/register')\n")
        fixed_lines.append("\n")
        fixed_lines.append("        try:\n")
        fixed_lines.append("            import uuid\n")
        fixed_lines.append("            from werkzeug.security import generate_password_hash\n")
        fixed_lines.append("            from database import get_db_connection\n")
        fixed_lines.append("\n")
        fixed_lines.append("            hashed = generate_password_hash(password)\n")
        fixed_lines.append("            nfc_badge_id = str(uuid.uuid4())[:8].upper()\n")
        fixed_lines.append("\n")
        fixed_lines.append("            conn = get_db_connection()\n")
        fixed_lines.append("            cursor = conn.cursor()\n")
        fixed_lines.append("\n")
        fixed_lines.append("            sql = \"INSERT INTO users (full_name, email, password_hash, phone_number, current_employment, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, 'attendee', %s)\"\n")
        fixed_lines.append("            cursor.execute(sql, (full_name, email, hashed, phone_number, current_employment, nfc_badge_id))\n")
        fixed_lines.append("\n")
        fixed_lines.append("            conn.commit()\n")
        fixed_lines.append("            cursor.close()\n")
        fixed_lines.append("            conn.close()\n")
        fixed_lines.append("\n")
        fixed_lines.append("            flash('Account created successfully! Please login.', 'success')\n")
        fixed_lines.append("            return redirect('/login')\n")
        fixed_lines.append("\n")
        fixed_lines.append("        except Exception as e:\n")
        fixed_lines.append("            print(f\"Registration error: {e}\")\n")
        fixed_lines.append("            if 'Duplicate entry' in str(e):\n")
        fixed_lines.append("                flash('Email already registered', 'danger')\n")
        fixed_lines.append("            else:\n")
        fixed_lines.append("                flash('Error creating account. Please try again.', 'danger')\n")
        fixed_lines.append("            return redirect('/register')\n")
        fixed_lines.append("\n")
        fixed_lines.append("    return render_template('register.html')\n")
        fixed_lines.append("\n")
        
        # Skip old registration code (find next route or function)
        while i < len(lines):
            if i > 0 and (lines[i].startswith('@app.route') or lines[i].startswith('def ')) and 'register' not in lines[i]:
                break
            i += 1
        
        print(f"{Colors.GREEN}✓ Fixed registration route{Colors.END}")
        continue
    
    fixed_lines.append(line)
    i += 1

# Write fixed file
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ INDENTATION FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.CYAN}python app.py{Colors.END} - Start Flask\n")