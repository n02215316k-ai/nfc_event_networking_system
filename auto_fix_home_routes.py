with open('templates/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix events.list to events.list_events
content = content.replace("url_for('events.list')", "url_for('events.list_events')")

# Fix index reference in notifications
content = content.replace(
    'href="{{ url_for(\'index\') }}" class="btn btn-sm btn-outline-primary">\n                        View All',
    'href="{{ url_for(\'notifications\') }}" class="btn btn-sm btn-outline-primary">\n                        View All'
)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ home.html routes fixed!")