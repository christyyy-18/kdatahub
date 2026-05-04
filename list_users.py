#!/usr/bin/env python
"""
Script to list all users and verify database connection
"""
import os
import django
import sys
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
django.setup()

from accounts.models import CustomUser, AgentRequest
from django.db import connection
from django.db.utils import OperationalError

def check_database_connection():
    """Check if database is connected"""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return True, connection.settings_dict['ENGINE']
    except OperationalError as e:
        return False, str(e)

def get_user_status(user):
    """Generate user status string"""
    statuses = []
    if user.is_superuser:
        statuses.append("ADMIN")
    elif user.is_manager:
        statuses.append("MANAGER")
    if user.is_agent:
        statuses.append("AGENT")
    if user.is_staff:
        statuses.append("STAFF")
    if not user.is_active:
        statuses.append("INACTIVE")
    if not statuses:
        statuses.append("CUSTOMER")
    return ", ".join(statuses)

def list_users():
    """List all users with their status"""
    print("=" * 100)
    print(f"{'USER LIST REPORT':<50} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    # Check database connection
    connected, db_info = check_database_connection()
    if connected:
        print(f"✓ Database Connected: {db_info}")
    else:
        print(f"✗ Database Connection Failed: {db_info}")
        return
    
    print("-" * 100)
    
    # Get all users
    users = CustomUser.objects.all().order_by('id')
    
    if not users.exists():
        print("No users found in database.")
        return
    
    print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Status':<25} {'Active':<8}")
    print("-" * 100)
    
    for user in users:
        status = get_user_status(user)
        active = "✓ Yes" if user.is_active else "✗ No"
        print(f"{user.id:<5} {user.username:<20} {user.email:<30} {status:<25} {active:<8}")
    
    print("-" * 100)
    print(f"Total Users: {users.count()}")
    
    # Count by status
    print("\n" + "=" * 100)
    print("USER STATISTICS")
    print("=" * 100)
    
    active_users = CustomUser.objects.filter(is_active=True).count()
    inactive_users = CustomUser.objects.filter(is_active=False).count()
    admin_users = CustomUser.objects.filter(is_superuser=True).count()
    manager_users = CustomUser.objects.filter(is_manager=True).count()
    agent_users = CustomUser.objects.filter(is_agent=True).count()
    customer_users = CustomUser.objects.filter(is_agent=False, is_manager=False, is_superuser=False).count()
    
    print(f"Total Users: {users.count()}")
    print(f"Active Users: {active_users}")
    print(f"Inactive Users: {inactive_users}")
    print(f"Administrators: {admin_users}")
    print(f"Managers: {manager_users}")
    print(f"Agents: {agent_users}")
    print(f"Customers: {customer_users}")
    
    # Agent requests
    print("\n" + "=" * 100)
    print("AGENT REQUESTS")
    print("=" * 100)
    
    pending_requests = AgentRequest.objects.filter(status='pending').count()
    approved_requests = AgentRequest.objects.filter(status='approved').count()
    rejected_requests = AgentRequest.objects.filter(status='rejected').count()
    
    print(f"Pending Requests: {pending_requests}")
    print(f"Approved Requests: {approved_requests}")
    print(f"Rejected Requests: {rejected_requests}")
    
    if pending_requests > 0:
        print("\nPending Agent Requests:")
        print("-" * 100)
        pending = AgentRequest.objects.filter(status='pending')
        for req in pending:
            print(f"  • {req.user.username} - {req.business_name} (Requested: {req.created_at.strftime('%Y-%m-%d')})")
    
    print("\n" + "=" * 100)

if __name__ == '__main__':
    list_users()
