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

# Event Details Template
EVENT_DETAILS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}{{ event.title }} - Event Management{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-calendar-alt me-2"></i>{{ event.title }}</h2>
        <div>
            <a href="{{ url_for('event_admin.live_attendance', event_id=event.id) }}" class="btn btn-success">
                <i class="fas fa-broadcast-tower me-1"></i>Live Attendance
            </a>
            <a href="{{ url_for('event_admin.generate_qr_codes', event_id=event.id) }}" class="btn btn-primary">
                <i class="fas fa-qrcode me-1"></i>QR Codes
            </a>
            <a href="{{ url_for('event_admin.event_reports', event_id=event.id) }}" class="btn btn-info">
                <i class="fas fa-chart-bar me-1"></i>Reports
            </a>
        </div>
    </div>

    <!-- Event Info Card -->
    <div class="row mb-4">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Event Information</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Date:</strong> {{ event.start_date|datetime_format('%B %d, %Y') }}</p>
                            <p><strong>Time:</strong> {{ event.start_date|datetime_format('%I:%M %p') }} - {{ event.end_date|datetime_format('%I:%M %p') }}</p>
                            <p><strong>Location:</strong> {{ event.location }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Category:</strong> <span class="badge bg-primary">{{ event.category }}</span></p>
                            <p><strong>Status:</strong> <span class="badge bg-success">{{ event.status }}</span></p>
                            <p><strong>Max Attendees:</strong> {{ event.max_attendees or 'Unlimited' }}</p>
                        </div>
                    </div>
                    <hr>
                    <p><strong>Description:</strong></p>
                    <p>{{ event.description }}</p>
                </div>
            </div>
        </div>

        <!-- Attendance Statistics -->
        <div class="col-md-4">
            <div class="card bg-primary text-white mb-3">
                <div class="card-body text-center">
                    <h6>Total Registered</h6>
                    <h2>{{ attendance_stats.total_registered or 0 }}</h2>
                </div>
            </div>
            <div class="card bg-success text-white mb-3">
                <div class="card-body text-center">
                    <h6>Checked In</h6>
                    <h2>{{ attendance_stats.total_checked_in or 0 }}</h2>
                </div>
            </div>
            <div class="card bg-info text-white mb-3">
                <div class="card-body text-center">
                    <h6>Currently Present</h6>
                    <h2>{{ attendance_stats.currently_present or 0 }}</h2>
                </div>
            </div>
            <div class="card bg-warning text-white">
                <div class="card-body text-center">
                    <h6>Checked Out</h6>
                    <h2>{{ attendance_stats.total_checked_out or 0 }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Check-in Methods -->
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Check-in Methods Distribution</h5>
                </div>
                <div class="card-body">
                    <canvas id="checkinMethodsChart" height="80"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Registrations Table -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Registered Attendees</h5>
                    <div>
                        <input type="text" class="form-control" id="search-attendees" placeholder="Search attendees...">
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover" id="attendees-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Registration Date</th>
                                    <th>Check-in Time</th>
                                    <th>Check-out Time</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for reg in registrations %}
                                <tr>
                                    <td>{{ reg.full_name }}</td>
                                    <td>{{ reg.email }}</td>
                                    <td>{{ reg.phone or '-' }}</td>
                                    <td>{{ reg.registration_date|datetime_format('%b %d, %Y') }}</td>
                                    <td>
                                        {% if reg.check_in_time %}
                                            {{ reg.check_in_time|datetime_format('%I:%M %p') }}
                                            <small class="text-muted">({{ reg.check_in_method }})</small>
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if reg.check_out_time %}
                                            {{ reg.check_out_time|datetime_format('%I:%M %p') }}
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if reg.current_status == 'present' %}
                                            <span class="badge bg-success">Present</span>
                                        {% elif reg.current_status == 'checked_out' %}
                                            <span class="badge bg-secondary">Checked Out</span>
                                        {% else %}
                                            <span class="badge bg-warning">Registered</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if not reg.check_in_time %}
                                        <button class="btn btn-sm btn-primary manual-checkin" data-user-id="{{ reg.user_id }}">
                                            Check In
                                        </button>
                                        {% endif %}
                                        <a href="/profile/{{ reg.user_id }}" class="btn btn-sm btn-info">View</a>
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
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Check-in methods chart
const ctx = document.getElementById('checkinMethodsChart').getContext('2d');
const methods = {{ checkin_methods|tojson }};

const labels = methods.map(m => m.check_in_method.toUpperCase());
const data = methods.map(m => m.count);

