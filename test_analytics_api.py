"""
Test API analytics endpoints directly
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.error_analytics_service import ErrorAnalyticsService
from app.models.user import User
from sqlalchemy import select


async def test_for_user(email: str):
    """Test analytics for specific user"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING ANALYTICS FOR: {email}")
    print('='*60)
    
    async with AsyncSessionLocal() as db:
        # Get user
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"❌ User không tồn tại: {email}")
            return
        
        user_id = str(user.id)
        print(f"✅ User ID: {user_id}")
        print(f"   Email: {user.email}")
        print(f"   Level: {user.level if hasattr(user, 'level') else 'N/A'}")
        
        # Test error_stats API
        print(f"\n📊 TESTING /api/analytics/error-stats")
        error_stats = await ErrorAnalyticsService.get_error_stats(
            db=db,
            user_id=user_id,
            days=30
        )
        print(f"   Response: {error_stats}")
        
        if error_stats.get("total_errors", 0) > 0:
            print(f"   ✅ Có {error_stats['total_errors']} errors")
            print(f"   By type: {error_stats.get('by_type', {})}")
            print(f"   By severity: {error_stats.get('by_severity', {})}")
        else:
            print(f"   ⚠️  Không có error logs (total_errors = 0)")
        
        # Test skill_tags API
        print(f"\n🎯 TESTING /api/analytics/skill-tags")
        top_skills = await ErrorAnalyticsService.get_top_skill_tags(
            db=db,
            user_id=user_id,
            limit=10,
            days=30
        )
        print(f"   Response: {top_skills}")
        
        if top_skills:
            print(f"   ✅ Có {len(top_skills)} skills")
            for skill in top_skills[:5]:
                print(f"      - {skill['skill_tag']}: {skill['count']} lần")
        else:
            print(f"   ⚠️  Không có skill tags")
        
        # Test breakdown
        print(f"\n📈 TESTING skill breakdown")
        breakdown = await ErrorAnalyticsService.get_skill_tag_breakdown(
            db=db,
            user_id=user_id,
            days=30
        )
        print(f"   Response keys: {list(breakdown.keys())}")
        
        if breakdown:
            print(f"   ✅ Có {len(breakdown)} skills trong breakdown")
            for skill, data in list(breakdown.items())[:3]:
                print(f"      - {skill}: {data}")
        else:
            print(f"   ⚠️  Breakdown rỗng")
        
        # Test recent errors
        print(f"\n🕐 TESTING recent errors")
        recent = await ErrorAnalyticsService.get_recent_errors(
            db=db,
            user_id=user_id,
            limit=5
        )
        print(f"   Response count: {len(recent)}")
        
        if recent:
            print(f"   ✅ Có {len(recent)} recent errors")
            for err in recent[:3]:
                print(f"      - [{err['error_type']}] {err['skill_tag']}: {err['user_input']}")
        else:
            print(f"   ⚠️  Không có recent errors")


async def main():
    print("\n🔍 BẮT ĐẦU TEST ANALYTICS API")
    print("="*60)
    
    # Test with fechuwntt@gmail.com (should have 29 errors)
    await test_for_user("fechuwntt@gmail.com")
    
    # Also test with test@example.com (should have 12 errors)
    await test_for_user("test@example.com")
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH TEST")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
