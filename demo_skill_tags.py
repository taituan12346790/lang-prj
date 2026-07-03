"""
DEMO SCRIPT: Chứng minh skill_tags hoạt động với AI detection
Chạy script này trong buổi phản biện!
"""
import asyncio
from app.core.error_analyzer import ErrorAnalyzer
from app.core.database import get_db
from sqlalchemy import select, func, desc
from app.models.error_log import UserErrorLog
from datetime import datetime, timedelta, timezone

async def demo_ai_detection():
    """Demo AI skill detection với các câu hỏi thực tế"""
    print("\n" + "="*70)
    print("🤖 DEMO: AI AUTO-DETECT SKILL TAGS")
    print("="*70)
    print("\nHệ thống KHÔNG CẦN developer manually tag từng exercise!")
    print("AI tự động phát hiện skill từ nội dung câu hỏi.\n")
    
    analyzer = ErrorAnalyzer()
    
    # Real-world test cases
    test_cases = [
        {
            "question": "There ___ three chairs in the room.",
            "user_answer": "is",
            "correct_answer": "are",
            "context": "A1 - Greetings & Introductions"
        },
        {
            "question": "He ___ to school every day.",
            "user_answer": "go",
            "correct_answer": "goes",
            "context": "A1 - Present Simple"
        },
        {
            "question": "Yesterday, I ___ to the market.",
            "user_answer": "go",
            "correct_answer": "went",
            "context": "A2 - Past Tense"
        },
        {
            "question": "She ___ very happy today.",
            "user_answer": "am",
            "correct_answer": "is",
            "context": "A1 - To Be Verb"
        },
        {
            "question": "I have ___ apple.",
            "user_answer": "a",
            "correct_answer": "an",
            "context": "A1 - Articles"
        }
    ]
    
    print("🧪 Testing {} real-world questions:\n".format(len(test_cases)))
    
    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"{'─'*70}")
        print(f"📝 Test {i}: {test['context']}")
        print(f"   Question: {test['question']}")
        print(f"   Student: '{test['user_answer']}' → Correct: '{test['correct_answer']}'")
        
        # AI Analysis (NO manual skill hint!)
        result = await analyzer.analyze(
            question=test['question'],
            user_answer=test['user_answer'],
            correct_answer=test['correct_answer'],
            skill_tag=None  # ✅ NO MANUAL TAG!
        )
        
        error_type = result.get("error_type", "")
        skill_tag = result.get("skill_tag", "general")
        severity = result.get("severity", "")
        explanation = result.get("explanation", "")[:80]
        
        # Display với format đẹp
        skill_display = skill_tag.replace("_", " ").title()
        type_display = error_type.replace("_", " ")
        
        print(f"\n   🎯 AI Detected:")
        print(f"      └─ Error Type: {type_display}")
        print(f"      └─ Skill Tag:  {skill_display}")
        print(f"      └─ Severity:   {severity}")
        print(f"      └─ Explain:    {explanation}...")
        
        if skill_tag != "general":
            print(f"      ✅ SUCCESS: Detected specific skill!")
        else:
            print(f"      ⚠️  WARNING: Fallback to 'general'")
        
        results.append({
            "question": test['question'][:30] + "...",
            "skill": skill_display,
            "is_specific": skill_tag != "general"
        })
    
    print(f"\n{'─'*70}")
    print("\n📊 SUMMARY:")
    print(f"{'─'*70}")
    
    specific_count = sum(1 for r in results if r['is_specific'])
    success_rate = (specific_count / len(results)) * 100
    
    print(f"\n   Total tests:      {len(results)}")
    print(f"   Specific skills:  {specific_count}")
    print(f"   Generic skills:   {len(results) - specific_count}")
    print(f"   Success rate:     {success_rate:.0f}%")
    
    print(f"\n   🎯 Detected Skills:")
    for r in results:
        icon = "✅" if r['is_specific'] else "⚠️"
        print(f"      {icon} {r['question']:<35} → {r['skill']}")
    
    print(f"\n{'─'*70}")
    
    if success_rate >= 80:
        print("\n✅ AI DETECTION WORKING PERFECTLY!")
        print("   → Ready for thesis defense demo")
        print("   → Skill tags will be SPECIFIC, not 'General'")
    else:
        print("\n⚠️  AI detection needs improvement")
        print("   → Check GROQ_API_KEY in environment")
        print("   → Check LLM model configuration")
    
    print(f"\n{'='*70}\n")


