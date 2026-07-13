# test_local_api_count.py - Test API call count locally
"""
Test script để đếm số API calls khi xử lý 1 chat message
"""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Monkey patch Groq client để đếm API calls
original_create = None
api_call_count = 0

def count_api_calls(func):
    """Wrapper để đếm số lần gọi API"""
    async def wrapper(*args, **kwargs):
        global api_call_count
        api_call_count += 1
        print(f"🔴 API CALL #{api_call_count} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        return await func(*args, **kwargs)
    return wrapper

def patch_groq_client():
    """Patch Groq client để đếm API calls"""
    global original_create, api_call_count
    api_call_count = 0
    print("✅ API call counter initialized")

async def test_single_chat():
    """Test 1 chat message và đếm API calls"""
    global api_call_count
    
    # Import sau khi load env
    from app.services.learning_service import LearningService
    from app.core.database import get_db
    
    # Reset counter
    api_call_count = 0
    start_time = datetime.now()
    
    # Test data
    user_id = "b88f3b13-1cb7-4dee-a636-b712e314421c"  # Test user
    user_input = "Chào bạn! Tôi đang học chủ đề 'Mua sắm & Giá cả'"
    
    print("\n" + "="*60)
    print("🧪 TESTING API CALL COUNT")
    print("="*60)
    print(f"User: {user_id}")
    print(f"Input: {user_input}")
    print(f"Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        # Get database session
        async for db in get_db():
            # Patch before creating service
            patch_groq_client()
            
            # Create service
            learning_service = LearningService()
            
            # Track API calls through llm_client
            from app.llm.llm_client import LLMClient
            original_generate = LLMClient.generate_async
            
            async def counted_generate(self, *args, **kwargs):
                global api_call_count
                api_call_count += 1
                print(f"🔴 API CALL #{api_call_count} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
                return await original_generate(self, *args, **kwargs)
            
            LLMClient.generate_async = counted_generate
            
            # Process chat
            print("🚀 Starting chat processing...\n")
            result = await learning_service.process(
                user_id=user_id,
                user_input=user_input,
                db=db
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Results
            print("\n" + "="*60)
            print("📊 TEST RESULTS")
            print("="*60)
            print(f"✅ Chat processed successfully")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print(f"🔴 Total API Calls: {api_call_count}")
            print(f"📝 Response length: {len(result.get('response', ''))}")
            print(f"🛠️  Tools used: {result.get('tools_used', [])}")
            print("="*60)
            
            if api_call_count > 5:
                print(f"\n⚠️  WARNING: {api_call_count} API calls is too high!")
                print("   Expected: 1-3 calls for a simple chat")
                print("   Investigate: retry logic, validation loops, or tool calls")
            else:
                print(f"\n✅ API call count is reasonable ({api_call_count} calls)")
            
            break
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n🔴 API Calls before error: {api_call_count}")

if __name__ == "__main__":
    print("Starting local test...")
    print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY', 'NOT SET')[:20]}...")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:30]}...")
    
    asyncio.run(test_single_chat())
