"""
Database Configuration and Connection Management
"""
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the project root (parent directory of applications)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("⚠️  Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Falling back to environment variables or defaults")

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'cs631_company_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': int(os.getenv('DB_PORT', 5432))
}

# Connection pool
connection_pool = None

def initialize_connection_pool():
    """Initialize the database connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            **DB_CONFIG
        )
        if connection_pool:
            print("✓ Database connection pool created successfully")
    except Exception as e:
        print(f"✗ Error creating connection pool: {e}")
        raise

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    if connection_pool is None:
        raise RuntimeError(
            "Database connection pool not initialized. "
            "Call initialize_connection_pool() first."
        )
    connection = connection_pool.getconn()
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection_pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=True):
    """Context manager for database cursors"""
    with get_db_connection() as connection:
        cursor = connection.cursor()
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

def close_connection_pool():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("✓ Database connection pool closed")

def test_connection():
    """Test database connection"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✓ Database connection successful")
            print(f"  PostgreSQL version: {version[0]}")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
