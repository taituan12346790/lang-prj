"""
Script để apply database migration cho analytics features
"""
from sqlalchemy import text
from app.core.database import async_engine
import asyncio


async def run_migration():
    """Apply migration manually"""
    print("🔄 Applying analytics migration...")
    
    async with async_engine.begin() as conn:
        # Check if columns already exist
        try:
            # Add next_review_date to user_topic_progress
            await conn.execute(text("""
                ALTER TABLE user_topic_progress 
                ADD COLUMN IF NOT EXISTS next_review_date TIMESTAMP WITH TIME ZONE
            """))
            print("✅ Added next_review_date to user_topic_progress")
        except Exception as e:
            print(f"⚠️  next_review_date might already exist: {e}")
        
        try:
            # Add weak_skills to user_topic_progress
            await conn.execute(text("""
                ALTER TABLE user_topic_progress 
                ADD COLUMN IF NOT EXISTS weak_skills JSONB
            """))
            print("✅ Added weak_skills to user_topic_progress")
        except Exception as e:
            print(f"⚠️  weak_skills might already exist: {e}")
        
        try:
            # Add study_streak to users
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS study_streak INTEGER DEFAULT 0 NOT NULL
            """))
            print("✅ Added study_streak to users")
        except Exception as e:
            print(f"⚠️  study_streak might already exist: {e}")
        
        try:
            # Add last_study_date to users
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS last_study_date TIMESTAMP WITH TIME ZONE
            """))
            print("✅ Added last_study_date to users")
        except Exception as e:
            print(f"⚠️  last_study_date might already exist: {e}")
    
    print("🎉 Migration completed!")


if __name__ == "__main__":
    asyncio.run(run_migration())
