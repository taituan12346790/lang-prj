"""
Script kiểm tra xem Phase 1 đã được cài đặt đúng chưa
"""
import sys
import importlib.util


def check_file_exists(filepath, description):
    """Check if file exists"""
    import os
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False


def check_module_import(module_name, description):
    """Check if module can be imported"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {description}: {module_name}")
            return True
        else:
            print(f"❌ {description} NOT FOUND: {module_name}")
            return False
    except Exception as e:
        print(f"❌ {description} ERROR: {e}")
        return False


def check_function_exists(module_path, function_name):
    """Check if function exists in module"""
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, function_name):
            print(f"✅ Function exists: {module_path}.{function_name}")
            return True
        else:
            print(f"❌ Function MISSING: {module_path}.{function_name}")
            return False
    except Exception as e:
        print(f"❌ Module import error: {module_path} - {e}")
        return False


def main():
    print("=" * 60)
    print("🔍 VERIFYING PHASE 1 INSTALLATION")
    print("=" * 60)
    print()
    
    results = []
    
    # 1. Check new service files
    print("📁 Checking new service files...")
    results.append(check_file_exists(
        "app/services/quiz_analytics_service.py",
        "Quiz Analytics Service"
    ))
    results.append(check_file_exists(
        "app/services/ai_context_service.py",
        "AI Context Service"
    ))
    print()
    
    # 2. Check new router
    print("🌐 Checking new router...")
    results.append(check_file_exists(
        "app/routers/analytics.py",
        "Analytics Router"
    ))
    print()
    
    # 3. Check migration script
    print("💾 Checking migration files...")
    results.append(check_file_exists(
        "run_migration.py",
        "Migration Script"
    ))
    results.append(check_file_exists(
        "alembic/versions/002_add_quiz_analytics.py",
        "Alembic Migration"
    ))
    print()
    
    # 4. Check documentation
    print("📚 Checking documentation...")
    results.append(check_file_exists(
        "IMPLEMENTATION_GUIDE.md",
        "Implementation Guide"
    ))
    results.append(check_file_exists(
        "PHASE1_COMPLETE.md",
        "Phase 1 Summary"
    ))
    results.append(check_file_exists(
        "REQUIREMENTS_EVALUATION.md",
        "Requirements Evaluation"
    ))
    print()
    
    # 5. Check if modules can be imported
    print("🔧 Checking module imports...")
    results.append(check_module_import(
        "app.services.quiz_analytics_service",
        "Quiz Analytics Service Import"
    ))
    results.append(check_module_import(
        "app.services.ai_context_service",
        "AI Context Service Import"
    ))
    results.append(check_module_import(
        "app.routers.analytics",
        "Analytics Router Import"
    ))
    print()
    
    # 6. Check key functions
    print("⚙️  Checking key functions...")
    results.append(check_function_exists(
        "app.services.quiz_analytics_service",
        "QuizAnalyticsService"
    ))
    results.append(check_function_exists(
        "app.services.ai_context_service",
        "AIContextService"
    ))
    print()
    
    # 7. Check model updates
    print("📊 Checking model updates...")
    try:
        from app.models.user_topic_progress import UserTopicProgress
        from app.models.user import User
        
        # Check if new fields exist in model definition
        if hasattr(UserTopicProgress, 'weak_skills'):
            print("✅ UserTopicProgress.weak_skills field exists")
            results.append(True)
        else:
            print("❌ UserTopicProgress.weak_skills field MISSING")
            results.append(False)
        
        if hasattr(UserTopicProgress, 'next_review_date'):
            print("✅ UserTopicProgress.next_review_date field exists")
            results.append(True)
        else:
            print("❌ UserTopicProgress.next_review_date field MISSING")
            results.append(False)
        
        if hasattr(User, 'study_streak'):
            print("✅ User.study_streak field exists")
            results.append(True)
        else:
            print("❌ User.study_streak field MISSING")
            results.append(False)
        
        if hasattr(User, 'last_study_date'):
            print("✅ User.last_study_date field exists")
            results.append(True)
        else:
            print("❌ User.last_study_date field MISSING")
            results.append(False)
    except Exception as e:
        print(f"❌ Model check error: {e}")
        results.extend([False] * 4)
    print()
    
    # 8. Summary
    print("=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total checks: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {passed/total*100:.1f}%")
    print()
    
    if failed == 0:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Phase 1 installation is COMPLETE")
        print()
        print("Next steps:")
        print("1. Run: python run_migration.py")
        print("2. Restart backend: python -m uvicorn app.main:app --reload")
        print("3. Restart frontend: streamlit run streamlit_app.py")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print(f"{failed} issue(s) need to be fixed")
        print()
        print("Please review the errors above and fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
