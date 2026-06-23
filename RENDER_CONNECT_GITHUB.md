# 🔗 KẾT NỐI GITHUB VỚI RENDER

## ❌ Vấn đề: Không thấy repo trên Render

Khi tạo Web Service mới trên Render và search repo, không thấy `taituan12346790/lang-prj` xuất hiện.

---

## ✅ Giải pháp

### Option 1: Kiểm tra Credentials
1. Trong search box, có dropdown **"Credentials (1)"** 
2. Click vào dropdown đó
3. Chọn đúng tài khoản GitHub: `taituan12346790`
4. Repo sẽ xuất hiện

### Option 2: Kết nối lại GitHub
1. Vào **Account Settings** (góc trên cùng, avatar)
2. Chọn **"Account"** → **"Connected Accounts"**
3. Tìm **GitHub** section
4. Click **"Connect GitHub"** hoặc **"Reconnect"**
5. Authorize Render truy cập repos của bạn
6. Quay lại trang tạo Web Service

### Option 3: Cấp quyền cho Render
1. Vào GitHub: https://github.com/settings/installations
2. Tìm **Render** trong danh sách installed apps
3. Click **Configure**
4. Trong **Repository access**:
   - Chọn **"Only select repositories"**
   - Thêm `lang-prj` vào danh sách
   - Hoặc chọn **"All repositories"**
5. Click **Save**
6. Quay lại Render và refresh

### Option 4: Dùng Public Git Repository
Nếu vẫn không thấy, thử:
1. Click tab **"Public Git Repository"** 
2. Paste URL: `https://github.com/taituan12346790/lang-prj`
3. Click **Connect**

---

## 🔍 Kiểm tra repo có public không

Repo phải **public** hoặc Render phải có quyền truy cập:

1. Vào: https://github.com/taituan12346790/lang-prj
2. Check góc trên: **Public** hay **Private**?
3. Nếu **Private**: 
   - Render cần được authorize (Option 3)
   - Hoặc đổi sang Public: Settings → Danger Zone → Change visibility

---

## 📋 Checklist

- [ ] Repo `lang-prj` tồn tại trên GitHub
- [ ] Repo là **Public** hoặc Render có quyền truy cập
- [ ] GitHub account đã connect với Render
- [ ] Chọn đúng credentials trong dropdown
- [ ] Render app đã được authorize trên GitHub

---

## 🚀 Sau khi thấy repo

1. Click vào `taituan12346790/lang-prj`
2. Click **Connect**
3. Tiếp tục setup:
   - **Name**: `ai-language-tutor-api`
   - **Branch**: `master`
   - **Root Directory**: để trống
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Add Environment Variables:
   - `DATABASE_URL` - Neon PostgreSQL URL
   - `GROQ_API_KEY` - Your Groq API key
   - `SECRET_KEY` - Generate bằng: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `ALGORITHM=HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=30`

5. Click **Create Web Service**

---

## 🆘 Nếu vẫn không được

**Screenshot và gửi:**
1. Trang Render search repos
2. GitHub repo page (`https://github.com/taituan12346790/lang-prj`)
3. GitHub Settings → Installed GitHub Apps → Render

**Hoặc dùng Manual Deploy:**
- Deploy bằng Docker
- Hoặc dùng Render Blueprint (render.yaml)
