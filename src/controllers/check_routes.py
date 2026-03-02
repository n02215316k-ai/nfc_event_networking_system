import sys
sys.path.insert(0, '.')

from app import app

print("=" * 80)
print("📋 ALL AVAILABLE ROUTES")
print("=" * 80)

routes = []
for rule in app.url_map.iter_rules():
    if 'events' in rule.endpoint:
        routes.append({
            'endpoint': rule.endpoint,
            'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
            'path': rule.rule
        })

print("\n🔍 Events-related routes:\n")
for route in sorted(routes, key=lambda x: x['endpoint']):
    print(f"  {route['endpoint']:30} {route['methods']:15} {route['path']}")

print("\n" + "=" * 80)
print("\n💡 The correct endpoint for home.html line 61 should be one of the above.")
print("   Most likely: 'events.browse' or 'events.index' or 'events.event_list'\n")