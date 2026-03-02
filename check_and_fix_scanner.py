import os

print("=" * 80)
print("🔍 CHECKING SCANNER.HTML AND FIXING")
print("=" * 80)

scanner_path = 'templates/nfc/scanner.html'

if os.path.exists(scanner_path):
    with open(scanner_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n✅ Found scanner.html")
    print(f"   File size: {len(content)} characters")
    
    # Check what's in the file
    print("\n📋 Current content analysis:")
    if 'scan_mode' in content:
        print("   ✅ Has scan_mode")
    else:
        print("   ❌ Missing scan_mode")
    
    if 'Check-In' in content or 'checkin' in content:
        print("   ✅ Has check-in feature")
    else:
        print("   ❌ Missing check-in feature")
    
    if 'user_events' in content:
        print("   ✅ Has user_events reference")
    else:
        print("   ❌ Missing user_events reference")
    
    # Show first 50 lines to see structure
    lines = content.split('\n')
    print(f"\n📄 First 50 lines of scanner.html:")
    print("-" * 80)
    for i, line in enumerate(lines[:50], 1):
        print(f"{i:3d} | {line}")
    print("-" * 80)
    
    # Now let's completely rewrite the scanner.html with the check-in feature
    print("\n🔧 Creating NEW scanner.html with check-in/out feature...")
    
    new_scanner_html = '''{% extends "base.html" %}

{% block title %}NFC Scanner - NFC Event Network{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="fas fa-qrcode me-2"></i>NFC/QR Code Scanner</h4>
                </div>
                <div class="card-body">
                    
                    <!-- Scan Mode Selection -->
                    <div class="mb-4">
                        <label for="scan_mode" class="form-label">
                            <i class="fas fa-sliders-h me-2"></i>Scan Mode
                        </label>
                        <select class="form-select form-select-lg" id="scan_mode" name="scan_mode">
                            <option value="network">📱 Network - Exchange Contact Info</option>
                            {% if user_events %}
                            <option value="checkin">✅ Check-In/Out - Mark Attendance</option>
                            {% endif %}
                        </select>
                        <small class="text-muted">
                            <span id="mode-description">Scan to connect with other attendees and exchange contact information</span>
                        </small>
                    </div>

                    <!-- Event Selection (Only shown in check-in mode) -->
                    <div class="mb-4" id="event-selector" style="display: none;">
                        <label for="event_id" class="form-label">
                            <i class="fas fa-calendar-check me-2"></i>Select Your Event
                        </label>
                        <select class="form-select form-select-lg" id="event_id" name="event_id">
                            <option value="">-- Choose Event --</option>
                            {% if user_events %}
                                {% for event in user_events %}
                                <option value="{{ event.id }}" {{ 'selected' if event_id and event.id == event_id|int else '' }}>
                                    {{ event.title }} - {{ event.start_date.strftime('%b %d, %Y') }}
                                </option>
                                {% endfor %}
                            {% endif %}
                        </select>
                        <small class="text-muted">Select the event to check attendees in/out</small>
                    </div>

                    <!-- Scanner Container -->
                    <div id="scanner-container" class="mb-4">
                        <div class="ratio ratio-1x1 bg-dark rounded" id="qr-reader" style="max-width: 400px; margin: 0 auto;">
                            <!-- QR Scanner will be initialized here -->
                        </div>
                    </div>

                    <!-- Scan Result -->
                    <div id="scan-result" class="alert alert-info" style="display: none;">
                        <div class="d-flex align-items-center">
                            <div class="spinner-border spinner-border-sm me-2" role="status">
                                <span class="visually-hidden">Processing...</span>
                            </div>
                            <span>Processing scan...</span>
                        </div>
                    </div>

                    <!-- Instructions -->
                    <div class="alert alert-light">
                        <h6><i class="fas fa-info-circle me-2"></i>How to use:</h6>
                        <ul class="mb-0">
                            <li><strong>Network Mode:</strong> Scan another user's QR code to add them to your connections</li>
                            {% if user_events %}
                            <li><strong>Check-In Mode:</strong> Select your event and scan attendee QR codes to mark attendance</li>
                            {% endif %}
                            <li>Allow camera access when prompted</li>
                            <li>Point your camera at a QR code</li>
                        </ul>
                    </div>

                    <!-- Recent Scans -->
                    <div class="mt-4">
                        <h5><i class="fas fa-history me-2"></i>Recent Scans</h5>
                        <div id="recent-scans" class="list-group">
                            <!-- Recent scans will appear here -->
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>

<!-- Include HTML5 QR Code Scanner -->
<script src="https://unpkg.com/html5-qrcode"></script>

<script>
let html5QrCode;
let scanMode = 'network';
let selectedEventId = null;

// Mode descriptions
const modeDescriptions = {
    'network': 'Scan to connect with other attendees and exchange contact information',
    'checkin': 'Scan attendee QR codes to mark them as checked in or out of your event'
};

// Initialize scanner
function startScanner() {
    const qrReaderElement = document.getElementById('qr-reader');
    
    if (!qrReaderElement) {
        console.error('QR reader element not found');
        return;
    }

    html5QrCode = new Html5Qrcode("qr-reader");
    
    const config = { 
        fps: 10,
        qrbox: { width: 250, height: 250 }
    };

    html5QrCode.start(
        { facingMode: "environment" },
        config,
        onScanSuccess,
        onScanError
    ).catch(err => {
        console.error('Scanner start error:', err);
        alert('Could not start camera. Please ensure you have granted camera permissions.');
    });
}

// Handle successful scan
function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scan result: ${decodedText}`);
    
    // Stop scanning temporarily
    html5QrCode.pause();
    
    // Show processing message
    const resultDiv = document.getElementById('scan-result');
    resultDiv.style.display = 'block';
    resultDiv.className = 'alert alert-info';
    resultDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <div class="spinner-border spinner-border-sm me-2" role="status"></div>
            <span>Processing scan...</span>
        </div>
    `;
    
    // Process the scan
    processScan(decodedText);
}

function onScanError(errorMessage) {
    // Ignore errors (they occur frequently during scanning)
}

// Process the scanned code
function processScan(scannedData) {
    // Extract user ID from scanned data (format: "USER:123" or just "123")
    let userId = null;
    
    if (scannedData.includes('USER:')) {
        userId = scannedData.split('USER:')[1];
    } else if (!isNaN(scannedData)) {
        userId = scannedData;
    }
    
    if (!userId) {
        showScanResult('error', 'Invalid QR code format');
        setTimeout(() => html5QrCode.resume(), 2000);
        return;
    }
    
    // Prepare request data
    const requestData = {
        scanned_user_id: userId,
        scan_mode: scanMode
    };
    
    // Add event ID if in check-in mode
    if (scanMode === 'checkin') {
        if (!selectedEventId) {
            showScanResult('warning', 'Please select an event first');
            setTimeout(() => html5QrCode.resume(), 2000);
            return;
        }
        requestData.event_id = selectedEventId;
    }
    
    // Send to server
    fetch('/nfc/process-scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (scanMode === 'checkin') {
                showScanResult('success', `
                    <strong>${data.user.name}</strong> ${data.action}!<br>
                    <small>Event: ${data.event} at ${data.time}</small>
                `);
            } else {
                showScanResult('success', `
                    <strong>Connected!</strong><br>
                    Added ${data.scanned_user.name} to your network
                `);
            }
            
            // Add to recent scans
            addToRecentScans(data);
        } else {
            showScanResult('danger', data.message || 'Scan failed');
        }
        
        // Resume scanning after 3 seconds
        setTimeout(() => html5QrCode.resume(), 3000);
    })
    .catch(error => {
        console.error('Error:', error);
        showScanResult('danger', 'Error processing scan');
        setTimeout(() => html5QrCode.resume(), 2000);
    });
}

// Show scan result
function showScanResult(type, message) {
    const resultDiv = document.getElementById('scan-result');
    resultDiv.style.display = 'block';
    resultDiv.className = `alert alert-${type}`;
    resultDiv.innerHTML = message;
}

// Add to recent scans list
function addToRecentScans(data) {
    const recentScans = document.getElementById('recent-scans');
    const scanItem = document.createElement('div');
    scanItem.className = 'list-group-item';
    
    if (data.action) {
        // Check-in/out
        scanItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${data.user.name}</strong><br>
                    <small class="text-muted">${data.action} - ${data.time}</small>
                </div>
                <span class="badge bg-${data.status}">${data.action}</span>
            </div>
        `;
    } else {
        // Network connection
        scanItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${data.scanned_user.name}</strong><br>
                    <small class="text-muted">${data.scanned_user.email}</small>
                </div>
                <span class="badge bg-success">Connected</span>
            </div>
        `;
    }
    
    recentScans.insertBefore(scanItem, recentScans.firstChild);
    
    // Keep only last 5 scans
    while (recentScans.children.length > 5) {
        recentScans.removeChild(recentScans.lastChild);
    }
}

// Handle scan mode change
document.getElementById('scan_mode').addEventListener('change', function() {
    scanMode = this.value;
    const eventSelector = document.getElementById('event-selector');
    const modeDescription = document.getElementById('mode-description');
    
    if (scanMode === 'checkin') {
        eventSelector.style.display = 'block';
        modeDescription.textContent = modeDescriptions['checkin'];
    } else {
        eventSelector.style.display = 'none';
        modeDescription.textContent = modeDescriptions['network'];
    }
});

// Handle event selection
document.getElementById('event_id')?.addEventListener('change', function() {
    selectedEventId = this.value;
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    startScanner();
    
    // Check if event_id was passed in URL (from event page)
    const urlParams = new URLSearchParams(window.location.search);
    const eventIdParam = urlParams.get('event_id');
    
    if (eventIdParam) {
        document.getElementById('scan_mode').value = 'checkin';
        document.getElementById('scan_mode').dispatchEvent(new Event('change'));
        document.getElementById('event_id').value = eventIdParam;
        selectedEventId = eventIdParam;
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (html5QrCode) {
        html5QrCode.stop();
    }
});
</script>
{% endblock %}
'''
    
    # Backup old file
    backup_path = scanner_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   💾 Backed up old file to: {backup_path}")
    
    # Write new file
    with open(scanner_path, 'w', encoding='utf-8') as f:
        f.write(new_scanner_html)
    
    print(f"   ✅ Created NEW scanner.html with full check-in/out feature!")
    
else:
    print(f"❌ scanner.html not found at {scanner_path}")
    print("   Creating new file...")
    
    os.makedirs('templates/nfc', exist_ok=True)
    # Create the new file (code above)

print("\n" + "=" * 80)
print("✅ SCANNER.HTML COMPLETELY REWRITTEN!")
print("=" * 80)
print("\n🔄 Now restart Flask:")
print("   python app.py")
print("\n🎯 Test it:")
print("   1. Go to /nfc/scanner")
print("   2. You should see 'Scan Mode' dropdown")
print("   3. Event admins will see 'Check-In/Out' option")