"""Seed topics to production database"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.topic_service import seed_topics_if_empty

async def main():
    print("🌱 Seeding topics to production database...")
    async for db in get_db():
        await seed_topics_if_empty(db)
        print("✅ Topics seeded successfully!")
        break

if __name__ == "__main__":
    # Set production DATABASE_URL
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8.c-2.ap-southeast-1.aws.neon.tech/neondb?ssl=require"
    asyncio.run(main())
