import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'nfc_event_management')
        self.connection = None
    
    def connect(self):
        """Create database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=True
                )
            return self.connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False, fetchone=False, return_lastrowid=False):
        """Execute a database query"""
        try:
            connection = self.connect()
            if connection is None:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                if fetchone:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
                cursor.close()
                return result
            
            # For INSERT, UPDATE, DELETE
            if return_lastrowid:
                lastrowid = cursor.lastrowid
                cursor.close()
                return lastrowid
            
            lastrowid = cursor.lastrowid
            cursor.close()
            return lastrowid
            
        except Error as e:
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            return None
    
    def insert(self, query, params=None):
        """Insert and return last insert id"""
        return self.execute_query(query, params)
    
    def update(self, query, params=None):
        """Update records"""
        return self.execute_query(query, params)
    
    def delete(self, query, params=None):
        """Delete records"""
        return self.execute_query(query, params)
    
    def select(self, query, params=None, fetchone=False):
        """Select records"""
        return self.execute_query(query, params, fetch=True, fetchone=fetchone)
    
    def select_one(self, query, params=None):
        """Select one record"""
        return self.execute_query(query, params, fetch=True, fetchone=True)
    
    def select_all(self, query, params=None):
        """Select all records"""
        return self.execute_query(query, params, fetch=True, fetchone=False)
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Create a global database instance
db = Database()