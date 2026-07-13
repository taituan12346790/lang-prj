# Quick test ExerciseGenerator with real LLM call
import asyncio
from app.llm.llm_client import LLMClient
from app.tools.exercise_generator import ExerciseGenerator

async def test():
    print("Testing ExerciseGenerator with 1 API call...")
    
    llm = LLMClient()
    generator = ExerciseGenerator(llm)
    
    # Track calls
    call_count = 0
    original_generate = llm.generate_async
    
    async def counted_generate(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"  🔴 API Call #{call_count}")
        return await original_generate(*args, **kwargs)
    
    llm.generate_async = counted_generate
    
    # Test
    result = await generator.generate_async(
        topic="Shopping",
        cefr_level="A1",
        num_exercises=3,
        lesson_type="exercise_only"
    )
    
    print(f"\n✅ Result: {len(result.get('exercises', []))} exercises")
    print(f"🔴 Total API Calls: {call_count}")
    
    if call_count <= 1:
        print("✅ PASS: Only 1 API call")
    else:
        print(f"❌ FAIL: {call_count} API calls (expected 1)")

asyncio.run(test())
