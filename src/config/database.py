import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    '''Database connection manager with connection pooling'''
    
    def __init__(self):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="nfc_social_pool",
                pool_size=10,
                pool_reset_session=True,
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'nfc_event_social_network'),
                autocommit=False
            )
            print("✓ Database connection pool created")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False, fetchone=False, return_lastrowid=False):
        '''Execute a database query'''
        conn = None
        cursor = None
        
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchone() if fetchone else cursor.fetchall()
                return result
            
            conn.commit()
            
            if return_lastrowid:
                return cursor.lastrowid
            
            return True
            
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            print(f"Database Error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_many(self, query, params_list):
        '''Execute multiple queries with different parameters'''
        conn = None
        cursor = None
        
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            
            cursor.executemany(query, params_list)
            conn.commit()
            
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Database Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Create global database instance
db = Database()