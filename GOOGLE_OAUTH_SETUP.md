# Hướng Dẫn Cấu Hình Google OAuth

## 📋 TÓM TẮT NHANH

Backend đã có sẵn code Google OAuth. Bạn chỉ cần:
1. Tạo credentials trên Google Cloud Console (5 phút)
2. Thêm 3 environment variables vào Render backend (1 phút)
3. Test login (30 giây)

---

## Bước 1: Tạo Google Cloud Project

1. Truy cập: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"**
3. Điền thông tin:
   - **Project name**: `AI Language Tutor` (hoặc tên khác)
   - **Location**: Để mặc định
4. Click **"Create"**
5. Đợi 10-20 giây để project được tạo

---

## Bước 2: Configure OAuth Consent Screen

1. Trong project vừa tạo, vào menu bên trái → **"APIs & Services"** → **"OAuth consent screen"**
2. Chọn **"External"** (cho phép bất kỳ Gmail nào login)
3. Click **"Create"**
4. Điền thông tin trang 1:
   - **App name**: `AI Language Tutor`
   - **User support email**: Chọn email của bạn
   - **App logo**: Bỏ qua (optional)
   - **App domain**: Bỏ qua (optional)
   - **Authorized domains**: Bỏ qua
   - **Developer contact information**: Email của bạn
5. Click **"Save and Continue"**
6. Trang 2 (Scopes): Click **"Save and Continue"** (không cần thêm gì)
7. Trang 3 (Test users): 
   - Click **"Add Users"**
   - Thêm email của bạn và người test khác (tối đa 100)
   - Click **"Add"**
8. Click **"Save and Continue"**
9. Click **"Back to Dashboard"**

---

## Bước 3: Tạo OAuth 2.0 Credentials

1. Vào **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** (ở trên cùng) → **"OAuth client ID"**
3. Chọn:
   - **Application type**: `Web application`
   - **Name**: `AI Language Tutor Web Client`

4. **Authorized JavaScript origins** (không bắt buộc nhưng nên thêm):
   ```
   https://ai-language-tutor-api-brqu.onrender.com
   http://localhost:8000
   ```

5. **Authorized redirect URIs** - Thêm 2 URIs:
   ```
   https://ai-language-tutor-api-brqu.onrender.com/api/auth/google/callback
   http://localhost:8000/api/auth/google/callback
   ```

6. Click **"Create"**

7. Popup hiện ra với credentials:
   ```
   Your Client ID
   xxxxx-xxxxx.apps.googleusercontent.com
   
   Your Client Secret  
   GOCSPX-xxxxxxxxxxxxx
   ```

8. **⚠️ QUAN TRỌNG**: Copy cả 2 giá trị này và lưu vào notepad
   - Click icon "Copy" bên cạnh mỗi giá trị
   - Paste vào notepad tạm

---

## Bước 4: Thêm Environment Variables vào Render

### 4.1. Vào Backend Service
1. Truy cập: https://dashboard.render.com/
2. Click vào service **"ai-language-tutor-api-brqu"**
3. Click tab **"Environment"** (menu bên trái)

### 4.2. Thêm Variables
Click **"Add Environment Variable"** và thêm lần lượt 3 biến:

**Biến 1:**
```
Key:   GOOGLE_CLIENT_ID
Value: <paste Client ID từ bước 3>
```

**Biến 2:**
```
Key:   GOOGLE_CLIENT_SECRET
Value: <paste Client Secret từ bước 3>
```

**Biến 3:**
```
Key:   BACKEND_URL
Value: https://ai-language-tutor-api-brqu.onrender.com
```

### 4.3. Save & Deploy
1. Click **"Save Changes"** (nút xanh ở trên)
2. Backend sẽ tự động restart (mất ~30 giây)
3. Đợi status chuyển thành **"Live"** (màu xanh)

---

## Bước 5: Test Google OAuth

### 5.1. Test Backend Endpoint
Mở browser và thử:
```
https://ai-language-tutor-api-brqu.onrender.com/api/auth/google
```

**Kết quả mong đợi:**
- Được redirect đến trang đăng nhập Google
- URL có dạng: `accounts.google.com/o/oauth2/v2/auth?...`

