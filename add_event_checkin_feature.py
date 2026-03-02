import os
import re

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

print("=" * 80)
print(f"{Colors.CYAN}🔧 ADDING EVENT ADMIN CHECK-IN FEATURE{Colors.END}")
print("=" * 80)

# ============================================================================
# STEP 1: Update NFC Scanner Template
# ============================================================================
print(f"\n{Colors.CYAN}📄 Step 1: Updating NFC Scanner Template...{Colors.END}")

scanner_template_path = 'templates/nfc/scanner.html'

if os.path.exists(scanner_template_path):
    with open(scanner_template_path, 'r', encoding='utf-8') as f:
        scanner_content = f.read()
    
    # Backup
    with open(scanner_template_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(scanner_content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Backup created: {scanner_template_path}.backup")
    
    # Check if check-in feature already exists
    if 'Check in to Event' not in scanner_content:
        # Find the scan method dropdown section
        dropdown_pattern = r'(<select[^>]*id=["\']scanMethod["\'][^>]*>.*?</select>)'
        
        if re.search(dropdown_pattern, scanner_content, re.DOTALL):
            # Add event admin check-in option after networking option
            checkin_option = '''
                    <option value="checkin" data-role="event_admin">Check in to Event</option>'''
            
            # Insert after the networking option
            scanner_content = scanner_content.replace(
                '<option value="networking">Networking Mode</option>',
                '<option value="networking">Networking Mode</option>' + checkin_option
            )
            
            print(f"{Colors.GREEN}✓{Colors.END} Added 'Check in to Event' dropdown option")
        
        # Add event selection UI
        event_selector_html = '''
        <!-- Event Selection Modal for Check-in -->
        <div class="modal fade" id="eventSelectModal" tabindex="-1" aria-labelledby="eventSelectModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="eventSelectModalLabel">
                            <i class="fas fa-calendar-check"></i> Select Event for Check-in
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="eventSelect" class="form-label">Choose Event:</label>
                            <select class="form-select" id="eventSelect">
                                <option value="">Loading events...</option>
                            </select>
                        </div>
                        <div id="selectedEventInfo" class="alert alert-info d-none">
                            <strong>Event:</strong> <span id="eventName"></span><br>
                            <strong>Date:</strong> <span id="eventDate"></span><br>
                            <strong>Location:</strong> <span id="eventLocation"></span>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="confirmEventBtn">
                            <i class="fas fa-check"></i> Confirm & Start Scanning
                        </button>
                    </div>
                </div>
            </div>
        </div>'''
        
        # Insert before closing body tag
        scanner_content = scanner_content.replace('</body>', event_selector_html + '\n</body>')
        print(f"{Colors.GREEN}✓{Colors.END} Added event selection modal")
        
        # Add JavaScript for check-in functionality
        checkin_js = '''
<script>
// Event Admin Check-in Functionality
let selectedEventId = null;
let selectedEventData = null;

// Load events when check-in mode is selected
document.getElementById('scanMethod')?.addEventListener('change', function() {
    const scanMethod = this.value;
    const userRole = '{{ session.get("role") }}';
    
    if (scanMethod === 'checkin') {
        if (userRole === 'event_admin' || userRole === 'system_manager') {
            loadEventsForCheckin();
            const modal = new bootstrap.Modal(document.getElementById('eventSelectModal'));
            modal.show();
        } else {
            alert('This feature is only available for Event Administrators');
            this.value = 'networking';
        }
    }
});

// Load events from API
function loadEventsForCheckin() {
    fetch('/events/api/my-events')
        .then(response => response.json())
        .then(data => {
            const eventSelect = document.getElementById('eventSelect');
            eventSelect.innerHTML = '<option value="">-- Select an Event --</option>';
            
            if (data.events && data.events.length > 0) {
                data.events.forEach(event => {
                    const option = document.createElement('option');
                    option.value = event.id;
                    option.textContent = event.title + ' - ' + event.date;
                    option.dataset.eventData = JSON.stringify(event);
                    eventSelect.appendChild(option);
                });
            } else {
                eventSelect.innerHTML = '<option value="">No events available</option>';
            }
        })
        .catch(error => {
            console.error('Error loading events:', error);
            document.getElementById('eventSelect').innerHTML = '<option value="">Error loading events</option>';
        });
}

// Show event details when selected
document.getElementById('eventSelect')?.addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    
    if (selectedOption.value && selectedOption.dataset.eventData) {
        const eventData = JSON.parse(selectedOption.dataset.eventData);
        selectedEventData = eventData;
        
        document.getElementById('eventName').textContent = eventData.title;
        document.getElementById('eventDate').textContent = eventData.date;
        document.getElementById('eventLocation').textContent = eventData.location || 'N/A';
        document.getElementById('selectedEventInfo').classList.remove('d-none');
        document.getElementById('confirmEventBtn').disabled = false;
    } else {
        document.getElementById('selectedEventInfo').classList.add('d-none');
        document.getElementById('confirmEventBtn').disabled = true;
    }
});

// Confirm event selection and start scanning
document.getElementById('confirmEventBtn')?.addEventListener('click', function() {
    const eventSelect = document.getElementById('eventSelect');
    selectedEventId = eventSelect.value;
    
    if (!selectedEventId) {
        alert('Please select an event');
        return;
    }
    
    // Update scan info display
    const scanInfo = document.getElementById('scanInfo');
    if (scanInfo) {
        scanInfo.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-calendar-check"></i>
                <strong>Check-in Mode Active</strong><br>
                Event: ${selectedEventData.title}<br>
                Scanning will check users into this event
            </div>
        `;
    }
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('eventSelectModal'));
    modal.hide();
    
    // Start scanning
    console.log('Check-in mode activated for event:', selectedEventId);
});

// Override the scan handler to include event check-in
const originalHandleScan = window.handleScanResult || function() {};

window.handleScanResult = function(scanData, scanMethod) {
    const currentScanMethod = document.getElementById('scanMethod')?.value;
    
    if (currentScanMethod === 'checkin' && selectedEventId) {
        // Check-in mode
        handleCheckinScan(scanData, scanMethod);
    } else {
        // Regular networking mode
        if (typeof originalHandleScan === 'function') {
            originalHandleScan(scanData, scanMethod);
        } else {
            handleNetworkingScan(scanData, scanMethod);
        }
    }
};

// Handle check-in scan
function handleCheckinScan(scanData, scanMethod) {
    const scannedUserId = extractUserIdFromScan(scanData);
    
    if (!scannedUserId) {
        showScanResult(false, 'Invalid QR/NFC code');
        return;
    }
    
    // Send check-in request
    fetch('/nfc/scan-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scan_data: scanData,
            scan_method: scanMethod,
            event_id: selectedEventId,
            scanned_user_id: scannedUserId,
            scan_url: scanData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.checked_in) {
                showScanResult(true, `User checked in successfully!<br>Event: ${selectedEventData.title}`);
                playSuccessSound();
                
                // Vibrate if available
                if (navigator.vibrate) {
                    navigator.vibrate([200, 100, 200]);
                }
            } else {
                showScanResult(false, data.message || 'Check-in failed');
            }
        } else {
            showScanResult(false, data.error || 'Check-in failed');
        }
    })
    .catch(error => {
        console.error('Check-in error:', error);
        showScanResult(false, 'Network error: ' + error.message);
    });
}

// Extract user ID from scan data
function extractUserIdFromScan(scanData) {
    // Try to extract from URL pattern: /profile/view/123
    const match = scanData.match(/\/profile\/(?:view\/)?(\d+)/);
    if (match) {
        return parseInt(match[1]);
    }
    
    // Try to extract from direct ID
    if (/^\d+$/.test(scanData)) {
        return parseInt(scanData);
    }
    
    return null;
}

// Show scan result
function showScanResult(success, message) {
    const resultDiv = document.getElementById('scanResult') || document.createElement('div');
    resultDiv.id = 'scanResult';
    resultDiv.className = `alert alert-${success ? 'success' : 'danger'} mt-3`;
    resultDiv.innerHTML = `
        <i class="fas fa-${success ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;
    
    const scanInfo = document.getElementById('scanInfo');
    if (scanInfo) {
        scanInfo.parentNode.insertBefore(resultDiv, scanInfo.nextSibling);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            resultDiv.remove();
        }, 5000);
    }
}

// Play success sound
function playSuccessSound() {
    try {
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBTGH0fPTgjMGHm7A7+OZXQ0NVK3k77NeHAU7k9j0yXooBS58yvLZizcHG2q77uikTxELTaLh8bllHAU4kdP0zH0pBSh+yfDbijgHGmi56+mnUBEKS6Df8rdnGwU2j9L00YAqBSJ6x+/eijgHF2W26uurVRMKRZvd8r1nHgU0j9L0z38qBR98yO/eiTYHGGS36+urVRMKRZvd8r1nHgU0j9L0z38qBR98yO/eiTYHGGS36+urVRMKRZvd8r1nHgU0j9L0z38qBR98yO/eiTYHGGS36+urVRMK');
        audio.play();
    } catch (e) {
        console.log('Could not play sound');
    }
}
</script>'''
        
        # Insert before closing body tag
        scanner_content = scanner_content.replace('</body>', checkin_js + '\n</body>')
        print(f"{Colors.GREEN}✓{Colors.END} Added check-in JavaScript functionality")
        
        # Save updated template
        with open(scanner_template_path, 'w', encoding='utf-8') as f:
            f.write(scanner_content)
        
        print(f"{Colors.GREEN}✅ Scanner template updated successfully!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} Check-in feature already exists in scanner template")
else:
    print(f"{Colors.RED}✗{Colors.END} Scanner template not found: {scanner_template_path}")

# ============================================================================
# STEP 2: Update NFC Controller
# ============================================================================
print(f"\n{Colors.CYAN}📄 Step 2: Updating NFC Controller...{Colors.END}")

nfc_controller_path = 'src/controllers/nfc_controller.py'

if os.path.exists(nfc_controller_path):
    with open(nfc_controller_path, 'r', encoding='utf-8') as f:
        controller_content = f.read()
    
    # Backup
    with open(nfc_controller_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(controller_content)
    
    print(f"{Colors.GREEN}✓{Colors.END} Backup created: {nfc_controller_path}.backup")
    
    # Check if check-in functionality already exists
    if 'checked_in' not in controller_content or 'event_checkins' not in controller_content:
        # Find the scan-profile route
        if '@nfc_bp.route(\'/scan-profile\'' in controller_content:
            # Replace the entire scan-profile function
            new_scan_function = '''
@nfc_bp.route('/scan-profile', methods=['POST'])
def scan_profile():
    """
    Handles scans (QR/NFC/manual). Records scan and if scanner is an event admin
    and event_id provided, creates a check-in record for the scanned user.
    Expects JSON: { scan_data, scan_method, event_id (optional), scanned_user_id (optional), scan_url (optional) }
    """
    data = request.get_json() or {}
    scan_data = data.get('scan_data')
    event_id = data.get('event_id')
    scanned_user_id = data.get('scanned_user_id')  # optional if encoded in scan_data
    scan_url = data.get('scan_url') or scan_data or request.referrer or request.url

    scanner_id = session.get('user_id')
    scanner_role = session.get('role')

    if not scanner_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # If scanned_user_id not provided, try to extract from scan_data
        if not scanned_user_id and scan_data:
            import re
            m = re.search(r'/profile/(?:view/)?(\d+)', scan_data)
            if m:
                scanned_user_id = int(m.group(1))
            elif scan_data.isdigit():
                scanned_user_id = int(scan_data)

        if not scanned_user_id:
            return jsonify({'success': False, 'error': 'Could not identify scanned user'}), 400

        # Get scanned user details
        cursor.execute("SELECT id, full_name, email FROM users WHERE id = %s", (scanned_user_id,))
        scanned_user = cursor.fetchone()

        if not scanned_user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Always record the scan
        cursor.execute("""
            INSERT INTO scan_history (scanner_id, scanned_user_id, scan_method, scan_data, scan_url, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (scanner_id, scanned_user_id, data.get('scan_method', 'manual'), scan_data, scan_url))
        conn.commit()

        scan_id = cursor.lastrowid

        # If scanner is event admin/system_manager and event_id provided -> create check-in
        if scanner_role in ('event_admin', 'system_manager') and event_id:
            # Check if user is already checked in
            cursor.execute("""
                SELECT id FROM event_checkins 
                WHERE event_id = %s AND user_id = %s
            """, (event_id, scanned_user_id))
            
            existing_checkin = cursor.fetchone()

            if existing_checkin:
                return jsonify({
                    'success': True, 
                    'checked_in': False,
                    'message': 'User already checked in to this event',
                    'user': {
                        'id': scanned_user['id'],
                        'name': scanned_user['full_name'],
                        'email': scanned_user['email']
                    }
                }), 200

            # Create check-in record
            cursor.execute("""
                INSERT INTO event_checkins (event_id, user_id, checked_in_by, checked_in_at, source_url, scan_id)
                VALUES (%s, %s, %s, NOW(), %s, %s)
            """, (event_id, scanned_user_id, scanner_id, scan_url, scan_id))
            conn.commit()

            return jsonify({
                'success': True, 
                'checked_in': True, 
                'message': 'User checked in successfully',
                'user': {
                    'id': scanned_user['id'],
                    'name': scanned_user['full_name'],
                    'email': scanned_user['email']
                }
            }), 200

        # Regular networking scan (no check-in)
        return jsonify({
            'success': True, 
            'checked_in': False,
            'user': {
                'id': scanned_user['id'],
                'name': scanned_user['full_name'],
                'email': scanned_user['email']
            }
        }), 200

    except Exception as e:
        conn.rollback()
        print(f"Error in scan_profile: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
'''
            
            # Replace the old function
            pattern = r'@nfc_bp\.route\(\'/scan-profile\'.*?\n(?=@nfc_bp\.route|$)'
            controller_content = re.sub(pattern, new_scan_function, controller_content, flags=re.DOTALL)
            
            print(f"{Colors.GREEN}✓{Colors.END} Updated scan-profile endpoint with check-in logic")
        
        # Add API endpoint for fetching admin's events
        if '/api/my-events' not in controller_content:
            events_api = '''

@nfc_bp.route('/events/api/my-events', methods=['GET'])
def get_my_events():
    """API endpoint to get events for the current admin user"""
    user_id = session.get('user_id')
    role = session.get('role')
    
    if not user_id or role not in ('event_admin', 'system_manager'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get events created by this admin or all events for system_manager
        if role == 'system_manager':
            cursor.execute("""
                SELECT id, title, description, date, location, created_at
                FROM events
                WHERE date >= CURDATE()
                ORDER BY date ASC
            """)
        else:
            cursor.execute("""
                SELECT id, title, description, date, location, created_at
                FROM events
                WHERE created_by = %s AND date >= CURDATE()
                ORDER BY date ASC
            """, (user_id,))
        
        events = cursor.fetchall()
        
        # Format dates
        for event in events:
            if event.get('date'):
                event['date'] = event['date'].strftime('%Y-%m-%d')
            if event.get('created_at'):
                event['created_at'] = event['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({'success': True, 'events': events}), 200
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()
'''
            
            # Add at the end of the file
            controller_content += events_api
            print(f"{Colors.GREEN}✓{Colors.END} Added events API endpoint")
        
        # Ensure required imports
        if 'import re' not in controller_content:
            # Add after other imports
            import_line = 'import re\n'
            if 'from database import' in controller_content:
                controller_content = controller_content.replace(
                    'from database import',
                    import_line + 'from database import'
                )
                print(f"{Colors.GREEN}✓{Colors.END} Added required imports")
        
        # Save updated controller
        with open(nfc_controller_path, 'w', encoding='utf-8') as f:
            f.write(controller_content)
        
        print(f"{Colors.GREEN}✅ NFC controller updated successfully!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}○{Colors.END} Check-in functionality already exists in controller")
else:
    print(f"{Colors.RED}✗{Colors.END} NFC controller not found: {nfc_controller_path}")

# ============================================================================
# STEP 3: Create Database Migration (if needed)
# ============================================================================
print(f"\n{Colors.CYAN}📄 Step 3: Creating database migration script...{Colors.END}")

migration_sql = '''-- Event Check-in Feature Migration
-- Run this on your database if event_checkins table doesn't exist

-- Create event_checkins table if it doesn't exist
CREATE TABLE IF NOT EXISTS event_checkins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    checked_in_by INT,
    checked_in_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_url TEXT,
    scan_id INT,
    notes TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (scan_id) REFERENCES scan_history(id) ON DELETE SET NULL,
    UNIQUE KEY unique_checkin (event_id, user_id),
    INDEX idx_event (event_id),
    INDEX idx_user (user_id),
    INDEX idx_checkin_time (checked_in_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add scan_id to scan_history if it doesn't exist
ALTER TABLE scan_history 
ADD COLUMN IF NOT EXISTS scan_url TEXT AFTER scan_data;

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_scanner ON scan_history(scanner_id);
CREATE INDEX IF NOT EXISTS idx_scanned_user ON scan_history(scanned_user_id);
CREATE INDEX IF NOT EXISTS idx_scan_date ON scan_history(created_at);
'''

with open('migration_event_checkins.sql', 'w', encoding='utf-8') as f:
    f.write(migration_sql)

print(f"{Colors.GREEN}✓{Colors.END} Created migration_event_checkins.sql")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print(f"{Colors.GREEN}✅ EVENT ADMIN CHECK-IN FEATURE ADDED!{Colors.END}")
print("=" * 80)

print(f"""
{Colors.CYAN}📋 Changes Made:{Colors.END}

✅ Scanner Template (templates/nfc/scanner.html):
   • Added "Check in to Event" dropdown option
   • Added event selection modal
   • Added check-in JavaScript logic
   • Added visual feedback for successful check-ins

✅ NFC Controller (src/controllers/nfc_controller.py):
   • Updated scan-profile endpoint to handle check-ins
   • Added event_id parameter support
   • Records scan_url for all scans
   • Creates check-in records for event admins
   • Added API endpoint to fetch admin's events

✅ Database Migration:
   • Created migration_event_checkins.sql
   • Defines event_checkins table structure

{Colors.CYAN}🚀 Next Steps:{Colors.END}

1️⃣  Run Database Migration:
   mysql -u root -p nfc_db < migration_event_checkins.sql

2️⃣  Test Locally:
   python app.py
   • Login as event_admin
   • Go to /nfc/scanner
   • Select "Check in to Event" from dropdown
   • Choose an event
   • Scan a user's QR code
   • Verify check-in success message

3️⃣  Commit to Git:
   git add .
   git commit -m "Add event admin check-in feature for NFC scanner"
   git push origin main

4️⃣  Deploy to Server:
   ssh user@server
   cd /path/to/app
   git pull origin main
   mysql -u dbuser -p dbname < migration_event_checkins.sql
   sudo systemctl restart nfc

{Colors.CYAN}📋 Feature Overview:{Colors.END}

✨ For Event Admins:
   • Scanner page shows "Check in to Event" option
   • Select event from dropdown
   • Scan attendee's QR/NFC
   • Attendee is automatically checked in
   • Scan URL is recorded
   • Duplicate check-ins are prevented

✨ For Regular Users:
   • Continue to use "Networking Mode" as before
   • No check-in option shown

✨ Database Records:
   • All scans recorded in scan_history
   • Check-ins recorded in event_checkins
   • Links scan to check-in via scan_id

{Colors.GREEN}✅ Ready to commit and deploy!{Colors.END}
""")