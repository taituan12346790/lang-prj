"""Test API endpoints directly"""
import asyncio
import httpx

API_BASE = "http://127.0.0.1:8000"

async def test_endpoints():
    print("🔍 Testing API endpoints...\n")
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{API_BASE}/health")
            if r.status_code == 200:
                print(f"   ✅ Health: {r.json()}")
            else:
                print(f"   ❌ Health failed: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        print("   💡 Please start backend: python -m uvicorn app.main:app --reload")
        return
    
    # Test 2: Register a test user
    print("\n2️⃣ Creating test user...")
    test_email = f"test_{int(asyncio.get_event_loop().time())}@example.com"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{API_BASE}/api/auth/register", json={
            "email": test_email,
            "password": "testpass123",
            "full_name": "Test User",
            "native_language": "vi",
            "target_language": "en"
        })
        if r.status_code in (200, 201):
            print(f"   ✅ User created: {test_email}")
        else:
            print(f"   ⚠️ Register: {r.status_code} - {r.text[:200]}")
    
    # Test 3: Login
    print("\n3️⃣ Logging in...")
    token = None
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{API_BASE}/api/auth/login", json={
            "email": test_email,
            "password": "testpass123"
        })
        if r.status_code == 200:
            data = r.json()
            token = data.get("access_token")
            print(f"   ✅ Login successful, got token")
        else:
            print(f"   ❌ Login failed: {r.status_code} - {r.text[:200]}")
            return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4: Dashboard
    print("\n4️⃣ Testing dashboard endpoint...")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{API_BASE}/api/learning/dashboard", headers=headers)
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ Dashboard loaded!")
            print(f"      Current level: {data.get('current_level')}")
            lp = data.get('level_progress', {})
            print(f"      Total topics: {lp.get('total_topics')}")
            print(f"      Completed: {lp.get('completed_topics')}")
        else:
            print(f"   ❌ Dashboard failed: {r.status_code}")
            print(f"      Error: {r.text[:500]}")
    
    # Test 5: Topics list
    print("\n5️⃣ Testing topics list endpoint...")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{API_BASE}/api/learning/topics/A1", headers=headers)
        if r.status_code == 200:
            topics = r.json()
            print(f"   ✅ Topics loaded: {len(topics)} topics")
            if topics:
                print(f"      First topic: {topics[0].get('name')}")
        else:
            print(f"   ❌ Topics failed: {r.status_code}")
            print(f"      Error: {r.text[:500]}")
    
    print("\n✅ API testing complete!")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
