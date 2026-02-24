from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from database import get_db_connection
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import qrcode
from io import BytesIO
import base64


# Database helper function
def execute_query(query, params=None, fetch=False, fetchone=False):
    """Execute database query with proper connection handling"""
    from database import get_db_connection
    
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchone() if fetchone else cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid if cursor.lastrowid else True
        
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.close()
        return None


events_bp = Blueprint('events', __name__)

def require_login(f):
    '''Decorator to require login'''
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@events_bp.route('/')
def list_events():
    '''List all published events'''
    category = request.args.get('category', '')
    
    query = '''
        SELECT e.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id AND status != 'cancelled') as registration_count
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.status = 'published'
    '''
    
    params = []
    if category:
        query += " AND e.category = %s"
        params.append(category)
    
    query += " ORDER BY e.start_date DESC"
    
    events = execute_query(query, tuple(params) if params else None, fetch=True) or []
    
    # Check if user is registered for each event
    if 'user_id' in session:
        for event in events:
            registered = execute_query(
                "SELECT id FROM attendance WHERE event_id = %s AND user_id = %s",
                (event['id'], session['user_id']),
                fetch=True,
                fetchone=True
            )
            event['is_registered'] = registered is not None
    
    return render_template('events/list.html', events=events, selected_category=category)

@events_bp.route('/create', methods=['GET', 'POST'])
@require_login
def create_event():
    '''Create a new event'''
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'other')
        location = request.form.get('location', '').strip()
        venue = request.form.get('venue', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        max_attendees = request.form.get('max_attendees', '')
        
        # Validation
        errors = []
        
        if not title or len(title) < 5:
            errors.append('Event title must be at least 5 characters.')
        
        if not description or len(description) < 20:
            errors.append('Event description must be at least 20 characters.')
        
        if not start_date or not end_date:
            errors.append('Please provide event start and end dates.')
        
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            if start_dt >= end_dt:
                errors.append('End date must be after start date.')
            
            if start_dt < datetime.now():
                errors.append('Event cannot start in the past.')
        except:
            errors.append('Invalid date format.')
        
        if max_attendees:
            try:
                max_attendees = int(max_attendees)
                if max_attendees < 1:
                    errors.append('Maximum attendees must be at least 1.')
            except:
                errors.append('Invalid maximum attendees value.')
        else:
            max_attendees = None
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('events/create.html')
        
        # Handle cover image upload
        cover_image = None
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename and current_app.allowed_file(file.filename):
                filename = secure_filename(f"event_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'events', filename)
                file.save(filepath)
                cover_image = f"uploads/events/{filename}"
        
        # Create event
        try:
            event_id = execute_query('''
                INSERT INTO events (title, description, category, location, venue,
                                  start_date, end_date, creator_id, status, max_attendees, cover_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'published', %s, %s)
            ''', (title, description, category, location, venue, start_date, end_date,
                  session['user_id'], max_attendees, cover_image), return_lastrowid=True)
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"EVENT:{event_id}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            qr_filename = f"event_{event_id}_qr.png"
            qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'events', qr_filename)
            img.save(qr_path)
            
            # Update event with QR code path
            execute_query(
                "UPDATE events SET qr_code = %s WHERE id = %s",
                (f"uploads/events/{qr_filename}", event_id)
            )
            
            # AUTO-CREATE FORUM FOR EVENT (New feature from prompt)
            forum_id = execute_query('''
                INSERT INTO forums (title, description, creator_id, event_id, is_public)
                VALUES (%s, %s, %s, %s, TRUE)
            ''', (f"{title} - Discussion Forum", 
                  f"Official discussion forum for {title}",
                  session['user_id'], event_id), return_lastrowid=True)
            
            # Add creator as forum admin
            execute_query('''
                INSERT INTO forum_members (forum_id, user_id, role)
                VALUES (%s, %s, 'admin')
            ''', (forum_id, session['user_id']))
            
            # Auto-register creator for the event
            execute_query('''
                INSERT INTO attendance (event_id, user_id, status)
                VALUES (%s, %s, 'registered')
            ''', (event_id, session['user_id']))
            
            flash('Event created successfully! Forum has been created automatically.', 'success')
            return redirect(url_for('events.detail', event_id=event_id))
            
        except Exception as e:
            flash('An error occurred while creating the event.', 'danger')
            print(f"Event creation error: {e}")
    
    return render_template('events/create.html')

@events_bp.route('/<int:event_id>')
def detail(event_id):
    '''View event details'''
    event = execute_query('''
        SELECT e.*, u.full_name as creator_name, u.id as creator_id,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id AND status = 'checked_in') as checked_in_count
        FROM events e
        JOIN users u ON e.creator_id = u.id
        WHERE e.id = %s
    ''', (event_id,), fetch=True, fetchone=True)
    
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events.list_events'))
    
    # Get attendees
    attendees = execute_query('''
        SELECT u.id, u.full_name, u.profile_picture, a.status, a.check_in_time, a.check_out_time
        FROM attendance a
        JOIN users u ON a.user_id = u.id
        WHERE a.event_id = %s
        ORDER BY a.registration_date DESC
    ''', (event_id,), fetch=True) or []
    
    # Check if current user is registered
    is_registered = False
    user_attendance = None
    
    if 'user_id' in session:
        user_attendance = execute_query(
            "SELECT * FROM attendance WHERE event_id = %s AND user_id = %s",
            (event_id, session['user_id']),
            fetch=True,
            fetchone=True
        )
        is_registered = user_attendance is not None
    
    # Get event forum
    forum = execute_query(
        "SELECT * FROM forums WHERE event_id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )
    
    # Check if user is creator or has manage rights
    can_manage = False
    if 'user_id' in session:
        can_manage = (event['creator_id'] == session['user_id'] or 
                     session.get('user_role') in ['system_manager', 'event_manager'])
    
    return render_template('events/detail.html',
                         event=event,
                         attendees=attendees,
                         is_registered=is_registered,
                         user_attendance=user_attendance,
                         forum=forum,
                         can_manage=can_manage)

@events_bp.route('/<int:event_id>/register', methods=['POST'])
@require_login
def register(event_id):
    '''Register for an event'''
    # Check if event exists and is published
    event = execute_query(
        "SELECT * FROM events WHERE id = %s AND status = 'published'",
        (event_id,),
        fetch=True,
        fetchone=True
    )
    
    if not event:
        flash('Event not found or not available for registration.', 'danger')
        return redirect(url_for('events.list_events'))
    
    # Check if already registered
    existing = execute_query(
        "SELECT id FROM attendance WHERE event_id = %s AND user_id = %s",
        (event_id, session['user_id']),
        fetch=True,
        fetchone=True
    )
    
    if existing:
        flash('You are already registered for this event.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Check max attendees
    if event['max_attendees']:
        current_count = execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE event_id = %s",
            (event_id,),
            fetch=True,
            fetchone=True
        )['count']
        
        if current_count >= event['max_attendees']:
            flash('This event has reached maximum capacity.', 'danger')
            return redirect(url_for('events.detail', event_id=event_id))
    
    # Register user
    try:
        execute_query('''
            INSERT INTO attendance (event_id, user_id, status)
            VALUES (%s, %s, 'registered')
        ''', (event_id, session['user_id']))
        
        # Create notification for event creator
        current_app.create_notification(
            event['creator_id'],
            'event_registration',
            'New Event Registration',
            f"{session['user_name']} registered for your event: {event['title']}",
            url_for('events.detail', event_id=event_id)
        )
        
        flash('Successfully registered for the event!', 'success')
        
    except Exception as e:
        flash('An error occurred during registration.', 'danger')
        print(f"Registration error: {e}")
    
    return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/<int:event_id>/unregister', methods=['POST'])
@require_login
def unregister(event_id):
    '''Unregister from an event'''
    try:
        execute_query(
            "DELETE FROM attendance WHERE event_id = %s AND user_id = %s",
            (event_id, session['user_id'])
        )
        
        flash('Successfully unregistered from the event.', 'info')
        
    except Exception as e:
        flash('An error occurred during unregistration.', 'danger')
        print(f"Unregistration error: {e}")
    
    return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@require_login
def edit(event_id):
    '''Edit an event'''
    # Get event
    event = execute_query(
        "SELECT * FROM events WHERE id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )
    
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events.list_events'))
    
    # Check permissions
    if event['creator_id'] != session['user_id'] and session.get('user_role') != 'system_manager':
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('events.detail', event_id=event_id))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'other')
        location = request.form.get('location', '').strip()
        venue = request.form.get('venue', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        max_attendees = request.form.get('max_attendees', '')
        status = request.form.get('status', 'published')
        
        # Handle cover image
        cover_image = event['cover_image']
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename and current_app.allowed_file(file.filename):
                filename = secure_filename(f"event_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'events', filename)
                file.save(filepath)
                cover_image = f"uploads/events/{filename}"
        
        max_attendees = int(max_attendees) if max_attendees else None
        
        # Update event
        try:
            execute_query('''
                UPDATE events 
                SET title = %s, description = %s, category = %s, location = %s, venue = %s,
                    start_date = %s, end_date = %s, max_attendees = %s, cover_image = %s, status = %s
                WHERE id = %s
            ''', (title, description, category, location, venue, start_date, end_date,
                  max_attendees, cover_image, status, event_id))
            
            flash('Event updated successfully!', 'success')
            return redirect(url_for('events.detail', event_id=event_id))
            
        except Exception as e:
            flash('An error occurred while updating the event.', 'danger')
            print(f"Event update error: {e}")
    
    return render_template('events/edit.html', event=event)

@events_bp.route('/<int:event_id>/delete', methods=['POST'])
@require_login
def delete(event_id):
    '''Delete an event'''
    event = execute_query(
        "SELECT creator_id FROM events WHERE id = %s",
        (event_id,),
        fetch=True,
        fetchone=True
    )
    
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events.list_events'))
    
    # Check permissions
    if event['creator_id'] != session['user_id'] and session.get('user_role') != 'system_manager':
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('events.detail', event_id=event_id))
    
    try:
        execute_query("DELETE FROM events WHERE id = %s", (event_id,))
        flash('Event deleted successfully.', 'success')
        return redirect(url_for('events.list_events'))
        
    except Exception as e:
        flash('An error occurred while deleting the event.', 'danger')
        print(f"Event deletion error: {e}")
        return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/my-events')
@require_login
def my_events():
    '''View events created by current user'''
    events = execute_query('''
        SELECT e.*,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id) as total_registered,
               (SELECT COUNT(*) FROM attendance WHERE event_id = e.id AND status = 'checked_in') as checked_in_count
        FROM events e
        WHERE e.creator_id = %s
        ORDER BY e.created_at DESC
    ''', (session['user_id'],), fetch=True) or []
    
    return render_template('events/my_events.html', events=events)