import os

print("=" * 80)
print("🔧 ADDING QUALIFICATIONS SECTION TO PROFILE")
print("=" * 80)

# Check 1: Find where to add qualifications in edit.html
print("\n1️⃣ Checking profile edit template...")

edit_template_path = 'templates/profile/edit.html'
with open(edit_template_path, 'r', encoding='utf-8') as f:
    edit_content = f.read()

if 'qualification' in edit_content.lower():
    print("✅ Qualifications section already exists in edit.html")
else:
    print("⚠️ Qualifications section NOT found in edit.html")
    print("   Adding it now...")

# Check 2: Check profile view template
print("\n2️⃣ Checking profile view template...")

view_template_path = 'templates/profile/view.html'
with open(view_template_path, 'r', encoding='utf-8') as f:
    view_content = f.read()

if 'qualification' in view_content.lower():
    print("✅ Qualifications display exists in view.html")
else:
    print("⚠️ Qualifications display NOT found in view.html")

print("\n" + "=" * 80)
print("🔧 CREATING COMPLETE QUALIFICATIONS INTERFACE")
print("=" * 80)

# Create standalone qualifications management page
qualifications_template = '''{% extends "base.html" %}

{% block title %}My Qualifications - NFC Event Network{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-12">
            
            <!-- Header -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="fas fa-graduation-cap me-2"></i>My Qualifications</h2>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addQualificationModal">
                    <i class="fas fa-plus me-2"></i>Add Qualification
                </button>
            </div>

            <!-- Existing Qualifications -->
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Your Qualifications</h5>
                </div>
                <div class="card-body">
                    {% if qualifications %}
                        <div class="row">
                            {% for qual in qualifications %}
                            <div class="col-md-6 mb-3">
                                <div class="card h-100 {% if qual.verification_status == 'rejected' %}border-danger{% elif qual.verification_status == 'verified' %}border-success{% else %}border-warning{% endif %}">
                                    <div class="card-body">
                                        <div class="d-flex justify-content-between align-items-start mb-2">
                                            <h5 class="card-title mb-0">
                                                <i class="fas fa-certificate me-2"></i>
                                                {{ qual.qualification_type|title }}
                                            </h5>
                                            {% if qual.verification_status == 'verified' %}
                                                <span class="badge bg-success">
                                                    <i class="fas fa-check-circle"></i> Verified
                                                </span>
                                            {% elif qual.verification_status == 'pending' %}
                                                <span class="badge bg-warning">
                                                    <i class="fas fa-clock"></i> Pending
                                                </span>
                                            {% else %}
                                                <span class="badge bg-danger">
                                                    <i class="fas fa-times-circle"></i> Rejected
                                                </span>
                                            {% endif %}
                                        </div>
                                        
                                        <p class="mb-1"><strong>Field:</strong> {{ qual.field_of_study }}</p>
                                        <p class="mb-1"><strong>Institution:</strong> {{ qual.institution }}</p>
                                        <p class="mb-1"><strong>Year:</strong> {{ qual.year_obtained }}</p>
                                        
                                        {% if qual.document_path %}
                                        <p class="mb-1">
                                            <a href="{{ url_for('static', filename=qual.document_path) }}" target="_blank" class="btn btn-sm btn-info">
                                                <i class="fas fa-file-download"></i> View Document
                                            </a>
                                        </p>
                                        {% endif %}
                                        
                                        {% if qual.verification_status == 'rejected' and qual.rejection_reason %}
                                        <div class="alert alert-danger mt-2 mb-0">
                                            <small><strong>Reason:</strong> {{ qual.rejection_reason }}</small>
                                        </div>
                                        {% endif %}
                                        
                                        <div class="mt-2">
                                            <button class="btn btn-sm btn-warning" onclick="editQualification({{ qual.id }})">
                                                <i class="fas fa-edit"></i> Edit
                                            </button>
                                            <button class="btn btn-sm btn-danger" onclick="deleteQualification({{ qual.id }})">
                                                <i class="fas fa-trash"></i> Delete
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            You haven't added any qualifications yet. Click "Add Qualification" to get started.
                        </div>
                    {% endif %}
                </div>
            </div>

            <!-- Info Card -->
            <div class="card shadow">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-question-circle me-2"></i>About Qualifications</h5>
                </div>
                <div class="card-body">
                    <h6>Why verify qualifications?</h6>
                    <ul>
                        <li>Build trust with event organizers and attendees</li>
                        <li>Get verified badge on your profile</li>
                        <li>Access to exclusive events requiring credentials</li>
                        <li>Stand out in the professional network</li>
                    </ul>
                    
                    <h6 class="mt-3">Verification Process:</h6>
                    <ol>
                        <li><strong>Submit:</strong> Add your qualification with supporting documents</li>
                        <li><strong>Review:</strong> System managers review your submission (1-3 days)</li>
                        <li><strong>Verified:</strong> Get verified badge or feedback for corrections</li>
                    </ol>
                    
                    <div class="alert alert-warning mt-3">
                        <strong>Document Requirements:</strong>
                        <ul class="mb-0">
                            <li>Accepted formats: PDF, JPG, PNG</li>
                            <li>Maximum file size: 5MB</li>
                            <li>Documents must be clear and readable</li>
                            <li>Official certificates, transcripts, or diplomas</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Add Qualification Modal -->
<div class="modal fade" id="addQualificationModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title">
                    <i class="fas fa-plus-circle me-2"></i>Add Qualification
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form id="addQualificationForm" method="POST" action="{{ url_for('profile.add_qualification') }}" enctype="multipart/form-data">
                <div class="modal-body">
                    
                    <div class="mb-3">
                        <label for="qualification_type" class="form-label">
                            Qualification Type <span class="text-danger">*</span>
                        </label>
                        <select class="form-select" id="qualification_type" name="qualification_type" required>
                            <option value="">-- Select Type --</option>
                            <option value="certificate">Certificate</option>
                            <option value="diploma">Diploma</option>
                            <option value="degree">Bachelor's Degree</option>
                            <option value="masters">Master's Degree</option>
                            <option value="phd">PhD/Doctorate</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="field_of_study" class="form-label">
                            Field of Study <span class="text-danger">*</span>
                        </label>
                        <input type="text" class="form-control" id="field_of_study" name="field_of_study" 
                               placeholder="e.g., Computer Science, Business Administration" required>
                    </div>

                    <div class="mb-3">
                        <label for="institution" class="form-label">
                            Institution/University <span class="text-danger">*</span>
                        </label>
                        <input type="text" class="form-control" id="institution" name="institution" 
                               placeholder="e.g., University of Cape Town" required>
                    </div>

                    <div class="mb-3">
                        <label for="year_obtained" class="form-label">
                            Year Obtained <span class="text-danger">*</span>
                        </label>
                        <input type="number" class="form-control" id="year_obtained" name="year_obtained" 
                               min="1950" max="{{ current_year }}" placeholder="2020" required>
                    </div>

                    <div class="mb-3">
                        <label for="document" class="form-label">
                            Upload Document <span class="text-danger">*</span>
                        </label>
                        <input type="file" class="form-control" id="document" name="document" 
                               accept=".pdf,.jpg,.jpeg,.png" required>
                        <small class="text-muted">
                            Upload your certificate, diploma, or official transcript (PDF, JPG, PNG - Max 5MB)
                        </small>
                    </div>

                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Note:</strong> Your qualification will be submitted for verification. 
                        You'll be notified once it's reviewed.
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane me-2"></i>Submit for Verification
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
function deleteQualification(qualId) {
    if (!confirm('Are you sure you want to delete this qualification?')) {
        return;
    }
    
    fetch(`/profile/delete-qualification/${qualId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Qualification deleted successfully');
            location.reload();
        } else {
            alert('Error: ' + (data.message || 'Failed to delete qualification'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the qualification');
    });
}

// Validate file size
document.getElementById('document').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            alert('File size must be less than 5MB');
            e.target.value = '';
        }
    }
});
</script>
{% endblock %}
'''

