# filepath: c:\\Users\\lenovo\\Downloads\\nfc\\utils\\qr_generator.py

import qrcode
import os
from io import BytesIO
import base64
from flask import request

def get_base_url():
    '''
    Get the base URL dynamically from the request context
    Falls back to localhost if not in request context
    '''
    try:
        # Get scheme (http/https)
        scheme = request.scheme
        # Get host (domain:port)
        host = request.host
        return f"{scheme}://{host}"
    except:
        # Fallback for when not in request context
        return "http://localhost:5000"


def generate_profile_qr(user_id, base_url=None):
    '''
    Generate QR code for user profile
    
    Args:
        user_id: User ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, profile_url)
    '''
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Create profile URL with dynamic domain
    profile_url = f"{base_url}/profile/view/{user_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    qr_dir = "static/qr_codes"
    os.makedirs(qr_dir, exist_ok=True)
    
    filename = f"user_{user_id}_qr.png"
    filepath = os.path.join(qr_dir, filename)
    
    img.save(filepath)
    
    # Return both file path and URL path
    return filepath, f"/static/qr_codes/{filename}", profile_url


def generate_event_qr(event_id, base_url=None):
    '''
    Generate QR code for event check-in
    
    Args:
        event_id: Event ID
        base_url: Base URL (auto-detected if None)
        
    Returns:
        tuple: (qr_code_path, qr_code_url, event_url)
    '''
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Create event URL with dynamic domain
    event_url = f"{base_url}/events/{event_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(event_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    qr_dir = "static/qr_codes/events"
    os.makedirs(qr_dir, exist_ok=True)
    
    filename = f"event_{event_id}_qr.png"
    filepath = os.path.join(qr_dir, filename)
    
    img.save(filepath)
    
    return filepath, f"/static/qr_codes/events/{filename}", event_url


def generate_qr_base64(data):
    '''
    Generate QR code as base64 string (for inline display)
    
    Args:
        data: Data to encode in QR
        
    Returns:
        str: Base64 encoded QR code image
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def verify_qr_data(qr_data, base_url=None):
    '''
    Verify and extract information from QR code data
    Works with any domain (localhost, production, etc.)
    
    Args:
        qr_data: Scanned QR code data
        base_url: Base URL (auto-detected if None)
        
    Returns:
        dict: Extracted information (type, id, url)
    '''
    # Auto-detect base URL if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Handle both with and without base URL
    if not qr_data.startswith('http'):
        # Assume it's a relative path
        qr_data = base_url + qr_data
    
    # Extract path from URL (works with any domain)
    try:
        from urllib.parse import urlparse
        parsed = urlparse(qr_data)
        path = parsed.path
    except:
        # Fallback: simple string manipulation
        if '://' in qr_data:
            path = qr_data.split('://', 1)[1]
            if '/' in path:
                path = '/' + path.split('/', 1)[1]
            else:
                path = '/'
        else:
            path = qr_data
    
    # Parse URL path (domain-agnostic)
    if "/profile/view/" in path:
        user_id = path.split("/profile/view/")[1].split("/")[0].split("?")[0]
        try:
            return {
                'type': 'profile',
                'user_id': int(user_id),
                'url': qr_data
            }
        except ValueError:
            return None
    elif "/events/" in path:
        event_id = path.split("/events/")[1].split("/")[0].split("?")[0]
        try:
            return {
                'type': 'event',
                'event_id': int(event_id),
                'url': qr_data
            }
        except ValueError:
            return None
    
    return None


def update_user_qr_url(user_id):
    '''
    Update user's QR code URL in database with current domain
    
    Args:
        user_id: User ID
    '''
    from database import get_db_connection
    
    base_url = get_base_url()
    profile_url = f"{base_url}/profile/view/{user_id}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE users SET qr_code_url = %s WHERE id = %s",
            (profile_url, user_id)
        )
        conn.commit()
        return profile_url
    except Exception as e:
        print(f"Error updating QR URL: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
