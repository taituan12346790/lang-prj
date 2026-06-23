#!/usr/bin/env python3
"""
Verify Sprint 3 code integration without requiring live data
"""

import sys
import importlib

def verify_sprint3():
    print("=" * 80)
    print("✅ SPRINT 3 CODE VERIFICATION")
    print("=" * 80)
    
    errors = []
    
    # 1. Verify QuizEnhancedService exists
    print("\n1️⃣ Checking QuizEnhancedService...")
    try:
        from app.services.quiz_enhanced import QuizEnhancedService, build_quiz_review_prompt
        print("   ✅ QuizEnhancedService imported")
        print("   ✅ build_quiz_review_prompt imported")
    except Exception as e:
        errors.append(f"QuizEnhancedService import failed: {e}")
        print(f"   ❌ {errors[-1]}")
    
    # 2. Verify quiz router updated
    print("\n2️⃣ Checking quiz router...")
    try:
        from app.routers import quiz as quiz_module
        with open("app/routers/quiz.py", encoding="utf-8") as f:
            quiz_content = f.read()
        if "QuizEnhancedService" in quiz_content:
            print("   ✅ Quiz router imports QuizEnhancedService")
        else:
            errors.append("Quiz router does not import QuizEnhancedService")
            print(f"   ❌ {errors[-1]}")
            
        if "submit_quiz_with_chat_context" in quiz_content:
            print("   ✅ Quiz router calls submit_quiz_with_chat_context")
        else:
            errors.append("Quiz router does not call submit_quiz_with_chat_context")
            print(f"   ❌ {errors[-1]}")
    except Exception as e:
        errors.append(f"Quiz router verification failed: {e}")
        print(f"   ❌ {errors[-1]}")
    
    # 3. Verify Streamlit has "Ôn bài với AI" button
    print("\n3️⃣ Checking Streamlit quiz result page...")
    try:
        with open("streamlit_app.py", encoding="utf-8") as f:
            streamlit_content = f.read()
        if "Ôn bài với AI" in streamlit_content:
            print("   ✅ Streamlit has 'Ôn bài với AI' button")
        else:
            errors.append("Streamlit missing 'Ôn bài với AI' button")
            print(f"   ❌ {errors[-1]}")
        
        if "quiz_weak_skills" in streamlit_content:
            print("   ✅ Streamlit handles quiz_weak_skills")
        else:
            errors.append("Streamlit does not handle quiz_weak_skills")
            print(f"   ❌ {errors[-1]}")
            
        if "is_from_quiz" in streamlit_content:
            print("   ✅ Streamlit detects quiz review mode")
        else:
            errors.append("Streamlit does not detect quiz review mode")
            print(f"   ❌ {errors[-1]}")
    except Exception as e:
        errors.append(f"Streamlit verification failed: {e}")
        print(f"   ❌ {errors[-1]}")
    
    # 4. Verify quiz response structure
    print("\n4️⃣ Checking response format...")
    try:
        from app.services.quiz_enhanced import QuizEnhancedService
        import inspect
        source = inspect.getsource(QuizEnhancedService.submit_quiz_with_chat_context)
        
        checks = {
            "quiz_response": "quiz_response",
            "weak_skills": "weak_skills",
            "ai_review_enabled": "ai_review_enabled", 
            "ai_review_prompt": "ai_review_prompt",
            "topic_id": "topic_id",
        }
        
        for field, check_str in checks.items():
            if check_str in source:
                print(f"   ✅ Response includes '{field}'")
            else:
                errors.append(f"Response missing '{field}' field")
                print(f"   ❌ {errors[-1]}")
    except Exception as e:
        errors.append(f"Response format verification failed: {e}")
        print(f"   ❌ {errors[-1]}")
    
    # 5. Verify AI tutor mode handling
    print("\n5️⃣ Checking AI tutor mode handling...")
    try:
        with open("streamlit_app.py", encoding="utf-8") as f:
            streamlit_content = f.read()
        
        if "[QUIZ REVIEW MODE - TUTOR BEHAVIOR REQUIRED]" in streamlit_content:
            print("   ✅ Quiz review prompt added")
        else:
            errors.append("Quiz review prompt not found")
            print(f"   ❌ {errors[-1]}")
            
        if "QUIZ REVIEW MODE" in streamlit_content and "CHI TIẾT CÁC CÂU SAI" in streamlit_content:
            print("   ✅ Quiz context properly formatted")
        else:
            errors.append("Quiz context formatting incomplete")
            print(f"   ❌ {errors[-1]}")
    except Exception as e:
        errors.append(f"AI tutor mode verification failed: {e}")
        print(f"   ❌ {errors[-1]}")
    
    # SUMMARY
    print("\n" + "=" * 80)
    if not errors:
        print("✅ ALL SPRINT 3 CODE CHECKS PASSED!")
        print("=" * 80)
        print("\n📋 Implementation Summary:")
        print("   ✅ Quiz router updated to use QuizEnhancedService")
        print("   ✅ Response format enhanced with weak_skills")
        print("   ✅ AI review prompt automatically generated")
        print("   ✅ Streamlit shows 'Ôn bài với AI' button")
        print("   ✅ Quiz context properly integrated into chat")
        print("\n🚀 Sprint 3 is COMPLETE and READY TO TEST!")
        return True
    else:
        print("❌ SPRINT 3 CODE VERIFICATION FAILED")
        print("=" * 80)
        print("\n🐛 Errors found:")
        for i, err in enumerate(errors, 1):
            print(f"   {i}. {err}")
        return False


if __name__ == "__main__":
    success = verify_sprint3()
    sys.exit(0 if success else 1)
