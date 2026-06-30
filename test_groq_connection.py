"""
Script để test Groq API connection và model availability
Chạy script này để verify model 'openai/gpt-oss-120b' có hoạt động không
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_groq_connection():
    """Test Groq API connection"""
    print("=" * 60)
    print("🔍 TESTING GROQ API CONNECTION")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env")
        return False
    
    print(f"✅ GROQ_API_KEY found: {api_key[:20]}...")
    
    # Import Groq
    try:
        from groq import Groq
        print("✅ Groq library imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Groq: {e}")
        return False
    
    # Initialize client
    try:
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return False
    
    # Test model: openai/gpt-oss-120b
    model = "openai/gpt-oss-120b"
    print(f"\n🧪 Testing model: {model}")
    print("-" * 60)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello' in one word."}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Model response: {result}")
        print(f"✅ Model '{model}' is working!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        
        # Check if it's a model not found error
        if "model" in str(e).lower() and "not found" in str(e).lower():
            print("\n💡 Suggestion: Model 'openai/gpt-oss-120b' may not exist in Groq.")
            print("   Try listing available models or check Groq documentation.")
        
        return False


def list_groq_models():
    """Try to list available Groq models"""
    print("\n" + "=" * 60)
    print("📋 ATTEMPTING TO LIST AVAILABLE MODELS")
    print("=" * 60)
    
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        
        # Note: Groq may not have a models.list() method
        # This is just an attempt
        if hasattr(client, "models"):
            if hasattr(client.models, "list"):
                models = client.models.list()
                print("Available models:")
                for model in models:
                    print(f"  - {model.id}")
            else:
                print("⚠️  Groq client doesn't have models.list() method")
        else:
            print("⚠️  Groq client doesn't have 'models' attribute")
            
    except Exception as e:
        print(f"⚠️  Could not list models: {e}")
    
    print("\n💡 Check Groq documentation for available models:")
    print("   https://console.groq.com/docs/models")


def test_alternative_models():
    """Test some common alternative models"""
    print("\n" + "=" * 60)
    print("🔄 TESTING ALTERNATIVE MODELS")
    print("=" * 60)
    
    alternative_models = [
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
    ]
    
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    working_models = []
    
    for model in alternative_models:
        print(f"\n🧪 Testing: {model}")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                temperature=0.7,
                max_tokens=20
            )
            result = response.choices[0].message.content.strip()
            print(f"   ✅ Works! Response: {result[:50]}...")
            working_models.append(model)
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}...")
    
    if working_models:
        print("\n" + "=" * 60)
        print("✅ WORKING MODELS:")
        for model in working_models:
            print(f"   - {model}")
        print("=" * 60)
    
    return working_models


if __name__ == "__main__":
    print("\n🚀 Starting Groq API Test...\n")
    
    # Test main model
    success = test_groq_connection()
    
    if not success:
        # Try listing models
        list_groq_models()
        
        # Test alternatives
        test_alternative_models()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETED")
    print("=" * 60)
    print()
