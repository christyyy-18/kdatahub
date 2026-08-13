#!/usr/bin/env python
"""Find elsie's manager account credentials"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
django.setup()

from accounts.models import CustomUser

# Search for elsie
users = CustomUser.objects.filter(username__icontains='elsie') | CustomUser.objects.filter(email__icontains='elsie')

if users.exists():
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Manager: {user.is_manager}")
        print(f"Is Agent: {user.is_agent}")
        print(f"Is Admin: {user.is_superuser}")
        print(f"Is Active: {user.is_active}")
        print("-" * 50)
else:
    print("No user found with 'elsie' in username or email")
    print("\nAll users in database:")
    all_users = CustomUser.objects.all()
    for user in all_users:
        print(f"Username: {user.username}, Email: {user.email}, Manager: {user.is_manager}")