new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: ['#0d6efd', '#198754', '#ffc107']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});

// Manual check-in
document.querySelectorAll('.manual-checkin').forEach(btn => {
    btn.addEventListener('click', function() {
        const userId = this.getAttribute('data-user-id');
        if (confirm('Manually check in this attendee?')) {
            fetch('/event-admin/event/{{ event.id }}/manual-checkin', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_id: userId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Check-in successful!');
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            });
        }
    });
});

// Search attendees
document.getElementById('search-attendees').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#attendees-table tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});
</script>
{% endblock %}
"""

# Event Reports Template
EVENT_REPORTS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Reports - {{ event.title }}{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-chart-line me-2"></i>Event Reports: {{ event.title }}</h2>
        <div>
            <button class="btn btn-primary" onclick="window.print()">
                <i class="fas fa-print me-1"></i>Print Report
            </button>
            <a href="{{ url_for('event_admin.event_details', event_id=event.id) }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Back
            </a>
        </div>
    </div>

    <!-- Summary Cards -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card border-primary">
                <div class="card-body text-center">
                    <h6 class="text-muted">Attendance Rate</h6>
                    <h2 class="text-primary">
                        {% set rate = (attendance_stats.total_checked_in / attendance_stats.total_registered * 100) if attendance_stats.total_registered > 0 else 0 %}
                        {{ "%.1f"|format(rate) }}%
                    </h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-success">
                <div class="card-body text-center">
                    <h6 class="text-muted">Total Networking</h6>
                    <h2 class="text-success">{{ networking_stats.total_connections }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-info">
                <div class="card-body text-center">
                    <h6 class="text-muted">Avg. Duration</h6>
                    <h2 class="text-info">2.5h</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-warning">
                <div class="card-body text-center">
                    <h6 class="text-muted">Peak Attendance</h6>
                    <h2 class="text-warning">
                        {{ attendance_stats.currently_present or 0 }}
                    </h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Attendance Timeline -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Attendance Over Time</h5>
                </div>
                <div class="card-body">
                    <canvas id="attendanceTimelineChart" height="80"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Top Networkers -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Top Networkers</h5>
                </div>
                <div class="card-body">
                    {% if top_networkers %}
                    <div class="list-group">
                        {% for networker in top_networkers %}
                        <div class="list-group-item d-flex justify-content-between align-items-center">
                            {{ networker.full_name }}
                            <span class="badge bg-primary rounded-pill">{{ networker.connections }} connections</span>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted">No networking data available</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Check-in Methods -->
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Check-in Method Breakdown</h5>
                </div>
                <div class="card-body">
                    <canvas id="checkinMethodsChart" height="200"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Detailed Attendance Table -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Detailed Attendance Log</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-sm table-striped">
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th>Attendee</th>
                                    <th>Action</th>
                                    <th>Method</th>
                                    <th>Duration</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in attendance_timeline %}
                                <tr>
                                    <td>{{ item.hour|datetime_format('%I:%M %p') }}</td>
                                    <td colspan="4">
                                        <strong>{{ item.count }} check-ins</strong>
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
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Attendance timeline chart
const timelineCtx = document.getElementById('attendanceTimelineChart').getContext('2d');
const timelineData = {{ attendance_timeline|tojson }};

new Chart(timelineCtx, {
    type: 'line',
    data: {
        labels: timelineData.map(d => new Date(d.hour).toLocaleTimeString()),
        datasets: [{
            label: 'Check-ins',
            data: timelineData.map(d => d.count),
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Check-in methods pie chart
const methodsCtx = document.getElementById('checkinMethodsChart').getContext('2d');
const methodsData = {{ checkin_methods|tojson }};

new Chart(methodsCtx, {
    type: 'pie',
    data: {
        labels: methodsData.map(m => m.check_in_method.toUpperCase()),
        datasets: [{
            data: methodsData.map(m => m.count),
            backgroundColor: ['#0d6efd', '#198754', '#ffc107']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});
</script>
{% endblock %}
"""

