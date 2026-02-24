import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

ENHANCED_SCANNER_UI = """
{% extends "base.html" %}
{% block title %}NFC/QR Scanner{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-10 mx-auto">
            <!-- Scanner Mode Selector -->
            <div class="card mb-4 shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-qrcode me-2"></i>NFC/QR Scanner
                        <span class="badge bg-light text-dark ms-2">{{ user_role|title }}</span>
                    </h4>
                </div>
                <div class="card-body">
                    <!-- Mode Selection -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="card border-primary h-100 scan-mode-card" data-mode="networking">
                                <div class="card-body text-center">
                                    <i class="fas fa-users fa-3x text-primary mb-3"></i>
                                    <h5>Networking Mode</h5>
                                    <p class="text-muted">Scan attendee badges to connect</p>
                                    <button class="btn btn-primary" onclick="selectMode('networking')">
                                        <i class="fas fa-handshake me-1"></i>Start Networking
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        {% if user_role in ['event_admin', 'system_manager'] %}
                        <div class="col-md-6">
                            <div class="card border-success h-100 scan-mode-card" data-mode="checkin">
                                <div class="card-body text-center">
                                    <i class="fas fa-clipboard-check fa-3x text-success mb-3"></i>
                                    <h5>Check-in Mode</h5>
                                    <p class="text-muted">Check attendees in/out of events</p>
                                    <button class="btn btn-success" onclick="selectMode('checkin')">
                                        <i class="fas fa-check me-1"></i>Start Check-in
                                    </button>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                    </div>

                    <!-- Scanner Interface -->
                    <div id="scanner-interface" class="d-none">
                        <div class="alert alert-info">
                            <strong id="mode-title">Networking Mode</strong>
                            <p class="mb-0" id="mode-description">Scan another attendee's badge to connect with them</p>
                        </div>

                        <!-- Event Selection (for check-in mode) -->
                        <div id="event-selector" class="d-none mb-3">
                            <label class="form-label"><strong>Select Event:</strong></label>
                            <select class="form-select" id="selected-event">
                                <option value="">Loading events...</option>
                            </select>
                        </div>

                        <!-- Camera Scanner -->
                        <div class="text-center mb-3">
                            <button class="btn btn-lg btn-success" id="start-scan-btn">
                                <i class="fas fa-camera me-2"></i>Start Camera
                            </button>
                            <button class="btn btn-lg btn-danger d-none" id="stop-scan-btn">
                                <i class="fas fa-stop me-2"></i>Stop Camera
                            </button>
                        </div>

                        <div id="camera-container" class="d-none mb-3">
                            <video id="scanner-video" class="w-100 rounded" style="max-height: 400px;"></video>
                            <canvas id="scanner-canvas" class="d-none"></canvas>
                        </div>

                        <!-- Scan Result -->
                        <div id="scan-result-container" class="d-none"></div>
                    </div>
                </div>
            </div>

            <!-- Real-time Stats (for admins in check-in mode) -->
            <div id="checkin-stats" class="card mb-4 d-none">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-chart-line me-2"></i>Real-time Check-in Stats</h5>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-md-3">
                            <h3 class="text-primary" id="stat-registered">0</h3>
                            <p class="text-muted">Total Registered</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-success" id="stat-checked-in">0</h3>
                            <p class="text-muted">Currently Checked In</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-info" id="stat-today">0</h3>
                            <p class="text-muted">Total Today</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-warning" id="stat-rate">0%</h3>
                            <p class="text-muted">Attendance Rate</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-history me-2"></i>Recent Activity</h5>
                </div>
                <div class="card-body">
                    <div id="recent-activity">
                        <p class="text-muted text-center">No activity yet</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
<script>
let currentMode = null;
let scanning = false;
let videoStream = null;
let selectedEventId = null;

function selectMode(mode) {
    currentMode = mode;
    document.getElementById('scanner-interface').classList.remove('d-none');
    
    if (mode === 'networking') {
        document.getElementById('mode-title').textContent = 'Networking Mode';
        document.getElementById('mode-description').textContent = 'Scan another attendee\\'s badge to connect';
        document.getElementById('event-selector').classList.add('d-none');
        document.getElementById('checkin-stats').classList.add('d-none');
    } else if (mode === 'checkin') {
        document.getElementById('mode-title').textContent = 'Check-in Mode';
        document.getElementById('mode-description').textContent = 'Scan attendee badges for event check-in/out';
        document.getElementById('event-selector').classList.remove('d-none');
        document.getElementById('checkin-stats').classList.remove('d-none');
        loadEvents();
    }
    
    // Scroll to scanner
    document.getElementById('scanner-interface').scrollIntoView({ behavior: 'smooth' });
}

function loadEvents() {
    fetch('/api/events?status=upcoming')
        .then(r => r.json())
        .then(data => {
            const select = document.getElementById('selected-event');
            select.innerHTML = '<option value="">Select an event...</option>';
            (data.events || []).forEach(event => {
                select.innerHTML += `<option value="${event.id}">${event.title}</option>`;
            });
            
            select.onchange = function() {
                selectedEventId = this.value;
                if (selectedEventId) {
                    loadEventStats(selectedEventId);
                }
            };
        });
}

function loadEventStats(eventId) {
    fetch(`/nfc/api/event/${eventId}/checkin-log`)
        .then(r => r.json())
        .then(data => {
            if (data.success && data.stats) {
                document.getElementById('stat-registered').textContent = data.stats.total_registered;
                document.getElementById('stat-checked-in').textContent = data.stats.currently_checked_in;
                document.getElementById('stat-today').textContent = data.stats.total_checkins_today;
                document.getElementById('stat-rate').textContent = data.stats.attendance_rate + '%';
            }
        });
}

// Camera scanning
document.getElementById('start-scan-btn').onclick = async function() {
    if (currentMode === 'checkin' && !selectedEventId) {
        alert('Please select an event first');
        return;
    }
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        
        videoStream = stream;
        const video = document.getElementById('scanner-video');
        video.srcObject = stream;
        video.play();
        
        document.getElementById('camera-container').classList.remove('d-none');
        this.classList.add('d-none');
        document.getElementById('stop-scan-btn').classList.remove('d-none');
        
        scanning = true;
        scanQRCode();
    } catch (err) {
        alert('Camera access denied: ' + err.message);
    }
};

document.getElementById('stop-scan-btn').onclick = function() {
    stopScanning();
};

function stopScanning() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        scanning = false;
        document.getElementById('camera-container').classList.add('d-none');
        document.getElementById('start-scan-btn').classList.remove('d-none');
        document.getElementById('stop-scan-btn').classList.add('d-none');
    }
}

function scanQRCode() {
    if (!scanning) return;
    
    const video = document.getElementById('scanner-video');
    const canvas = document.getElementById('scanner-canvas');
    const context = canvas.getContext('2d');
    
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (code) {
            handleScan(code.data);
            return;
        }
    }
    
    requestAnimationFrame(scanQRCode);
}

function handleScan(scanData) {
    scanning = false;
    stopScanning();
    
    // Process scan
    fetch('/nfc/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            scan_data: scanData,
            scan_method: 'qr',
            event_id: selectedEventId
        })
    })
    .then(r => r.json())
    .then(data => {
        displayScanResult(data);
        addToActivity(data);
        
        if (currentMode === 'checkin' && selectedEventId) {
            loadEventStats(selectedEventId);
        }
    })
    .catch(err => {
        alert('Error: ' + err.message);
    });
}

function displayScanResult(data) {
    const container = document.getElementById('scan-result-container');
    container.classList.remove('d-none');
    
    if (data.success) {
        if (data.action === 'new_connection') {
            container.innerHTML = `
                <div class="alert alert-success">
                    <h5><i class="fas fa-check-circle me-2"></i>New Connection!</h5>
                    <p><strong>${data.user.full_name}</strong></p>
                    <p class="mb-0">${data.user.email}</p>
                    ${data.user.job_title ? '<p class="mb-0">' + data.user.job_title + '</p>' : ''}
                </div>
            `;
        } else if (data.action === 'checked_in') {
            container.innerHTML = `
                <div class="alert alert-success">
                    <h5><i class="fas fa-sign-in-alt me-2"></i>Checked In!</h5>
                    <p><strong>${data.attendee.full_name}</strong></p>
                    <p class="mb-0">Event: ${data.event.title}</p>
                </div>
            `;
        } else if (data.action === 'checked_out') {
            container.innerHTML = `
                <div class="alert alert-info">
                    <h5><i class="fas fa-sign-out-alt me-2"></i>Checked Out!</h5>
                    <p><strong>${data.attendee.full_name}</strong></p>
                    <p class="mb-0">Event: ${data.event.title}</p>
                </div>
            `;
        }
    } else {
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-times-circle me-2"></i>${data.message}
            </div>
        `;
    }
    
    setTimeout(() => {
        container.classList.add('d-none');
    }, 5000);
}

function addToActivity(data) {
    const activity = document.getElementById('recent-activity');
    const time = new Date().toLocaleTimeString();
    
    if (activity.querySelector('p.text-muted')) {
        activity.innerHTML = '';
    }
    
    const item = document.createElement('div');
    item.className = 'border-bottom pb-2 mb-2';
    
    let icon = data.success ? 'check-circle text-success' : 'times-circle text-danger';
    item.innerHTML = `
        <div class="d-flex justify-content-between">
            <div>
                <i class="fas fa-${icon} me-2"></i>
                <strong>${data.message}</strong>
            </div>
            <small class="text-muted">${time}</small>
        </div>
    `;
    
    activity.insertBefore(item, activity.firstChild);
    
    // Keep only last 10
    while (activity.children.length > 10) {
        activity.removeChild(activity.lastChild);
    }
}

// Auto-refresh stats every 10 seconds in check-in mode
setInterval(() => {
    if (currentMode === 'checkin' && selectedEventId) {
        loadEventStats(selectedEventId);
    }
}, 10000);
</script>

<style>
.scan-mode-card {
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}
.scan-mode-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
</style>
{% endblock %}
"""

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}PHASE 3: CREATING ENHANCED SCANNER UI{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

filepath = 'templates/nfc/scanner.html'
os.makedirs(os.path.dirname(filepath), exist_ok=True)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(ENHANCED_SCANNER_UI.strip())

print(f"{Colors.GREEN}✓{Colors.END} Created: {filepath}")
print(f"  - Networking mode for all users")
print(f"  - Check-in mode for admins")
print(f"  - Real-time stats display")
print(f"  - Activity log")
print(f"\n{Colors.GREEN}✅ Enhanced scanner UI created!{Colors.END}\n")