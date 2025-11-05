import requests
import json

BASE_URL = "http://localhost:5000"

def test_backend():
    print("Testing Leave Management System Backend...")
    
    # Test 1: Admin Login
    print("\n1. Testing Admin Login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@company.com",
        "password": "admin123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        admin_data = response.json()
        admin_token = admin_data['access_token']
        print("✓ Admin login successful")
        print(f"Token: {admin_token[:50]}...")
    else:
        print("✗ Admin login failed")
        return
    
    # Test 2: Employee Login
    print("\n2. Testing Employee Login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "john@company.com",
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        employee_data = response.json()
        employee_token = employee_data['access_token']
        print("✓ Employee login successful")
        print(f"Token: {employee_token[:50]}...")
    else:
        print("✗ Employee login failed")
        return
    
    # Test 3: Create leave request as employee
    print("\n3. Testing Leave Request Creation...")
    headers = {"Authorization": f"Bearer {employee_token}"}
    response = requests.post(f"{BASE_URL}/leaves", json={
        "start_date": "2024-11-10",
        "end_date": "2024-11-15",
        "reason": "Vacation leave"
    }, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✓ Leave request created successfully")
    else:
        print(f"✗ Leave request creation failed: {response.text}")
    
    # Test 4: Get leave requests as admin
    print("\n4. Testing Admin Leave Requests Access...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/leaves", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        leaves = response.json()
        print(f"✓ Admin retrieved {len(leaves)} leave requests")
        if leaves:
            print(f"First request: {leaves[0]['reason']} (Status: {leaves[0]['status']})")
    else:
        print(f"✗ Failed to get leave requests: {response.text}")
    
    # Test 5: Get stats as admin
    print("\n5. Testing Stats Endpoint...")
    response = requests.get(f"{BASE_URL}/stats", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print("✓ Stats retrieved successfully:")
        print(f"  - Total requests: {stats['total_requests']}")
        print(f"  - Pending: {stats['pending_requests']}")
        print(f"  - Approved: {stats['approved_requests']}")
        print(f"  - Rejected: {stats['rejected_requests']}")
        print(f"  - Employees: {stats['total_employees']}")
    else:
        print(f"✗ Failed to get stats: {response.text}")
    
    # Test 6: Get users list as admin
    print("\n6. Testing Users Endpoint...")
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"✓ Retrieved {len(users)} users")
        for user in users:
            print(f"  - {user['name']} ({user['email']}) - {user['role']}")
    else:
        print(f"✗ Failed to get users: {response.text}")
    
    print("\n✅ Backend testing completed!")

if __name__ == "__main__":
    test_backend()