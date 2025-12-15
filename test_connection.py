#!/usr/bin/env python3
"""
Simple script to test database configuration and connection
"""
import sys
import os

# Add applications directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'applications'))

print("="*70)
print("DATABASE CONNECTION TEST")
print("="*70)

# Step 1: Check if .env file exists
print("\n1. Checking for .env file...")
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    print(f"   ✓ Found .env file at: {env_file}")
else:
    print(f"   ✗ .env file not found at: {env_file}")
    print("   Create it by copying .env.example:")
    print("   cp .env.example .env")

# Step 2: Check python-dotenv
print("\n2. Checking python-dotenv...")
try:
    import dotenv
    version = getattr(dotenv, '__version__', 'unknown')
    print(f"   ✓ python-dotenv is installed (version {version})")
except ImportError:
    print("   ✗ python-dotenv is NOT installed")
    print("   Install it with: pip3 install python-dotenv --user")
    print("   OR use a virtual environment")

# Step 3: Load database config
print("\n3. Loading database configuration...")
try:
    from database_config import DB_CONFIG
    print("   ✓ Configuration loaded:")
    print(f"      Host:     {DB_CONFIG['host']}")
    print(f"      Database: {DB_CONFIG['database']}")
    print(f"      User:     {DB_CONFIG['user']}")
    print(f"      Port:     {DB_CONFIG['port']}")
    print(f"      Password: {'*' * len(str(DB_CONFIG['password']))}")
except Exception as e:
    print(f"   ✗ Error loading config: {e}")
    sys.exit(1)

# Step 4: Check psycopg2
print("\n4. Checking psycopg2...")
try:
    import psycopg2
    print(f"   ✓ psycopg2 is installed")
except ImportError:
    print("   ✗ psycopg2 is NOT installed")
    print("   Install it with: pip3 install psycopg2-binary --user")
    sys.exit(1)

# Step 5: Initialize connection pool
print("\n5. Initializing connection pool...")
try:
    from database_config import initialize_connection_pool
    initialize_connection_pool()
    print("   ✓ Connection pool initialized")
except Exception as e:
    print(f"   ✗ Error initializing pool: {e}")
    print("\n   Common issues:")
    print("   - PostgreSQL server not running")
    print("   - Wrong username/password in .env")
    print("   - Database doesn't exist (run: createdb cs631_company_db)")
    sys.exit(1)

# Step 6: Test connection
print("\n6. Testing database connection...")
try:
    from database_config import test_connection
    if test_connection():
        print("   ✓ Successfully connected to database")
    else:
        print("   ✗ Connection test failed")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Error testing connection: {e}")
    sys.exit(1)

# Step 7: Close connection
print("\n7. Closing connection pool...")
try:
    from database_config import close_connection_pool
    close_connection_pool()
except Exception as e:
    print(f"   ✗ Error closing pool: {e}")

print("\n" + "="*70)
print("✅ ALL TESTS PASSED - Your database is configured correctly!")
print("="*70)
print("\nYou can now run the demo:")
print("  cd applications && python3 demo.py")
print()
