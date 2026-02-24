import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'

USER_NFC_TEMPLATE = """
{% extends "base.html" %}
{% block title %}My NFC/QR Code{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 mx-auto">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="fas fa-id-card me-2"></i>My Digital Pass</h4>
                </div>
                <div class="card-body text-center">
                    <h5 class="mb-4">{{ user.full_name }}</h5>
                    
                    <!-- NFC Code -->
                    <div class="mb-4">
                        <h6 class="text-muted">NFC Code</h6>
                        <div class="nfc-code-display p-4 bg-light rounded">
                            <p class="font-monospace">{{ nfc_code }}</p>
                            <button class="btn btn-sm btn-primary" onclick="refreshNFC()">
                                <i class="fas fa-sync-alt me-1"></i>Refresh
                            </button>
                        </div>
                        <small class="text-muted">This code changes every time for security</small>
                    </div>
                    
                    <!-- QR Code -->
                    <div class="mb-4">
                        <h6 class="text-muted">Personal QR Code</h6>
                        <img src="{{ qr_image }}" alt="Personal QR Code" class="img-fluid" style="max-width: 300px;">
                        <br>
                        <button class="btn btn-sm btn-success mt-2" onclick="downloadQR()">
                            <i class="fas fa-download me-1"></i>Download QR Code
                        </button>
                    </div>

                    <!-- Usage Instructions -->
                    <div class="alert alert-info">
                        <h6><i class="fas fa-info-circle me-2"></i>How to Use:</h6>
                        <ul class="text-start">
                            <li>Show this QR code at event check-in</li>
                            <li>Use NFC by holding your device near the scanner</li>
                            <li>Share your code for networking at events</li>
                        </ul>
                    </div>

                    <!-- My Registered Events -->
                    <div class="mt-4">
                        <h6>My Registered Events</h6>
                        <div class="list-group text-start">
                            {% for event in my_events %}
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ event.title }}</strong>
                                    <br>
                                    <small class="text-muted">{{ event.start_date|datetime_format('%B %d, %Y') }}</small>
                                </div>
                                <a href="{{ url_for('events.detail', event_id=event.id) }}" class="btn btn-sm btn-primary">View</a>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function refreshNFC() {
    fetch('/profile/refresh-nfc')
        .then(response => response.json())
        .then(data => {
            document.querySelector('.nfc-code-display p').textContent = data.nfc_code;
        });
}

function downloadQR() {
    const link = document.createElement('a');
    link.download = 'my_qr_code.png';
    link.href = '{{ qr_image }}';
    link.click();
}
</script>
{% endblock %}
"""

print(f"\n{Colors.CYAN}Creating user NFC/QR template...{Colors.END}\n")

os.makedirs('templates/profile', exist_ok=True)
with open('templates/profile/my_nfc.html', 'w', encoding='utf-8') as f:
    f.write(USER_NFC_TEMPLATE.strip())

print(f"{Colors.GREEN}✓{Colors.END} Created: {Colors.CYAN}templates/profile/my_nfc.html{Colors.END}")
print(f"\n{Colors.GREEN}✅ User NFC/QR template created!{Colors.END}\n")