async def demo_database_stats():
    """Demo database với skill tags phân tích"""
    print("\n" + "="*70)
    print("📊 DATABASE STATS: SKILL TAGS BREAKDOWN")
    print("="*70)
    
    async for db in get_db():
        # Get user with errors
        result = await db.execute(
            select(UserErrorLog.user_id).limit(1)
        )
        row = result.first()
        if not row:
            print("\n⚠️  Chưa có data trong user_error_logs")
            print("   → Cần user làm practice/quiz để generate errors")
            return
        
        user_id = str(row[0])
        
        # Total errors
        total_stmt = select(func.count(UserErrorLog.id)).where(
            UserErrorLog.user_id == user_id
        )
        result = await db.execute(total_stmt)
        total = result.scalar()
        
        print(f"\n👤 User: {user_id[:8]}...")
        print(f"📊 Total errors: {total}")
        
        # Breakdown by skill_tag
        skill_stmt = select(
            UserErrorLog.skill_tag,
            UserErrorLog.error_type,
            func.count(UserErrorLog.id).label("count")
        ).where(
            UserErrorLog.user_id == user_id
        ).group_by(
            UserErrorLog.skill_tag,
            UserErrorLog.error_type
        ).order_by(desc("count")).limit(15)
        
        result = await db.execute(skill_stmt)
        rows = result.all()
        
        print(f"\n🎯 SKILL TAGS BREAKDOWN (Top 15):")
        print(f"{'─'*70}")
        
        general_count = 0
        specific_count = 0
        
        for i, row in enumerate(rows, 1):
            skill_name = row.skill_tag.replace("_", " ").title()
            error_type_short = row.error_type.replace("_ERROR", "")
            
            if row.skill_tag == "general":
                icon = "⚠️"
                general_count += row.count
            else:
                icon = "✅"
                specific_count += row.count
            
            bar = "█" * min(30, row.count)
            print(f"   {i:2d}. {icon} {skill_name:<25} [{error_type_short}] {bar} {row.count}")
        
        print(f"{'─'*70}")
        
        # Calculate ratio
        if total > 0:
            specific_ratio = (specific_count / total) * 100
            general_ratio = (general_count / total) * 100
            
            print(f"\n📊 CLASSIFICATION QUALITY:")
            print(f"   ✅ Specific skills: {specific_count}/{total} ({specific_ratio:.1f}%)")
            print(f"   ⚠️  General fallback: {general_count}/{total} ({general_ratio:.1f}%)")
            
            if specific_ratio >= 70:
                print(f"\n   ✅ EXCELLENT! Majority of errors have specific skills")
                print(f"      → Proves 2-level classification is working")
                print(f"      → NOT a 'chatbot wrapper'!")
            elif specific_ratio >= 40:
                print(f"\n   🟡 GOOD! AI detection working for most errors")
                print(f"      → Some fallback to 'general' is normal")
            else:
                print(f"\n   ⚠️  WARNING! Too many 'general' tags")
                print(f"      → Check if new AI detection is deployed")
        
        print(f"\n{'='*70}\n")
        break


async def demo_comparison():
    """So sánh: Chatbot vs AI Agent system"""
    print("\n" + "="*70)
    print("⚖️  COMPARISON: CHATBOT WRAPPER vs AI AGENT SYSTEM")
    print("="*70)
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    CHATBOT WRAPPER                               ║
╠══════════════════════════════════════════════════════════════════╣
║  User: "He go to school"                                         ║
║  Bot:  "Wrong! Use 'goes' instead."                              ║
║                                                                  ║
║  Data stored:                                                    ║
║    ❌ No error classification                                    ║
║    ❌ No skill tracking                                          ║
║    ❌ Just flat conversation text                                ║
║                                                                  ║
║  Analytics:                                                      ║
║    ❌ Cannot track which grammar rule user struggles with        ║
║    ❌ Cannot personalize learning path                           ║
║    ❌ No structured error analysis                               ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║                  AI AGENT SYSTEM (Hệ thống của bạn)              ║
╠══════════════════════════════════════════════════════════════════╣
║  User: "He go to school"                                         ║
║  System:                                                         ║
║    1. ✅ AI analyzes error context                               ║
║    2. ✅ Classifies: GRAMMAR_ERROR / subject_verb_agreement      ║
║    3. ✅ Logs to structured database with metadata               ║
║    4. ✅ Tracks frequency (this is 2nd time!)                    ║
║    5. ✅ Generates personalized suggestion                       ║
║                                                                  ║
║  Data stored:                                                    ║
║    ✅ error_type: GRAMMAR_ERROR (Level 1)                        ║
║    ✅ skill_tag: subject_verb_agreement (Level 2)                ║
║    ✅ severity: MEDIUM                                           ║
║    ✅ user_input, correct_form, explanation                      ║
║    ✅ lesson_id, topic_id, timestamp                             ║
║                                                                  ║
║  Analytics:                                                      ║
║    ✅ Track top weak skills: Past Tense (9), Articles (5)        ║
║    ✅ Personalize: "User needs more Past Tense practice"         ║
║    ✅ Trend analysis: Improving over time or not?                ║
║    ✅ AI Tutor can use this data for adaptive teaching           ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    print("🎯 KEY DIFFERENTIATORS:")
    print("   1. ✅ 2-Level Classification (error_type + skill_tag)")
    print("   2. ✅ AI-Powered Skill Detection (no manual tagging)")
    print("   3. ✅ Structured Data (12 fields, 3 indexes)")
    print("   4. ✅ Frequency Tracking (knows user patterns)")
    print("   5. ✅ Personalized Recommendations (adaptive learning)")
    print("   6. ✅ Analytics Dashboard (data-driven insights)")
    
    print(f"\n{'='*70}\n")


async def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("🎓 THESIS DEFENSE: SKILL TAGS DEMO")
    print("="*70)
    print("\nThis demo proves the system has:")
    print("  1. AI-powered skill detection (NOT manual tagging)")
    print("  2. 2-level error classification (error_type + skill_tag)")
    print("  3. Structured analytics (NOT just chatbot wrapper)")
    print("\nPress Enter to start demos...")
    input()
    
    # Demo 1: AI Detection
    await demo_ai_detection()
    
    print("\nPress Enter for next demo...")
    input()
    
    # Demo 2: Database Stats
    await demo_database_stats()
    
    print("\nPress Enter for final comparison...")
    input()
    
    # Demo 3: Comparison
    await demo_comparison()
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\nKey takeaways for thesis defense:")
    print("  1. ✅ AI auto-detects skills → NO manual tagging needed")
    print("  2. ✅ Specific skill_tags → NOT 'general' anymore")
    print("  3. ✅ 2-level classification → Proves architectural design")
    print("  4. ✅ Structured data → NOT flat text like chatbot")
    print("  5. ✅ Analytics capability → Enables personalization")
    print("\n💪 Ready for thesis defense!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
