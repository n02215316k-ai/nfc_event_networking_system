# filepath: c:\Users\lenovo\Downloads\nfc\src\controllers\groups.py
from flask import Blueprint, render_template, redirect, url_for, session, flash
from database import get_db_connection

group_bp = Blueprint('group', __name__, url_prefix='/groups')

@group_bp.route('/')
def list_groups():
    """List all groups"""
    groups = db.execute_query("""
        SELECT g.*, u.full_name as creator_name,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.is_private = FALSE
        ORDER BY g.created_at DESC
    """, fetch=True) or []
    
    return render_template('groups/list.html', groups=groups)

@group_bp.route('/<int:group_id>')
def view_group(group_id):
    """View group details"""
    group = db.execute_query("""
        SELECT g.*, u.full_name as creator_name
        FROM groups g
        JOIN users u ON g.creator_id = u.id
        WHERE g.id = %s
    """, (group_id,), fetch=True, fetchone=True)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('group.list_groups'))
    
    members = db.execute_query("""
        SELECT u.*, gm.role
        FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = %s
    """, (group_id,), fetch=True) or []
    
    return render_template('groups/view.html', group=group, members=members)
