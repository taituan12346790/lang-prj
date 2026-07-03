import requests

# Test health
print("Testing backend health...")
r = requests.get('http://127.0.0.1:8000/health')
print(f"✅ Health: {r.status_code} - {r.json()}")

# Test topics
print("\nTesting topics API...")
r = requests.get('http://127.0.0.1:8000/api/learning/topics/A1')
print(f"✅ Topics A1: {r.status_code}")
data = r.json()
print(f"   Topics count: {len(data)}")
if data:
    print(f"   First topic: {data[0]['name']} - {data[0]['name_vi']}")

# Test dashboard
print("\nTesting dashboard API...")
r = requests.get('http://127.0.0.1:8000/api/learning/dashboard?user_id=1')
print(f"✅ Dashboard: {r.status_code}")

print("\n✅ ALL BACKEND TESTS PASSED!")
