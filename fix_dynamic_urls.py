# filepath: fix_dynamic_urls.py

print("=" * 80)
print("🔧 FIXING DYNAMIC URL IMPLEMENTATION")
print("=" * 80)

# Fix 1: Update profile controller
profile_path = 'src/controllers/profile_controller.py'
with open(profile_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure dynamic URL generation in view_user_profile
if "request.url_root" not in content:
    print("\n1️⃣ Fixing profile controller...")
    
    # Find the view_user_profile function
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def view_user_profile(user_id):' in line:
            # Find where to add dynamic URL code
            for j in range(i, min(i+150, len(lines))):
                if 'return render_template' in lines[j]:
                    # Add dynamic URL code before return
                    indent = '    '
                    url_code = f"""
{indent}# Generate dynamic profile URL
{indent}profile_url = request.url_root.rstrip('/') + url_for('profile.view_user_profile', user_id=user['id'])
{indent}
{indent}# Generate QR code with dynamic URL
{indent}qr = qrcode.QRCode(version=1, box_size=10, border=5)
{indent}qr.add_data(profile_url)
{indent}qr.make(fit=True)
{indent}
{indent}img = qr.make_image(fill_color="black", back_color="white")
{indent}buffer = BytesIO()
{indent}img.save(buffer, format='PNG')
{indent}qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
{indent}"""
                    lines.insert(j, url_code)
                    break
            break
    
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("   ✅ Profile controller updated!")

print("\n✅ ALL FIXES APPLIED!")
print("\n🔄 Restart Flask: python app.py")
