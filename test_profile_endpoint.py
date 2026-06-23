import requests

# Test if profile endpoint is now available
print("Testing profile endpoint availability...\n")

# Check docs to see if profile route is registered
try:
    r = requests.get('http://127.0.0.1:8000/docs')
    if r.status_code == 200:
        print("✅ Backend is up")
        if '/api/profile' in r.text:
            print("✅ Profile route is registered in docs!")
        else:
            print("❌ Profile route NOT in docs")
except Exception as e:
    print(f"❌ Error: {e}")

# Check OpenAPI spec
try:
    r = requests.get('http://127.0.0.1:8000/api/openapi.json')
    if r.status_code == 200:
        spec = r.json()
        paths = spec.get('paths', {})
        if '/api/profile/' in paths:
            print("✅ /api/profile/ found in OpenAPI spec!")
        else:
            print("❌ /api/profile/ NOT in OpenAPI spec")
            print(f"   Available paths: {list(paths.keys())[:10]}")
except Exception as e:
    print(f"❌ Error checking OpenAPI: {e}")
