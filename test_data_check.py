#!/usr/bin/env python3
"""
Simple test to verify test data loading and basic functionality
"""

import sys
sys.path.insert(0, '/d/lang_prj')

try:
    print("Testing test_data module...")
    from app.services.test_data import (
        get_placement_test, 
        get_test_by_level, 
        A1_TEST_QUESTIONS,
        A1_ANSWER_KEY,
        PLACEMENT_TEST_QUESTIONS,
        PLACEMENT_ANSWER_KEY
    )
    from app.schemas.test import Level
    
    # Test A1
    print("\n1️⃣  Testing A1 Level...")
    print(f"   Questions: {len(A1_TEST_QUESTIONS)}")
    print(f"   Answer key: {len(A1_ANSWER_KEY)}")
    
    sample_q = A1_TEST_QUESTIONS[0]
    print(f"   Sample question: {sample_q['question_id']}")
    print(f"   - Question: {sample_q['question'][:50]}...")
    print(f"   - Options: {sample_q['options']}")
    print(f"   - Correct: {A1_ANSWER_KEY.get(sample_q['question_id'])}")
    print("   ✅ A1 data OK")
    
    # Test Placement
    print("\n2️⃣  Testing Placement Test...")
    q, a = get_placement_test()
    print(f"   Questions: {len(q)}")
    print(f"   Answer key: {len(a)}")
    print(f"   Sample: {q[0]['question_id']} → {a.get(q[0]['question_id'])}")
    print("   ✅ Placement data OK")
    
    # Test other levels
    print("\n3️⃣  Testing other levels...")
    for level in [Level.A2, Level.B1, Level.B2, Level.C1, Level.C2]:
        try:
            questions, answers = get_test_by_level(level)
            print(f"   {level.value}: {len(questions)} Q, {len(answers)} A ✅")
        except Exception as e:
            print(f"   {level.value}: ERROR - {e}")
    
    print("\n✨ Basic test data loading works!")
    print("\nNow you should:")
    print("1. Start the server: python -m uvicorn app.main:app --reload")
    print("2. Test endpoints:")
    print("   - GET /api/test/placement/questions")
    print("   - GET /api/test/level/A1/questions")
    print("   - POST /api/test/placement (with auth)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
