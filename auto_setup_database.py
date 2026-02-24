import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ{Colors.END} {text}")

def execute_sql_file(cursor, filepath):
    """Execute SQL file with multiple statements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolon and execute each statement
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    # Ignore "already exists" errors
                    if "already exists" not in str(e).lower():
                        print_error(f"SQL Error: {e}")
        
        return True
    except Exception as e:
        print_error(f"Error reading SQL file: {e}")
        return False

def setup_database():
    """Complete database setup"""
    print_header("🗄️  NFC Event System - Database Setup")
    
    # Load environment variables
    load_dotenv()
    
    # Get database credentials
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'nfc_event_system')
    
    print_info(f"Database Host: {db_host}")
    print_info(f"Database User: {db_user}")
    print_info(f"Database Name: {db_name}\n")
    
    try:
        # Connect to MySQL (without database)
        print_info("Connecting to MySQL server...")
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            print_success("Connected to MySQL server")
            cursor = connection.cursor()
            
            # Create database
            print_info(f"Creating database '{db_name}'...")
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print_success(f"Database '{db_name}' created")
            
            # Use the database
            cursor.execute(f"USE {db_name}")
            connection.database = db_name
            
            # Execute schema SQL file
            schema_file = 'database/schema.sql'
            if os.path.exists(schema_file):
                print_info("Executing schema.sql...")
                if execute_sql_file(cursor, schema_file):
                    print_success("Database schema created")
                    connection.commit()
            else:
                print_error(f"Schema file not found: {schema_file}")
                return False
            
            # Insert default system manager
            print_info("Creating default system manager...")
            
            from werkzeug.security import generate_password_hash
            
            password_hash = generate_password_hash('admin123')
            
            cursor.execute('''
                INSERT INTO users (full_name, email, password_hash, role, is_verified, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            ''', ('System Manager', 'admin@nfcevents.com', password_hash, 'system_manager', 1))
            
            admin_id = cursor.lastrowid
            connection.commit()
            
            print_success("System manager created!")
            
            # Create sample users
            print_info("Creating sample users...")
            
            sample_users = [
                ('Thabo Ncube', 'thabo@nfcevents.com', 'user', 'University of Zimbabwe'),
                ('Nokuthula Dube', 'nokuthula@nfcevents.com', 'user', 'Harare Institute of Technology'),
                ('Mpilo Moyo', 'mpilo@nfcevents.com', 'user', 'National University of Science & Technology'),
            ]
            
            user_password = generate_password_hash('user123')
            
            for full_name, email, role, employment in sample_users:
                cursor.execute('''
                    INSERT INTO users (full_name, email, password_hash, role, current_employment, is_verified, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ''', (full_name, email, user_password, role, employment, 1))
            
            connection.commit()
            print_success(f"{len(sample_users)} sample users created")
            
            # Create sample event
            print_info("Creating sample event...")
            
            cursor.execute('''
                INSERT INTO events (
                    title, description, category, location, venue,
                    start_date, end_date, max_attendees, creator_id, status, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ''', (
                'Zimbabwe Tech Summit 2026',
                'Annual technology and innovation summit bringing together tech enthusiasts, entrepreneurs, and researchers from across Zimbabwe.',
                'conference',
                'Harare, Zimbabwe',
                'Rainbow Towers Hotel',
                '2026-03-15 09:00:00',
                '2026-03-17 17:00:00',
                500,
                admin_id,
                'published'
            ))
            
            event_id = cursor.lastrowid
            connection.commit()
            print_success("Sample event created")
            
            # Create event forum
            cursor.execute('''
                INSERT INTO forums (title, description, creator_id, event_id, is_public, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            ''', (
                'Zimbabwe Tech Summit Discussion',
                'Official discussion forum for Zimbabwe Tech Summit 2026',
                admin_id,
                event_id,
                1
            ))
            
            connection.commit()
            print_success("Event forum created")
            
            # Print summary
            print_header("✅ Database Setup Complete!")
            
            print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
            print(f"{Colors.GREEN}Default Credentials:{Colors.END}")
            print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
            print(f"\n{Colors.CYAN}System Manager:{Colors.END}")
            print(f"  Email:    admin@nfcevents.com")
            print(f"  Password: admin123")
            
            print(f"\n{Colors.CYAN}Sample Users:{Colors.END}")
            print(f"  Email:    thabo@nfcevents.com")
            print(f"  Password: user123")
            
            print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
            print(f"{Colors.GREEN}Next Steps:{Colors.END}")
            print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
            print(f"\n1. Install dependencies:")
            print(f"   pip install -r requirements.txt")
            print(f"\n2. Run the application:")
            print(f"   python app.py")
            print(f"\n3. Access at:")
            print(f"   http://localhost:5000")
            print()
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print_error(f"MySQL Error: {e}")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Check if .env exists
    if not os.path.exists('.env'):
        print_error(".env file not found!")
        print_info("Creating .env file from .env.example...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print_success(".env file created")
            print()
            print(f"{Colors.YELLOW}⚠️  IMPORTANT:{Colors.END}")
            print(f"Please edit .env file and set your database password!")
            print(f"Then run this script again.")
            sys.exit(1)
        else:
            print_error(".env.example file not found!")
            sys.exit(1)
    
    # Check if schema.sql exists
    if not os.path.exists('database/schema.sql'):
        print_error("database/schema.sql not found!")
        print_info("Please run the setup scripts in order:")
        print("  1. python auto_setup_part1.py")
        print("  2. python auto_setup_part2.py")
        print("  3. python auto_setup_part3.py")
        sys.exit(1)
    
    success = setup_database()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)