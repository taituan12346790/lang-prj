# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone
import logging

from authlib.integrations.starlette_client import OAuth

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token

from app.schemas.auth import (
    UserRegister, 
    UserLogin, 
    LoginResponse, 
    UserResponse
)
from app.models.user import User
from app.models.user_profile import UserProfile


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

logger = logging.getLogger(__name__)

# ====================== GOOGLE OAUTH SETUP ======================
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


# ====================== REGISTER ======================
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        auth_provider="local",
        is_active=True,
        is_verified=True
    )
    db.add(new_user)
    await db.flush()

    new_profile = UserProfile(
        user_id=new_user.id,
        native_language=user_data.native_language,
        target_language=user_data.target_language
    )
    db.add(new_profile)

    await db.commit()
    await db.refresh(new_user)
    return new_user


# ====================== LOGIN ======================
@router.post("/login", response_model=LoginResponse)
async def login_user(
    user_data: UserLogin, 
    db: AsyncSession = Depends(get_db)
):
    normalized_email = user_data.email.lower().strip()
    result = await db.execute(select(User).where(User.email == normalized_email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if user.auth_provider != "local":
        raise HTTPException(
            status_code=401, 
            detail=f"This account uses {user.auth_provider} login. Please use that method."
        )

    if not user.hashed_password or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(last_login=datetime.now(timezone.utc))
    )
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer", "user": user}


# ====================== GOOGLE LOGIN ======================
@router.get("/google")
async def google_login(request: Request):
    """Bắt đầu đăng nhập Google"""
    redirect_uri = f"{settings.BACKEND_URL.rstrip('/')}/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """Xử lý callback từ Google"""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')

        if not user_info or not user_info.get('email'):
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")

        email = user_info.get('email')

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            # Tạo user mới
            user = User(
                email=email,
                full_name=user_info.get('name'),
                avatar_url=user_info.get('picture'),
                google_id=user_info.get('sub'),
                auth_provider="google",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            await db.flush()

            # Create profile with default values - user will be redirected to onboarding
            new_profile = UserProfile(
                user_id=user.id,
                native_language="vi",  # Default, can be changed in onboarding
                target_language="en",  # Default, can be changed in onboarding
                onboarding_completed=False  # Flag to show onboarding
            )
            db.add(new_profile)
        else:
            # User đã tồn tại
            if user.auth_provider != "google":
                logger.warning(f"Email {email} tried to login with Google but registered with {user.auth_provider}")
                raise HTTPException(
                    status_code=409,
                    detail=f"This email is already registered with {user.auth_provider}. "
                           f"Please login with that method first to link accounts."
                )
            
            # Update thông tin
            user.avatar_url = user_info.get('picture')
            user.google_id = user_info.get('sub')

        await db.commit()
        await db.refresh(user)

        access_token = create_access_token(data={"user_id": str(user.id)})

        # Check if user needs onboarding
        profile_result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
        profile = profile_result.scalar_one_or_none()
        
        needs_onboarding = profile and not profile.onboarding_completed

        # Redirect về Streamlit frontend với token
        # Auto-detect frontend URL based on environment
        if settings.ENVIRONMENT == "production":
            streamlit_url = "https://ai-language-tutor-frontend.onrender.com"
        else:
            streamlit_url = "http://localhost:8501"
        
        if needs_onboarding:
            # Redirect to onboarding page
            return RedirectResponse(
                url=f"{streamlit_url}/?token={access_token}&onboarding=true"
            )
        else:
            # Normal redirect
            return RedirectResponse(
                url=f"{streamlit_url}/?token={access_token}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Google callback failed")
        raise HTTPException(status_code=400, detail="Google login failed. Please try again.")


# ====================== SWAGGER ======================
@router.post("/token", response_model=LoginResponse)
async def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return await login_user(user_data, db)