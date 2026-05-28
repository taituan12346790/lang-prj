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
from app.routers import auth, chat
from app.core.register_tools import register_all_tools
from app.llm.llm_client import get_llm_client


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


# ====================== MIDDLEWARE ======================
# CORS Configuration - Allow all origins (OAuth needs this for redirects)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OAuth redirects need to work from any origin
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

# ====================== ROUTE REGISTRATION ======================
# Auth Routes
app.include_router(
    auth.router,
    tags=["Authentication"]
)

# Chat Routes (Main AI Interaction)
app.include_router(
    chat.router,
    tags=["Chat"]
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
    """Health check endpoint"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "timestamp": None  # Can add timestamp if needed
    }


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