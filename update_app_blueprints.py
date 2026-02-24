import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

print(f"\n{Colors.CYAN}Updating app.py with new blueprints...{Colors.END}\n")

filepath = 'app.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already registered
    if 'event_admin_bp' in content and 'nfc_bp' in content:
        print(f"{Colors.YELLOW}○{Colors.END} Blueprints already registered")
    else:
        # Find the imports section
        import_section = """
from src.controllers.event_admin_controller import event_admin_bp
from src.controllers.nfc_controller import nfc_bp"""
        
        # Find the blueprint registration section
        register_section = """
    app.register_blueprint(event_admin_bp)
    app.register_blueprint(nfc_bp)"""
        
        # Add imports after other controller imports
        if 'from src.controllers.system_manager_controller import system_manager_bp' in content:
            content = content.replace(
                'from src.controllers.system_manager_controller import system_manager_bp',
                'from src.controllers.system_manager_controller import system_manager_bp' + import_section
            )
        
        # Add blueprint registrations
        if 'app.register_blueprint(system_manager_bp)' in content:
            content = content.replace(
                'app.register_blueprint(system_manager_bp)',
                'app.register_blueprint(system_manager_bp)' + register_section
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"{Colors.GREEN}✓{Colors.END} Updated app.py with new blueprints")

except Exception as e:
    print(f"{Colors.YELLOW}⚠{Colors.END} Could not auto-update app.py: {e}")
    print(f"\n{Colors.CYAN}Manual steps:{Colors.END}")
    print("1. Add these imports to app.py:")
    print("   from src.controllers.event_admin_controller import event_admin_bp")
    print("   from src.controllers.nfc_controller import nfc_bp")
    print("\n2. Register blueprints:")
    print("   app.register_blueprint(event_admin_bp)")
    print("   app.register_blueprint(nfc_bp)")

print(f"\n{Colors.GREEN}✅ Blueprint update complete!{Colors.END}\n")