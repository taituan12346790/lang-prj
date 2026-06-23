"""Validation script for Round 4 improvements"""
from loguru import logger
import re

def check_css_fixes():
    """Check if CSS fixes are in place"""
    logger.info("Checking CSS fixes...")
    
    with open("streamlit_app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check warning text fix
    if ".stAlert" in content and ".stWarning" in content and "color: white !important" in content:
        logger.info("  ✅ Warning/alert text color fix found")
        css_warning = True
    else:
        logger.error("  ❌ Warning/alert text color fix NOT found")
        css_warning = False
    
    # Check popover dropdown fix
    if "[data-testid=\"stPopover\"] [data-baseweb=\"popover\"]" in content:
        logger.info("  ✅ Popover dropdown text color fix found")
        css_popover = True
    else:
        logger.error("  ❌ Popover dropdown text color fix NOT found")
        css_popover = False
    
    return css_warning and css_popover

def check_auto_resolve():
    """Check if auto-resolve context logic exists"""
    logger.info("Checking auto-resolve context...")
    
    with open("streamlit_app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for AUTO-RESOLVE section
    if "AUTO-RESOLVE" in content and "dashboard_data = api_dashboard()" in content:
        logger.info("  ✅ Auto-resolve context logic found")
        
        # Check if it looks for IN_PROGRESS topics
        if "IN_PROGRESS" in content and "NOT_STARTED" in content:
            logger.info("  ✅ Auto-resolve priority logic (IN_PROGRESS → NOT_STARTED) found")
            return True
        else:
            logger.warning("  ⚠️ Auto-resolve priority logic incomplete")
            return False
    else:
        logger.error("  ❌ Auto-resolve context logic NOT found")
        return False

def check_proactive_message():
    """Check if proactive message includes topic details"""
    logger.info("Checking proactive message improvement...")
    
    with open("streamlit_app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if proactive message uses topic_name_vi and lesson_title
    if "topic_name = context_verify.get(\"topic_name_vi\"" in content and \
       "lesson_title = context_verify.get(\"lesson_title\"" in content:
        logger.info("  ✅ Proactive message uses specific topic/lesson names")
        return True
    else:
        logger.error("  ❌ Proactive message does not use topic/lesson details")
        return False

def check_logging_improvements():
    """Check if logging was improved for debugging"""
    logger.info("Checking logging improvements...")
    
    with open("app/core/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for enhanced logging
    if "Topic:" in content and "Lesson:" in content and "learning_context" in content:
        logger.info("  ✅ Enhanced logging found in pipeline.py")
        return True
    else:
        logger.warning("  ⚠️ Enhanced logging not found in pipeline.py")
        return False

def main():
    logger.info("=" * 60)
    logger.info("ROUND 4 VALIDATION - UX Improvements & Bug Fixes")
    logger.info("=" * 60)
    
    results = {
        "CSS Fixes": check_css_fixes(),
        "Auto-Resolve Context": check_auto_resolve(),
        "Proactive Message": check_proactive_message(),
        "Logging": check_logging_improvements()
    }
    
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for feature, status in results.items():
        status_icon = "✅" if status else "❌"
        logger.info(f"{status_icon} {feature}")
    
    logger.info("=" * 60)
    logger.info(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        logger.info("🎉 All Round 4 improvements validated!")
    else:
        logger.warning(f"⚠️ {total - passed} check(s) failed")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
