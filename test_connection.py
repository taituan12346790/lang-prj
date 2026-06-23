"""
Test Backend Connection & Google OAuth
Quick script to verify everything is working
"""
import httpx
import sys

API_BASE = "http://127.0.0.1:8000"

def test_backend():
    """Test if backend is accessible"""
    print("\n🔍 Testing Backend Connection...")
    print(f"   URL: {API_BASE}")
    
    try:
        with httpx.Client(timeout=5) as client:
            r = client.get(f"{API_BASE}/health")
        
        if r.status_code == 200:
            print("   ✅ Backend is ONLINE")
            print(f"   Response: {r.json()}")
            return True
        else:
            print(f"   ❌ Backend returned {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        print("\n💡 Solution:")
        print("   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        return False

def test_google_oauth():
    """Test if Google OAuth endpoint works"""
    print("\n🔵 Testing Google OAuth...")
    
    try:
        with httpx.Client(timeout=5, follow_redirects=False) as client:
            r = client.get(f"{API_BASE}/api/auth/google")
        
        if r.status_code in (302, 307):
            print("   ✅ Google OAuth endpoint working")
            location = r.headers.get("location", "")
            if "accounts.google.com" in location:
                print("   ✅ Redirects to Google correctly")
                return True
            else:
                print(f"   ⚠️  Redirects to: {location[:100]}")
                return False
        else:
            print(f"   ❌ Unexpected status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_api_endpoints():
    """Test main API endpoints"""
    print("\n📋 Testing API Endpoints...")
    
    endpoints = [
        ("/health", "Health Check"),
        ("/api/learning/test-ping", "Learning Router Test"),
        ("/api/test/placement/questions", "Placement Test"),
    ]
    
    results = []
    for path, name in endpoints:
        try:
            with httpx.Client(timeout=5) as client:
                r = client.get(f"{API_BASE}{path}")
            
            if r.status_code in (200, 401):  # 401 is OK for protected routes
                print(f"   ✅ {name}")
                results.append(True)
            else:
                print(f"   ❌ {name} - Status {r.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ❌ {name} - {str(e)[:50]}")
            results.append(False)
    
    return all(results)

def main():
    print("="*60)
    print("   🧪 AI LANGUAGE TUTOR - CONNECTION TEST")
    print("="*60)
    
    # Test 1: Backend
    backend_ok = test_backend()
    
    if not backend_ok:
        print("\n❌ Backend is not running!")
        print("   Please start backend first:")
        print("   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        sys.exit(1)
    
    # Test 2: Google OAuth
    oauth_ok = test_google_oauth()
    
    # Test 3: API Endpoints
    api_ok = test_api_endpoints()
    
    # Summary
    print("\n" + "="*60)
    print("   📊 SUMMARY")
    print("="*60)
    
    print(f"   Backend Connection:  {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Google OAuth:        {'✅ PASS' if oauth_ok else '❌ FAIL'}")
    print(f"   API Endpoints:       {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if backend_ok and oauth_ok and api_ok:
        print("\n   🎉 ALL TESTS PASSED!")
        print("\n   ✅ System is ready to use!")
        print("\n   🚀 Next steps:")
        print("      1. Start Streamlit: python -m streamlit run streamlit_app.py --server.port 8501")
        print("      2. Open browser: http://localhost:8501")
        print("      3. Try Google login or email/password")
    else:
        print("\n   ⚠️  SOME TESTS FAILED")
        print("      Check errors above and restart services")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
