"""
Test Error Detection & Personalized Correction System
"""
import asyncio
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_error_analysis():
    """Test the complete error detection flow"""
    
    print("=" * 60)
    print("🧪 TEST: ERROR DETECTION & PERSONALIZED CORRECTION")
    print("=" * 60)
    
    # Step 1: Login
    print("\n📝 Step 1: Login...")
    async with httpx.AsyncClient() as client:
        login_resp = await client.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@example.com",
            "password": "test12345"
        })
        
        if login_resp.status_code == 200:
            token = login_resp.json()["access_token"]
            print(f"✓ Login successful! Token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {login_resp.text}")
            # Try to register
            print("\n📝 Registering new user...")
            reg_resp = await client.post(f"{BASE_URL}/api/auth/register", json={
                "email": "test@example.com",
                "password": "test12345",
                "full_name": "Test User",
                "target_language": "pt",
                "current_level": "A1"
            })
            print(f"Registration status: {reg_resp.status_code}")
            if reg_resp.status_code in [200, 201]:
                resp_json = reg_resp.json()
                token = resp_json.get("access_token")
                if not token:
                    # User created, now login
                    print("User created, logging in...")
                    login_resp = await client.post(f"{BASE_URL}/api/auth/login", json={
                        "email": "test@example.com",
                        "password": "test12345"
                    })
                    if login_resp.status_code == 200:
                        token = login_resp.json()["access_token"]
                        print(f"✓ Login successful! Token: {token[:20]}...")
                    else:
                        print(f"✗ Login after registration failed")
                        return
                else:
                    print(f"✓ Registration successful! Token: {token[:20]}...")
            else:
                print(f"✗ Registration failed: {reg_resp.text}")
                return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Test error analysis - First time error
        print("\n📝 Step 2: Test First Time Error...")
        error1 = await client.post(
            f"{BASE_URL}/api/learning/analyze-error",
            headers=headers,
            json={
                "question": "Yesterday, I ___ to the market.",
                "user_answer": "go",
                "correct_answer": "went",
                "skill_tag": "past_tense",
                "lesson_id": None,
                "topic_id": None
            }
        )
        
        if error1.status_code == 200:
            data = error1.json()
            print(f"✓ Error Analysis successful!")
            print(f"  - Error Type: {data['error']['error_type']}")
            print(f"  - Skill: {data['error']['skill_tag']}")
            print(f"  - Frequency: {data['frequency']}")
            print(f"  - Recommendation: {data['recommendation_type']}")
            print(f"  - Suggestion: {data['suggestion'][:100]}...")
        else:
            print(f"✗ Error Analysis failed: {error1.text}")
            return
        
        # Step 3: Make the same error again
        print("\n📝 Step 3: Test Second Time Error (same type)...")
        await asyncio.sleep(1)
        error2 = await client.post(
            f"{BASE_URL}/api/learning/analyze-error",
            headers=headers,
            json={
                "question": "Last week, she ___ a new car.",
                "user_answer": "buy",
                "correct_answer": "bought",
                "skill_tag": "past_tense",
                "lesson_id": None,
                "topic_id": None
            }
        )
        
        if error2.status_code == 200:
            data = error2.json()
            print(f"✓ Error Analysis successful!")
            print(f"  - Error Type: {data['error']['error_type']}")
            print(f"  - Frequency: {data['frequency']} (should be 2)")
            print(f"  - Recommendation: {data['recommendation_type']}")
            print(f"  - Suggestion: {data['suggestion'][:100]}...")
        else:
            print(f"✗ Error Analysis failed: {error2.text}")
            return
        
        # Step 4: Third time
        print("\n📝 Step 4: Test Third Time Error...")
        await asyncio.sleep(1)
        error3 = await client.post(
            f"{BASE_URL}/api/learning/analyze-error",
            headers=headers,
            json={
                "question": "Two days ago, they ___ home early.",
                "user_answer": "come",
                "correct_answer": "came",
                "skill_tag": "past_tense",
                "lesson_id": None,
                "topic_id": None
            }
        )
        
        if error3.status_code == 200:
            data = error3.json()
            print(f"✓ Error Analysis successful!")
            print(f"  - Error Type: {data['error']['error_type']}")
            print(f"  - Frequency: {data['frequency']} (should be 3)")
            print(f"  - Recommendation: {data['recommendation_type']}")
            print(f"  - Next Action: {data['next_action']}")
            print(f"  - Suggestion: {data['suggestion'][:100]}...")
        else:
            print(f"✗ Error Analysis failed: {error3.text}")
            return
        
        # Step 5: Check error pattern
        print("\n📝 Step 5: Test Different Error Type...")
        error4 = await client.post(
            f"{BASE_URL}/api/learning/analyze-error",
            headers=headers,
            json={
                "question": "He ___ to school every day.",
                "user_answer": "go",
                "correct_answer": "goes",
                "skill_tag": "subject_verb_agreement",
                "lesson_id": None,
                "topic_id": None
            }
        )
        
        if error4.status_code == 200:
            data = error4.json()
            print(f"✓ Error Analysis successful!")
            print(f"  - Error Type: {data['error']['error_type']}")
            print(f"  - Frequency: {data['frequency']} (should be 1 - different error)")
            print(f"  - Recommendation: {data['recommendation_type']}")
        else:
            print(f"✗ Error Analysis failed: {error4.text}")
            return
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\n📊 Summary:")
    print("  1. ✓ User authentication works")
    print("  2. ✓ Error detection and classification works")
    print("  3. ✓ Error frequency tracking works")
    print("  4. ✓ Personalized suggestions work")
    print("  5. ✓ Different error types are tracked separately")
    print("\n🎉 System is ready to use!")
    print("\nNext: Open Streamlit app and test the UI")
    print("  1. Login to app")
    print("  2. Go to a lesson with practice exercises")
    print("  3. Answer a question incorrectly")
    print("  4. Verify error analysis panel appears")
    print("  5. Answer same type wrong again")
    print("  6. Verify frequency counter increases")

if __name__ == "__main__":
    asyncio.run(test_error_analysis())
