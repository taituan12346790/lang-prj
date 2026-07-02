"""
Test AI skill detection in ErrorAnalyzer
"""
import asyncio
from app.core.error_analyzer import ErrorAnalyzer

async def test_skill_detection():
    """Test if AI can detect specific skills from questions"""
    analyzer = ErrorAnalyzer()
    
    # Test cases with expected skills
    test_cases = [
        {
            "question": "There ___ three chairs",
            "user_answer": "is",
            "correct_answer": "are",
            "expected_skill": "there_is_are",
            "expected_type": "GRAMMAR_ERROR"
        },
        {
            "question": "He ___ to school every day.",
            "user_answer": "go",
            "correct_answer": "goes",
            "expected_skill": "subject_verb_agreement",
            "expected_type": "GRAMMAR_ERROR"
        },
        {
            "question": "Yesterday, I ___ to the market.",
            "user_answer": "go",
            "correct_answer": "went",
            "expected_skill": "past_tense",
            "expected_type": "GRAMMAR_ERROR"
        },
        {
            "question": "I _____ a student.",
            "user_answer": "is",
            "correct_answer": "am",
            "expected_skill": "pronouns",
            "expected_type": "GRAMMAR_ERROR"
        },
        {
            "question": "They _____ from Vietnam.",
            "user_answer": "is",
            "correct_answer": "are",
            "expected_skill": "subject_verb_agreement",
            "expected_type": "GRAMMAR_ERROR"
        }
    ]
    
    print("\n" + "="*70)
    print("🧪 TESTING AI SKILL DETECTION")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['question']}")
        print(f"   User: '{test['user_answer']}' → Correct: '{test['correct_answer']}'")
        print(f"   Expected: {test['expected_type']} / {test['expected_skill']}")
        
        # Analyze with NO skill hint (test AI detection)
        result = await analyzer.analyze(
            question=test['question'],
            user_answer=test['user_answer'],
            correct_answer=test['correct_answer'],
            skill_tag=None  # Force AI to detect
        )
        
        detected_type = result.get("error_type", "")
        detected_skill = result.get("skill_tag", "")
        
        print(f"   Detected: {detected_type} / {detected_skill}")
        
        # Check if detected correctly
        type_match = detected_type == test['expected_type']
        skill_match = detected_skill.lower() in [test['expected_skill'], test['expected_skill'].replace("_", " ")]
        
        if type_match and (skill_match or detected_skill != "general"):
            print(f"   ✅ PASSED")
            passed += 1
        else:
            print(f"   ❌ FAILED")
            if not type_match:
                print(f"      → Error type mismatch: expected {test['expected_type']}, got {detected_type}")
            if detected_skill == "general":
                print(f"      → Skill detection failed: got 'general' instead of specific skill")
            failed += 1
        
        print(f"   Explanation: {result.get('explanation', '')[:100]}...")
    
    print("\n" + "="*70)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed > 0:
        print("\n❌ AI skill detection needs improvement!")
        print("   → Error analyzer may not be parsing LLM response correctly")
        print("   → Or LLM prompt needs to be more specific")
    else:
        print("\n✅ AI skill detection is working!")
        print("   → Ready to use in production")
    print()

if __name__ == "__main__":
    asyncio.run(test_skill_detection())
