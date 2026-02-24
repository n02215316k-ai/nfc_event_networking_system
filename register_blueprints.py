import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Registering new blueprints in app.py...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where to add imports (after other controller imports)
    import_index = -1
    for i, line in enumerate(lines):
        if 'from src.controllers' in line and 'import' in line:
            import_index = i + 1
    
    # Find where to add registrations (after other register_blueprint calls)
    register_index = -1
    for i, line in enumerate(lines):
        if 'app.register_blueprint' in line:
            register_index = i + 1
    
    # Check if already added
    content = ''.join(lines)
    
    if 'event_admin_bp' not in content:
        # Add imports
        if import_index > 0:
            lines.insert(import_index, 'from src.controllers.event_admin_controller import event_admin_bp\n')
            lines.insert(import_index + 1, 'from src.controllers.nfc_controller import nfc_bp\n')
            register_index += 2  # Adjust index
        
        # Add registrations
        if register_index > 0:
            lines.insert(register_index, '    app.register_blueprint(event_admin_bp)\n')
            lines.insert(register_index + 1, '    app.register_blueprint(nfc_bp)\n')
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"{Colors.GREEN}✓{Colors.END} Added event_admin_bp import and registration")
        print(f"{Colors.GREEN}✓{Colors.END} Added nfc_bp import and registration")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} Blueprints already registered")
    
    print(f"\n{Colors.GREEN}✅ Blueprints registered!{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")
    print(f"\n{Colors.CYAN}Please add manually to app.py:{Colors.END}\n")
    print("# Imports (add after other controller imports):")
    print("from src.controllers.event_admin_controller import event_admin_bp")
    print("from src.controllers.nfc_controller import nfc_bp")
    print("\n# Registrations (add after other app.register_blueprint calls):")
    print("app.register_blueprint(event_admin_bp)")
    print("app.register_blueprint(nfc_bp)")