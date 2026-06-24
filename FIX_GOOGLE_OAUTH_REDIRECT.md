# 🔧 FIX GOOGLE OAUTH REDIRECT ISSUE

## ❌ VẤN ĐỀ
Sau khi đăng nhập Google, user bị redirect về URL cũ:
- **URL cũ (SAI)**: `https://ai-language-tutor-frontend.onrender.com`
- **URL mới (ĐÚNG)**: `https://aitutorlang.onrender.com`

## ✅ ĐÃ SỬA CODE

### 1. Updated `app/routers/auth.py`
- Thay đổi URL production từ `ai-language-tutor-frontend.onrender.com` → `aitutorlang.onrender.com`
- Thêm hỗ trợ biến môi trường `FRONTEND_URL` để dễ cấu hình

### 2. Updated `app/core/config.py`
- Thêm field `FRONTEND_URL` vào Settings

### 3. Updated `.env`
- Thêm `FRONTEND_URL=http://localhost:8501` cho local testing

---

## 🚀 CÁC BƯỚC CẦN LÀM TRÊN RENDER

### ✅ Bước 1: Update Environment Variable trên Render Backend

1. Vào https://dashboard.render.com/
2. Click vào service **Backend** (`lang-prj-backend`)
3. Click tab **"Environment"**
4. **Thêm biến mới:**
   ```
   Key:   FRONTEND_URL
   Value: https://aitutorlang.onrender.com
   ```
5. Click **"Save Changes"**
6. Backend sẽ tự động restart (~30 giây)

### ✅ Bước 2: Update Google Cloud Console Redirect URIs

1. Vào https://console.cloud.google.com/
2. Chọn project của bạn
3. Menu bên trái → **"APIs & Services"** → **"Credentials"**
4. Click vào **OAuth 2.0 Client ID** mà bạn đang dùng
5. Trong **"Authorized redirect URIs"**, thêm các URI sau:

   **Backend callback URIs** (giữ nguyên):
   ```
   https://lang-prj-backend.onrender.com/api/auth/google/callback
   http://localhost:8000/api/auth/google/callback
   ```

   **Frontend URIs** (KHÔNG CẦN thiết cho OAuth callback, nhưng có thể thêm vào Authorized JavaScript origins):
   ```
   https://aitutorlang.onrender.com
   http://localhost:8501
   ```

6. **XÓA URI cũ** (nếu có):
   ```
   ❌ https://ai-language-tutor-frontend.onrender.com (XÓA)
   ```

7. Click **"Save"**

**LƯU Ý:** OAuth callback luôn đi qua backend (`/api/auth/google/callback`), sau đó backend redirect về frontend với token. Nên chỉ cần đảm bảo **backend callback URI** đúng là đủ.

---

## 🧪 TEST

### Test 1: Check Environment Variable
```bash
# Vào Render Backend service → Shell tab
echo $FRONTEND_URL
# Kết quả mong đợi: https://aitutorlang.onrender.com
```

### Test 2: Test Google OAuth Flow
1. Vào frontend: https://aitutorlang.onrender.com
2. Click **"Đăng nhập bằng Google"**
3. Chọn tài khoản Google
4. **Kiểm tra URL sau khi đăng nhập:**
   - ✅ ĐÚNG: `https://aitutorlang.onrender.com/?token=...`
   - ❌ SAI: `https://ai-language-tutor-frontend.onrender.com/?token=...`

### Test 3: Check Backend Logs
Nếu vẫn lỗi, xem logs:
```
Render Dashboard → Backend service → Logs tab
```

Tìm dòng có "Redirect" hoặc "OAuth" để debug.

---

## 🔍 TROUBLESHOOTING

### ❌ Vẫn redirect về URL cũ
**Nguyên nhân:** Environment variable chưa được load

**Giải pháp:**
1. Kiểm tra lại Render → Environment có `FRONTEND_URL` chưa
2. Manual Deploy để force restart:
   - Render Dashboard → Backend service
   - Click **"Manual Deploy"** → **"Deploy latest commit"**

---

### ❌ Lỗi: "Redirect URI mismatch"
**Nguyên nhân:** Google Console chưa có backend callback URI

**Giải pháp:**
1. Kiểm tra Google Console → Credentials → OAuth Client
2. Đảm bảo có URI: `https://lang-prj-backend.onrender.com/api/auth/google/callback`
3. Save và đợi 1-2 phút để Google update

---

### ❌ Redirect đúng URL nhưng không đăng nhập được
**Nguyên nhân:** Token không hợp lệ hoặc frontend không parse được

**Giải pháp:**
1. Check frontend có parse `?token=...` từ URL không
2. Check backend logs xem token có được tạo không
3. Thử clear cache/cookies và login lại

---

## 📝 CHECKLIST

- [ ] **Code đã update** (DONE - commit changes)
- [ ] **Bước 1**: Thêm `FRONTEND_URL=https://aitutorlang.onrender.com` vào Render backend
- [ ] **Bước 2**: Update Google Console redirect URIs
  - [ ] Giữ backend callback URIs
  - [ ] Xóa frontend URL cũ (nếu có)
- [ ] **Test**: Login Google và kiểm tra URL redirect

---

## 🎯 KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành các bước:
1. User click "Đăng nhập Google" trên `aitutorlang.onrender.com`
2. Redirect đến Google login
3. Chọn tài khoản
4. **Redirect về `aitutorlang.onrender.com/?token=...`** ✅
5. Frontend tự động parse token và đăng nhập user

---

## ⏱️ THỜI GIAN

- Bước 1 (Render env): **1 phút**
- Bước 2 (Google Console): **2 phút**
- Test: **30 giây**

**Tổng: ~4 phút** 🎉

---

## 🚨 QUAN TRỌNG

**Sau khi fix, commit và push code:**
```bash
git add .
git commit -m "Fix: Update Google OAuth redirect to new frontend URL"
git push origin main
```

Render sẽ tự động deploy backend với code mới.

---

**Created:** 2026-06-24
**Status:** ⏳ PENDING - Cần update Render environment variable
