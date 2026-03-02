# DEPLOYMENT CONFIGURATION GUIDE

## 🌐 Dynamic URL Configuration

This system now automatically detects the domain it's running on.
No configuration needed for localhost vs production!

### How It Works:

1. **QR Code Generation**: Uses Flask request context
   - Localhost: http://localhost:5000/profile/view/123
   - Production: https://yourdomain.com/profile/view/123

2. **QR Code Verification**: Domain-agnostic parsing
   - Extracts user ID from any domain
   - Works with http/https
   - Works with any port

3. **Frontend**: Uses window.location.origin
   - Automatically matches current domain
   - Works in any environment

### Deployment Checklist:

#### For Production Deployment:

1. **Environment Variables**:
   Create a .env file or set environment variables:
   
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key
   MYSQL_HOST=your-db-host
   MYSQL_USER=your-db-user
   MYSQL_PASSWORD=your-db-password
   MYSQL_DATABASE=your-db-name

2. **HTTPS Configuration**:
   - Ensure your server uses HTTPS in production
   - Flask will auto-detect scheme (http/https)

3. **Regenerate QR Codes** (if migrating from localhost):
   
   # For production domain
   python regenerate_all_qr_codes.py https://yourdomain.com
   
   # For localhost (default)
   python regenerate_all_qr_codes.py

4. **Test URLs**:
   - Visit: https://yourdomain.com/profile/qr
   - Scan QR code
   - Should redirect to: https://yourdomain.com/profile/view/[id]

### Supported Deployment Platforms:

✅ **Heroku**:
   - Automatic domain detection
   - Use environment variables for DB config
   - Add gunicorn to requirements.txt

✅ **AWS / Azure / GCP**:
   - Configure load balancer for HTTPS
   - Set environment variables
   - Use managed database service

✅ **VPS (DigitalOcean, Linode, etc.)**:
   - Configure nginx/apache for HTTPS
   - Set domain in DNS
   - System auto-detects domain

✅ **Docker**:
   - Use environment variables
   - Map ports correctly
   - System adapts to container's domain

### Testing:

# Test on localhost
python app.py
# QR codes will use: http://localhost:5000

# Test on production
# QR codes will use: https://yourdomain.com

### No Configuration Needed! 🎉

The system automatically adapts to whatever domain it's running on.
Just deploy and it works!

### Troubleshooting:

**QR codes still show localhost after deployment:**
   Run: python regenerate_all_qr_codes.py https://yourdomain.com

**Mixed content errors (http/https):**
   Ensure your server is properly configured for HTTPS

**Domain detection not working:**
   Check that Flask can access request.scheme and request.host
