# 🔐 PHÂN TÍCH CHI TIẾT HỆ THỐNG

## PHẦN 1: BẢO MẬT (SECURITY)

### 1.1. Xác thực (Authentication)

#### **A. Multi-provider Authentication**

**Hỗ trợ 2 phương thức đăng nhập:**

```python
# 1. Local Authentication (Email + Password)
POST /api/auth/register
POST /api/auth/login

# 2. OAuth 2.0 (Google)
GET /api/auth/google
GET /api/auth/google/callback
```

**Quy trình Google OAuth:**
```
1. User click "Login with Google"
2. Redirect to Google consent screen
3. User approve → Google callback with token
4. Backend verify token with Google
5. Create/update user in database
6. Generate JWT token
7. Redirect to frontend with token
```

**Implementation details:**

```python
# app/core/security.py
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()  # Random salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )
```

**Security features:**
- ✅ bcrypt hashing (industry standard)
- ✅ Random salt per password
- ✅ Cost factor: 12 rounds (2^12 = 4096 iterations)
- ✅ Timing attack resistant

---

#### **B. JWT (JSON Web Tokens)**

**Token structure:**
```json
{
  "user_id": "uuid",
  "sub": "uuid",
  "exp": 1719878400,  // Expiration timestamp
  "iat": 1719792000   // Issued at
}
```

**Configuration:**
```python
# app/core/config.py
SECRET_KEY = "..." # 256-bit secret key
ALGORITHM = "HS256"  # HMAC-SHA256
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
```

**Token validation flow:**
```
1. Client sends: Authorization: Bearer <token>
2. OAuth2PasswordBearer extracts token
3. decode_access_token() verifies signature
4. Extract user_id from payload
5. Query database for user
6. Check is_active status
7. Return User object or 401 Unauthorized
```

**Security considerations:**
- ✅ Token có expiration (7 days)
- ✅ Signature verification (prevent tampering)
- ✅ Stateless (không cần session storage)
- ⚠️ Token revocation: Cần implement blacklist nếu scale

---

### 1.2. Phân quyền (Authorization)

**Role-based access (Future - Phase 2):**
```python
# users table
is_active: BOOLEAN  # ✅ Implemented
is_verified: BOOLEAN  # ✅ Implemented
role: VARCHAR  # ❌ Not yet (for admin/teacher roles)
```

**Current implementation:**
```python
# app/core/deps.py
async def get_current_user(token, db):
    # Validate JWT
    # Check is_active
    # Return user or raise 401/403
```

**Access control patterns:**
```python
# Protected endpoint
@router.get("/api/analytics/dashboard")
async def get_analytics(
    current_user: User = Depends(get_current_user)  # ← Dependency injection
):
    # Only authenticated users can access
    return analytics_data
```

---

### 1.3. Bảo mật dữ liệu (Data Security)

#### **A. Database security**

**Connection string security:**
```python
# .env file (NOT in git)
DATABASE_URL=postgresql://user:pass@host/db

# .gitignore
.env
*.env
```

**SQL Injection prevention:**
```python
# ✅ GOOD: Sử dụng SQLAlchemy ORM
result = await db.execute(
    select(User).where(User.email == email)
)

# ❌ BAD: Raw SQL với string concatenation
query = f"SELECT * FROM users WHERE email = '{email}'"
```
