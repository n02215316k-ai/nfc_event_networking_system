import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

WORKING_NFC_SCANNER = """
{% extends "base.html" %}
{% block title %}NFC/QR Scanner{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 mx-auto">
            <!-- Scanner Mode Selection -->
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="fas fa-qrcode me-2"></i>NFC/QR Scanner</h4>
                </div>
                <div class="card-body">
                    <div class="btn-group w-100 mb-3" role="group">
                        <button type="button" class="btn btn-outline-primary active" id="btn-qr-mode">
                            <i class="fas fa-qrcode me-1"></i>QR Code Scanner
                        </button>
                        <button type="button" class="btn btn-outline-primary" id="btn-nfc-mode">
                            <i class="fas fa-wifi me-1"></i>NFC Scanner
                        </button>
                    </div>

                    <!-- QR Scanner -->
                    <div id="qr-scanner-section">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>QR Code Scanner:</strong> Click "Start Camera" and point at a QR code
                        </div>
                        
                        <div class="text-center mb-3">
                            <button class="btn btn-success btn-lg" id="start-camera">
                                <i class="fas fa-camera me-2"></i>Start Camera
                            </button>
                            <button class="btn btn-danger btn-lg d-none" id="stop-camera">
                                <i class="fas fa-stop me-2"></i>Stop Camera
                            </button>
                        </div>

                        <!-- Camera Preview -->
                        <div id="camera-preview" class="d-none">
                            <video id="qr-video" class="w-100 rounded" style="max-height: 400px;"></video>
                            <canvas id="qr-canvas" class="d-none"></canvas>
                        </div>

                        <!-- Scan Result -->
                        <div id="scan-result" class="alert alert-success d-none mt-3">
                            <h5><i class="fas fa-check-circle me-2"></i>Scan Successful!</h5>
                            <p id="scan-data"></p>
                            <button class="btn btn-primary" id="process-scan">Process Scan</button>
                        </div>
                    </div>

                    <!-- NFC Scanner -->
                    <div id="nfc-scanner-section" class="d-none">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>NFC Scanner:</strong> Click "Start NFC" and hold your phone near an NFC tag
                        </div>

                        <div class="text-center mb-3">
                            <button class="btn btn-success btn-lg" id="start-nfc">
                                <i class="fas fa-wifi me-2"></i>Start NFC Scan
                            </button>
                        </div>

                        <div id="nfc-status" class="alert alert-secondary">
                            <p class="mb-0"><i class="fas fa-circle-notch fa-spin me-2"></i>Ready to scan...</p>
                        </div>

                        <div id="nfc-result" class="alert alert-success d-none">
                            <h5><i class="fas fa-check-circle me-2"></i>NFC Tag Detected!</h5>
                            <p id="nfc-data"></p>
                            <button class="btn btn-primary" id="process-nfc">Process NFC</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Scans -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-history me-2"></i>Recent Scans</h5>
                </div>
                <div class="card-body">
                    <div id="recent-scans" class="list-group">
                        <p class="text-muted">No scans yet</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
<script>
// Mode switching
document.getElementById('btn-qr-mode').addEventListener('click', function() {
    this.classList.add('active');
    document.getElementById('btn-nfc-mode').classList.remove('active');
    document.getElementById('qr-scanner-section').classList.remove('d-none');
    document.getElementById('nfc-scanner-section').classList.add('d-none');
});

document.getElementById('btn-nfc-mode').addEventListener('click', function() {
    this.classList.add('active');
    document.getElementById('btn-qr-mode').classList.remove('active');
    document.getElementById('nfc-scanner-section').classList.remove('d-none');
    document.getElementById('qr-scanner-section').classList.add('d-none');
});

// QR Code Scanner
let videoStream = null;
let scanning = false;

document.getElementById('start-camera').addEventListener('click', async function() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        
        videoStream = stream;
        const video = document.getElementById('qr-video');
        video.srcObject = stream;
        video.play();
        
        document.getElementById('camera-preview').classList.remove('d-none');
        document.getElementById('start-camera').classList.add('d-none');
        document.getElementById('stop-camera').classList.remove('d-none');
        
        scanning = true;
        scanQRCode();
    } catch (err) {
        alert('Camera access denied: ' + err.message);
    }
});

document.getElementById('stop-camera').addEventListener('click', function() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        scanning = false;
        document.getElementById('camera-preview').classList.add('d-none');
        document.getElementById('start-camera').classList.remove('d-none');
        document.getElementById('stop-camera').classList.add('d-none');
    }
});

function scanQRCode() {
    if (!scanning) return;
    
    const video = document.getElementById('qr-video');
    const canvas = document.getElementById('qr-canvas');
    const context = canvas.getContext('2d');
    
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (code) {
            handleQRScan(code.data);
            return;
        }
    }
    
    requestAnimationFrame(scanQRCode);
}

function handleQRScan(data) {
    scanning = false;
    document.getElementById('scan-data').textContent = 'Data: ' + data;
    document.getElementById('scan-result').classList.remove('d-none');
    
    document.getElementById('process-scan').onclick = function() {
        processCheckin(data, 'qr');
    };
    
    addToRecentScans(data, 'QR Code');
}

// NFC Scanner
document.getElementById('start-nfc').addEventListener('click', async function() {
    if ('NDEFReader' in window) {
        try {
            const ndef = new NDEFReader();
            await ndef.scan();
            
            document.getElementById('nfc-status').innerHTML = 
                '<p class="mb-0 text-success"><i class="fas fa-check-circle me-2"></i>Scanning... Hold NFC tag near device</p>';
            
            ndef.addEventListener('reading', ({ message, serialNumber }) => {
                let nfcData = serialNumber;
                
                for (const record of message.records) {
                    if (record.recordType === 'text') {
                        const textDecoder = new TextDecoder(record.encoding);
                        nfcData = textDecoder.decode(record.data);
                    }
                }
                
                handleNFCScan(nfcData);
            });
            
        } catch (err) {
            alert('NFC Error: ' + err.message);
            document.getElementById('nfc-status').innerHTML = 
                '<p class="mb-0 text-danger"><i class="fas fa-times-circle me-2"></i>Error: ' + err.message + '</p>';
        }
    } else {
        alert('NFC not supported on this device. Please use a compatible Android device with Chrome.');
    }
});

function handleNFCScan(data) {
    document.getElementById('nfc-data').textContent = 'NFC Data: ' + data;
    document.getElementById('nfc-result').classList.remove('d-none');
    
    document.getElementById('process-nfc').onclick = function() {
        processCheckin(data, 'nfc');
    };
    
    addToRecentScans(data, 'NFC Tag');
}

// Process check-in
function processCheckin(data, method) {
    fetch('/nfc/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            scan_data: data,
            scan_method: method
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert('✅ ' + result.message);
            if (result.redirect) {
                window.location.href = result.redirect;
            }
        } else {
            alert('❌ ' + result.message);
        }
    })
    .catch(error => {
        alert('Error: ' + error.message);
    });
}

// Recent scans
function addToRecentScans(data, type) {
    const recentScans = document.getElementById('recent-scans');
    const time = new Date().toLocaleTimeString();
    
    const scanItem = document.createElement('div');
    scanItem.className = 'list-group-item';
    scanItem.innerHTML = `
        <div class="d-flex justify-content-between">
            <div>
                <strong>${type}</strong>
                <br><small class="text-muted">${data}</small>
            </div>
            <small class="text-muted">${time}</small>
        </div>
    `;
    
    if (recentScans.querySelector('p')) {
        recentScans.innerHTML = '';
    }
    
    recentScans.insertBefore(scanItem, recentScans.firstChild);
}
</script>
{% endblock %}
"""

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}PHASE 2: ENHANCING NFC SCANNER TO ACTUALLY WORK{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

filepath = 'templates/nfc/scanner.html'
os.makedirs(os.path.dirname(filepath), exist_ok=True)

# Backup existing
if os.path.exists(filepath):
    import shutil
    backup = filepath + '.backup_' + str(int(__import__('time').time()))
    shutil.copy2(filepath, backup)
    print(f"{Colors.GREEN}✓{Colors.END} Backup: {backup}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(WORKING_NFC_SCANNER.strip())

print(f"{Colors.GREEN}✓{Colors.END} Enhanced: {filepath}")
print(f"\n{Colors.GREEN}✅ Working NFC/QR scanner created!{Colors.END}\n")