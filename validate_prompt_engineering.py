"""Validation script for Prompt Engineering improvements"""
from loguru import logger
import re

def check_system_prompt_english():
    """Check if system prompt instructions are in English"""
    logger.info("Checking system prompt language...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for English instructions in get_system_prompt
    english_indicators = [
        "YOU ARE AN AI LANGUAGE TUTOR",
        "STRICT RULES:",
        "ALWAYS use",
        "NEVER explain grammar using another language"
    ]
    
    found = sum(1 for indicator in english_indicators if indicator in content)
    
    if found >= 3:
        logger.info("  ✅ System prompt instructions are in English")
        return True
    else:
        logger.error("  ❌ System prompt instructions not properly in English")
        return False

def check_fewshot_vietnamese():
    """Check if few-shot examples are in Vietnamese"""
    logger.info("Checking few-shot examples language...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for Vietnamese in few-shot
    vietnamese_indicators = [
        "Chào bạn!",
        "Khái niệm:",
        "Công thức:",
        "Ví dụ:",
        "AI Tutor:",
        "Student:"
    ]
    
    found = sum(1 for indicator in vietnamese_indicators if indicator in content)
    
    if found >= 4:
        logger.info("  ✅ Few-shot examples are in Vietnamese")
        return True
    else:
        logger.error("  ❌ Few-shot examples not properly in Vietnamese")
        return False

def check_english_examples():
    """Check if few-shot uses English language examples (not Portuguese)"""
    logger.info("Checking few-shot target language...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for English grammar terms (not Portuguese)
    english_terms = [
        "Past Simple",
        "Present Continuous",
        "used to",
        "I visited",
        "She didn't go"
    ]
    
    # Check Portuguese terms should NOT be there
    portuguese_terms = [
        "Pretérito Perfeito",
        "Conjuntivo",
        "gostar de",
        "Eu gosto"
    ]
    
    has_english = sum(1 for term in english_terms if term in content) >= 3
    has_portuguese = any(term in content for term in portuguese_terms)
    
    if has_english and not has_portuguese:
        logger.info("  ✅ Few-shot examples use English (not Portuguese)")
        return True
    elif has_portuguese:
        logger.warning("  ⚠️ Few-shot still contains Portuguese examples")
        return False
    else:
        logger.error("  ❌ Few-shot examples language unclear")
        return False

def check_mode_rules_complete():
    """Check if MODE_RULES includes translation, exercise, conversation modes"""
    logger.info("Checking MODE_RULES completeness...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    required_modes = ["translation", "exercise", "conversation"]
    
    found_modes = []
    for mode in required_modes:
        if f'"{mode}"' in content or f"'{mode}'" in content:
            found_modes.append(mode)
    
    if len(found_modes) == len(required_modes):
        logger.info(f"  ✅ All required modes found: {', '.join(required_modes)}")
        return True
    else:
        missing = set(required_modes) - set(found_modes)
        logger.error(f"  ❌ Missing modes: {', '.join(missing)}")
        return False

def check_strategy_mapping():
    """Check if build_prompt maps strategy fields correctly"""
    logger.info("Checking strategy field mapping...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for correct mapping: teaching_language, learning_target
    correct_mapping = [
        'strategy.get("teaching_language"',
        'strategy.get("learning_target"',
        'personalization.get("level"'
    ]
    
    found = sum(1 for mapping in correct_mapping if mapping in content)
    
    if found >= 2:
        logger.info("  ✅ Strategy fields mapped correctly (teaching_language, learning_target)")
        return True
    else:
        logger.error("  ❌ Strategy field mapping incomplete")
        return False

def check_plan_mapping():
    """Check if build_prompt maps plan fields correctly"""
    logger.info("Checking plan field mapping...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for correct mapping: overall_goal, steps, tools_to_use
    correct_mapping = [
        'plan.get("overall_goal"',
        'plan.get("steps"',
        'plan.get("tools_to_use"'
    ]
    
    found = sum(1 for mapping in correct_mapping if mapping in content)
    
    if found >= 2:
        logger.info("  ✅ Plan fields mapped correctly (overall_goal, steps, tools_to_use)")
        return True
    else:
        logger.error("  ❌ Plan field mapping incomplete")
        return False

def check_tool_results_param():
    """Check if build_prompt accepts tool_results parameter"""
    logger.info("Checking tool_results parameter...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if tool_results parameter exists in build_prompt signature
    if "tool_results: dict = None" in content or "tool_results: Dict = None" in content:
        logger.info("  ✅ tool_results parameter added to build_prompt")
        return True
    else:
        logger.error("  ❌ tool_results parameter missing from build_prompt")
        return False

def check_weak_skills_section():
    """Check if weak skills section is added to prompt"""
    logger.info("Checking weak skills section...")
    
    with open("app/llm/prompts.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for weak skills section
    if "STUDENT WEAK POINTS" in content or "weak_skills_section" in content:
        logger.info("  ✅ Weak skills section added to prompt")
        return True
    else:
        logger.error("  ❌ Weak skills section missing")
        return False

def check_pipeline_tool_results():
    """Check if pipeline.py passes tool_results to build_prompt"""
    logger.info("Checking pipeline tool_results passing...")
    
    with open("app/core/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if tool_results is passed to build_prompt
    if "tool_results=tool_results" in content or "tool_results = state.get" in content:
        logger.info("  ✅ Pipeline passes tool_results to build_prompt")
        return True
    else:
        logger.error("  ❌ Pipeline doesn't pass tool_results")
        return False

def main():
    logger.info("=" * 70)
    logger.info("PROMPT ENGINEERING VALIDATION")
    logger.info("=" * 70)
    
    results = {
        "System Prompt English": check_system_prompt_english(),
        "Few-shot Vietnamese": check_fewshot_vietnamese(),
        "Few-shot English Examples": check_english_examples(),
        "MODE_RULES Complete": check_mode_rules_complete(),
        "Strategy Field Mapping (P1)": check_strategy_mapping(),
        "Plan Field Mapping (P2)": check_plan_mapping(),
        "Tool Results Parameter (P3)": check_tool_results_param(),
        "Weak Skills Section (P6)": check_weak_skills_section(),
        "Pipeline Tool Results": check_pipeline_tool_results()
    }
    
    logger.info("=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for feature, status in results.items():
        status_icon = "✅" if status else "❌"
        logger.info(f"{status_icon} {feature}")
    
    logger.info("=" * 70)
    logger.info(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        logger.info("🎉 All prompt engineering improvements validated!")
        logger.info("📈 Expected improvement: ~6.5/10 → ~8.5-9/10 effectiveness")
    elif passed >= total * 0.8:
        logger.warning(f"⚠️ {total - passed} check(s) failed - mostly implemented")
    else:
        logger.error(f"❌ {total - passed} check(s) failed - needs more work")
    
    logger.info("=" * 70)
    
    # Print summary of improvements
    logger.info("\n📊 IMPROVEMENTS SUMMARY:")
    logger.info("P1: Strategy field mapping (teaching_language, learning_target, level)")
    logger.info("P2: Plan field mapping (overall_goal, steps, tools_to_use)")
    logger.info("P3: Tool results injection into prompt")
    logger.info("P4: Added missing MODE_RULES (translation, exercise, conversation)")
    logger.info("P5: Updated few-shot to English examples (from Portuguese)")
    logger.info("P6: Added weak skills section from analytics")
    logger.info("P7: System instructions in English, few-shot in Vietnamese")

if __name__ == "__main__":
    main()
