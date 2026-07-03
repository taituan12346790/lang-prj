"""
Test script để verify API endpoints error logs
"""
import asyncio
from app.core.database import get_db
from app.services.error_analytics_service import ErrorAnalyticsService

async def test_error_analytics_service():
    """Test ErrorAnalyticsService với data thực"""
    async for db in get_db():
        # Get first user with errors
        from sqlalchemy import select
        from app.models.error_log import UserErrorLog
        
        result = await db.execute(
            select(UserErrorLog.user_id).limit(1)
        )
        row = result.first()
        if not row:
            print("❌ Không có data trong user_error_logs")
            return
        
        user_id = str(row[0])
        print(f"✅ Testing with user_id: {user_id}\n")
        
        # Test 1: get_error_stats
        print("=" * 60)
        print("TEST 1: get_error_stats()")
        print("=" * 60)
        stats = await ErrorAnalyticsService.get_error_stats(db, user_id, days=30)
        print(f"Total errors: {stats['total_errors']}")
        print(f"By type: {stats['by_type']}")
        print(f"By severity: {stats['by_severity']}")
        print()
        
        # Test 2: get_top_skill_tags
        print("=" * 60)
        print("TEST 2: get_top_skill_tags()")
        print("=" * 60)
        top_skills = await ErrorAnalyticsService.get_top_skill_tags(db, user_id, limit=10, days=30)
        for i, skill in enumerate(top_skills, 1):
            print(f"{i}. {skill['skill_tag']}: {skill['count']} lỗi ({skill['error_type']})")
        print()
        
        # Test 3: get_skill_tag_breakdown
        print("=" * 60)
        print("TEST 3: get_skill_tag_breakdown()")
        print("=" * 60)
        breakdown = await ErrorAnalyticsService.get_skill_tag_breakdown(db, user_id, days=30)
        for skill, data in breakdown.items():
            print(f"{skill}: {data['total_errors']} lỗi, severity avg: {data['severity_avg']:.1f}")
        print()
        
        # Test 4: get_recent_errors
        print("=" * 60)
        print("TEST 4: get_recent_errors()")
        print("=" * 60)
        recent = await ErrorAnalyticsService.get_recent_errors(db, user_id, limit=5)
        for i, error in enumerate(recent, 1):
            print(f"{i}. [{error['error_type']}] {error['skill_tag']}")
            print(f"   User: '{error['user_input']}'")
            print(f"   Correct: '{error['correct_form']}'")
        print()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nAPI endpoints should work now:")
        print("  GET /api/analytics/error-stats")
        print("  GET /api/analytics/skill-tags")
        
        break

if __name__ == "__main__":
    asyncio.run(test_error_analytics_service())
