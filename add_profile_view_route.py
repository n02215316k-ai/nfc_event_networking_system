import os

print("=" * 80)
print("🔧 ADDING PROFILE VIEW ROUTE")
print("=" * 80)

profile_path = "src/controllers/profile_controller.py"

with open(profile_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if view_user_profile exists
if "def view_user_profile(" in content:
    print("✅ view_user_profile() function exists")
else:
    print("❌ view_user_profile() function is MISSING - Adding it now...")
    
    # Find insertion point (after imports, before other routes)
    insert_point = content.find("\n\n@profile_bp.route")
    
    if insert_point == -1:
        # No routes yet, add after blueprint definition
        insert_point = content.find("profile_bp = Blueprint")
        insert_point = content.find("\n", insert_point) + 1
    
    view_route = """

@profile_bp.route('/view/<int:user_id>')
def view_user_profile(user_id):
    '''View any user's profile (public)'''
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get user details
        cursor.execute('''
            SELECT id, full_name, email, profile_picture, bio, 
                   qr_code_url, created_at
            FROM users 
            WHERE id = %s
        ''', (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('home.index'))
        
        # Check if viewing own profile
        is_own_profile = False
        if 'user_id' in session:
            is_own_profile = (session['user_id'] == user_id)
        
        # Get upcoming events
        cursor.execute('''
            SELECT e.* 
            FROM events e
            JOIN event_registrations er ON e.id = er.event_id
            WHERE er.user_id = %s AND e.date >= CURDATE()
            ORDER BY e.date ASC
            LIMIT 5
        ''', (user_id,))
        
        upcoming_events = cursor.fetchall()
        
        # Check if connected
        is_connected = False
        if 'user_id' in session and not is_own_profile:
            cursor.execute('''
                SELECT id FROM scan_history 
                WHERE scanner_id = %s AND scanned_user_id = %s
            ''', (session['user_id'], user_id))
            is_connected = cursor.fetchone() is not None
        
        return render_template('profile/view.html',
                             user=user,
                             upcoming_events=upcoming_events,
                             is_own_profile=is_own_profile,
                             is_connected=is_connected)
    
    except Exception as e:
        print(f"Error viewing profile: {e}")
        flash('Error loading profile', 'error')
        return redirect(url_for('home.index'))
    
    finally:
        cursor.close()
        conn.close()
"""
    
    content = content[:insert_point] + view_route + content[insert_point:]
    
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added view_user_profile() route")

# Check for /me route
if "@profile_bp.route('/me')" in content:
    print("✅ /profile/me route exists")
else:
    print("⚠️  /profile/me route is MISSING - Adding it now...")
    
    # Find insertion point
    insert_point = content.find("\n\n@profile_bp.route")
    
    if insert_point == -1:
        insert_point = content.find("profile_bp = Blueprint")
        insert_point = content.find("\n", insert_point) + 1
    
    me_route = """

@profile_bp.route('/me')
def me():
    '''Redirect to current user's profile'''
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('profile.view_user_profile', user_id=session['user_id']))
"""
    
    content = content[:insert_point] + me_route + content[insert_point:]
    
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added /profile/me route")

print("\n" + "=" * 80)
print("✅ ROUTES ADDED")
print("=" * 80)

print("""
🚀 Routes Available:
  • /profile/me                - Your profile (redirects to /view/<id>)
  • /profile/view/<user_id>    - View any user's profile
  • /profile/qr                - Your QR code
  • /profile/edit              - Edit profile

🔧 Now restart: python app.py
""")