#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
django.setup()

from accounts.models import CustomUser

# Update christable to manager status
christable = CustomUser.objects.filter(username='christable').first()
if christable:
    christable.is_manager = True
    christable.save()
    print(f"✓ {christable.username} - is_manager set to {christable.is_manager}")
else:
    print("✗ christable not found")

# Update amanyarko to agent status
amanyarko = CustomUser.objects.filter(username='amanyarko').first()
if amanyarko:
    amanyarko.is_agent = True
    amanyarko.save()
    print(f"✓ {amanyarko.username} - is_agent set to {amanyarko.is_agent}")
else:
    print("✗ amanyarko not found")

print("\nStatus update complete!")
