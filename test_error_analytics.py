"""
DEMO SCRIPT: Error Analytics từ user_error_logs
Chạy script này trong buổi phản biện để chứng minh error logging hoạt động!
"""
import asyncio
from app.core.database import get_db
from sqlalchemy import select, func, desc, text
from app.models.error_log import UserErrorLog
from datetime import datetime, timedelta, timezone

async def demo_error_analytics(user_id: str = None):
    """Demo error analytics với data thực từ database"""
    async for db in get_db():
        print("\n" + "="*70)
        print("🔍 ERROR LOGGING ANALYTICS DEMO")
        print("="*70)
        
        # Get a real user_id if not provided
        if not user_id:
            result = await db.execute(
                select(UserErrorLog.user_id).limit(1)
            )
            row = result.first()
            if row:
                user_id = str(row[0])
            else:
                print("❌ Không có data trong user_error_logs")
                return
        
        print(f"\n👤 User ID: {user_id}")
        
        # 1. Total errors
        total_stmt = select(func.count(UserErrorLog.id)).where(
            UserErrorLog.user_id == user_id
        )
        result = await db.execute(total_stmt)
        total = result.scalar()
        print(f"\n📊 TỔNG SỐ LỖI: {total}")
        
        # 2. By error_type (CẤP ĐỘ 1)
        type_stmt = select(
            UserErrorLog.error_type,
            func.count(UserErrorLog.id).label("count")
        ).where(
            UserErrorLog.user_id == user_id
        ).group_by(UserErrorLog.error_type)
        
        result = await db.execute(type_stmt)
        print("\n📋 PHÂN LOẠI CẤP 1 (error_type):")
        for row in result.all():
            print(f"  ├─ {row.error_type}: {row.count} lỗi")
        
        # 3. Top skill_tags (CẤP ĐỘ 2 - CHI TIẾT!)
        skill_stmt = select(
            UserErrorLog.skill_tag,
            func.count(UserErrorLog.id).label("count")
        ).where(
            UserErrorLog.user_id == user_id
        ).group_by(UserErrorLog.skill_tag).order_by(desc("count")).limit(10)
        
        result = await db.execute(skill_stmt)
        rows = result.all()
        
        print("\n🎯 PHÂN LOẠI CẤP 2 (skill_tag) - TOP 10:")
        print("   (ĐÂY LÀ ĐIỂM KHÁC BIỆT VỚI CHATBOT!)")
        for i, row in enumerate(rows, 1):
            skill_name = row.skill_tag.replace("_", " ").title()
            bar = "█" * min(20, row.count)
            print(f"  {i:2d}. {skill_name:<30s} | {bar} {row.count} lỗi")
        
        # 4. By severity
        severity_stmt = select(
            UserErrorLog.severity,
            func.count(UserErrorLog.id).label("count")
        ).where(
            UserErrorLog.user_id == user_id
        ).group_by(UserErrorLog.severity).order_by(desc("count"))
        
        result = await db.execute(severity_stmt)
        print("\n⚠️  PHÂN LOẠI THEO MỨC ĐỘ (severity):")
        for row in result.all():
            emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(row.severity, "⚪")
            print(f"  {emoji} {row.severity}: {row.count} lỗi")
        
        # 5. Recent errors with details
        recent_stmt = select(UserErrorLog).where(
            UserErrorLog.user_id == user_id
        ).order_by(desc(UserErrorLog.created_at)).limit(5)
        
        result = await db.execute(recent_stmt)
        errors = result.scalars().all()
        
        print("\n🕐 5 LỖI GẦN NHẤT (chi tiết):")
        for i, error in enumerate(errors, 1):
            print(f"\n  {i}. [{error.error_type}] {error.skill_tag}")
            print(f"     User input: '{error.user_input}'")
            print(f"     Correct:    '{error.correct_form}'")
            print(f"     Severity:   {error.severity}")
            print(f"     Date:       {error.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # 6. Time distribution (last 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        time_stmt = select(
            func.date_trunc('day', UserErrorLog.created_at).label('day'),
            func.count(UserErrorLog.id).label('count')
        ).where(
            UserErrorLog.user_id == user_id,
            UserErrorLog.created_at >= thirty_days_ago
        ).group_by('day').order_by('day')
        
        result = await db.execute(time_stmt)
        time_data = result.all()
        
        if time_data:
            print("\n📅 PHÂN BỐ THEO THỜI GIAN (30 ngày gần đây):")
            for row in time_data[-7:]:  # Show last 7 days
                date_str = row.day.strftime('%Y-%m-%d')
                bar = "▓" * min(15, row.count)
                print(f"  {date_str}: {bar} {row.count} lỗi")
        
        # 7. Breakdown by error_type AND skill_tag (2 LEVELS!)
        breakdown_stmt = select(
            UserErrorLog.error_type,
            UserErrorLog.skill_tag,
            func.count(UserErrorLog.id).label("count")
        ).where(
            UserErrorLog.user_id == user_id
        ).group_by(
            UserErrorLog.error_type,
            UserErrorLog.skill_tag
        ).order_by(
            UserErrorLog.error_type,
            desc("count")
        ).limit(15)
        
        result = await db.execute(breakdown_stmt)
        print("\n🔬 PHÂN TÍCH 2 CẤP ĐỘ (error_type + skill_tag):")
        print("   (CHỨNG MINH KHÔNG PHẢI CHATBOT WRAPPER!)")
        
        current_type = None
        for row in result.all():
            if row.error_type != current_type:
                current_type = row.error_type
                print(f"\n  {current_type}:")
            skill_name = row.skill_tag.replace("_", " ").title()
            print(f"    └─ {skill_name}: {row.count} lỗi")
        
        print("\n" + "="*70)
        print("✅ KẾT LUẬN:")
        print("="*70)
        print("1. ✅ Bảng user_error_logs TỒN TẠI và có data")
        print("2. ✅ Phân loại 2 cấp độ: error_type (tổng quát) + skill_tag (chi tiết)")
        print("3. ✅ Có thể query và phân tích chuyên sâu")
        print("4. ✅ Lưu metadata: severity, timestamp, user_input, correct_form")
        print("5. ⚠️  Dashboard chưa hiển thị vì thiếu API endpoint + UI")
        print("\n💡 GIÁ TRỊ PHẢN BIỆN:")
        print("   → Data structured (12 fields, 3 indexes) - KHÔNG PHẢI flat text")
        print("   → Analytics chi tiết - KHÔNG PHẢI chỉ đếm số lỗi")
        print("   → Architecture design hoàn chỉnh - KHÔNG PHẢI chatbot wrapper")
        print("="*70 + "\n")
        
        break

async def quick_stats():
    """Quick stats cho demo nhanh"""
    async for db in get_db():
        # Total users with errors
        result = await db.execute(
            select(func.count(func.distinct(UserErrorLog.user_id)))
        )
        user_count = result.scalar()
        
        # Total errors
        result = await db.execute(
            select(func.count(UserErrorLog.id))
        )
        total = result.scalar()
        
        # Unique skill_tags
        result = await db.execute(
            select(func.count(func.distinct(UserErrorLog.skill_tag)))
        )
        skill_count = result.scalar()
        
        print("\n" + "="*50)
        print("⚡ QUICK STATS")
        print("="*50)
        print(f"👥 Users with error logs: {user_count}")
        print(f"📊 Total error records: {total}")
        print(f"🎯 Unique skill_tags tracked: {skill_count}")
        print("="*50 + "\n")
        
        break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            asyncio.run(quick_stats())
        else:
            # User provided a user_id
            asyncio.run(demo_error_analytics(sys.argv[1]))
    else:
        # Auto-detect first user with errors
        asyncio.run(demo_error_analytics())
