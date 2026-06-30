"""Test using subprocess to call curl"""
import subprocess
import json

# First login
login_cmd = [
    'curl', '-X', 'POST',
    'http://127.0.0.1:8000/api/auth/login',
    '-H', 'Content-Type: application/json',
    '-d', '{"email":"test_421745@example.com","password":"testpass123"}'
]

print("1️⃣ Logging in...")
result = subprocess.run(login_cmd, capture_output=True, text=True)
if result.returncode == 0:
    data = json.loads(result.stdout)
    token = data.get("access_token")
    print(f"   ✅ Got token: {token[:50]}...")
    
    # Test dashboard
    print("\n2️⃣ Testing dashboard...")
    dashboard_cmd = [
        'curl', '-X', 'GET',
        'http://127.0.0.1:8000/api/learning/dashboard',
        '-H', f'Authorization: Bearer {token}'
    ]
    
    result = subprocess.run(dashboard_cmd, capture_output=True, text=True)
    print(f"   Status: {result.returncode}")
    print(f"   Output: {result.stdout[:500]}")
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            print(f"   ✅ Dashboard loaded!")
            print(f"   Level: {data.get('current_level')}")
        except:
            print(f"   ❌ Not JSON response")
else:
    print(f"   ❌ Login failed: {result.stderr}")
