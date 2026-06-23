"""Quick test to check if API can load topics"""
import asyncio
import httpx

async def test():
    base = "http://localhost:8501"
    
    # Test 1: Get dashboard
    print("Testing GET /api/learning/dashboard...")
    try:
        async with httpx.AsyncClient() as client:
            # You need a valid token - get from your browser
            token = "YOUR_TOKEN_HERE"  # Replace with actual token
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.get(f"{base}/api/learning/dashboard", headers=headers, timeout=10.0)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Current topic: {data.get('current_topic', {}).get('name', 'None')}")
            else:
                print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("Note: You need to set a valid token in the script")
    print("Backend might not be running on port 8501")
    # asyncio.run(test())
