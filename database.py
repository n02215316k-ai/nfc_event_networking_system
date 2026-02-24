import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # No password
    'database': 'nfc_event_management',  # Your actual database
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

def get_db_connection():
    """
    Create and return a MySQL database connection
    """
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset=DB_CONFIG['charset']
        )
        
        if connection.is_connected():
            return connection
        else:
            print("Failed to connect to database")
            return None
            
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def test_connection():
    """
    Test database connection
    """
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"✓ Connected to database: {db_name[0]}")
            cursor.close()
            conn.close()
            return True
        else:
            print("✗ Connection failed")
            return False
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Test connection when run directly
    print("Testing database connection...")
    test_connection()