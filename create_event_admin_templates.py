import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

def create_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}{filepath}{Colors.END}")

# Event Admin Dashboard Template
DASHBOARD_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Event Admin Dashboard{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-calendar-check me-2"></i>Event Admin Dashboard</h2>
    
    <!-- Statistics Cards -->
    <div class="row mt-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5>Total Events</h5>
                    <h2>{{ stats.total_events }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5>Upcoming Events</h5>
                    <h2>{{ stats.upcoming_events }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5>Total Registrations</h5>
                    <h2>{{ stats.total_registrations }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <h5>Total Attended</h5>
                    <h2>{{ stats.total_attended }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- My Events -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">My Events</h5>
                    <a href="{{ url_for('events.create_event') }}" class="btn btn-primary">
                        <i class="fas fa-plus me-1"></i>Create New Event
                    </a>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Event Title</th>
                                    <th>Date</th>
                                    <th>Registrations</th>
                                    <th>Attended</th>
                                    <th>Currently Present</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for event in my_events %}
                                <tr>
                                    <td>{{ event.title }}</td>
                                    <td>{{ event.start_date|datetime_format('%b %d, %Y') }}</td>
                                    <td><span class="badge bg-primary">{{ event.total_registrations }}</span></td>
                                    <td><span class="badge bg-success">{{ event.total_attended }}</span></td>
                                    <td><span class="badge bg-info">{{ event.currently_present }}</span></td>
                                    <td>
                                        <a href="{{ url_for('event_admin.event_details', event_id=event.id) }}" 
                                           class="btn btn-sm btn-primary">Manage</a>
                                        <a href="{{ url_for('event_admin.live_attendance', event_id=event.id) }}" 
                                           class="btn btn-sm btn-success">Live</a>
                                        <a href="{{ url_for('event_admin.event_reports', event_id=event.id) }}" 
                                           class="btn btn-sm btn-info">Reports</a>
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

    <!-- Recent Activity -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Recent Activity</h5>
                </div>
                <div class="card-body">
                    {% if recent_activity %}
                    <div class="list-group">
                        {% for activity in recent_activity %}
                        <div class="list-group-item">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <strong>{{ activity.user_name }}</strong>
                                    <span class="badge bg-{{ 'success' if activity.scan_type == 'check_in' else 'warning' if activity.scan_type == 'check_out' else 'info' }}">
                                        {{ activity.scan_type|replace('_', ' ')|title }}
                                    </span>
                                    - {{ activity.event_title }}
                                </div>
                                <small class="text-muted">{{ activity.created_at|timeago }}</small>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted">No recent activity</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# Live Attendance Template
LIVE_ATTENDANCE_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Live Attendance - {{ event.title }}{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-broadcast-tower me-2"></i>Live Attendance: {{ event.title }}</h2>
        <a href="{{ url_for('event_admin.event_details', event_id=event.id) }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-1"></i>Back to Event
        </a>
    </div>

    <!-- Real-time Stats -->
    <div class="row">
        <div class="col-md-4">
            <div class="card text-white bg-primary">
                <div class="card-body text-center">
                    <h5>Total Registered</h5>
                    <h1 id="total-registered">0</h1>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-success">
                <div class="card-body text-center">
                    <h5>Checked In</h5>
                    <h1 id="total-checked-in">0</h1>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-info">
                <div class="card-body text-center">
                    <h5>Currently Present</h5>
                    <h1 id="currently-present">0</h1>
                </div>
            </div>
        </div>
    </div>

    <!-- Attendance List -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Attendance Log</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover" id="attendance-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Check-in Time</th>
                                    <th>Method</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="attendance-tbody">
                                <!-- Dynamic content -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
let eventId = {{ event.id }};

function updateAttendance() {
    fetch(`/event-admin/event/${eventId}/attendance/data`)
        .then(response => response.json())
        .then(data => {
            // Update stats
            document.getElementById('total-registered').textContent = data.stats.total_registered || 0;
            document.getElementById('total-checked-in').textContent = data.stats.total_checked_in || 0;
            document.getElementById('currently-present').textContent = data.stats.currently_present || 0;
            
            // Update table
            let tbody = document.getElementById('attendance-tbody');
            tbody.innerHTML = '';
            
            data.attendance.forEach(record => {
                let row = `
                    <tr>
                        <td>${record.full_name}</td>
                        <td>${record.email}</td>
                        <td>${record.check_in_time || '-'}</td>
                        <td><span class="badge bg-primary">${record.check_in_method || '-'}</span></td>
                        <td>
                            ${record.check_out_time 
                                ? '<span class="badge bg-secondary">Checked Out</span>' 
                                : '<span class="badge bg-success">Present</span>'}
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Error:', error));
}

// Update every 5 seconds
updateAttendance();
setInterval(updateAttendance, 5000);
</script>
{% endblock %}
"""

# NFC Scanner Template
SCANNER_TEMPLATE = """
{% extends "base.html" %}
{% block title %}NFC/QR Scanner{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2><i class="fas fa-qrcode me-2"></i>NFC/QR Scanner</h2>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Scan Settings</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label">Select Event</label>
                        <select class="form-select" id="event-select">
                            <option value="">-- Select Event --</option>
                            {% for event in events %}
                            <option value="{{ event.id }}">{{ event.title }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Scan Type</label>
                        <select class="form-select" id="scan-type">
                            <option value="check_in">Check-In</option>
                            <option value="check_out">Check-Out</option>
                            <option value="networking">Networking</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Scan Method</label>
                        <div class="btn-group w-100" role="group">
                            <button type="button" class="btn btn-outline-primary active" id="qr-mode">QR Code</button>
                            <button type="button" class="btn btn-outline-primary" id="nfc-mode">NFC</button>
                        </div>
                    </div>
                    
                    <button class="btn btn-success w-100" id="start-scan">
                        <i class="fas fa-play me-2"></i>Start Scanning
                    </button>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Scanner</h5>
                </div>
                <div class="card-body text-center">
                    <div id="qr-reader" style="width: 100%; display: none;"></div>
                    <div id="nfc-reader" style="display: none;">
                        <i class="fas fa-wifi fa-5x text-primary mb-3"></i>
                        <p>Hold NFC device near reader...</p>
                    </div>
                    <div id="scan-result" class="mt-3"></div>
                </div>
            </div>
            
            <!-- Recent Scans -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5 class="mb-0">Recent Scans</h5>
                </div>
                <div class="card-body">
                    <div id="recent-scans" class="list-group">
                        <!-- Dynamic content -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/html5-qrcode"></script>
<script>
let html5QrCode;
let currentMode = 'qr';

document.getElementById('start-scan').addEventListener('click', function() {
    let eventId = document.getElementById('event-select').value;
    let scanType = document.getElementById('scan-type').value;
    
    if (!eventId) {
        alert('Please select an event first');
        return;
    }
    
    if (currentMode === 'qr') {
        startQRScanner(eventId, scanType);
    } else {
        startNFCScanner(eventId, scanType);
    }
});

function startQRScanner(eventId, scanType) {
    document.getElementById('qr-reader').style.display = 'block';
    document.getElementById('nfc-reader').style.display = 'none';
    
    html5QrCode = new Html5Qrcode("qr-reader");
    
    html5QrCode.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        (decodedText) => {
            processScan(decodedText, eventId, scanType, 'qr');
            html5QrCode.stop();
        }
    );
}

function startNFCScanner(eventId, scanType) {
    document.getElementById('qr-reader').style.display = 'none';
    document.getElementById('nfc-reader').style.display = 'block';
    
    if ('NDEFReader' in window) {
        const reader = new NDEFReader();
        reader.scan().then(() => {
            reader.onreading = event => {
                const message = event.message.records[0].data;
                processScan(message, eventId, scanType, 'nfc');
            };
        });
    } else {
        alert('NFC not supported on this device');
    }
}

function processScan(scanData, eventId, scanType, method) {
    let endpoint = method === 'qr' ? '/nfc/qr-scan' : '/nfc/scan';
    
    fetch(endpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            [method === 'qr' ? 'qr_data' : 'scan_data']: scanData,
            event_id: eventId,
            scan_type: scanType
        })
    })
    .then(response => response.json())
    .then(data => {
        displayScanResult(data);
        addToRecentScans(data);
    });
}

function displayScanResult(data) {
    let resultDiv = document.getElementById('scan-result');
    let className = data.success ? 'alert-success' : 'alert-danger';
    
    resultDiv.innerHTML = `
        <div class="alert ${className}">
            <strong>${data.success ? '✓' : '✗'}</strong> ${data.message}
            ${data.user ? `<br><small>${data.user.name} (${data.user.email})</small>` : ''}
        </div>
    `;
}

function addToRecentScans(data) {
    let scansDiv = document.getElementById('recent-scans');
    let scanItem = `
        <div class="list-group-item">
            <div class="d-flex justify-content-between">
                <div>
                    ${data.user ? data.user.name : 'Unknown'}
                    <span class="badge bg-${data.success ? 'success' : 'danger'}">${data.action}</span>
                </div>
                <small>${new Date().toLocaleTimeString()}</small>
            </div>
        </div>
    `;
    scansDiv.insertAdjacentHTML('afterbegin', scanItem);
}

// Mode switching
document.getElementById('qr-mode').addEventListener('click', function() {
    currentMode = 'qr';
    this.classList.add('active');
    document.getElementById('nfc-mode').classList.remove('active');
});

document.getElementById('nfc-mode').addEventListener('click', function() {
    currentMode = 'nfc';
    this.classList.add('active');
    document.getElementById('qr-mode').classList.remove('active');
});
</script>
{% endblock %}
"""

print(f"\n{Colors.CYAN}Creating Event Admin Templates...{Colors.END}\n")

create_file('templates/event_admin/dashboard.html', DASHBOARD_TEMPLATE)
create_file('templates/event_admin/live_attendance.html', LIVE_ATTENDANCE_TEMPLATE)
create_file('templates/nfc/scanner.html', SCANNER_TEMPLATE)

print(f"\n{Colors.GREEN}✅ Event Admin Templates created!{Colors.END}\n")