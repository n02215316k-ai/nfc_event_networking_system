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


admin_bp = Blueprint('admin', __name__)

def require_admin():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'system_manager']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    return None

@admin_bp.route('/dashboard')
def system_dashboard():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    stats = {
        'total_users': execute_query("SELECT COUNT(*) as count FROM users", fetch=True, fetchone=True)['count'],
        'total_events': execute_query("SELECT COUNT(*) as count FROM events", fetch=True, fetchone=True)['count'],
        'pending_verifications': execute_query("SELECT COUNT(*) as count FROM documents WHERE status = 'pending'", fetch=True, fetchone=True)['count']
    }
    
    users = execute_query("SELECT * FROM users ORDER BY created_at DESC LIMIT 10", fetch=True) or []
    
    return render_template('admin/dashboard.html', stats=stats, users=users)

@admin_bp.route('/users')
def manage_users():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    users = execute_query("SELECT * FROM users ORDER BY created_at DESC", fetch=True) or []
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/documents')
def verify_documents():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    pending_docs = execute_query("""
        SELECT d.*, u.full_name as user_name, u.email
        FROM documents d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.submitted_at ASC
    """, fetch=True) or []
    
    verified_docs = execute_query("""
        SELECT d.*, u.full_name as user_name, v.full_name as verifier_name
        FROM documents d
        JOIN users u ON d.user_id = u.id
        LEFT JOIN users v ON d.verified_by = v.id
        WHERE d.status IN ('verified', 'rejected')
        ORDER BY d.verified_at DESC
        LIMIT 20
    """, fetch=True) or []
    
    return render_template('admin/documents.html', pending_docs=pending_docs, verified_docs=verified_docs)
