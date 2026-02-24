filepath = 'app.py'

print("\n📋 Checking app.py for registered blueprints...\n")
print("=" * 80)

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blueprints_to_check = {
        'event_admin_bp': 'Event Admin',
        'nfc_bp': 'NFC/QR Scanner',
    }
    
    print("IMPORTS:")
    for bp, name in blueprints_to_check.items():
        if f'import {bp}' in content or f'{bp}' in content:
            print(f"  ✓ {name} ({bp}) - Imported")
        else:
            print(f"  ✗ {name} ({bp}) - NOT IMPORTED")
    
    print("\nREGISTRATIONS:")
    for bp, name in blueprints_to_check.items():
        if f'register_blueprint({bp})' in content:
            print(f"  ✓ {name} ({bp}) - Registered")
        else:
            print(f"  ✗ {name} ({bp}) - NOT REGISTERED")
    
    print("\n" + "=" * 80)
    
    if 'event_admin_bp' not in content:
        print("\n⚠️  Blueprints are NOT registered!")
        print("\nAdd these lines to app.py:")
        print("\n# After other imports:")
        print("from src.controllers.event_admin_controller import event_admin_bp")
        print("from src.controllers.nfc_controller import nfc_bp")
        print("\n# After other blueprint registrations:")
        print("app.register_blueprint(event_admin_bp)")
        print("app.register_blueprint(nfc_bp)")

except Exception as e:
    print(f"Error: {e}")