"""Quick test of error classifier"""
from app.core.error_analyzer import ErrorAnalyzer

analyzer = ErrorAnalyzer()

# Test case 1
result = analyzer._quick_classify(
    question="Yesterday, I ___ to the market.",
    user_answer="go",
    correct_answer="went"
)
print(f"Test 1: {result} (expected: TENSE_MISMATCH)")

# Test case 2
result2 = analyzer._quick_classify(
    question="Last week, she ___ a new car.",
    user_answer="buy",
    correct_answer="bought"
)
print(f"Test 2: {result2} (expected: TENSE_MISMATCH)")

# Test case 3
result3 = analyzer._quick_classify(
    question="He ___ to school every day.",
    user_answer="go",
    correct_answer="goes"
)
print(f"Test 3: {result3} (expected: SUBJECT_VERB_AGREEMENT)")
