"""
Copy ALL error logs from local to production
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from loguru import logger

from app.models.error_log import UserErrorLog


async def copy_errors():
    """Copy errors from local to production"""
    
    # Local database
    local_url = "postgresql+asyncpg://postgres:fechuwntt123@localhost:5432/langprj_db?prepared_statement_cache_size=0"
    
    # Production database
    prod_url = "postgresql+asyncpg://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?ssl=require&prepared_statement_cache_size=0"
    
    # Connect to local
    local_engine = create_async_engine(local_url, echo=False)
    local_session = sessionmaker(local_engine, class_=AsyncSession, expire_on_commit=False)
    
    # Connect to production
    prod_engine = create_async_engine(prod_url, echo=False)
    prod_session = sessionmaker(prod_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with local_session() as local_sess:
        # Get all errors from local
        stmt = select(UserErrorLog)
        result = await local_sess.execute(stmt)
        local_errors = result.scalars().all()
        
        logger.info(f"📊 Found {len(local_errors)} errors in LOCAL database")
        
        # Get existing IDs in production
        async with prod_session() as prod_sess:
            stmt = select(UserErrorLog.id)
            result = await prod_sess.execute(stmt)
            existing_ids = {row[0] for row in result.all()}
            
            logger.info(f"📊 Found {len(existing_ids)} errors already in PRODUCTION")
            
            # Copy new errors
            new_count = 0
            for error in local_errors:
                if error.id not in existing_ids:
                    # Create new error in production
                    new_error = UserErrorLog(
                        id=error.id,
                        user_id=error.user_id,
                        error_type=error.error_type,
                        skill_tag=error.skill_tag,
                        severity=error.severity,
                        user_input=error.user_input,
                        user_answer=error.user_answer,
                        correct_form=error.correct_form,
                        question=error.question,
                        lesson_id=error.lesson_id,
                        topic_id=error.topic_id,
                        explanation=error.explanation,
                        suggestion=error.suggestion,
                        extra_data=error.extra_data,
                        created_at=error.created_at
                    )
                    prod_sess.add(new_error)
                    new_count += 1
                    
                    if new_count % 10 == 0:
                        logger.info(f"  Copied {new_count} errors...")
            
            await prod_sess.commit()
            
            logger.success(f"\n✅ Copied {new_count} NEW errors to PRODUCTION")
            logger.info(f"📊 Total errors in PRODUCTION now: {len(existing_ids) + new_count}")
    
    await local_engine.dispose()
    await prod_engine.dispose()


if __name__ == "__main__":
    asyncio.run(copy_errors())
