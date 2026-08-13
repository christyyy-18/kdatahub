#!/usr/bin/env python
"""Create or update manager account for elsie"""
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
django.setup()

CustomUser = get_user_model()

# Manager credentials
username = 'elsie'
email = 'elsie@manager.com'
password = 'Manager@123Elsie'  # You should change this after first login

# Check if user exists
user = CustomUser.objects.filter(username=username).first()

if user:
    print(f"User '{username}' already exists")
    user.is_manager = True
    user.is_staff = True
    user.set_password(password)
    user.save()
    print(f"Updated {username} to manager status")
else:
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_manager=True,
        is_staff=True,
        is_active=True
    )
    print(f"Created new manager account")

print("\n" + "="*60)
print("MANAGER ACCOUNT CREDENTIALS")
print("="*60)
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Email: {email}")
print("="*60)
print("\nLogin URL: http://localhost:8000/accounts/manager_login/")
print("\nIMPORTANT: Please change this password after first login!")
print("="*60)
