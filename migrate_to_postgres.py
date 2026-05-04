#!/usr/bin/env python
"""
Complete migration from SQLite to PostgreSQL
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

django.setup()

from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

def check_db_connection():
    """Check database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        print("✓ Database connected successfully")
        print(f"  Database: {connection.settings_dict['ENGINE']}")
        return True
    except OperationalError as e:
        print(f"✗ Database connection failed: {e}")
        return False

def run_migrations():
    """Apply all migrations"""
    print("\n" + "="*50)
    print("APPLYING MIGRATIONS")
    print("="*50)
    
    try:
        call_command('migrate', '--noinput', verbosity=2)
        print("\n✓ Migrations applied successfully")
        return True
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        return False

def show_migrations():
    """Show migration status"""
    print("\n" + "="*50)
    print("MIGRATION STATUS")
    print("="*50)
    try:
        call_command('showmigrations', verbosity=1)
        return True
    except Exception as e:
        print(f"Error showing migrations: {e}")
        return False

def count_tables():
    """Count tables in database"""
    print("\n" + "="*50)
    print("DATABASE TABLES")
    print("="*50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            
        if tables:
            print(f"Total tables: {len(tables)}\n")
            for table in tables:
                print(f"  • {table[0]}")
        else:
            print("No tables found in database")
        return True
    except Exception as e:
        print(f"Error counting tables: {e}")
        return False

if __name__ == '__main__':
    print("POSTGRESQL MIGRATION SETUP")
    print("="*50)
    
    # Check connection
    if not check_db_connection():
        sys.exit(1)
    
    # Show current migrations
    show_migrations()
    
    # Run migrations
    run_migrations()
    
    # Show tables
    count_tables()
    
    print("\n" + "="*50)
    print("MIGRATION COMPLETE")
    print("="*50)
