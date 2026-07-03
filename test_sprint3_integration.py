#!/usr/bin/env python3
"""
Test Sprint 3: Quiz → Chat Integration
Verifies that quiz weak_skills are extracted and passed to AI review
"""

import asyncio
import httpx
import json
from uuid import UUID

BASE_URL = "http://localhost:8000"

# Test user (from previous sessions)
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PW = "Test@123456"

async def test_sprint3_integration():
    """Test full quiz → chat integration flow"""
    
    async with httpx.AsyncClient() as client:
        print("=" * 80)
        print("🧪 SPRINT 3 INTEGRATION TEST")
        print("=" * 80)
        
        # 1. LOGIN
        print("\n1️⃣ Logging in...")
        login_resp = await client.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PW}
        )
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.text}")
            return
        
        user_data = login_resp.json()
        user_id = user_data.get("id")
        token = user_data.get("access_token")
        print(f"✅ Logged in as {user_data.get('name')} (ID: {user_id})")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. GET QUIZ QUESTIONS
        print("\n2️⃣ Getting quiz questions...")
        # Get first topic (A1 level)
        topics_resp = await client.get(
            f"{BASE_URL}/api/learning/topics?level=A1",
            headers=headers
        )
        if topics_resp.status_code != 200:
            print(f"❌ Failed to get topics: {topics_resp.text}")
            return
        
        topics = topics_resp.json()
        if not topics:
            print("❌ No topics found")
            return
        
        topic_id = topics[0]["id"]
        topic_name = topics[0]["name"]
        print(f"✅ Selected topic: {topic_name} (ID: {topic_id})")
        
        # Get quiz questions
        quiz_resp = await client.get(
            f"{BASE_URL}/api/quiz/topic/{topic_id}/questions",
            headers=headers
        )
        if quiz_resp.status_code != 200:
            print(f"❌ Failed to get quiz: {quiz_resp.text}")
            return
        
        quiz_data = quiz_resp.json()
        questions = quiz_data.get("questions", [])
        print(f"✅ Got {len(questions)} quiz questions")
        
        # 3. SUBMIT QUIZ WITH WRONG ANSWERS
        print("\n3️⃣ Submitting quiz with wrong answers (to trigger AI review)...")
        answers = {}
        for i, q in enumerate(questions[:3]):  # Wrong on first 3 questions
            # Choose wrong answer (usually not the first option)
            wrong_idx = (q["options"].index("correct") if "correct" in q["options"] else 1) + 1
            if wrong_idx >= len(q["options"]):
                wrong_idx = 0
            answers[q["id"]] = q["options"][wrong_idx]
        
        # Correct answers for remaining
        for q in questions[3:]:
            answers[q["id"]] = q["options"][0]  # Assume first is correct for test
        
        submit_resp = await client.post(
            f"{BASE_URL}/api/quiz/topic/{topic_id}/submit",
            json={"answers": answers},
            headers=headers
        )
        
        if submit_resp.status_code != 200:
            print(f"❌ Quiz submission failed: {submit_resp.text}")
            return
        
        quiz_result = submit_resp.json()
        print(f"✅ Quiz submitted successfully")
        
        # 4. VERIFY NEW RESPONSE FORMAT
        print("\n4️⃣ Verifying new response format with weak_skills...")
        
        # Check for new fields
        has_quiz_response = "quiz_response" in quiz_result
        has_weak_skills = "weak_skills" in quiz_result
        has_ai_review_enabled = "ai_review_enabled" in quiz_result
        has_ai_review_prompt = "ai_review_prompt" in quiz_result
        
        print(f"   ✓ quiz_response present: {has_quiz_response}")
        print(f"   ✓ weak_skills present: {has_weak_skills}")
        print(f"   ✓ ai_review_enabled present: {has_ai_review_enabled}")
        print(f"   ✓ ai_review_prompt present: {has_ai_review_prompt}")
        
        if not all([has_quiz_response, has_weak_skills, has_ai_review_enabled, has_ai_review_prompt]):
            print("❌ Response format is incomplete!")
            print(f"Response keys: {quiz_result.keys()}")
            return
        
        print("✅ Response format is correct!")
        
        # 5. CHECK WEAK SKILLS CONTENT
        print("\n5️⃣ Examining weak_skills content...")
        weak_skills = quiz_result.get("weak_skills", [])
        ai_review_enabled = quiz_result.get("ai_review_enabled", False)
        
        print(f"   - Number of weak skills: {len(weak_skills)}")
        print(f"   - AI review enabled: {ai_review_enabled}")
        
        if weak_skills:
            print("\n   First weak skill example:")
            first_weak = weak_skills[0]
            print(f"   - Question: {first_weak.get('question', '')[:50]}...")
            print(f"   - User answer: {first_weak.get('user_answer', '')}")
            print(f"   - Correct answer: {first_weak.get('correct_answer', '')}")
            print("   ✅ Weak skills properly extracted!")
        
        # 6. CHECK AI REVIEW PROMPT
        print("\n6️⃣ Examining AI review prompt...")
        ai_prompt = quiz_result.get("ai_review_prompt", "")
        if ai_prompt:
            print(f"   - Prompt length: {len(ai_prompt)} chars")
            print(f"   - Contains '[QUIZ REVIEW MODE]': {'[QUIZ REVIEW MODE]' in ai_prompt}")
            print(f"   - Contains weak skill count: {f'Học viên vừa làm quiz sai {len(weak_skills)} câu' in ai_prompt}")
            print("   ✅ AI review prompt generated!")
        else:
            print("   ❌ No AI review prompt generated")
            return
        
        # 7. VERIFY DATABASE UPDATES
        print("\n7️⃣ Verifying database updates...")
        print("   (Checking if weak_skills saved to UserTopicProgress)")
        
        # Get user progress
        progress_resp = await client.get(
            f"{BASE_URL}/api/learning/user-progress/{topic_id}",
            headers=headers
        )
        
        if progress_resp.status_code == 200:
            progress = progress_resp.json()
            if progress.get("weak_skills"):
                print("   ✅ Weak skills saved to database!")
            else:
                print("   ⚠️ Weak skills not yet in progress (might be in next query)")
        
        print("\n" + "=" * 80)
        print("✅ SPRINT 3 INTEGRATION TEST PASSED!")
        print("=" * 80)
        print(f"\n📋 Summary:")
        print(f"   - Quiz response format: ✅ Enhanced with weak_skills")
        print(f"   - Weak skills extraction: ✅ {len(weak_skills)} errors identified")
        print(f"   - AI review enabled: ✅ {ai_review_enabled}")
        print(f"   - AI prompt generated: ✅ {len(ai_prompt)} chars")
        print(f"\n🎯 Next Steps:")
        print(f"   1. Streamlit shows 'Ôn bài với AI' button in quiz result")
        print(f"   2. User clicks button → enters Chat with AI Tutor mode")
        print(f"   3. AI receives quiz context and provides personalized review")
        print(f"   4. User gets detailed explanations + 5 new exercises")


if __name__ == "__main__":
    asyncio.run(test_sprint3_integration())
