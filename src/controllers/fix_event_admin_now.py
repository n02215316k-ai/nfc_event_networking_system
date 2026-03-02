file_path = 'src/controllers/event_admin_controller.py'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the broken section
broken_code = """    
    
        # Calculate attendance statistics
        cursor.execute("""

fixed_code = """    
    # Calculate attendance statistics
    attendance_stats = execute_query("""

content = content.replace(broken_code, fixed_code)

# Also fix the return statement that's misaligned
broken_return = """        
        attendance_data = cursor.fetchone()
        attendance_stats = {
            'total_registered': attendance_data['total_registered'] or 0,
            'total_checked_in': attendance_data['total_checked_in'] or 0
        }
        
        return render_template('event_admin/reports.html',
                             attendance_stats=attendance_stats,"""

fixed_return = """    """, (event_id,), fetch=True, fetchone=True) or {
        'total_registered': 0,
        'total_checked_in': 0
    }
    
    return render_template('event_admin/reports.html',
                         attendance_stats=attendance_stats,"""

content = content.replace(broken_return, fixed_return)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed! Now run: python app.py")