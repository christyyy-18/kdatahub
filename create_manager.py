#!/usr/bin/env python
"""Create or update a manager account.

The password is never stored in this file -- it is read from the
MANAGER_PASSWORD environment variable, or prompted for if that is not set:

    MANAGER_PASSWORD='...' python create_manager.py elsie elsie@example.com

A password written into a script ends up in the repository and, from there,
in everyone's clone.
"""
import getpass
import os
import sys

import django
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
django.setup()

CustomUser = get_user_model()

username = sys.argv[1] if len(sys.argv) > 1 else input('Username: ').strip()
email = sys.argv[2] if len(sys.argv) > 2 else input('Email: ').strip()

password = os.environ.get('MANAGER_PASSWORD')
if not password:
    password = getpass.getpass('Password: ')
    if password != getpass.getpass('Confirm password: '):
        sys.exit('Passwords do not match.')

user = CustomUser.objects.filter(username=username).first()

try:
    validate_password(password, user)
except ValidationError as exc:
    sys.exit('Password rejected: ' + '; '.join(exc.messages))

if user:
    user.is_manager = True
    user.is_staff = True
    user.set_password(password)
    user.save()
    print(f"Updated '{username}' to manager status and reset the password.")
else:
    CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_manager=True,
        is_staff=True,
        is_active=True,
    )
    print(f"Created manager account '{username}'.")

print(f"Sign in at /accounts/manager-login/ as '{username}'.")
