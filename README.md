# NFC Event & Social Network System

A comprehensive event management and social networking platform with NFC/QR code scanning capabilities.

## Features

✅ **User Authentication & Profiles**
- User registration and login
- Profile management with qualifications
- Document verification system
- Follow/unfollow users

✅ **Event Management**
- Create and manage events
- NFC/QR code check-in/check-out
- Event registration and attendance tracking
- Automatic forum creation for events

✅ **Social Networking**
- User profiles with biography
- Follow/unfollow system
- Direct messaging
- Discussion forums

✅ **Forum System**
- Create public/private forums
- Post and reply to discussions
- Forum moderators
- File attachments

✅ **NFC/QR Scanning**
- Event check-in/check-out
- Networking mode for profile viewing
- Real-time attendance tracking

✅ **System Management**
- Admin dashboard
- User management
- Event analytics
- Document verification
- System reports

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd nfc-event-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**
```bash
mysql -u root -p < config/schema.sql
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
```
http://localhost:5000
```

## Default Credentials

**System Manager:**
- Email: admin@nfcevents.com
- Password: admin123

## Project Structure

```
nfc-event-system/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   ├── database.py            # Database connection
│   └── schema.sql             # Database schema
├── src/
│   ├── controllers/           # Application controllers
│   └── utils/                 # Utility functions
├── templates/                 # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── events/
│   ├── profile/
│   ├── forum/
│   ├── messaging/
│   ├── nfc/
│   └── system_manager/
└── static/
    ├── uploads/               # User uploads
    └── qrcodes/              # Generated QR codes
```

## Technologies Used

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** Bootstrap 5, jQuery
- **Icons:** Font Awesome
- **QR Codes:** qrcode library

## License

MIT License

## Support

For support, email support@nfcevents.com