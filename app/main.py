# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from loguru import logger

from app.core.config import settings
from app.routers import auth, chat, test, profile, analytics
from app.routers import learning_path, quiz as quiz_router
from app.core.register_tools import register_all_tools
from app.llm.llm_client import get_llm_client
from app.core.database import get_db


# ====================== LIFESPAN EVENTS ======================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # ===== STARTUP =====
    logger.info("🚀 Starting AI Language Tutor...")
    
    try:
        # Lazy-load LLM client on startup (not import time)
        llm_client = get_llm_client()
        register_all_tools(llm_client)
        logger.success("✅ Tools registered successfully")
    except Exception as e:
        logger.error(f"❌ Failed to register tools: {e}")
        raise

    # Seed topics if DB is empty
    try:
        from app.services.topic_service import seed_topics_if_empty
        async for db in get_db():
            await seed_topics_if_empty(db)
            break
        logger.success("✅ Topics seeded/verified")
    except Exception as e:
        logger.warning(f"⚠️  Topic seeding skipped: {e}")
    
    logger.success(
        f"🎉 App initialized | Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}"
    )
    
    yield
    
    # ===== SHUTDOWN =====
    logger.info("🛑 Shutting down AI Language Tutor...")


# ====================== APP INITIALIZATION ======================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Language Tutor - Personalized Language Learning with AI",
    version="0.1.0",
    debug=settings.DEBUG,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# ====================== ROUTE REGISTRATION (MUST BE BEFORE MIDDLEWARE) ======================
# Auth Routes
app.include_router(auth.router, tags=["Authentication"])

# Profile Routes
app.include_router(profile.router, tags=["Profile"])

# Chat Routes
app.include_router(chat.router, tags=["Chat"])

# Test Routes
app.include_router(test.router, tags=["Test & Level"])

# Learning Path Routes
logger.info(f"📌 Registering learning_path router: {learning_path.router}")
logger.info(f"   Router ID: {id(learning_path.router)}")
logger.info(f"   Prefix: {learning_path.router.prefix}")
logger.info(f"   Routes: {len(learning_path.router.routes)}")
for r in learning_path.router.routes:
    if hasattr(r, 'path'):
        logger.info(f"      - {r.path}")
app.include_router(learning_path.router, tags=["Learning Path"])
logger.success("✅ Learning Path routes registered")

# Quiz Routes
app.include_router(quiz_router.router, tags=["Quiz"])

# Analytics Routes
app.include_router(analytics.router, tags=["Analytics"])

# Writing Routes
from app.routers import writing
app.include_router(writing.router, tags=["Writing"])

# AI Exercise Routes
from app.routers import ai_exercise
app.include_router(ai_exercise.router, tags=["AI Exercise"])

# ====================== MIDDLEWARE ======================
# CORS Configuration - Allow Streamlit Cloud and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Local Streamlit
        "https://*.streamlit.app",  # Streamlit Cloud
        "https://streamlit.app",
        "*"  # Allow all (fine for public API)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

# SessionMiddleware - Required for Google OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=False,  # Set True if using HTTPS
)

# ====================== OAUTH TEST PAGE ======================
@app.get("/auth/test")
async def oauth_test_page():
    """Serve OAuth test page"""
    with open("test_oauth.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


# ====================== HEALTH CHECK ENDPOINTS ======================
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Language Tutor API",
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
        "docs": "/docs" if settings.DEBUG else None,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - Enhanced for debugging"""
    import os
    
    health_status = {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "checks": {}
    }
    
    # Check Groq API Key
    groq_key = os.getenv("GROQ_API_KEY")
    health_status["checks"]["groq_api_key"] = "configured" if groq_key else "missing"
    
    # Check Database URL
    db_url = os.getenv("DATABASE_URL")
    health_status["checks"]["database_url"] = "configured" if db_url else "missing"
    
    # Test database connection
    try:
        from app.core.database import get_db
        from sqlalchemy import text
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            health_status["checks"]["database_connection"] = "connected"
            break
    except Exception as e:
        health_status["checks"]["database_connection"] = f"failed: {str(e)}"
        health_status["status"] = "degraded"
    
    # Test Groq API
    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            # Quick test
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            health_status["checks"]["groq_api"] = "working"
        except Exception as e:
            health_status["checks"]["groq_api"] = f"failed: {str(e)[:100]}"
            health_status["status"] = "degraded"
    else:
        health_status["checks"]["groq_api"] = "not_configured"
    
    return health_status


# ====================== GLOBAL EXCEPTION HANDLERS ======================
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
            "type": "http_error"
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation failed",
            "details": exc.errors(),
            "type": "validation_error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler"""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "type": "internal_error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# ====================== RUN DIRECTLY ======================
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=not settings.is_production
    )