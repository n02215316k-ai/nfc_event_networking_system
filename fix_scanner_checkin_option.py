import os

print("=" * 80)
print("🔧 FIXING SCANNER - ALWAYS SHOW CHECK-IN OPTION")
print("=" * 80)

scanner_path = 'templates/nfc/scanner.html'

with open(scanner_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the scan mode dropdown to always show both options
old_dropdown = '''                        <select class="form-select form-select-lg" id="scan_mode" name="scan_mode">
                            <option value="network">📱 Network - Exchange Contact Info</option>
                            {% if user_events %}
                            <option value="checkin">✅ Check-In/Out - Mark Attendance</option>
                            {% endif %}
                        </select>'''

new_dropdown = '''                        <select class="form-select form-select-lg" id="scan_mode" name="scan_mode">
                            <option value="network">📱 Network - Exchange Contact Info</option>
                            <option value="checkin">✅ Check-In/Out - Mark Attendance</option>
                        </select>'''

content = content.replace(old_dropdown, new_dropdown)

# Also update the event selector to show a message when no events
old_event_selector = '''                        <select class="form-select form-select-lg" id="event_id" name="event_id">
                            <option value="">-- Choose Event --</option>
                            {% if user_events %}
                                {% for event in user_events %}
                                <option value="{{ event.id }}" {{ 'selected' if event_id and event.id == event_id|int else '' }}>
                                    {{ event.title }} - {{ event.start_date.strftime('%b %d, %Y') }}
                                </option>
                                {% endfor %}
                            {% endif %}
                        </select>'''

new_event_selector = '''                        <select class="form-select form-select-lg" id="event_id" name="event_id">
                            <option value="">-- Choose Event --</option>
                            {% if user_events %}
                                {% for event in user_events %}
                                <option value="{{ event.id }}" {{ 'selected' if event_id and event.id == event_id|int else '' }}>
                                    {{ event.title }} - {{ event.start_date.strftime('%b %d, %Y') }}
                                </option>
                                {% endfor %}
                            {% else %}
                                <option value="" disabled>No events available</option>
                            {% endif %}
                        </select>'''

content = content.replace(old_event_selector, new_event_selector)

# Add a note when no events are available
old_small_text = '''                        <small class="text-muted">Select the event to check attendees in/out</small>'''

new_small_text = '''                        <small class="text-muted">
                            {% if user_events %}
                            Select the event to check attendees in/out
                            {% else %}
                            <span class="text-warning">⚠️ You don't have any events yet. <a href="{{ url_for('events.my_events') }}">Create one</a> to use check-in mode.</span>
                            {% endif %}
                        </small>'''

content = content.replace(old_small_text, new_small_text)

# Write back
with open(scanner_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Scanner updated!")
print("\n📋 Changes made:")
print("   ✅ Check-in option now always visible in dropdown")
print("   ✅ Shows helpful message when no events available")
print("   ✅ Links to create events page")

print("\n" + "=" * 80)
print("✅ FIX COMPLETE!")
print("=" * 80)
print("\n🔄 Restart Flask and test:")
print("   python app.py")
print("\n   Both options should now be visible:")
print("   • 📱 Network - Exchange Contact Info")
print("   • ✅ Check-In/Out - Mark Attendance")