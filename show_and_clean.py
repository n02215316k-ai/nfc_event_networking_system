class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}SHOWING BROKEN CODE AND CLEANING{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines around 962
print(f"{Colors.RED}Lines 955-970 (showing the error area):{Colors.END}\n")
for i in range(954, min(970, len(lines))):
    line_num = i + 1
    if line_num == 962:
        print(f"{Colors.RED}{line_num:4d}: {lines[i]}{Colors.END}", end='')
    else:
        print(f"{line_num:4d}: {lines[i]}", end='')

print(f"\n{Colors.YELLOW}{'='*70}{Colors.END}\n")

# Backup
with open('app.py.backup_clean', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_clean{Colors.END}\n")

# Clean approach: Remove ALL lines after register() that have weird indentation
new_lines = []
in_register = False
register_line = -1

for i, line in enumerate(lines):
    # Find where register route starts
    if "@app.route('/register'" in line:
        register_line = i
        in_register = True
        print(f"{Colors.CYAN}Found @app.route('/register') at line {i+1}{Colors.END}")
        
        # Add the complete correct registration route
        new_lines.append("@app.route('/register', methods=['GET', 'POST'])\n")
        new_lines.append("def register():\n")
        new_lines.append("    '''Public user registration'''\n")
        new_lines.append("    if request.method == 'POST':\n")
        new_lines.append("        full_name = request.form.get('full_name')\n")
        new_lines.append("        email = request.form.get('email')\n")
        new_lines.append("        password = request.form.get('password')\n")
        new_lines.append("        confirm_password = request.form.get('confirm_password')\n")
        new_lines.append("        phone_number = request.form.get('phone_number', '')\n")
        new_lines.append("        current_employment = request.form.get('current_employment', '')\n")
        new_lines.append("\n")
        new_lines.append("        if password != confirm_password:\n")
        new_lines.append("            flash('Passwords do not match', 'danger')\n")
        new_lines.append("            return redirect('/register')\n")
        new_lines.append("\n")
        new_lines.append("        try:\n")
        new_lines.append("            import uuid\n")
        new_lines.append("            from werkzeug.security import generate_password_hash\n")
        new_lines.append("            from database import get_db_connection\n")
        new_lines.append("\n")
        new_lines.append("            hashed = generate_password_hash(password)\n")
        new_lines.append("            nfc_badge_id = str(uuid.uuid4())[:8].upper()\n")
        new_lines.append("\n")
        new_lines.append("            conn = get_db_connection()\n")
        new_lines.append("            cursor = conn.cursor()\n")
        new_lines.append("\n")
        new_lines.append("            sql = \"INSERT INTO users (full_name, email, password_hash, phone_number, current_employment, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, 'attendee', %s)\"\n")
        new_lines.append("            cursor.execute(sql, (full_name, email, hashed, phone_number, current_employment, nfc_badge_id))\n")
        new_lines.append("\n")
        new_lines.append("            conn.commit()\n")
        new_lines.append("            cursor.close()\n")
        new_lines.append("            conn.close()\n")
        new_lines.append("\n")
        new_lines.append("            flash('Account created successfully! Please login.', 'success')\n")
        new_lines.append("            return redirect('/login')\n")
        new_lines.append("\n")
        new_lines.append("        except Exception as e:\n")
        new_lines.append("            print(f\"Registration error: {e}\")\n")
        new_lines.append("            if 'Duplicate entry' in str(e):\n")
        new_lines.append("                flash('Email already registered', 'danger')\n")
        new_lines.append("            else:\n")
        new_lines.append("                flash('Error creating account. Please try again.', 'danger')\n")
        new_lines.append("            return redirect('/register')\n")
        new_lines.append("\n")
        new_lines.append("    return render_template('register.html')\n")
        new_lines.append("\n")
        new_lines.append("\n")
        continue
    
    # Skip everything until we hit the next route/function at column 0
    if in_register:
        # If we find another @app.route or def at column 0, stop skipping
        if (line.startswith('@app.route') or line.startswith('def ')) and not line.startswith('    '):
            in_register = False
            print(f"{Colors.GREEN}Found next route/function at line {i+1}: {line.strip()[:50]}...{Colors.END}")
            new_lines.append(line)
        # Otherwise skip this line (it's broken registration code)
        continue
    
    # Normal lines - keep as is
    new_lines.append(line)

# Write cleaned file
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ CLEANED ALL ORPHANED CODE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Removed all broken registration code{Colors.END}")
print(f"{Colors.CYAN}Inserted clean registration route{Colors.END}\n")

print(f"{Colors.BOLD}Now try:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")