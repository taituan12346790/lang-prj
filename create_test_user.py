# create_test_user.py - Create test user in local DB
import asyncio
from sqlalchemy import text
from app.core.database import async_engine
import uuid

async def create_user():
    user_id = "b88f3b13-1cb7-4dee-a636-b712e314421c"
    
    async with async_engine.begin() as conn:
        # Check if user exists in users table
        result = await conn.execute(text(f"""
            SELECT id FROM users WHERE id = '{user_id}'
        """))
        if not result.fetchone():
            print("Creating user in users table...")
            await conn.execute(text(f"""
                INSERT INTO users (id, email, hashed_password, is_active, is_verified)
                VALUES ('{user_id}', 'test_local@example.com', 'hashed_password', true, true)
            """))
            print("✅ User created")
        else:
            print("✅ User already exists")
        
        # Check if profile exists
        result = await conn.execute(text(f"""
            SELECT id FROM user_profiles WHERE user_id = '{user_id}'
        """))
        if not result.fetchone():
            print("Creating user profile...")
            profile_id = str(uuid.uuid4())
            await conn.execute(text(f"""
                INSERT INTO user_profiles (
                    id, user_id, native_language, target_language, 
                    current_level, placement_score, weak_skills, strong_skills,
                    learning_style, interests, goals, preferred_topics,
                    total_sessions, total_conversations, streak_days,
                    onboarding_completed, learning_mode
                )
                VALUES (
                    '{profile_id}', '{user_id}', 'vi', 'English',
                    'A1', 0.0, '{{}}', '{{}}',
                    'balanced', '[]', '[]', '[]',
                    0, 0, 0,
                    true, 'normal'
                )
            """))
            print("✅ User profile created")
            print(f"   target_language: English")
            print(f"   current_level: A1")
        else:
            print("✅ User profile already exists")

asyncio.run(create_user())
