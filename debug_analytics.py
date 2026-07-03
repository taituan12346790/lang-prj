"""
Debug script to check why Analytics shows 0
Kiểm tra:
1. Có data trong user_error_logs không?
2. API endpoints có hoạt động không?
3. User_id có đúng không?
"""
import asyncio
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.error_log import UserErrorLog
from app.models.user import User
from datetime import datetime, timedelta, timezone


async def check_error_logs():
    """Kiểm tra dữ liệu trong bảng user_error_logs"""
    print("=" * 60)
    print("1️⃣  KIỂM TRA DỮ LIỆU ERROR LOGS")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Count total errors
        total_stmt = select(func.count(UserErrorLog.id))
        total_result = await db.execute(total_stmt)
        total = total_result.scalar()
        
        print(f"\n📊 Tổng số error logs trong database: {total}")
        
        if total == 0:
            print("⚠️  KHÔNG CÓ DỮ LIỆU ERROR LOGS!")
            print("    → Người dùng chưa làm bài tập nào có lỗi")
            print("    → Hoặc hệ thống chưa log lỗi")
            return
        
        # Get all users with errors
        users_stmt = select(
            UserErrorLog.user_id,
            func.count(UserErrorLog.id).label("count")
        ).group_by(UserErrorLog.user_id)
        
        users_result = await db.execute(users_stmt)
        users = users_result.all()
        
        print(f"\n👥 Số người dùng có error logs: {len(users)}")
        for user_row in users:
            user_id = user_row.user_id
            count = user_row.count
            
            # Get user email
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            email = user.email if user else "Unknown"
            print(f"   • {email}: {count} errors")
        
        # Check recent errors (last 30 days)
        print("\n📅 Kiểm tra lỗi trong 30 ngày gần đây:")
        since_date = datetime.now(timezone.utc) - timedelta(days=30)
        
        for user_row in users:
            user_id = user_row.user_id
            
            # Get user email
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            email = user.email if user else "Unknown"
            
            # Count errors in last 30 days
            recent_stmt = select(func.count(UserErrorLog.id)).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            )
            recent_result = await db.execute(recent_stmt)
            recent_count = recent_result.scalar()
            
            print(f"   • {email}: {recent_count} errors (30 ngày)")
            
            if recent_count > 0:
                # Show top skill tags
                skill_stmt = select(
                    UserErrorLog.skill_tag,
                    func.count(UserErrorLog.id).label("count")
                ).where(
                    UserErrorLog.user_id == user_id,
                    UserErrorLog.created_at >= since_date
                ).group_by(UserErrorLog.skill_tag).limit(5)
                
                skill_result = await db.execute(skill_stmt)
                skills = skill_result.all()
                
                print(f"     Top skills:")
                for skill_row in skills:
                    print(f"       - {skill_row.skill_tag}: {skill_row.count} lần")


async def test_api_query():
    """Test query giống như API endpoint"""
    print("\n" + "=" * 60)
    print("2️⃣  TEST API QUERY")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Get all users
        users_stmt = select(User)
        users_result = await db.execute(users_stmt)
        users = users_result.scalars().all()
        
        print(f"\n👤 Danh sách users trong hệ thống:")
        for user in users:
            print(f"   • {user.email} (ID: {user.id})")
        
        # Test with first user
        if users:
            test_user = users[0]
            user_id = str(test_user.id)
            
            print(f"\n🧪 Test API query với user: {test_user.email}")
            print(f"   User ID: {user_id}")
            
            # Simulate API query (from ErrorAnalyticsService.get_error_stats)
            days = 30
            since_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Total errors
            total_stmt = select(func.count(UserErrorLog.id)).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            )
            total_result = await db.execute(total_stmt)
            total = total_result.scalar() or 0
            
            print(f"\n   📊 Query result: {total} errors")
            
            if total > 0:
                # By error_type
                type_stmt = select(
                    UserErrorLog.error_type,
                    func.count(UserErrorLog.id).label("count")
                ).where(
                    UserErrorLog.user_id == user_id,
                    UserErrorLog.created_at >= since_date
                ).group_by(UserErrorLog.error_type)
                
                type_result = await db.execute(type_stmt)
                by_type = {row.error_type: row.count for row in type_result.all()}
                
                print(f"   📋 By error_type: {by_type}")
                
                # Top skills
                skill_stmt = select(
                    UserErrorLog.skill_tag,
                    func.count(UserErrorLog.id).label("count")
                ).where(
                    UserErrorLog.user_id == user_id,
                    UserErrorLog.created_at >= since_date
                ).group_by(UserErrorLog.skill_tag).order_by(
                    func.count(UserErrorLog.id).desc()
                ).limit(5)
                
                skill_result = await db.execute(skill_stmt)
                top_skills = skill_result.all()
                
                print(f"   🎯 Top 5 skills:")
                for skill_row in top_skills:
                    print(f"       - {skill_row.skill_tag}: {skill_row.count} lần")
            else:
                print(f"   ⚠️  KHÔNG CÓ DỮ LIỆU cho user này!")


async def check_quiz_data():
    """Kiểm tra xem có dữ liệu quiz không"""
    print("\n" + "=" * 60)
    print("3️⃣  KIỂM TRA DỮ LIỆU QUIZ")
    print("=" * 60)
    
    from app.models.exercise_result import ExerciseResult
    
    async with AsyncSessionLocal() as db:
        # Count total quiz results
        total_stmt = select(func.count(ExerciseResult.id))
        total_result = await db.execute(total_stmt)
        total = total_result.scalar()
        
        print(f"\n📝 Tổng số quiz results: {total}")
        
        if total == 0:
            print("⚠️  KHÔNG CÓ DỮ LIỆU QUIZ!")
            return
        
        # Get users with quiz data
        users_stmt = select(
            ExerciseResult.user_id,
            func.count(ExerciseResult.id).label("count"),
            func.sum(func.cast(ExerciseResult.is_correct, func.INTEGER)).label("correct")
        ).group_by(ExerciseResult.user_id)
        
        users_result = await db.execute(users_stmt)
        users = users_result.all()
        
        print(f"\n👥 Số người dùng đã làm quiz: {len(users)}")
        for user_row in users:
            user_id = user_row.user_id
            count = user_row.count
            correct = user_row.correct or 0
            
            # Get user email
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            email = user.email if user else "Unknown"
            accuracy = (correct / count * 100) if count > 0 else 0
            
            print(f"   • {email}: {count} bài tập ({accuracy:.0f}% đúng)")


async def main():
    """Main function"""
    print("\n🔍 BẮT ĐẦU KIỂM TRA ANALYTICS")
    print("=" * 60)
    
    await check_error_logs()
    await test_api_query()
    await check_quiz_data()
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH KIỂM TRA")
    print("=" * 60)
    print("\n💡 KẾT LUẬN:")
    print("   - Nếu 'Tổng số error logs' = 0 → Chưa có dữ liệu lỗi")
    print("   - Nếu 'Tổng số quiz results' = 0 → Chưa có dữ liệu bài tập")
    print("   - Analytics chỉ hiển thị nếu CÓ DỮ LIỆU!")
    print("   - User cần làm bài tập VÀ có lỗi thì mới có error logs")
    print()


if __name__ == "__main__":
    asyncio.run(main())
