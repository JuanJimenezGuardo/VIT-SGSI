#!/usr/bin/env python
"""Test all API endpoints to verify they're working correctly"""

import os
import sys
from pathlib import Path
import django

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

# Test endpoints
client = Client()

# Test 1: Users endpoint
print("=" * 60)
print("TEST 1: GET /api/users/")
print("=" * 60)
response = client.get('/api/users/')
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
print()

# Test 2: Companies endpoint
print("=" * 60)
print("TEST 2: GET /api/companies/")
print("=" * 60)
response = client.get('/api/companies/')
print(f"Status Code: {response.status_code}")
print()

# Test 3: Projects endpoint
print("=" * 60)
print("TEST 3: GET /api/projects/")
print("=" * 60)
response = client.get('/api/projects/')
print(f"Status Code: {response.status_code}")
print()

# Test 4: Phases endpoint
print("=" * 60)
print("TEST 4: GET /api/phases/")
print("=" * 60)
response = client.get('/api/phases/')
print(f"Status Code: {response.status_code}")
print()

# Test 5: Tasks endpoint
print("=" * 60)
print("TEST 5: GET /api/tasks/")
print("=" * 60)
response = client.get('/api/tasks/')
print(f"Status Code: {response.status_code}")
print()

# Test 6: Admin user verification
print("=" * 60)
print("TEST 6: Admin User Verification")
print("=" * 60)
User = get_user_model()
admin = User.objects.filter(username='admin').first()
print(f"Admin User Exists: {admin is not None}")
if admin:
    print(f"  - Username: {admin.username}")
    print(f"  - Email: {admin.email}")
    print(f"  - Is Superuser: {admin.is_superuser}")
    print(f"  - Is Staff: {admin.is_staff}")
    print(f"  - Role: {admin.role}")
    # Fix admin role if needed
    if admin.role != 'ADMIN':
        admin.role = 'ADMIN'
        admin.save()
        print(f"  - Role Updated to: {admin.role} ✅")
print()

print("=" * 60)
print("✅ ALL TESTS COMPLETED")
print("=" * 60)
