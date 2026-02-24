#!/usr/bin/env python
"""Script to fix admin user role"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.users.models import User

admin = User.objects.get(username='admin')
admin.role = 'ADMIN'
admin.save()
print(f'✓ Admin user role updated to: {admin.role}')
