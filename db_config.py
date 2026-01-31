"""
Database Configuration Module
Handles MySQL database connection settings and connection pooling
"""
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, pooling
from typing import Optional
import os 

load_dotenv()

SQLPASS = os.getenv("SQLPASS")

class DatabaseConfig:
    """Database configuration and connection management"""
    
    # Database connection parameters
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',  # Change this to your MySQL username
        'password': SQLPASS,
        'database': 'budget_tracker',
        'port': 3306
    }
    
    # Connection pool
    _connection_pool: Optional[pooling.MySQLConnectionPool] = None
    
    @classmethod
    def initialize_pool(cls, pool_name: str = "budget_pool", pool_size: int = 5):
        """Initialize connection pool"""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                **cls.DB_CONFIG
            )
            print("Connection pool initialized successfully")
        except Error as e:
            print(f"Error initializing connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        
        try:
            return cls._connection_pool.get_connection()
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            raise
    
    @classmethod
    def close_pool(cls):
        """Close all connections in the pool"""
        if cls._connection_pool:
            # Connection pools don't have a direct close method
            # Connections are returned to the pool automatically
            cls._connection_pool = None
            print("Connection pool closed")

def get_db_connection():
    """Helper function to get a database connection"""
    return DatabaseConfig.get_connection()

def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """
    Execute a SQL query with optional parameters
    
    Args:
        query: SQL query string
        params: Query parameters as tuple
        fetch: If True, fetch and return results
    
    Returns:
        Query results if fetch=True, otherwise None
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
            
    except Error as e:
        if connection:
            connection.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
