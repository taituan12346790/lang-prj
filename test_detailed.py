"""Detailed API test with error messages"""
import asyncio
import httpx
import json

API_BASE = "http://127.0.0.1:8000"

async def test():
    print("🔍 Detailed API Testing\n")
    
    # Create user
    test_email = f"debug_{int(asyncio.get_event_loop().time())}@example.com"
    print(f"1️⃣ Creating user: {test_email}")
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{API_BASE}/api/auth/register", json={
            "email": test_email,
            "password": "testpass123",
            "full_name": "Debug User",
            "native_language": "vi",
            "target_language": "en"
        })
        print(f"   Status: {r.status_code}")
        if r.status_code not in (200, 201):
            print(f"   Response: {r.text}")
            return
    
    # Login
    print(f"\n2️⃣ Logging in...")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{API_BASE}/api/auth/login", json={
            "email": test_email,
            "password": "testpass123"
        })
        print(f"   Status: {r.status_code}")
        if r.status_code != 200:
            print(f"   Response: {r.text}")
            return
        data = r.json()
        token = data.get("access_token")
        print(f"   Token: {token[:50]}...")
    
    # Test dashboard with full error
    print(f"\n3️⃣ Testing /api/learning/dashboard...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{API_BASE}/api/learning/dashboard", headers=headers)
        print(f"   Status: {r.status_code}")
        print(f"   Headers: {dict(r.headers)}")
        print(f"   Body: {r.text[:1000]}")
        
        if r.status_code == 200:
            print("   ✅ SUCCESS!")
            data = r.json()
            print(f"   Level: {data.get('current_level')}")
        else:
            print("   ❌ FAILED!")
            try:
                err = r.json()
                print(f"   Error: {json.dumps(err, indent=2)}")
            except:
                pass

if __name__ == "__main__":
    asyncio.run(test())
