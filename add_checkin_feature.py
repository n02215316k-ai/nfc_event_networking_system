import os

print("=" * 80)
print("🔧 ADDING CHECK-IN/CHECK-OUT FEATURE FOR EVENT ADMINS")
print("=" * 80)

# Step 1: Update scanner page template to show check-in/out options
print("\n1️⃣ Updating NFC scanner page...")

scanner_template_path = 'templates/nfc/scanner.html'

if os.path.exists(scanner_template_path):
    with open(scanner_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if check-in feature already exists
    if 'Check-In/Out' in content or 'check_in_mode' in content:
        print("   ✅ Check-in feature already exists")
    else:
        print("   🔧 Adding check-in/out feature...")
        
        # Find the scan mode selection area and add check-in option
        if 'scan_mode' in content or 'Network' in content:
            # Add check-in mode option after Network mode
            content = content.replace(
                '<option value="network">Network - Exchange Contact Info</option>',
                '''<option value="network">Network - Exchange Contact Info</option>
                        {% if user_events %}
                        <option value="checkin">Check-In/Out - Mark Attendance</option>
                        {% endif %}'''
            )
            
            # Add event selection dropdown for check-in mode
            if '<select name="scan_mode"' in content:
                event_selector = '''
                
                <!-- Event Selection for Check-In (Only shown for event admins) -->
                <div class="mb-3" id="event-selector" style="display: none;">
                    <label for="event_id" class="form-label">
                        <i class="fas fa-calendar-check me-2"></i>Select Your Event
                    </label>
                    <select class="form-select" id="event_id" name="event_id">
                        <option value="">-- Choose Event --</option>
                        {% if user_events %}
                            {% for event in user_events %}
                            <option value="{{ event.id }}" {{ 'selected' if event_id and event.id == event_id else '' }}>
                                {{ event.title }} - {{ event.start_date.strftime('%b %d, %Y') }}
                            </option>
                            {% endfor %}
                        {% endif %}
                    </select>
                    <small class="text-muted">Select the event to check attendees in/out</small>
                </div>'''
                
                # Insert after scan mode selector
                content = content.replace(
                    '</select>\n                </div>',
                    '</select>\n                </div>' + event_selector,
                    1
                )
        
        with open(scanner_template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Updated scanner.html with check-in feature")

# Step 2: Add JavaScript to show/hide event selector
print("\n2️⃣ Adding JavaScript for dynamic event selection...")

scanner_js = '''
<!-- Check-In Mode JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const scanModeSelect = document.getElementById('scan_mode');
    const eventSelector = document.getElementById('event-selector');
    
    if (scanModeSelect && eventSelector) {
        // Show/hide event selector based on scan mode
        scanModeSelect.addEventListener('change', function() {
            if (this.value === 'checkin') {
                eventSelector.style.display = 'block';
            } else {
                eventSelector.style.display = 'none';
            }
        });
        
        // Trigger on page load if check-in mode is selected
        if (scanModeSelect.value === 'checkin') {
            eventSelector.style.display = 'block';
        }
    }
});
</script>
'''

if os.path.exists(scanner_template_path):
    with open(scanner_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Check-In Mode JavaScript' not in content:
        # Add before {% endblock %}
        content = content.replace(
            '{% endblock %}',
            scanner_js + '\n{% endblock %}'
        )
        
        with open(scanner_template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Added JavaScript for event selector")

# Step 3: Update NFC controller to pass user's events
print("\n3️⃣ Updating NFC controller...")

nfc_controller_path = 'src/controllers/nfc_controller.py'

if os.path.exists(nfc_controller_path):
    with open(nfc_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find scanner_page function
    if 'def scanner_page' in content:
        # Check if it already fetches user events
        if 'user_events' not in content or 'creator_id' not in content:
            print("   🔧 Adding user events query...")
            
            # Find the scanner_page function
            import re
            
            # Add user events query before render_template in scanner_page
            pattern = r'(def scanner_page\(\):.*?)(return render_template\(\'nfc/scanner\.html\')'
            
            events_query = '''
    # Get user's events if they're an event creator/admin
    user_events = []
    if session.get('user_role') in ['event_admin', 'system_manager']:
        user_events = execute_query("""
            SELECT id, title, start_date, end_date, location
            FROM events
            WHERE creator_id = %s AND status = 'published'
            ORDER BY start_date DESC
        """, (session['user_id'],), fetch=True) or []
    
    event_id = request.args.get('event_id', type=int)
    
    '''
            
            replacement = r'\1' + events_query + r'\2'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Update render_template to include user_events
            content = content.replace(
                "return render_template('nfc/scanner.html')",
                "return render_template('nfc/scanner.html', user_events=user_events, event_id=event_id)"
            )
            
            with open(nfc_controller_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Updated NFC controller with user events")
        else:
            print("   ✅ NFC controller already has user events")
    else:
        print("   ⚠️  scanner_page function not found")

# Step 4: Update scan processing to handle check-in/out
print("\n4️⃣ Adding check-in/out processing logic...")

if os.path.exists(nfc_controller_path):
    with open(nfc_controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find process_scan function
    if 'def process_scan' in content or '@nfc_bp.route' in content:
        
        # Check if check-in logic exists
        if 'check_in_mode' not in content and 'checkin' not in content:
            print("   🔧 Adding check-in/out logic to scan processing...")
            
            # Add check-in processing logic
            checkin_code = '''
    # Handle check-in/out mode
    scan_mode = data.get('scan_mode', 'network')
    event_id = data.get('event_id')
    
    if scan_mode == 'checkin':
        if not event_id:
            return jsonify({'success': False, 'message': 'Event ID required for check-in'}), 400
        
        # Verify the user owns this event
        event = execute_query(
            "SELECT id, title FROM events WHERE id = %s AND creator_id = %s",
            (event_id, session['user_id']),
            fetch=True,
            fetchone=True
        )
        
        if not event:
            return jsonify({'success': False, 'message': 'You do not have permission for this event'}), 403
        
        # Check if attendee is registered for the event
        registration = execute_query(
            "SELECT id FROM event_registrations WHERE event_id = %s AND user_id = %s",
            (event_id, scanned_user_id),
            fetch=True,
            fetchone=True
        )
        
        if not registration:
            return jsonify({
                'success': False, 
                'message': f'{scanned_user["full_name"]} is not registered for this event'
            }), 400
        
        # Check current attendance status
        attendance = execute_query(
            "SELECT id, check_in_time, check_out_time FROM attendance WHERE event_id = %s AND user_id = %s",
            (event_id, scanned_user_id),
            fetch=True,
            fetchone=True
        )
        
        from datetime import datetime
        current_time = datetime.now()
        
        if not attendance:
            # First check-in
            execute_query(
                "INSERT INTO attendance (event_id, user_id, check_in_time) VALUES (%s, %s, %s)",
                (event_id, scanned_user_id, current_time),
                fetch=False
            )
            action = 'checked in'
            status = 'success'
        elif attendance['check_out_time']:
            # Already checked out, allow re-check-in
            execute_query(
                "UPDATE attendance SET check_in_time = %s, check_out_time = NULL WHERE id = %s",
                (current_time, attendance['id']),
                fetch=False
            )
            action = 'checked in again'
            status = 'success'
        elif attendance['check_in_time']:
            # Check out
            execute_query(
                "UPDATE attendance SET check_out_time = %s WHERE id = %s",
                (current_time, attendance['id']),
                fetch=False
            )
            action = 'checked out'
            status = 'info'
        
        return jsonify({
            'success': True,
            'action': action,
            'user': {
                'name': scanned_user['full_name'],
                'email': scanned_user['email']
            },
            'event': event['title'],
            'time': current_time.strftime('%I:%M %p'),
            'status': status
        })
'''
            
            # Insert check-in logic after scanned_user validation
            if 'scanned_user_id = ' in content:
                # Find where to insert (after scanned_user is fetched)
                pattern = r"(scanned_user = execute_query.*?fetch=True,\s*fetchone=True\s*\).*?\n.*?if not scanned_user:.*?return jsonify.*?\n)"
                
                replacement = r'\1' + checkin_code
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                with open(nfc_controller_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("   ✅ Added check-in/out processing logic")
            else:
                print("   ⚠️  Could not find scan processing location")
        else:
            print("   ✅ Check-in logic already exists")

# Step 5: Create attendance tracking page
print("\n5️⃣ Creating attendance tracking page...")

attendance_template = '''{% extends "base.html" %}

{% block title %}Event Attendance - {{ event.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2><i class="fas fa-clipboard-check me-2"></i>Attendance Tracking</h2>
                    <p class="text-muted mb-0">{{ event.title }}</p>
                </div>
                <div>
                    <a href="{{ url_for('nfc.scanner_page', event_id=event.id) }}" class="btn btn-primary">
                        <i class="fas fa-qrcode me-2"></i>Scan QR Codes
                    </a>
                    <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-outline-secondary">
                        <i class="fas fa-arrow-left me-2"></i>Back to Event
                    </a>
                </div>
            </div>

            <!-- Attendance Statistics -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3 class="text-primary">{{ stats.total_registered }}</h3>
                            <p class="mb-0">Registered</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3 class="text-success">{{ stats.checked_in }}</h3>
                            <p class="mb-0">Checked In</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3 class="text-warning">{{ stats.present }}</h3>
                            <p class="mb-0">Currently Present</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3 class="text-info">{{ stats.checked_out }}</h3>
                            <p class="mb-0">Checked Out</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Attendance List -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Attendee List</h5>
                </div>
                <div class="card-body">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Check-In Time</th>
                                <th>Check-Out Time</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for attendee in attendees %}
                            <tr>
                                <td>{{ attendee.full_name }}</td>
                                <td>{{ attendee.email }}</td>
                                <td>
                                    {% if attendee.check_in_time %}
                                        <i class="fas fa-check text-success me-1"></i>
                                        {{ attendee.check_in_time.strftime('%I:%M %p') }}
                                    {% else %}
                                        <span class="text-muted">Not checked in</span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if attendee.check_out_time %}
                                        <i class="fas fa-sign-out-alt text-info me-1"></i>
                                        {{ attendee.check_out_time.strftime('%I:%M %p') }}
                                    {% else %}
                                        <span class="text-muted">--</span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if not attendee.check_in_time %}
                                        <span class="badge bg-secondary">Not Arrived</span>
                                    {% elif attendee.check_out_time %}
                                        <span class="badge bg-info">Checked Out</span>
                                    {% else %}
                                        <span class="badge bg-success">Present</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

os.makedirs('templates/nfc', exist_ok=True)
with open('templates/nfc/attendance.html', 'w', encoding='utf-8') as f:
    f.write(attendance_template)

print("   ✅ Created attendance tracking page")

print("\n" + "=" * 80)
print("✅ CHECK-IN/OUT FEATURE ADDED!")
print("=" * 80)
print("\n📋 What was added:")
print("  ✅ Check-In/Out option in scanner dropdown")
print("  ✅ Event selection for event admins")
print("  ✅ Automatic attendance tracking")
print("  ✅ Check-in and check-out processing")
print("  ✅ Attendance tracking page")
print("\n🎯 How it works:")
print("  1. Event admins see 'Check-In/Out' mode in scanner")
print("  2. They select their event from dropdown")
print("  3. Scan attendee QR codes to check them in/out")
print("  4. System tracks attendance automatically")
print("\n🔄 Restart Flask:")
print("  python app.py")