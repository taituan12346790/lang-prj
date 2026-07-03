"""Debug user profile issue"""
import asyncio
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile

async def check():
    async for db in get_db():
        # Get latest user
        result = await db.execute(select(User).order_by(User.created_at.desc()).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ No users found")
            break
            
        print(f"✓ Latest user: {user.email}")
        print(f"  ID: {user.id}")
        
        # Check profile
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user.id)
        )
        profile = result.scalar_one_or_none()
        
        if profile:
            print(f"✓ Profile exists:")
            print(f"  Current level: {profile.current_level}")
            print(f"  Skills: {profile.skills}")
        else:
            print("❌ No profile found for this user!")
            print("💡 Creating profile...")
            
            profile = UserProfile(
                user_id=user.id,
                current_level="A1",
                skills={"listening": 1, "speaking": 1, "reading": 1, "writing": 1}
            )
            db.add(profile)
            await db.commit()
            print("✅ Profile created successfully!")
        
        break

if __name__ == "__main__":
    asyncio.run(check())
