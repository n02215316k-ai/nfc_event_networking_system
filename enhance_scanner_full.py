import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}ADDING NFC BUTTON + MANUAL INPUT TO SCANNER{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

ENHANCED_SCANNER = """{% extends 'base.html' %}

{% block title %}NFC/QR Scanner - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-qrcode me-2"></i>
                        NFC/QR Scanner
                    </h4>
                </div>
                <div class="card-body">
                    
                    <!-- Scanner Mode Selection -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Scanner Mode:</label>
                            <select id="scannerMode" class="form-select">
                                <option value="networking">Networking (Connect with People)</option>
                                {% if session.role in ['event_admin', 'system_manager'] %}
                                <option value="checkin">Event Check-in/out</option>
                                {% endif %}
                            </select>
                        </div>
                        
                        <!-- Event Selection (for check-in mode) -->
                        <div class="col-md-6" id="eventSelectionDiv" style="display: none;">
                            <label class="form-label fw-bold">Select Event:</label>
                            <select id="eventSelect" class="form-select">
                                <option value="">-- Select Event --</option>
                            </select>
                        </div>
                    </div>

                    <!-- Scan Method Tabs -->
                    <ul class="nav nav-tabs mb-3" id="scanMethodTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="camera-tab" data-bs-toggle="tab" data-bs-target="#camera" type="button">
                                <i class="fas fa-camera"></i> Camera QR Scan
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="nfc-tab" data-bs-toggle="tab" data-bs-target="#nfc" type="button">
                                <i class="fas fa-wifi"></i> NFC Scan
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="manual-tab" data-bs-toggle="tab" data-bs-target="#manual" type="button">
                                <i class="fas fa-keyboard"></i> Manual Entry
                            </button>
                        </li>
                    </ul>

                    <!-- Tab Content -->
                    <div class="tab-content" id="scanMethodContent">
                        
                        <!-- Camera QR Scanner -->
                        <div class="tab-pane fade show active" id="camera" role="tabpanel">
                            <div class="text-center mb-3">
                                <div id="reader" style="width: 100%; max-width: 500px; margin: 0 auto;"></div>
                                <button id="startCameraBtn" class="btn btn-primary mt-3">
                                    <i class="fas fa-camera"></i> Start Camera Scanner
                                </button>
                                <button id="stopCameraBtn" class="btn btn-danger mt-3" style="display: none;">
                                    <i class="fas fa-stop"></i> Stop Camera
                                </button>
                            </div>
                        </div>

                        <!-- NFC Scanner -->
                        <div class="tab-pane fade" id="nfc" role="tabpanel">
                            <div class="text-center p-5">
                                <div id="nfcStatus" class="mb-4">
                                    <i class="fas fa-wifi fa-3x text-primary mb-3"></i>
                                    <h5>NFC Ready</h5>
                                    <p class="text-muted">Click the button below and tap an NFC badge</p>
                                </div>
                                <button id="startNfcBtn" class="btn btn-primary btn-lg">
                                    <i class="fas fa-wifi me-2"></i> Start NFC Scan
                                </button>
                                <button id="stopNfcBtn" class="btn btn-danger btn-lg" style="display: none;">
                                    <i class="fas fa-stop me-2"></i> Stop NFC Scan
                                </button>
                                
                                <div class="alert alert-info mt-4" id="nfcInstructions">
                                    <strong>How to use NFC:</strong>
                                    <ol class="text-start mt-2 mb-0">
                                        <li>Click "Start NFC Scan" button</li>
                                        <li>Tap your phone to another phone/badge</li>
                                        <li>Wait for confirmation</li>
                                    </ol>
                                    <small class="text-muted d-block mt-2">
                                        Note: NFC requires compatible hardware and may not work on all devices
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Manual Entry -->
                        <div class="tab-pane fade" id="manual" role="tabpanel">
                            <div class="p-4">
                                <div class="mb-3">
                                    <label for="manualBadgeId" class="form-label fw-bold">
                                        Enter Badge ID or Email:
                                    </label>
                                    <input type="text" 
                                           class="form-control form-control-lg" 
                                           id="manualBadgeId" 
                                           placeholder="e.g., NFC-ABC123XYZ or user@email.com"
                                           autocomplete="off">
                                    <small class="text-muted">
                                        Badge ID format: NFC-XXXXXXXXXXXX
                                    </small>
                                </div>
                                <button id="submitManualBtn" class="btn btn-primary btn-lg w-100">
                                    <i class="fas fa-check me-2"></i> Submit
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Scan Result Display -->
                    <div id="scanResult" class="mt-4" style="display: none;">
                        <div class="alert" id="resultAlert">
                            <div id="resultContent"></div>
                        </div>
                    </div>

                    <!-- Recent Scans -->
                    <div class="mt-4">
                        <h5>Recent Scans</h5>
                        <div id="recentScans" class="list-group">
                            <div class="list-group-item text-muted text-center">
                                No scans yet
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>

<!-- HTML5 QR Code Scanner Library -->
<script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>

<script>
let html5QrCode = null;
let scannerMode = 'networking';
let selectedEventId = null;
let recentScans = [];

// Scanner Mode Change
document.getElementById('scannerMode').addEventListener('change', function() {
    scannerMode = this.value;
    const eventDiv = document.getElementById('eventSelectionDiv');
    
    if (scannerMode === 'checkin') {
        eventDiv.style.display = 'block';
        loadEvents();
    } else {
        eventDiv.style.display = 'none';
    }
});

// Event Selection
document.getElementById('eventSelect').addEventListener('change', function() {
    selectedEventId = this.value;
});

// Load Events for Check-in Mode
async function loadEvents() {
    try {
        const response = await fetch('/api/events/upcoming');
        const data = await response.json();
        
        const eventSelect = document.getElementById('eventSelect');
        eventSelect.innerHTML = '<option value="">-- Select Event --</option>';
        
        if (data.events && data.events.length > 0) {
            data.events.forEach(event => {
                eventSelect.innerHTML += `<option value="${event.id}">${event.title} - ${event.event_date}</option>`;
            });
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Camera QR Scanner
document.getElementById('startCameraBtn').addEventListener('click', function() {
    startCameraScanner();
});

document.getElementById('stopCameraBtn').addEventListener('click', function() {
    stopCameraScanner();
});

function startCameraScanner() {
    html5QrCode = new Html5Qrcode("reader");
    
    html5QrCode.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        onScanSuccess,
        onScanError
    ).then(() => {
        document.getElementById('startCameraBtn').style.display = 'none';
        document.getElementById('stopCameraBtn').style.display = 'inline-block';
    }).catch(err => {
        showResult('error', `Camera error: ${err}`);
    });
}

function stopCameraScanner() {
    if (html5QrCode) {
        html5QrCode.stop().then(() => {
            document.getElementById('startCameraBtn').style.display = 'inline-block';
            document.getElementById('stopCameraBtn').style.display = 'none';
        });
    }
}

function onScanSuccess(decodedText, decodedResult) {
    processScan(decodedText, 'qr');
    stopCameraScanner();
}

function onScanError(error) {
    // Ignore continuous scanning errors
}

// NFC Scanner
document.getElementById('startNfcBtn').addEventListener('click', async function() {
    if ('NDEFReader' in window) {
        try {
            const ndef = new NDEFReader();
            await ndef.scan();
            
            document.getElementById('startNfcBtn').style.display = 'none';
            document.getElementById('stopNfcBtn').style.display = 'inline-block';
            document.getElementById('nfcStatus').innerHTML = `
                <i class="fas fa-wifi fa-3x text-success fa-pulse mb-3"></i>
                <h5 class="text-success">NFC Scanning Active</h5>
                <p class="text-muted">Tap an NFC badge now...</p>
            `;
            
            ndef.addEventListener("reading", ({ message, serialNumber }) => {
                let nfcData = '';
                for (const record of message.records) {
                    const decoder = new TextDecoder(record.encoding);
                    nfcData = decoder.decode(record.data);
                }
                processScan(nfcData, 'nfc');
            });
            
        } catch (error) {
            showResult('error', `NFC Error: ${error.message}`);
        }
    } else {
        showResult('warning', 'NFC is not supported on this device. Please use QR code or manual entry.');
    }
});

document.getElementById('stopNfcBtn').addEventListener('click', function() {
    document.getElementById('startNfcBtn').style.display = 'inline-block';
    document.getElementById('stopNfcBtn').style.display = 'none';
    document.getElementById('nfcStatus').innerHTML = `
        <i class="fas fa-wifi fa-3x text-primary mb-3"></i>
        <h5>NFC Ready</h5>
        <p class="text-muted">Click the button below and tap an NFC badge</p>
    `;
});

// Manual Entry
document.getElementById('submitManualBtn').addEventListener('click', function() {
    const badgeId = document.getElementById('manualBadgeId').value.trim();
    if (badgeId) {
        processScan(badgeId, 'manual');
    } else {
        showResult('error', 'Please enter a badge ID or email');
    }
});

// Allow Enter key for manual entry
document.getElementById('manualBadgeId').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('submitManualBtn').click();
    }
});

// Process Scan
async function processScan(scanData, scanMethod) {
    try {
        // Validate for check-in mode
        if (scannerMode === 'checkin' && !selectedEventId) {
            showResult('error', 'Please select an event first');
            return;
        }
        
        const response = await fetch('/nfc/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                scan_data: scanData,
                scan_method: scanMethod,
                scanner_mode: scannerMode,
                event_id: selectedEventId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult('success', data.message);
            addRecentScan(data, scanMethod);
            
            // Clear manual input
            document.getElementById('manualBadgeId').value = '';
        } else {
            showResult('error', data.message || 'Scan failed');
        }
        
    } catch (error) {
        showResult('error', `Error: ${error.message}`);
    }
}

// Show Result
function showResult(type, message) {
    const resultDiv = document.getElementById('scanResult');
    const resultAlert = document.getElementById('resultAlert');
    const resultContent = document.getElementById('resultContent');
    
    resultAlert.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'warning'}`;
    resultContent.innerHTML = message;
    resultDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}

// Add to Recent Scans
function addRecentScan(data, method) {
    const scanItem = {
        time: new Date().toLocaleTimeString(),
        method: method.toUpperCase(),
        message: data.message,
        type: data.action || 'scan'
    };
    
    recentScans.unshift(scanItem);
    if (recentScans.length > 5) recentScans.pop();
    
    updateRecentScans();
}

function updateRecentScans() {
    const container = document.getElementById('recentScans');
    
    if (recentScans.length === 0) {
        container.innerHTML = '<div class="list-group-item text-muted text-center">No scans yet</div>';
        return;
    }
    
    container.innerHTML = recentScans.map(scan => `
        <div class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-primary me-2">${scan.method}</span>
                    <span>${scan.message}</span>
                </div>
                <small class="text-muted">${scan.time}</small>
            </div>
        </div>
    `).join('');
}
</script>
{% endblock %}
"""

scanner_path = 'templates/nfc/scanner.html'
os.makedirs(os.path.dirname(scanner_path), exist_ok=True)

with open(scanner_path, 'w', encoding='utf-8') as f:
    f.write(ENHANCED_SCANNER.strip())

print(f"{Colors.GREEN}✓{Colors.END} Enhanced scanner.html with:")
print(f"  {Colors.GREEN}✓{Colors.END} Camera QR scanning")
print(f"  {Colors.GREEN}✓{Colors.END} NFC button (for compatible devices)")
print(f"  {Colors.GREEN}✓{Colors.END} Manual entry field")
print(f"  {Colors.GREEN}✓{Colors.END} Recent scans display")
print(f"  {Colors.GREEN}✓{Colors.END} Networking & Check-in modes")

print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Scanner fully enhanced!{Colors.END}")
print(f"\n{Colors.CYAN}How to use:{Colors.END}")
print(f"  1. Restart: {Colors.BOLD}python app.py{Colors.END}")
print(f"  2. Visit: {Colors.BOLD}http://localhost:5000/nfc/scanner{Colors.END}")
print(f"  3. Choose scan method:")
print(f"     • Camera tab - QR code scanning")
print(f"     • NFC tab - Tap badges (if device supports)")
print(f"     • Manual tab - Type badge ID")
print()