# QR Codes Generation Template
QR_CODES_TEMPLATE = """
{% extends "base.html" %}
{% block title %}QR Codes - {{ event.title }}{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-qrcode me-2"></i>Event QR Codes: {{ event.title }}</h2>
        <div>
            <button class="btn btn-primary" onclick="downloadAllQR()">
                <i class="fas fa-download me-1"></i>Download All
            </button>
            <button class="btn btn-success" onclick="window.print()">
                <i class="fas fa-print me-1"></i>Print All
            </button>
            <a href="{{ url_for('event_admin.event_details', event_id=event.id) }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Back
            </a>
        </div>
    </div>

    <div class="alert alert-info">
        <i class="fas fa-info-circle me-2"></i>
        <strong>Instructions:</strong> Each attendee has a unique QR code for event check-in. 
        You can print these codes and distribute them, or attendees can scan from their devices.
    </div>

    <!-- QR Codes Grid -->
    <div class="row">
        {% for reg in registrations %}
        <div class="col-md-3 mb-4">
            <div class="card qr-card">
                <div class="card-body text-center">
                    <h6 class="card-title">{{ reg.full_name }}</h6>
                    <p class="text-muted small">{{ reg.email }}</p>
                    
                    {% if reg.qr_image %}
                    <img src="{{ reg.qr_image }}" class="img-fluid qr-code-img" alt="QR Code" style="max-width: 200px;">
                    {% else %}
                    <div class="qr-placeholder" data-reg-id="{{ reg.id }}">
                        <p>Generating QR code...</p>
                    </div>
                    {% endif %}
                    
                    <div class="mt-3">
                        <button class="btn btn-sm btn-primary" onclick="downloadQR('{{ reg.id }}', '{{ reg.full_name }}')">
                            <i class="fas fa-download me-1"></i>Download
                        </button>
                        <button class="btn btn-sm btn-success" onclick="emailQR('{{ reg.id }}')">
                            <i class="fas fa-envelope me-1"></i>Email
                        </button>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<style>
@media print {
    .btn, .alert, nav, footer { display: none !important; }
    .qr-card { page-break-inside: avoid; }
    .col-md-3 { width: 50%; }
}
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>

<script>
function downloadQR(regId, name) {
    const qrImg = document.querySelector(`[data-reg-id="${regId}"]`).parentElement.querySelector('.qr-code-img');
    const link = document.createElement('a');
    link.download = `${name}_QR.png`;
    link.href = qrImg.src;
    link.click();
}

function emailQR(regId) {
    fetch(`/event-admin/event/{{ event.id }}/email-qr/${regId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('QR code sent successfully!');
        } else {
            alert('Error: ' + data.message);
        }
    });
}

function downloadAllQR() {
    const zip = new JSZip();
    const qrImages = document.querySelectorAll('.qr-code-img');
    
    qrImages.forEach((img, index) => {
        const name = img.parentElement.querySelector('.card-title').textContent;
        const base64Data = img.src.split(',')[1];
        zip.file(`${name}_QR.png`, base64Data, {base64: true});
    });
    
    zip.generateAsync({type: 'blob'}).then(function(content) {
        saveAs(content, '{{ event.title }}_QR_Codes.zip');
    });
}
</script>
{% endblock %}
"""

# Networking Analytics Template
NETWORKING_ANALYTICS_TEMPLATE = """
{% extends "base.html" %}
{% block title %}Networking Analytics - Event Admin{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <h2><i class="fas fa-project-diagram me-2"></i>Networking Analytics</h2>

    <div class="row mt-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Total Connections: {{ total_connections }}</h5>
                </div>
                <div class="card-body">
                    <canvas id="networkingChart" height="80"></canvas>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Networking by Event</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Event</th>
                                    <th>Total Connections</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for event in networking_by_event %}
                                <tr>
                                    <td>{{ event.title }}</td>
                                    <td><span class="badge bg-primary">{{ event.total_connections }}</span></td>
                                    <td>
                                        <a href="{{ url_for('event_admin.event_reports', event_id=event.id) }}" 
                                           class="btn btn-sm btn-info">View Details</a>
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
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('networkingChart').getContext('2d');
const data = {{ networking_by_event|tojson }};

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: data.map(d => d.title),
        datasets: [{
            label: 'Connections',
            data: data.map(d => d.total_connections),
            backgroundColor: '#0d6efd'
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
</script>
{% endblock %}
"""

print(f"\n{Colors.CYAN}Creating remaining Event Admin templates...{Colors.END}\n")

create_file('templates/event_admin/event_details.html', EVENT_DETAILS_TEMPLATE)
create_file('templates/event_admin/reports.html', EVENT_REPORTS_TEMPLATE)
create_file('templates/event_admin/qr_codes.html', QR_CODES_TEMPLATE)
create_file('templates/event_admin/networking_analytics.html', NETWORKING_ANALYTICS_TEMPLATE)

print(f"\n{Colors.GREEN}✅ All Event Admin templates created!{Colors.END}\n")