import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}FIXING NFC SCANNER BUTTON VISIBILITY{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

FIXED_SCANNER = """{% extends 'base.html' %}

{% block title %}NFC/QR Scanner{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            
            <!-- Page Header -->
            <div class="text-center mb-4 text-white animate-in">
                <h1 class="display-4 fw-bold">
                    <i class="fas fa-qrcode me-3"></i>
                    NFC/QR Scanner
                </h1>
                <p class="lead">Scan badges to connect or check-in to events</p>
            </div>
            
            <div class="card shadow-lg animate-in">
                <div class="card-header bg-gradient text-white" style="background: linear-gradient(135deg, #4F46E5, #06B6D4);">
                    <div class="row align-items-center">
                        <div class="col-md-6">
                            <h4 class="mb-0">
                                <i class="fas fa-broadcast-tower me-2"></i>
                                Scanner Controls
                            </h4>
                        </div>
                        <div class="col-md-6 text-end">
                            <span class="badge bg-light text-dark">
                                <i class="fas fa-circle text-success pulse"></i> Ready
                            </span>
                        </div>
                    </div>
                </div>
                
                <div class="card-body p-4">
                    
                    <!-- Scanner Mode Selection -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <label class="form-label fw-bold">
                                <i class="fas fa-sliders-h me-2"></i>
                                Scanner Mode:
                            </label>
                            <select id="scannerMode" class="form-select form-select-lg">
                                <option value="networking">🤝 Networking (Connect with People)</option>
                                {% if session.role in ['event_admin', 'system_manager'] %}
                                <option value="checkin">✅ Event Check-in/out</option>
                                {% endif %}
                            </select>
                        </div>
                        
                        <!-- Event Selection (for check-in mode) -->
                        <div class="col-md-6" id="eventSelectionDiv" style="display: none;">
                            <label class="form-label fw-bold">
                                <i class="fas fa-calendar-check me-2"></i>
                                Select Event:
                            </label>
                            <select id="eventSelect" class="form-select form-select-lg">
                                <option value="">-- Select Event --</option>
                            </select>
                        </div>
                    </div>

                    <hr class="my-4">

                    <!-- Scan Method Tabs with LARGE VISIBLE BUTTONS -->
                    <ul class="nav nav-tabs nav-fill mb-4" id="scanMethodTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="camera-tab" data-bs-toggle="tab" data-bs-target="#camera" type="button">
                                <i class="fas fa-camera fa-2x d-block mb-2"></i>
                                <span class="fw-bold">Camera QR</span>
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="nfc-tab" data-bs-toggle="tab" data-bs-target="#nfc" type="button">
                                <i class="fas fa-wifi fa-2x d-block mb-2"></i>
                                <span class="fw-bold">NFC Scan</span>
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="manual-tab" data-bs-toggle="tab" data-bs-target="#manual" type="button">
                                <i class="fas fa-keyboard fa-2x d-block mb-2"></i>
                                <span class="fw-bold">Manual Entry</span>
                            </button>
                        </li>
                    </ul>

                    <!-- Tab Content -->
                    <div class="tab-content" id="scanMethodContent">
                        
                        <!-- Camera QR Scanner -->
                        <div class="tab-pane fade show active" id="camera" role="tabpanel">
                            <div class="text-center p-4">
                                <div id="reader" class="mb-4" style="border-radius: 16px; overflow: hidden; max-width: 500px; margin: 0 auto; border: 3px solid #4F46E5;"></div>
                                
                                <div class="d-grid gap-3">
                                    <button id="startCameraBtn" class="btn btn-primary btn-lg">
                                        <i class="fas fa-camera fa-2x d-block mb-2"></i>
                                        <span class="fs-5 fw-bold">START CAMERA SCANNER</span>
                                    </button>
                                    <button id="stopCameraBtn" class="btn btn-danger btn-lg" style="display: none;">
                                        <i class="fas fa-stop fa-2x d-block mb-2"></i>
                                        <span class="fs-5 fw-bold">STOP CAMERA</span>
                                    </button>
                                </div>
                                
                                <div class="alert alert-info mt-4">
                                    <i class="fas fa-info-circle me-2"></i>
                                    <strong>How to use:</strong> Click the button above, allow camera access, then point your camera at a QR code
                                </div>
                            </div>
                        </div>

                        <!-- NFC Scanner -->
                        <div class="tab-pane fade" id="nfc" role="tabpanel">
                            <div class="text-center p-5">
                                <div id="nfcStatus" class="mb-4">
                                    <i class="fas fa-wifi fa-5x text-primary mb-3 pulse"></i>
                                    <h3 class="fw-bold">NFC Ready</h3>
                                    <p class="text-muted fs-5">Click the button below and tap an NFC badge</p>
                                </div>
                                
                                <div class="d-grid gap-3 mb-4">
                                    <button id="startNfcBtn" class="btn btn-success btn-lg">
                                        <i class="fas fa-wifi fa-2x d-block mb-2"></i>
                                        <span class="fs-5 fw-bold">START NFC SCAN</span>
                                    </button>
                                    <button id="stopNfcBtn" class="btn btn-danger btn-lg" style="display: none;">
                                        <i class="fas fa-stop fa-2x d-block mb-2"></i>
                                        <span class="fs-5 fw-bold">STOP NFC SCAN</span>
                                    </button>
                                </div>
                                
                                <div class="alert alert-info">
                                    <h5 class="alert-heading">
                                        <i class="fas fa-lightbulb me-2"></i>
                                        How to use NFC:
                                    </h5>
                                    <ol class="text-start mb-0">
                                        <li class="mb-2">Click "START NFC SCAN" button above</li>
                                        <li class="mb-2">Tap your phone to another phone/badge</li>
                                        <li class="mb-2">Wait for confirmation message</li>
                                    </ol>
                                    <hr>
                                    <small class="text-muted">
                                        <i class="fas fa-exclamation-triangle me-1"></i>
                                        Note: NFC requires compatible hardware. Not all devices support NFC scanning.
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Manual Entry -->
                        <div class="tab-pane fade" id="manual" role="tabpanel">
                            <div class="p-4">
                                <div class="mb-4">
                                    <label for="manualBadgeId" class="form-label fs-5 fw-bold">
                                        <i class="fas fa-id-card me-2"></i>
                                        Enter Badge ID or Email:
                                    </label>
                                    <input type="text" 
                                           class="form-control form-control-lg" 
                                           id="manualBadgeId" 
                                           placeholder="e.g., NFC-ABC123XYZ or user@email.com"
                                           autocomplete="off"
                                           style="font-size: 1.2rem; padding: 1rem;">
                                    <small class="text-muted mt-2 d-block">
                                        <i class="fas fa-info-circle me-1"></i>
                                        Badge ID format: NFC-XXXXXXXXXXXX
                                    </small>
                                </div>
                                
                                <div class="d-grid">
                                    <button id="submitManualBtn" class="btn btn-primary btn-lg">
                                        <i class="fas fa-paper-plane fa-2x d-block mb-2"></i>
                                        <span class="fs-5 fw-bold">SUBMIT SCAN</span>
                                    </button>
                                </div>
                                
                                <div class="alert alert-warning mt-4">
                                    <i class="fas fa-keyboard me-2"></i>
                                    <strong>Manual Entry:</strong> Type the badge ID shown on someone's badge or enter their email address
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Scan Result Display -->
                    <div id="scanResult" class="mt-4" style="display: none;">
                        <div class="alert alert-dismissible fade show" id="resultAlert">
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            <div id="resultContent"></div>
                        </div>
                    </div>

                </div>
            </div>
            
            <!-- Recent Scans Card -->
            <div class="card shadow-lg mt-4 animate-in">
                <div class="card-header bg-light">
                    <h5 class="mb-0">
                        <i class="fas fa-history me-2"></i>
                        Recent Scans
                    </h5>
                </div>
                <div class="card-body">
                    <div id="recentScans" class="list-group">
                        <div class="list-group-item text-muted text-center">
                            <i class="fas fa-inbox fa-3x mb-3 d-block"></i>
                            No scans yet. Start scanning to see your activity here!
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</div>

<!-- HTML5 QR Code Scanner Library -->
<script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>

<style>
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .nav-tabs .nav-link {
        padding: 1.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    #reader video {
        border-radius: 12px;
    }
</style>

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

// Load Events
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

// Camera Scanner
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
        { 
            fps: 10, 
            qrbox: { width: 250, height: 250 },
            aspectRatio: 1.0
        },
        onScanSuccess,
        onScanError
    ).then(() => {
        document.getElementById('startCameraBtn').style.display = 'none';
        document.getElementById('stopCameraBtn').style.display = 'block';
    }).catch(err => {
        showResult('danger', `Camera error: ${err}. Please allow camera access.`);
    });
}

function stopCameraScanner() {
    if (html5QrCode) {
        html5QrCode.stop().then(() => {
            document.getElementById('startCameraBtn').style.display = 'block';
            document.getElementById('stopCameraBtn').style.display = 'none';
        });
    }
}

function onScanSuccess(decodedText, decodedResult) {
    console.log('QR Code scanned:', decodedText);
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
            document.getElementById('stopNfcBtn').style.display = 'block';
            document.getElementById('nfcStatus').innerHTML = `
                <i class="fas fa-wifi fa-5x text-success fa-pulse mb-3"></i>
                <h3 class="text-success fw-bold">NFC Scanning Active</h3>
                <p class="text-muted fs-5">Tap an NFC badge now...</p>
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
            showResult('danger', `NFC Error: ${error.message}`);
        }
    } else {
        showResult('warning', 'NFC is not supported on this device. Please use QR code or manual entry instead.');
    }
});

document.getElementById('stopNfcBtn').addEventListener('click', function() {
    document.getElementById('startNfcBtn').style.display = 'block';
    document.getElementById('stopNfcBtn').style.display = 'none';
    document.getElementById('nfcStatus').innerHTML = `
        <i class="fas fa-wifi fa-5x text-primary mb-3"></i>
        <h3 class="fw-bold">NFC Ready</h3>
        <p class="text-muted fs-5">Click the button below and tap an NFC badge</p>
    `;
});

// Manual Entry
document.getElementById('submitManualBtn').addEventListener('click', function() {
    const badgeId = document.getElementById('manualBadgeId').value.trim();
    if (badgeId) {
        processScan(badgeId, 'manual');
    } else {
        showResult('danger', 'Please enter a badge ID or email');
    }
});

document.getElementById('manualBadgeId').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('submitManualBtn').click();
    }
});

// Process Scan
async function processScan(scanData, scanMethod) {
    try {
        if (scannerMode === 'checkin' && !selectedEventId) {
            showResult('danger', 'Please select an event first');
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
            showResult('success', `<i class="fas fa-check-circle fa-2x d-block mb-2"></i><strong>${data.message}</strong>`);
            addRecentScan(data, scanMethod);
            document.getElementById('manualBadgeId').value = '';
        } else {
            showResult('danger', `<i class="fas fa-times-circle fa-2x d-block mb-2"></i><strong>${data.message || 'Scan failed'}</strong>`);
        }
        
    } catch (error) {
        showResult('danger', `Error: ${error.message}`);
    }
}

// Show Result
function showResult(type, message) {
    const resultDiv = document.getElementById('scanResult');
    const resultAlert = document.getElementById('resultAlert');
    const resultContent = document.getElementById('resultContent');
    
    resultAlert.className = `alert alert-${type} alert-dismissible fade show`;
    resultContent.innerHTML = message;
    resultDiv.style.display = 'block';
    
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}

// Recent Scans
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
        container.innerHTML = `
            <div class="list-group-item text-muted text-center">
                <i class="fas fa-inbox fa-3x mb-3 d-block"></i>
                No scans yet. Start scanning!
            </div>
        `;
        return;
    }
    
    container.innerHTML = recentScans.map(scan => `
        <div class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-primary me-2">${scan.method}</span>
                    <strong>${scan.message}</strong>
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
    f.write(FIXED_SCANNER.strip())

print(f"{Colors.GREEN}✓{Colors.END} Fixed scanner.html with LARGE VISIBLE BUTTONS")
print(f"  {Colors.GREEN}✓{Colors.END} Camera QR button - HIGHLY VISIBLE")
print(f"  {Colors.GREEN}✓{Colors.END} NFC button - HIGHLY VISIBLE")
print(f"  {Colors.GREEN}✓{Colors.END} Manual entry - HIGHLY VISIBLE")
print(f"  {Colors.GREEN}✓{Colors.END} Tab navigation with large icons")
print(f"  {Colors.GREEN}✓{Colors.END} Modern card design")
print()