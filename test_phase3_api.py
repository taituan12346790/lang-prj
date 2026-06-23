"""
Quick test script for Phase 3 execute-action endpoint
Run: python test_phase3_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_execute_action_without_auth():
    """Test that endpoint exists (should get 401 without auth)"""
    url = f"{BASE_URL}/api/learning/execute-action"
    
    payload = {
        "action_type": "offer_practice",
        "params": {"count": 5}
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 401:
        print("✅ Endpoint exists! (Got expected 401 Unauthorized)")
        return True
    elif response.status_code == 422:
        print("⚠️ Validation error - check request schema")
        return False
    elif response.status_code == 404:
        print("❌ Endpoint not found!")
        return False
    else:
        print(f"⚠️ Unexpected status code: {response.status_code}")
        return False

def test_openapi_schema():
    """Check if endpoint appears in OpenAPI schema"""
    url = f"{BASE_URL}/openapi.json"
    
    try:
        response = requests.get(url)
        schema = response.json()
        
        # Check if our endpoint exists in paths
        paths = schema.get("paths", {})
        execute_action_path = "/api/learning/execute-action"
        
        if execute_action_path in paths:
            print(f"✅ Endpoint found in OpenAPI schema!")
            print(f"   Methods: {list(paths[execute_action_path].keys())}")
            
            # Get the schema
            post_schema = paths[execute_action_path].get("post", {})
            request_body = post_schema.get("requestBody", {})
            print(f"   Request body: {request_body.get('content', {}).keys()}")
            
            return True
        else:
            print(f"❌ Endpoint NOT found in OpenAPI schema")
            print(f"Available learning endpoints:")
            for path in paths:
                if "/api/learning" in path:
                    print(f"   - {path}")
            return False
    except Exception as e:
        print(f"❌ Error checking OpenAPI schema: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3 API Endpoint Test")
    print("=" * 60)
    
    print("\n1. Testing OpenAPI Schema:")
    print("-" * 60)
    schema_ok = test_openapi_schema()
    
    print("\n2. Testing Endpoint Access:")
    print("-" * 60)
    endpoint_ok = test_execute_action_without_auth()
    
    print("\n" + "=" * 60)
    if schema_ok and endpoint_ok:
        print("✅ Phase 3 API Implementation: PASS")
        print("\nNext steps:")
        print("1. Login to Streamlit frontend")
        print("2. Navigate to a topic and click 'Học tiếp'")
        print("3. Send a message to AI Tutor")
        print("4. Check for action buttons below AI response")
    else:
        print("❌ Phase 3 API Implementation: FAIL")
        print("\nCheck:")
        print("- Is backend running on port 8000?")
        print("- Did you restart backend after code changes?")
    print("=" * 60)
