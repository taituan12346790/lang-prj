"""
Script test để đếm số API calls khi chat
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Counter để đếm calls
api_call_count = 0

# Monkey patch Groq client để đếm calls
import groq
original_create = None

def count_api_call(*args, **kwargs):
    global api_call_count
    api_call_count += 1
    print(f"🔴 API CALL #{api_call_count}")
    return original_create(*args, **kwargs)

# Patch
from app.llm.llm_client import LLMClient
client = LLMClient()

# Monkey patch groq client
if hasattr(client, 'client') and hasattr(client.client, 'chat') and hasattr(client.client.chat, 'completions'):
    original_create = client.client.chat.completions.create
    client.client.chat.completions.create = count_api_call
    print("✅ Patched Groq client to count API calls")

async def test_simple_chat():
    """Test 1 chat đơn giản"""
    global api_call_count
    api_call_count = 0
    
    from app.services.learning_service import LearningService
    from app.core.database import get_db
    from sqlalchemy.ext.asyncio import AsyncSession
    
    print("\n" + "="*50)
    print("TEST: Simple chat")
    print("="*50)
    
    service = LearningService()
    
    # Use dependency injection pattern
    async for db in get_db():
        result = await service.process(
            user_input="Hello, how are you?",
            user_id="b88f3b13-1cb7-4dee-a636-b712e314421c",
            db=db,
            session_id="test-session-001"
        )
        break  # Only use first iteration
    
    print(f"\n{'='*50}")
    print(f"✅ RESULT: {result.get('success')}")
    print(f"🔴 TOTAL API CALLS: {api_call_count}")
    print(f"{'='*50}\n")
    
    return api_call_count

if __name__ == "__main__":
    calls = asyncio.run(test_simple_chat())
    
    if calls > 5:
        print(f"⚠️  WARNING: Too many API calls ({calls})!")
        print("Expected: 1-3 calls")
        print("Actual:", calls)
    else:
        print(f"✅ API calls OK: {calls}")
