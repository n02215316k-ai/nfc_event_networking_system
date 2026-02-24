import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

# Ndebele/Zimbabwean names for sample data
NDEBELE_NAMES = [
    ("Nkosiyethu", "Dube"),
    ("Thembinkosi", "Ncube"),
    ("Nomusa", "Moyo"),
    ("Siphiwe", "Khumalo"),
    ("Mandla", "Ndlovu"),
    ("Zanele", "Sibanda"),
    ("Mbuso", "Mpofu"),
    ("Lindiwe", "Nkomo")
]

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )

def initialize_database():
    print("=" * 70)
    print("🗄️  NFC Event & Social Network - Database Setup")
    print("=" * 70)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create database
        db_name = os.getenv('DB_NAME', 'nfc_event_social_network')
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"\n✓ Database '{db_name}' created")
        
        cursor.execute(f"USE {db_name}")
        
        # Execute schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        statements = [s.strip() for s in schema_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print("✓ Database schema created")
        
        # Create System Manager with Ndebele name
        admin_email = "admin@eventsocial.zw"
        admin_password = "Admin@123"
        admin_name = "Mandla Ndlovu"
        password_hash = generate_password_hash(admin_password)
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role, is_verified, 
                             current_employment, current_research_area, biography)
            VALUES (%s, %s, %s, 'system_manager', TRUE, 
                    'System Administrator', 'Digital Identity Systems',
                    'System Manager for NFC Event & Social Network Platform')
        ''', (admin_email, password_hash, admin_name))
        admin_id = cursor.lastrowid
        conn.commit()
        
        print(f"\n✓ System Manager created:")
        print(f"  📧 Email: {admin_email}")
        print(f"  🔑 Password: {admin_password}")
        print(f"  👤 Name: {admin_name}")
        
        # Create sample users with Ndebele names
        print("\n📝 Creating sample users...")
        sample_users = []
        
        for i, (first, last) in enumerate(NDEBELE_NAMES[:6]):
            email = f"{first.lower()}.{last.lower()}@eventsocial.zw"
            full_name = f"{first} {last}"
            role = 'event_manager' if i < 2 else 'user'
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, role, 
                                 current_employment, current_research_area, biography)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                email,
                generate_password_hash('password123'),
                full_name,
                role,
                f"{'Event Coordinator' if role == 'event_manager' else 'Researcher'} at University of Zimbabwe",
                f"{'Event Management' if role == 'event_manager' else 'Technology & Innovation'}",
                f"Passionate about community development and technology in Zimbabwe."
            ))
            
            user_id = cursor.lastrowid
            sample_users.append({
                'id': user_id,
                'name': full_name,
                'email': email,
                'role': role
            })
            
            # Assign NFC badge
            nfc_badge = f"NFC{str(user_id).zfill(6)}"
            cursor.execute("UPDATE users SET nfc_badge_id = %s WHERE id = %s", (nfc_badge, user_id))
        
        conn.commit()
        print(f"  ✓ Created {len(sample_users)} sample users")
        
        # Create sample events
        print("\n📅 Creating sample events...")
        event_ids = []
        
        events_data = [
            ("Zimbabwe Tech Summit 2026", "Annual technology conference bringing together innovators across Zimbabwe", 
             "technology", "Harare", "Rainbow Towers Hotel"),
            ("Healthcare Innovation Workshop", "Exploring digital health solutions for rural communities",
             "healthcare", "Bulawayo", "Bulawayo Conference Centre"),
            ("Education Technology Symposium", "Transforming education through technology in Zimbabwe",
             "education", "Harare", "University of Zimbabwe")
        ]
        
        from datetime import datetime, timedelta
        
        for i, (title, desc, cat, loc, venue) in enumerate(events_data):
            start_date = datetime.now() + timedelta(days=15 + i*7)
            end_date = start_date + timedelta(hours=8)
            creator_id = sample_users[i % 2]['id']  # Rotate between event managers
            
            cursor.execute('''
                INSERT INTO events (title, description, category, location, venue,
                                  start_date, end_date, creator_id, status, max_attendees)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'published', %s)
            ''', (title, desc, cat, loc, venue, start_date, end_date, creator_id, 150))
            
            event_id = cursor.lastrowid
            event_ids.append(event_id)
            
            # Create forum for event
            cursor.execute('''
                INSERT INTO forums (title, description, creator_id, event_id, is_public)
                VALUES (%s, %s, %s, %s, TRUE)
            ''', (f"{title} - Discussion Forum", f"Forum for {title}", creator_id, event_id))
            
            forum_id = cursor.lastrowid
            
            # Add creator as forum admin
            cursor.execute('''
                INSERT INTO forum_members (forum_id, user_id, role)
                VALUES (%s, %s, 'admin')
            ''', (forum_id, creator_id))
        
        conn.commit()
        print(f"  ✓ Created {len(event_ids)} events with forums")
        
        # Create independent forum
        cursor.execute('''
            INSERT INTO forums (title, description, creator_id, is_public)
            VALUES ('Zimbabwe Developers Community', 
                    'A community for developers and tech enthusiasts in Zimbabwe',
                    %s, TRUE)
        ''', (sample_users[0]['id'],))
        
        forum_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO forum_members (forum_id, user_id, role)
            VALUES (%s, %s, 'admin')
        ''', (forum_id, sample_users[0]['id']))
        
        conn.commit()
        print("  ✓ Created independent forum")
        
        print("\n" + "=" * 70)
        print("✅ Database initialization complete!")
        print("=" * 70)
        
        print("\n📝 Sample Accounts:")
        print(f"\n👑 System Manager:")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        
        print(f"\n🎫 Event Managers:")
        for user in sample_users[:2]:
            print(f"   {user['name']}: {user['email']} / password123")
        
        print(f"\n👤 Regular Users:")
        for user in sample_users[2:4]:
            print(f"   {user['name']}: {user['email']} / password123")
        
        print("\n⚠️  CHANGE ALL PASSWORDS AFTER FIRST LOGIN!")
        
        print("\n📋 Next steps:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your MySQL password")
        print("3. Run: python run.py")
        print("4. Visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()