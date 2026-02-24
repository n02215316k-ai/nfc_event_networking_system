import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Fixing profile_controller.py...{Colors.END}\n")

filepath = 'src/controllers/profile_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if login_required is already imported/defined
    if 'def login_required' in content or 'from functools import wraps' in content:
        print(f"{Colors.YELLOW}○{Colors.END} login_required already exists, checking placement...")
    else:
        # Add login_required decorator at the top after imports
        login_decorator = """
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
"""
        
        # Find the Blueprint definition line
        if 'profile_bp = Blueprint' in content:
            # Insert decorator definition after Blueprint and before first route
            parts = content.split('profile_bp = Blueprint')
            if len(parts) == 2:
                # Add after the blueprint definition
                blueprint_line = parts[1].split('\n')[0]
                content = parts[0] + 'profile_bp = Blueprint' + blueprint_line + '\n' + login_decorator + '\n'.join(parts[1].split('\n')[1:])
        
    # Ensure imports are present
    if 'from functools import wraps' not in content:
        # Add import at the top
        lines = content.split('\n')
        import_index = 0
        for i, line in enumerate(lines):
            if line.startswith('from flask import') or line.startswith('import '):
                import_index = i + 1
        
        lines.insert(import_index, 'from functools import wraps')
        content = '\n'.join(lines)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Fixed profile_controller.py")
    print(f"\n{Colors.GREEN}✅ Profile controller fixed successfully!{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")
    print(f"\n{Colors.CYAN}Manual fix needed:{Colors.END}")
    print(f"Open: {filepath}")
    print(f"\nAdd this after the Blueprint definition:\n")
    print("""
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
""")