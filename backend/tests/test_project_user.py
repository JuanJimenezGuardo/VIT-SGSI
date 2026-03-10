#!/usr/bin/env python
"""Test ProjectUser endpoint"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

# Step 1: Login to get token
print("=" * 60)
print("STEP 1: Logging in...")
print("=" * 60)
login_data = {"username": "admin", "password": "admin"}
response = requests.post(f"{BASE_URL}/token/", json=login_data)
print(f"Status: {response.status_code}" )
if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access']
    print("✓ Login successful")
    print(f"Access Token: {access_token[:50]}...")
else:
    print("✗ Login failed")
    print(response.text)
    exit(1)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Step 2: Get all project-users
print("\n" + "=" * 60)
print("STEP 2: GET /api/project-users/")
print("=" * 60)
response = requests.get(f"{BASE_URL}/project-users/", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    project_users = response.json()
    print(f"✓ Found {len(project_users)} project-user assignments")
    for pu in project_users:
        print(f"  - User {pu['username']} assigned to Project '{pu['project_name']}' as {pu['role']}")
else:
    print("✗ Failed to get project-users")
    print(response.text)

# Step 3: Create a project-user assignment (if we have data)
print("\n" + "=" * 60)
print("STEP 3: Check for available projects and users")
print("=" * 60)

# Get projects
response = requests.get(f"{BASE_URL}/projects/", headers=headers)
if response.status_code == 200:
    projects = response.json()
    print(f"✓ Found {len(projects)} projects")
    if projects:
        print(f"  First project: ID={projects[0]['id']}, Name='{projects[0]['name']}'")
else:
    print("✗ Failed to get projects")
    projects = []

# Get users
response = requests.get(f"{BASE_URL}/users/", headers=headers)
if response.status_code == 200:
    users = response.json()
    print(f"✓ Found {len(users)} users")
    if users:
        print(f"  First user: ID={users[0]['id']}, Username='{users[0]['username']}'")
else:
    print("✗ Failed to get users")
    users = []

# Step 4: Try to create a project-user assignment
if projects and users:
    print("\n" + "=" * 60)
    print("STEP 4: POST /api/project-users/ (Create assignment)")
    print("=" * 60)
    
    assignment_data = {
        "project": projects[0]['id'],
        "user": users[0]['id'],
        "role": "CONSULTANT"
    }
    
    print(f"Creating assignment: User {users[0]['username']} → Project '{projects[0]['name']}' as CONSULTANT")
    response = requests.post(f"{BASE_URL}/project-users/", headers=headers, json=assignment_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✓ Assignment created successfully!")
        print(f"  ID: {result['id']}")
        print(f"  User: {result['username']} ({result['user_email']})")
        print(f"  Project: {result['project_name']}")
        print(f"  Role: {result['role']}")
    elif response.status_code == 400:
        print("✗ Bad request (possibly duplicate assignment)")
        print(response.json())
    else:
        print("✗ Failed to create assignment")
        print(response.text)
else:
    print("\n⚠ Skipping assignment creation - no projects or users available")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
