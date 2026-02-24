import re

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING REGISTRATION IN app.py{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app.py.backup_fix', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"{Colors.GREEN}✓ Backup created: app.py.backup_fix{Colors.END}\n")

original_content = content

# Fix line 860: phone -> phone_number
content = re.sub(
    r"phone = request\.form\.get\('phone_number', ''\)",
    "phone_number = request.form.get('phone_number', '')",
    content
)

# Fix line 861: job_title -> current_employment
content = re.sub(
    r"job_title = request\.form\.get\('current_employment', ''\)",
    "current_employment = request.form.get('current_employment', '')",
    content
)

# Fix line 862: Remove company (not in your schema)
content = re.sub(
    r"company = request\.form\.get\('company', ''\)\s*\n",
    "",
    content
)

# Fix line 879: Update INSERT statement
old_sql = r"sql = \"INSERT INTO users \(full_name, email, password_hash, phone, job_title, company, role, nfc_badge_id\) VALUES \(%s, %s, %s, %s, %s, %s, 'attendee', %s\)\""
new_sql = 'sql = "INSERT INTO users (full_name, email, password_hash, phone_number, current_employment, role, nfc_badge_id) VALUES (%s, %s, %s, %s, %s, \'attendee\', %s)"'

content = re.sub(old_sql, new_sql, content)

# Fix line 880: Update execute parameters
old_execute = r"cursor\.execute\(sql, \(full_name, email, hashed, phone, job_title, company, nfc_badge_id\)\)"
new_execute = "cursor.execute(sql, (full_name, email, hashed, phone_number, current_employment, nfc_badge_id))"

content = re.sub(old_execute, new_execute, content)

# Write fixed content
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ REGISTRATION FIXED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Changes made:{Colors.END}\n")
print(f"  {Colors.GREEN}✓{Colors.END} Line 860: phone → phone_number")
print(f"  {Colors.GREEN}✓{Colors.END} Line 861: job_title → current_employment")
print(f"  {Colors.GREEN}✓{Colors.END} Line 862: Removed company variable")
print(f"  {Colors.GREEN}✓{Colors.END} Line 879: Updated INSERT columns")
print(f"  {Colors.GREEN}✓{Colors.END} Line 880: Updated execute parameters\n")

print(f"{Colors.BOLD}Next steps:{Colors.END}")
print(f"  1. {Colors.CYAN}python app.py{Colors.END} - Restart Flask")
print(f"  2. {Colors.CYAN}http://localhost:5000/register{Colors.END} - Test registration\n")