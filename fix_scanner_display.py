import os

print("=" * 80)
print("🔧 FIXING SCANNER DISPLAY ISSUE")
print("=" * 80)

# ============================================================================
# STEP 1: Create improved scanner template with proper video display
# ============================================================================
print("\n📋 Creating enhanced scanner template...")

scanner_template = '''{% extends "base.html" %}

{% block extra_css %}
<style>
    #qr-reader {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        border: 3px solid #007bff;
        border-radius: 10px;
        overflow: hidden;
    }
    
    #qr-reader video {
        width: 100% !important;
        height: auto !important;
        display: block !important;
    }
    
    #qr-reader__dashboard {
        background: #f8f9fa;
        padding: 10px;
    }
    
    #qr-reader__dashboard_section {
        padding: 5px;
    }
    
    .scan-result-card {
        animation: slideIn 0.3s ease-in;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .scanner-status {
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    .method-selector {
        margin-bottom: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Main Scanner Area -->
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4><i class="fas fa-camera"></i> QR/NFC Scanner</h4>
                </div>
                <div class="card-body">
                    <!-- Scan Method Selector -->
                    <div class="method-selector">
                        <label class="font-weight-bold">Scan Method:</label>
                        <div class="btn-group btn-group-toggle w-100" data-toggle="buttons">
                            <label class="btn btn-outline-primary active" id="qr-mode-btn">
                                <input type="radio" name="scan_method" value="qr" checked> 
                                <i class="fas fa-qrcode"></i> QR Code
                            </label>
                            <label class="btn btn-outline-success" id="nfc-mode-btn">
                                <input type="radio" name="scan_method" value="nfc"> 
                                <i class="fas fa-wifi"></i> NFC Tag
                            </label>
                            <label class="btn btn-outline-secondary" id="manual-mode-btn">
                                <input type="radio" name="scan_method" value="manual"> 
                                <i class="fas fa-keyboard"></i> Manual
                            </label>
                        </div>
                    </div>
                    
                    <!-- Event Selector -->
                    <div class="form-group">
                        <label for="event-select" class="font-weight-bold">Event (Optional):</label>
                        <select class="form-control" id="event-select">
                            <option value="">No Event / General Networking</option>
                            {% for event in events %}
                            <option value="{{ event.id }}">{{ event.title }} - {{ event.date }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <!-- QR Scanner Container -->
                    <div id="qr-container">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            <strong>Point your camera at a QR code to scan</strong>
                        </div>
                        <div id="qr-reader"></div>
                        <div class="text-center mt-2">
                            <button onclick="startQRScanner()" class="btn btn-success" id="start-qr-btn">
                                <i class="fas fa-play"></i> Start QR Scanner
                            </button>
                            <button onclick="stopQRScanner()" class="btn btn-danger" id="stop-qr-btn" style="display: none;">
                                <i class="fas fa-stop"></i> Stop Scanner
                            </button>
                        </div>
                    </div>
                    
                    <!-- NFC Container -->
                    <div id="nfc-container" style="display: none;">
                        <div class="alert alert-info text-center">
                            <i class="fas fa-wifi fa-3x mb-3"></i>
                            <h5>NFC Mode Active</h5>
                            <p>Bring your NFC-enabled device close to an NFC tag</p>
                        </div>
                        <button onclick="startNFC()" class="btn btn-success btn-lg btn-block">
                            <i class="fas fa-wifi"></i> Enable NFC Reading
                        </button>
                        <div id="nfc-status" class="mt-3"></div>
                    </div>
                    
                    <!-- Manual Entry Container -->
                    <div id="manual-container" style="display: none;">
                        <div class="alert alert-info">
                            <i class="fas fa-keyboard"></i>
                            <strong>Manual Entry:</strong> Enter profile URL or user ID
                        </div>
                        <div class="form-group">
                            <label>Profile URL or User ID:</label>
                            <input type="text" class="form-control" id="manual-input" 
                                   placeholder="http://localhost:5000/profile/view/123 or just 123">
                        </div>
                        <button onclick="processManualEntry()" class="btn btn-primary btn-block">
                            <i class="fas fa-check"></i> Connect
                        </button>
                    </div>
                    
                    <!-- Scan Result -->
                    <div id="result-container" style="display: none;" class="mt-4">
                        <div class="card scan-result-card border-success">
                            <div class="card-header bg-success text-white">
                                <h5><i class="fas fa-check-circle"></i> Scan Successful!</h5>
                            </div>
                            <div class="card-body" id="scan-result"></div>
                        </div>
                    </div>
                    
                    <!-- Error Display -->
                    <div id="error-container" style="display: none;" class="mt-4">
                        <div class="alert alert-danger" id="error-message"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sidebar -->
        <div class="col-md-4">
            <!-- Instructions -->
            <div class="card mb-3">
                <div class="card-header bg-info text-white">
                    <h5><i class="fas fa-info-circle"></i> Instructions</h5>
                </div>
                <div class="card-body">
                    <div id="qr-instructions">
                        <h6><i class="fas fa-qrcode"></i> QR Code Scanning:</h6>
                        <ol class="small">
                            <li>Click "Start QR Scanner"</li>
                            <li>Allow camera access when prompted</li>
                            <li>Point camera at QR code</li>
                            <li>Wait for automatic scan</li>
                        </ol>
                    </div>
                    
                    <div id="nfc-instructions" style="display: none;">
                        <h6><i class="fas fa-wifi"></i> NFC Scanning:</h6>
                        <ol class="small">
                            <li>Click "Enable NFC Reading"</li>
                            <li>Ensure NFC is enabled on device</li>
                            <li>Hold device near NFC tag</li>
                            <li>Connection automatic</li>
                        </ol>
                    </div>
                    
                    <div id="manual-instructions" style="display: none;">
                        <h6><i class="fas fa-keyboard"></i> Manual Entry:</h6>
                        <ol class="small">
                            <li>Get user's profile URL or ID</li>
                            <li>Enter in the text field</li>
                            <li>Click "Connect"</li>
                            <li>View profile or message</li>
                        </ol>
                    </div>
                    
                    <hr>
                    
                    <div class="text-center">
                        <a href="{{ url_for('nfc.recent_scans') }}" class="btn btn-outline-primary btn-sm btn-block">
                            <i class="fas fa-history"></i> View Recent Scans
                        </a>
                        <a href="{{ url_for('profile.qr_code') }}" class="btn btn-outline-info btn-sm btn-block">
                            <i class="fas fa-qrcode"></i> My QR Code
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Statistics -->
            <div class="card">
                <div class="card-header bg-secondary text-white">
                    <h5><i class="fas fa-chart-bar"></i> Your Stats</h5>
                </div>
                <div class="card-body" id="stats-container">
                    <div class="text-center text-muted">
                        <div class="spinner-border spinner-border-sm" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                        <p class="small mt-2">Loading stats...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Include html5-qrcode library -->
<script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>

<script>
let html5QrCode = null;
let isScanning = false;
let currentMethod = 'qr';

// ============================================================================
// QR CODE SCANNER FUNCTIONS
// ============================================================================

function startQRScanner() {
    if (isScanning) {
        console.log("Scanner already running");
        return;
    }
    
    console.log("Starting QR scanner...");
    
    const config = {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0
    };
    
    html5QrCode = new Html5Qrcode("qr-reader");
    
    Html5Qrcode.getCameras().then(cameras => {
        if (cameras && cameras.length) {
            // Use back camera if available
            const cameraId = cameras.length > 1 ? cameras[1].id : cameras[0].id;
            
            html5QrCode.start(
                cameraId,
                config,
                onScanSuccess,
                onScanFailure
            ).then(() => {
                isScanning = true;
                document.getElementById('start-qr-btn').style.display = 'none';
                document.getElementById('stop-qr-btn').style.display = 'inline-block';
                console.log("QR Scanner started successfully");
            }).catch(err => {
                console.error("Error starting scanner:", err);
                showError("Failed to start camera: " + err);
            });
        } else {
            showError("No cameras found on this device");
        }
    }).catch(err => {
        console.error("Error getting cameras:", err);
        showError("Could not access camera: " + err);
    });
}

function stopQRScanner() {
    if (html5QrCode && isScanning) {
        html5QrCode.stop().then(() => {
            isScanning = false;
            document.getElementById('start-qr-btn').style.display = 'inline-block';
            document.getElementById('stop-qr-btn').style.display = 'none';
            console.log("QR Scanner stopped");
        }).catch(err => {
            console.error("Error stopping scanner:", err);
        });
    }
}

function onScanSuccess(decodedText, decodedResult) {
    console.log("QR Code detected:", decodedText);
    
    // Stop scanning temporarily
    stopQRScanner();
    
    // Process the scan
    processScan(decodedText, 'qr');
}

function onScanFailure(error) {
    // Ignore scan failures (they happen constantly while scanning)
    // console.warn("Scan error:", error);
}

// ============================================================================
// SCAN PROCESSING
// ============================================================================

function processScan(scanData, method) {
    const eventId = document.getElementById('event-select').value;
    
    console.log("Processing scan:", { scanData, method, eventId });
    
    // Show loading
    document.getElementById('result-container').style.display = 'none';
    document.getElementById('error-container').style.display = 'none';
    
    fetch('/nfc/scan-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scan_data: scanData,
            scan_method: method,
            event_id: eventId || null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayScanResult(data.user);
            loadStats();
            
            // Restart scanner after 4 seconds
            setTimeout(() => {
                if (currentMethod === 'qr') {
                    document.getElementById('result-container').style.display = 'none';
                    startQRScanner();
                }
            }, 4000);
        } else {
            showError(data.error || 'Scan failed');
            
            // Restart scanner after 2 seconds
            setTimeout(() => {
                if (currentMethod === 'qr') {
                    startQRScanner();
                }
            }, 2000);
        }
    })
    .catch(error => {
        console.error('Scan error:', error);
        showError('Network error: ' + error.message);
        
        // Restart scanner after 2 seconds
        setTimeout(() => {
            if (currentMethod === 'qr') {
                startQRScanner();
            }
        }, 2000);
    });
}

function displayScanResult(user) {
    const resultHTML = `
        <div class="row align-items-center">
            <div class="col-auto">
                ${user.profile_picture ? 
                    `<img src="/static/${user.profile_picture}" class="rounded-circle" 
                          style="width: 80px; height: 80px; object-fit: cover;">` :
                    `<div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center" 
                          style="width: 80px; height: 80px; font-size: 32px;">
                        ${user.name[0].toUpperCase()}
                    </div>`
                }
            </div>
            <div class="col">
                <h5 class="mb-1">${user.name}</h5>
                <p class="text-muted mb-2">${user.email}</p>
                ${user.position ? `<p class="small mb-0"><i class="fas fa-briefcase"></i> ${user.position}</p>` : ''}
                ${user.institution ? `<p class="small mb-0"><i class="fas fa-building"></i> ${user.institution}</p>` : ''}
            </div>
        </div>
        <hr>
        <div class="btn-group w-100" role="group">
            <a href="${user.profile_url}" class="btn btn-primary">
                <i class="fas fa-user"></i> View Profile
            </a>
            <a href="/messages/compose?recipient=${user.id}" class="btn btn-info">
                <i class="fas fa-envelope"></i> Message
            </a>
            <button onclick="document.getElementById('result-container').style.display='none'; startQRScanner();" 
                    class="btn btn-secondary">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
    `;
    
    document.getElementById('scan-result').innerHTML = resultHTML;
    document.getElementById('result-container').style.display = 'block';
    document.getElementById('error-container').style.display = 'none';
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-container').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';
}

// ============================================================================
// NFC FUNCTIONS
// ============================================================================

async function startNFC() {
    if (!('NDEFReader' in window)) {
        showError('NFC is not supported on this browser. Try Chrome on Android.');
        return;
    }
    
    try {
        const ndef = new NDEFReader();
        await ndef.scan();
        
        document.getElementById('nfc-status').innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i> NFC scanning active. Tap a tag now.
            </div>
        `;
        
        ndef.addEventListener("reading", ({ message, serialNumber }) => {
            console.log("NFC tag detected:", serialNumber);
            
            for (const record of message.records) {
                console.log("Record type:", record.recordType);
                
                if (record.recordType === "url" || record.recordType === "text") {
                    const decoder = new TextDecoder();
                    const data = decoder.decode(record.data);
                    console.log("NFC data:", data);
                    
                    processScan(data, 'nfc');
                    break;
                }
            }
        });
        
        ndef.addEventListener("readingerror", () => {
            showError("Failed to read NFC tag. Try again.");
        });
        
    } catch (error) {
        console.error("NFC error:", error);
        showError('NFC Error: ' + error.message);
    }
}

// ============================================================================
// MANUAL ENTRY
// ============================================================================

function processManualEntry() {
    const input = document.getElementById('manual-input').value.trim();
    
    if (!input) {
        showError('Please enter a profile URL or user ID');
        return;
    }
    
    // Check if it's a URL or just an ID
    let scanData;
    if (input.includes('http')) {
        scanData = input;
    } else {
        // Assume it's a user ID
        scanData = `http://localhost:5000/profile/view/${input}`;
    }
    
    processScan(scanData, 'manual');
}

// ============================================================================
// MODE SWITCHING
// ============================================================================

document.getElementById('qr-mode-btn').addEventListener('click', () => {
    currentMethod = 'qr';
    document.getElementById('qr-container').style.display = 'block';
    document.getElementById('nfc-container').style.display = 'none';
    document.getElementById('manual-container').style.display = 'none';
    
    document.getElementById('qr-instructions').style.display = 'block';
    document.getElementById('nfc-instructions').style.display = 'none';
    document.getElementById('manual-instructions').style.display = 'none';
    
    stopQRScanner();
});

document.getElementById('nfc-mode-btn').addEventListener('click', () => {
    currentMethod = 'nfc';
    stopQRScanner();
    
    document.getElementById('qr-container').style.display = 'none';
    document.getElementById('nfc-container').style.display = 'block';
    document.getElementById('manual-container').style.display = 'none';
    
    document.getElementById('qr-instructions').style.display = 'none';
    document.getElementById('nfc-instructions').style.display = 'block';
    document.getElementById('manual-instructions').style.display = 'none';
});

document.getElementById('manual-mode-btn').addEventListener('click', () => {
    currentMethod = 'manual';
    stopQRScanner();
    
    document.getElementById('qr-container').style.display = 'none';
    document.getElementById('nfc-container').style.display = 'none';
    document.getElementById('manual-container').style.display = 'block';
    
    document.getElementById('qr-instructions').style.display = 'none';
    document.getElementById('nfc-instructions').style.display = 'none';
    document.getElementById('manual-instructions').style.display = 'block';
});

// ============================================================================
// STATISTICS
// ============================================================================

function loadStats() {
    fetch('/nfc/scan-stats')
        .then(response => response.json())
        .then(data => {
            const qrCount = data.by_method.find(m => m.scan_method === 'qr')?.count || 0;
            const nfcCount = data.by_method.find(m => m.scan_method === 'nfc')?.count || 0;
            const manualCount = data.by_method.find(m => m.scan_method === 'manual')?.count || 0;
            
            const statsHTML = `
                <div class="text-center">
                    <h2 class="mb-0">${data.total}</h2>
                    <p class="text-muted small">Total Scans</p>
                    <hr>
                    <div class="row small">
                        <div class="col-4">
                            <i class="fas fa-qrcode text-info"></i><br>
                            <strong>${qrCount}</strong><br>
                            <span class="text-muted">QR</span>
                        </div>
                        <div class="col-4">
                            <i class="fas fa-wifi text-success"></i><br>
                            <strong>${nfcCount}</strong><br>
                            <span class="text-muted">NFC</span>
                        </div>
                        <div class="col-4">
                            <i class="fas fa-keyboard text-secondary"></i><br>
                            <strong>${manualCount}</strong><br>
                            <span class="text-muted">Manual</span>
                        </div>
                    </div>
                    <hr>
                    <p class="small mb-0">
                        <i class="fas fa-calendar"></i> Last 7 days: <strong>${data.recent_7_days}</strong>
                    </p>
                </div>
            `;
            document.getElementById('stats-container').innerHTML = statsHTML;
        })
        .catch(err => {
            console.error('Error loading stats:', err);
            document.getElementById('stats-container').innerHTML = `
                <p class="text-center text-muted small">Unable to load stats</p>
            `;
        });
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("Scanner page loaded");
    loadStats();
    
    // Auto-start QR scanner
    // startQRScanner(); // Commented out - user must click to start
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopQRScanner();
});
</script>
{% endblock %}
'''

