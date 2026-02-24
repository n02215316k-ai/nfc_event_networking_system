from flask import Blueprint, render_template, redirect, url_for, session, flash
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


user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>')
def view_profile(user_id):
    user = execute_query(
        "SELECT * FROM users WHERE id = %s",
        (user_id,), fetch=True, fetchone=True
    )
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    
    followers_count = execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE following_id = %s",
        (user_id,), fetch=True, fetchone=True
    )['count']
    
    following_count = execute_query(
        "SELECT COUNT(*) as count FROM followers WHERE follower_id = %s",
        (user_id,), fetch=True, fetchone=True
    )['count']
    
    is_following = False
    if 'user_id' in session:
        follow = execute_query(
            "SELECT * FROM followers WHERE follower_id = %s AND following_id = %s",
            (session['user_id'], user_id), fetch=True, fetchone=True
        )
        is_following = follow is not None
    
    return render_template('users/profile.html', 
                         user=user, 
                         followers_count=followers_count,
                         following_count=following_count,
                         is_following=is_following)
