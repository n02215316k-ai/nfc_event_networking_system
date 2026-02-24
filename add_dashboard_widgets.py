DASHBOARD_WIDGET = """
<!-- Quick Access NFC Features -->
<div class="row mt-4">
    <div class="col-md-12">
        <div class="card border-primary">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-qrcode me-2"></i>NFC & QR Features</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <a href="{{ url_for('nfc.scanner_page') }}" class="btn btn-lg btn-outline-primary w-100 mb-3">
                            <i class="fas fa-camera fa-2x d-block mb-2"></i>
                            <strong>Scanner</strong>
                            <br><small>Scan NFC/QR Codes</small>
                        </a>
                    </div>
                    <div class="col-md-3">
                        <a href="{{ url_for('profile.my_nfc') }}" class="btn btn-lg btn-outline-success w-100 mb-3">
                            <i class="fas fa-id-card fa-2x d-block mb-2"></i>
                            <strong>My QR Code</strong>
                            <br><small>Personal Digital Pass</small>
                        </a>
                    </div>
                    {% if session.get('role') in ['event_admin', 'system_manager'] %}
                    <div class="col-md-3">
                        <a href="{{ url_for('event_admin.dashboard') }}" class="btn btn-lg btn-outline-info w-100 mb-3">
                            <i class="fas fa-calendar-check fa-2x d-block mb-2"></i>
                            <strong>Event Admin</strong>
                            <br><small>Manage Events</small>
                        </a>
                    </div>
                    <div class="col-md-3">
                        <a href="{{ url_for('event_admin.networking_analytics') }}" class="btn btn-lg btn-outline-warning w-100 mb-3">
                            <i class="fas fa-project-diagram fa-2x d-block mb-2"></i>
                            <strong>Networking</strong>
                            <br><small>View Analytics</small>
                        </a>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
"""

print("\n📝 Dashboard Widget HTML Created")
print("\nAdd this to templates/index.html or templates/dashboard.html")
print("(after the welcome message or existing content)\n")
print("=" * 80)
print(DASHBOARD_WIDGET)
print("=" * 80)