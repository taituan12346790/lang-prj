"""Analyze why so many errors have skill_tag = 'general'"""
import asyncio
from sqlalchemy import select
from app.core.database import get_db
from app.models.error_log import UserErrorLog


async def analyze_general_skills():
    """Check errors with skill_tag = 'general'"""
    async for db in get_db():
        # Get "general" skill errors
        result = await db.execute(
            select(UserErrorLog)
            .where(UserErrorLog.skill_tag == "general")
            .limit(10)
        )
        records = result.scalars().all()
        
        print("\n" + "="*70)
        print("ERRORS WITH skill_tag = 'general' (first 10)")
        print("="*70)
        
        for i, record in enumerate(records, 1):
            print(f"\n[{i}] Error Type: {record.error_type}")
            print(f"  Question: {record.question[:80]}...")
            print(f"  User Input: {record.user_input[:60]}...")
            print(f"  Correct: {record.correct_form[:60]}...")
            print(f"  Skill Tag: {record.skill_tag}")
            
            # Check if AI was used
            if record.extra_data:
                method = record.extra_data.get("analysis_method", "UNKNOWN")
                print(f"  Analysis Method: {method}")
                
                # If AI was used, check if it detected skill
                if method == "AI_CLASSIFICATION":
                    print(f"  → AI classified but still got 'general' skill!")
                elif method == "FALLBACK":
                    print(f"  → Fallback (AI failed, no skill detected)")
        
        print("\n" + "="*70)
        
        # Count by analysis_method
        result2 = await db.execute(
            select(UserErrorLog)
            .where(UserErrorLog.skill_tag == "general")
        )
        all_general_skill = result2.scalars().all()
        
        ai_classified = sum(
            1 for r in all_general_skill 
            if r.extra_data and r.extra_data.get("analysis_method") == "AI_CLASSIFICATION"
        )
        fallback = sum(
            1 for r in all_general_skill 
            if r.extra_data and r.extra_data.get("analysis_method") == "FALLBACK"
        )
        no_method = len(all_general_skill) - ai_classified - fallback
        
        print(f"\nTOTAL skill='general': {len(all_general_skill)}")
        print(f"  AI_CLASSIFICATION: {ai_classified} (AI ran but returned 'general')")
        print(f"  FALLBACK: {fallback} (AI failed)")
        print(f"  NO METHOD: {no_method} (old data or no analysis)")
        print("="*70 + "\n")
        
        break


if __name__ == "__main__":
    asyncio.run(analyze_general_skills())