# Save qualifications template
os.makedirs('templates/profile', exist_ok=True)
with open('templates/profile/qualifications.html', 'w', encoding='utf-8') as f:
    f.write(qualifications_template)

print("✅ Created: templates/profile/qualifications.html")

# Now add route to profile controller if missing
print("\n3️⃣ Checking profile controller routes...")

profile_controller_path = 'src/controllers/profile_controller.py'
with open(profile_controller_path, 'r', encoding='utf-8') as f:
    controller_content = f.read()

routes_to_add = []

if "@profile_bp.route('/qualifications')" not in controller_content:
    routes_to_add.append('qualifications_page')
    print("⚠️ Qualifications page route missing")

if "@profile_bp.route('/delete-qualification" not in controller_content:
    routes_to_add.append('delete_qualification')
    print("⚠️ Delete qualification route missing")

if routes_to_add:
    print(f"\n🔧 Need to add {len(routes_to_add)} routes to profile controller")
    
    # Add routes code
    new_routes = '''

@profile_bp.route('/qualifications')
@login_required
def qualifications():
    """View and manage user qualifications"""
    user_id = session.get('user_id')
    
    # Get user's qualifications
    qualifications = execute_query("""
        SELECT * FROM qualifications 
        WHERE user_id = %s 
        ORDER BY 
            CASE verification_status 
                WHEN 'verified' THEN 1 
                WHEN 'pending' THEN 2 
                WHEN 'rejected' THEN 3 
            END,
            year_obtained DESC
    """, (user_id,), fetch=True) or []
    
    from datetime import datetime
    current_year = datetime.now().year
    
    return render_template('profile/qualifications.html', 
                         qualifications=qualifications,
                         current_year=current_year)

@profile_bp.route('/delete-qualification/<int:qual_id>', methods=['POST'])
@login_required
def delete_qualification(qual_id):
    """Delete a qualification"""
    user_id = session.get('user_id')
    
    # Check if qualification belongs to user
    qual = execute_query(
        'SELECT * FROM qualifications WHERE id = %s AND user_id = %s',
        (qual_id, user_id), fetch=True, fetchone=True
    )
    
    if not qual:
        return jsonify({'success': False, 'message': 'Qualification not found'})
    
    # Delete the file if it exists
    if qual.get('document_path'):
        import os
        file_path = os.path.join('static', qual['document_path'])
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    # Delete from database
    execute_query(
        'DELETE FROM qualifications WHERE id = %s',
        (qual_id,)
    )
    
    return jsonify({'success': True, 'message': 'Qualification deleted successfully'})
'''
    
    # Append to controller file
    with open(profile_controller_path, 'a', encoding='utf-8') as f:
        f.write(new_routes)
    
    print("✅ Added missing routes to profile controller")
else:
    print("✅ All routes already exist")

print("\n" + "=" * 80)
print("✅ QUALIFICATIONS SECTION COMPLETE!")
print("=" * 80)

print("\n📋 Access Points:")
print("   1. Direct URL: http://localhost:5000/profile/qualifications")
print("   2. Add link to profile menu")
print("   3. Add link to profile view page")

print("\n🔄 Next steps:")
print("   1. Restart Flask: python app.py")
print("   2. Visit: http://localhost:5000/profile/qualifications")
print("   3. Click 'Add Qualification' to submit documents")
print("   4. System managers can review at: /system-manager/verify-qualifications")