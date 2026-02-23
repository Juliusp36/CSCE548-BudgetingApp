"""
Database Configuration Module
Handles MySQL database connection settings and connection pooling
"""

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, pooling
from typing import Optional
import os
from urllib.parse import urlparse

load_dotenv()

# ==============================
# Railway MySQL Public URL Logic
# ==============================

DATABASE_URL = os.getenv("MYSQL_PUBLIC_URL")

if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    parsed = urlparse(DATABASE_URL)

    DB_CONFIG = {
        'host': parsed.hostname,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
        'port': parsed.port or 3306
    }
else:
    # Fallback to manual env vars (for local or Render)
    DB_CONFIG = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_NAME"),
        'port': int(os.getenv("DB_PORT", 3306))
    }


class DatabaseConfig:
    """Database configuration and connection management"""

    DB_CONFIG = DB_CONFIG
    _connection_pool: Optional[pooling.MySQLConnectionPool] = None

    @classmethod
    def initialize_pool(cls, pool_name: str = "budget_pool", pool_size: int = 5):
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
        if cls._connection_pool is None:
            cls.initialize_pool()

        try:
            return cls._connection_pool.get_connection()
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            raise

    @classmethod
    def close_pool(cls):
        if cls._connection_pool:
            cls._connection_pool = None
            print("Connection pool closed")


def get_db_connection():
    return DatabaseConfig.get_connection()


def execute_query(query: str, params: tuple = None, fetch: bool = False):
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
            return cursor.fetchall()
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