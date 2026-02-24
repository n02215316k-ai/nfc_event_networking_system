from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection


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


group_bp = Blueprint('group', __name__)

@group_bp.route('/')
def list_groups():
    groups = execute_query("""
        SELECT g.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        ORDER BY g.created_at DESC
    """, fetch=True) or []
    
    return render_template('groups/list.html', groups=groups)

@group_bp.route('/<int:group_id>')
def view_group(group_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    group = execute_query("""
        SELECT g.*, u.full_name as creator_name
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.id = %s
    """, (group_id,), fetch=True, fetchone=True)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('group.list_groups'))
    
    is_member = execute_query(
        "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
        (group_id, session['user_id']), fetch=True, fetchone=True
    ) is not None
    
    members = execute_query("""
        SELECT u.*, gm.role
        FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = %s
    """, (group_id,), fetch=True) or []
    
    return render_template('groups/view.html', group=group, is_member=is_member, members=members)
