import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Registering blueprints in app.py...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already registered
    if 'app.register_blueprint(event_admin_bp)' in content:
        print(f"{Colors.YELLOW}○{Colors.END} Blueprints already registered")
    else:
        # Find where other blueprints are registered
        lines = content.split('\n')
        insert_index = -1
        
        for i, line in enumerate(lines):
            if 'app.register_blueprint(' in line:
                insert_index = i + 1
        
        if insert_index > 0:
            # Add the registrations
            lines.insert(insert_index, '    app.register_blueprint(event_admin_bp)')
            lines.insert(insert_index + 1, '    app.register_blueprint(nfc_bp)')
            
            # Write back
            content = '\n'.join(lines)
            
            # Backup
            with open(filepath + '.backup', 'w', encoding='utf-8') as f:
                f.write('\n'.join(content.split('\n')))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"{Colors.GREEN}✓{Colors.END} Registered event_admin_bp")
            print(f"{Colors.GREEN}✓{Colors.END} Registered nfc_bp")
            print(f"{Colors.GREEN}✓{Colors.END} Backup created: app.py.backup")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.END} Could not find registration location")
            print("\nManually add these lines to app.py (after other register_blueprint calls):")
            print("    app.register_blueprint(event_admin_bp)")
            print("    app.register_blueprint(nfc_bp)")
    
    print(f"\n{Colors.GREEN}✅ Blueprint registration complete!{Colors.END}\n")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Error: {e}")
    print(f"\n{Colors.CYAN}Manual fix:{Colors.END}")
    print("Open app.py and add these lines after the other app.register_blueprint() calls:")
    print("\n    app.register_blueprint(event_admin_bp)")
    print("    app.register_blueprint(nfc_bp)")