from app import app

print("\n" + "="*80)
print("AVAILABLE ROUTES")
print("="*80 + "\n")

routes = []
for rule in app.url_map.iter_rules():
    routes.append({
        'endpoint': rule.endpoint,
        'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
        'path': rule.rule
    })

# Sort by endpoint
routes.sort(key=lambda x: x['endpoint'])

current_blueprint = None
for route in routes:
    blueprint = route['endpoint'].split('.')[0] if '.' in route['endpoint'] else 'main'
    
    if blueprint != current_blueprint:
        print(f"\n📘 {blueprint.upper()}")
        print("-" * 80)
        current_blueprint = blueprint
    
    print(f"  {route['endpoint']:40} {route['methods']:15} {route['path']}")

print("\n" + "="*80 + "\n")