os.makedirs('templates/nfc', exist_ok=True)

with open('templates/nfc/scanner.html', 'w', encoding='utf-8') as f:
    f.write(scanner_template)

print("  ✅ Created enhanced scanner template")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ SCANNER FIX COMPLETE!")
print("=" * 80)

print("""
🎯 Changes Made:
  ✅ Enhanced scanner template with proper video display
  ✅ Added CSS to ensure video shows correctly
  ✅ Added manual start button (user must click to start camera)
  ✅ Improved error handling and console logging
  ✅ Added three modes: QR, NFC, Manual entry
  ✅ Better UI with instructions and stats

🚀 Next Steps:
  1. Restart Flask app: python app.py
  2. Visit: http://localhost:5000/nfc/scanner
  3. Click "Start QR Scanner" button
  4. Allow camera access when prompted
  5. Point camera at QR code

💡 Troubleshooting:
  • If white screen persists: Check browser console (F12) for errors
  • Camera permission: Ensure browser has camera access
  • HTTPS required: Some browsers require HTTPS for camera (use localhost)
  • Try different browser: Chrome works best for camera features

📱 To Test:
  1. Open /profile/qr on another device
  2. Scan that QR code with the scanner
  3. Should detect and show profile

✅ The scanner now has a START button - you must click it first!
""")