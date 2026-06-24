import asyncio
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model="llama3-70b-8192", temperature=0.7, max_tokens=1500):  # TEMP: Switch to avoid rate limit
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate_async(self, user_input: str, system_prompt: str = "", **kwargs):
        # Accept alias user_prompt for backward compatibility
        if not user_input and kwargs.get("user_prompt"):
            user_input = kwargs["user_prompt"]
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        # DEBUG: Log model being used
        print(f"🔍 DEBUG: Using model: {self.model}")
        
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ LLM error: {e}")
            print(f"❌ Model attempted: {self.model}")
            raise  # Re-raise để error được catch ở router

    async def stream_async(self, user_input: str, system_prompt: str = "", **kwargs):
        """Stream LLM response chunk by chunk (for better UX)"""
        if not user_input and kwargs.get("user_prompt"):
            user_input = kwargs["user_prompt"]
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        print(f"🔍 DEBUG: Streaming with model: {self.model}")
        
        try:
            # Groq supports streaming
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"❌ LLM stream error: {e}")
            raise

    async def generate_structured_async(self, system_prompt, user_prompt, response_format, **kwargs):
        # Tạm thời bỏ qua structured, trả về None để fallback
        return None


# Lazy initialize on first use
_llm_client = None

def get_llm_client():
    """Get or lazily initialize LLM client"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

# For backward compatibility during import
llm_client = None
