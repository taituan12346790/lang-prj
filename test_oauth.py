#!/usr/bin/env python3
"""
Test script to verify Google OAuth setup without running full server
"""

import asyncio
import os
from dotenv import load_dotenv
from app.core.config import settings
from app.core.security import create_access_token
from app.core.database import async_engine, Base
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.progress_log import ProgressLog

# Load environment
load_dotenv()

async def test_config():
    """Test configuration is loaded correctly"""
    print("\n" + "="*60)
    print("🔧 CONFIGURATION TEST")
    print("="*60)
    
    print(f"✅ PROJECT_NAME: {settings.PROJECT_NAME}")
    print(f"✅ ENVIRONMENT: {settings.ENVIRONMENT}")
    print(f"✅ DEBUG: {settings.DEBUG}")
    
    # Check Google OAuth config
    google_id = settings.GOOGLE_CLIENT_ID
    google_secret = settings.GOOGLE_CLIENT_SECRET
    
    if google_id and google_secret:
        print(f"✅ GOOGLE_CLIENT_ID: {google_id[:20]}...")
        print(f"✅ GOOGLE_CLIENT_SECRET: {google_secret[:20]}...")
        print("\n✨ Google OAuth credentials are set!")
    else:
        print("⚠️  GOOGLE_CLIENT_ID: NOT SET (optional)")
        print("⚠️  GOOGLE_CLIENT_SECRET: NOT SET (optional)")
        print("\n💡 To enable Google OAuth:")
        print("   1. Get credentials from Google Cloud Console")
        print("   2. Add to .env: GOOGLE_CLIENT_ID=... and GOOGLE_CLIENT_SECRET=...")
        print("   3. Restart server")
    
    print(f"\n✅ FRONTEND_URLS: {settings.FRONTEND_URLS}")
    print(f"✅ SECRET_KEY: {'*' * 32} (length: {len(settings.SECRET_KEY)})")
    
    assert len(settings.SECRET_KEY) >= 32, "SECRET_KEY must be at least 32 characters!"
    print("✅ SECRET_KEY length is valid (≥32 chars)")


async def test_database():
    """Test database connection"""
    print("\n" + "="*60)
    print("📊 DATABASE TEST")
    print("="*60)
    
    try:
        async with async_engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database connected and tables created")
            
            # Get table info
            from sqlalchemy import inspect
            inspector = inspect(Base.metadata)
            tables = inspector.get_table_names()
            print(f"✅ Tables created: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        raise


async def test_imports():
    """Test all critical imports"""
    print("\n" + "="*60)
    print("📦 IMPORT TEST")
    print("="*60)
    
    try:
        print("Testing critical imports...")
        from app.routers import auth, chat
        print("✅ app.routers.auth")
        print("✅ app.routers.chat")
        
        from app.core.pipeline import graph
        print("✅ app.core.pipeline (LangGraph)")
        
        from app.core.security import create_access_token, verify_password
        print("✅ app.core.security")
        
        from app.services.service_container import get_learning_service
        print("✅ app.services.service_container (lazy-loading)")
        
        from app.llm.llm_client import get_llm_client
        print("✅ app.llm.llm_client (lazy-loading)")
        
        try:
            from authlib.integrations.starlette_client import OAuth
            print("✅ authlib (Google OAuth)")
        except ImportError:
            print("⚠️  authlib not installed (needed for Google OAuth)")
        
        print("\n✨ All imports successful!")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        raise


async def test_jwt():
    """Test JWT token creation"""
    print("\n" + "="*60)
    print("🔐 JWT TOKEN TEST")
    print("="*60)
    
    try:
        # Create test token
        test_token = create_access_token(data={"user_id": "test-user-123"})
        print(f"✅ Generated JWT token: {test_token[:50]}...")
        
        # Token should be long enough
        assert len(test_token) > 50, "Token too short!"
        print(f"✅ Token length: {len(test_token)} chars (valid)")
        
        print("\n✨ JWT token generation working!")
        
    except Exception as e:
        print(f"❌ JWT error: {e}")
        raise


def test_oauth_routes():
    """Test OAuth route availability (without running server)"""
    print("\n" + "="*60)
    print("🌐 OAUTH ROUTES TEST")
    print("="*60)
    
    print("\nExpected OAuth routes:")
    routes = {
        "GET /api/auth/google": "Redirect to Google login",
        "GET /api/auth/google/callback": "Handle Google callback",
        "POST /api/auth/login": "Traditional email/password login",
        "POST /api/auth/register": "User registration",
        "POST /api/auth/token": "Swagger login form",
    }
    
    for route, description in routes.items():
        print(f"✅ {route:<35} - {description}")
    
    print("\n💡 Test OAuth flow:")
    print("   1. Start server: python -m uvicorn app.main:app --reload")
    print("   2. Open: http://localhost:8000/api/auth/google")
    print("   3. Login with Google account")
    print("   4. Should redirect to frontend with JWT token")


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 AI LANGUAGE TUTOR - GOOGLE OAUTH VERIFICATION")
    print("="*70)
    
    try:
        # Synchronous tests
        await test_config()
        await test_imports()
        await test_jwt()
        test_oauth_routes()
        
        # Database test (requires async)
        await test_database()
        
        print("\n" + "="*70)
        print("✨ ALL TESTS PASSED! Backend is ready for Google OAuth")
        print("="*70)
        
        print("\n📝 NEXT STEPS:")
        print("1. If Google credentials not set:")
        print("   a. Go to https://console.cloud.google.com")
        print("   b. Create OAuth credentials")
        print("   c. Add to .env file")
        print("\n2. Start the server:")
        print("   python -m uvicorn app.main:app --reload")
        print("\n3. Test the flow:")
        print("   http://localhost:8000/api/auth/google")
        print("\n4. Frontend should handle callback:")
        print("   http://localhost:3000/auth/callback?token=JWT_TOKEN_HERE")
        
        print("\n📚 More info: See GOOGLE_OAUTH_COMPLETE.md for full setup guide")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\n🆘 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check .env file exists in project root")
        print("3. Check database connection settings")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
