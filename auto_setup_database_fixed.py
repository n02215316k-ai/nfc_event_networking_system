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

def execute_sql_file(cursor, connection, filepath):
    """Execute SQL file properly"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Remove comments and empty lines
        lines = []
        for line in sql_content.split('\n'):
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('--') and not line.startswith('/*'):
                lines.append(line)
        
        sql_content = ' '.join(lines)
        
        # Split by semicolon but be careful with delimiters
        statements = []
        current_statement = []
        in_delimiter = False
        
        for part in sql_content.split(';'):
            part = part.strip()
            if not part:
                continue
                
            # Check for DELIMITER statements
            if 'DELIMITER' in part.upper():
                if '$$' in part:
                    in_delimiter = True
                    continue
                else:
                    in_delimiter = False
                    if current_statement:
                        statements.append(' '.join(current_statement))
                        current_statement = []
                    continue
            
            if in_delimiter:
                current_statement.append(part)
                if '$$' in part:
                    # End of delimiter block
                    stmt = ' '.join(current_statement).replace('$$', '')
                    if stmt.strip():
                        statements.append(stmt)
                    current_statement = []
                    in_delimiter = False
            else:
                if part.strip():
                    statements.append(part)
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            statement = statement.strip()
            if statement:
                try:
                    # Execute the statement
                    for result in cursor.execute(statement, multi=True):
                        pass
                    connection.commit()
                    print_success(f"Executed statement {i}/{len(statements)}")
                except Error as e:
                    error_msg = str(e).lower()
                    # Ignore certain errors
                    if "already exists" in error_msg or "duplicate" in error_msg:
                        print_info(f"Skipping: {error_msg[:50]}...")
                    else:
                        print_error(f"SQL Error in statement {i}: {e}")
                        print(f"Statement: {statement[:100]}...")
        
        return True
    except Exception as e:
        print_error(f"Error reading SQL file: {e}")
        import traceback
        traceback.print_exc()
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
    db_name = os.getenv('DB_NAME', 'nfc_event_management')
    
    print_info(f"Database Host: {db_host}")
    print_info(f"Database User: {db_user}")
    print_info(f"Database Name: {db_name}\n")
    
    connection = None
    cursor = None
    
    try:
        # Connect to MySQL (without database)
        print_info("Connecting to MySQL server...")
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            autocommit=False
        )
        
        if connection.is_connected():
            print_success("Connected to MySQL server")
            cursor = connection.cursor()
            
            # Create database
            print_info(f"Creating database '{db_name}'...")
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print_success(f"Database '{db_name}' created")
            
            # Close and reconnect to the new database
            cursor.close()
            connection.close()
            
            print_info(f"Connecting to database '{db_name}'...")
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                autocommit=False
            )
            cursor = connection.cursor()
            print_success(f"Connected to database '{db_name}'")
            
            # Execute schema SQL file
            schema_file = 'database/schema.sql'
            if os.path.exists(schema_file):
                print_info("Executing schema.sql...")
                if execute_sql_file(cursor, connection, schema_file):
                    print_success("Database schema created successfully")
                else:
                    print_error("Failed to create database schema")
                    return False
            else:
                print_error(f"Schema file not found: {schema_file}")
                return False
            
            # Verify tables were created
            print_info("Verifying tables...")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if len(tables) == 0:
                print_error("No tables created! Schema execution failed.")
                return False
            
            print_success(f"{len(tables)} tables created:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Insert default system manager
            print_info("\nCreating default system manager...")
            
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
            
            return True
            
    except Error as e:
        print_error(f"MySQL Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print_info("Database connection closed")

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
        print_info("Please ensure database folder and schema.sql exist")
        sys.exit(1)
    
    success = setup_database()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)