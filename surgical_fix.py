class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}SURGICAL FIX FOR app.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py line by line
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Backup
with open('app.py.backup_surgical', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_surgical{Colors.END}\n")

# New corrected lines
new_lines = []
skip_mode = False
register_route_found = False

i = 0
while i < len(lines):
    line = lines[i]
    
    # Find the broken registration route
    if "@app.route('/register'" in line and not register_route_found:
        print(f"{Colors.YELLOW}Found registration route at line {i+1}, replacing...{Colors.END}")
        register_route_found = True
        
        # Insert the correct registration route
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
        
        # Skip all the old broken registration code
        skip_mode = True
        i += 1
        continue
    
    # If we're in skip mode, look for the next route or function definition
    if skip_mode:
        # Check if we've reached another route or top-level function
        if line.startswith('@app.route') or (line.startswith('def ') and not line.startswith('    ')):
            skip_mode = False
            new_lines.append(line)
        i += 1
        continue
    
    # Normal mode - copy line as is
    new_lines.append(line)
    i += 1

# Write the fixed file
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ SURGICAL FIX COMPLETE!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Registration route has been completely replaced{Colors.END}")
print(f"{Colors.CYAN}All broken indentation removed{Colors.END}\n")

print(f"{Colors.BOLD}Now try:{Colors.END}")
print(f"  {Colors.CYAN}python app.py{Colors.END}\n")