**Nếu thấy lỗi:**
- "Missing client_id" → Chưa add environment variables
- "Redirect URI mismatch" → Sai URI trong Google Console

### 5.2. Test Full Flow từ Frontend
1. Vào: `https://ai-language-tutor-frontend.onrender.com`
2. Click **"Đăng nhập bằng Google"**
3. Chọn tài khoản Google
4. Màn hình xác nhận quyền: Click **"Continue"**
5. Sẽ được redirect về frontend với đã đăng nhập

---

## Troubleshooting

### ❌ Lỗi: "Missing required parameter: client_id"
**Nguyên nhân:** Backend chưa có GOOGLE_CLIENT_ID

**Giải pháp:**
1. Kiểm tra lại Render → Environment có 3 biến chưa
2. Restart backend service (Manual Deploy)

---

### ❌ Lỗi: "Redirect URI mismatch"
**Nguyên nhân:** URI trong Google Console khác URI backend sử dụng

**Giải pháp:**
1. Vào Google Console → Credentials → Click vào Client ID vừa tạo
2. Xem **Authorized redirect URIs** có chứa:
   ```
   https://ai-language-tutor-api-brqu.onrender.com/api/auth/google/callback
   ```
3. Nếu không có → Click **"Add URI"** → Paste URI → **"Save"**

---

### ❌ Lỗi: "Access blocked: Authorization Error"
**Nguyên nhân:** App đang ở Testing mode và user chưa được add vào test users

**Giải pháp Option 1 (Nhanh):**
1. Vào Google Console → OAuth consent screen → Test users
2. Click **"Add Users"**
3. Thêm email của người cần test
4. Click **"Save"**

**Giải pháp Option 2 (Lâu hơn - cho production):**
1. Vào Google Console → OAuth consent screen
2. Click **"Publish App"**
3. Google sẽ review app (có thể mất vài ngày)
4. Sau khi approved, bất kỳ ai cũng có thể login

---

### ❌ Lỗi: "This app has not been verified"
**Nguyên nhân:** App đang ở unverified state (bình thường với testing)

**Giải pháp:**
1. Người dùng click **"Advanced"** ở màn hình cảnh báo
2. Click **"Go to AI Language Tutor (unsafe)"**
3. Proceed với login

**Lưu ý:** Chỉ test users (đã add ở Bước 2) mới thấy màn hình này

---

## Backend Code Reference

Backend đã có sẵn code này trong `app/routers/auth.py`:

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    # ... xử lý login/register user
```

**✅ Không cần sửa code gì!** Chỉ cần set environment variables.

---

## Checklist

- [ ] **Bước 1**: Tạo Google Cloud Project
- [ ] **Bước 2**: Configure OAuth Consent Screen
  - [ ] Chọn External
  - [ ] Điền App name, emails
  - [ ] Add test users (email của bạn)
- [ ] **Bước 3**: Tạo OAuth Client ID
  - [ ] Application type: Web application
  - [ ] Add Authorized redirect URIs
  - [ ] Copy Client ID và Client Secret
- [ ] **Bước 4**: Set environment variables trên Render
  - [ ] GOOGLE_CLIENT_ID
  - [ ] GOOGLE_CLIENT_SECRET
  - [ ] BACKEND_URL
- [ ] **Bước 5**: Test
  - [ ] Backend redirect endpoint
  - [ ] Full login flow từ frontend

---

## Notes

- **Free tier**: Google Cloud Console hoàn toàn miễn phí cho OAuth
- **Quota**: Google cho phép unlimited OAuth requests (miễn phí)
- **Testing mode**: Giới hạn 100 test users, đủ cho thesis/demo
- **Production**: Cần submit app review nếu muốn publish công khai (không bắt buộc cho thesis)
- **Security**: Client Secret được lưu an toàn trên Render, không expose ra frontend

---

## Thời Gian Ước Tính

- Bước 1-3 (Google Console): **5 phút**
- Bước 4 (Render config): **1 phút**
- Bước 5 (Test): **30 giây**

**Tổng: ~7 phút** để có Google login hoàn chỉnh! 🎉
