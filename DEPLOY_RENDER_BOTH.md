# 🚀 Deploy CẢ BACKEND + FRONTEND trên Render

## ✅ **Ưu điểm:**
- ✅ Tất cả trên 1 platform (Render)
- ✅ Không cần Streamlit Cloud (tránh lỗi requirements)
- ✅ Dễ quản lý (1 dashboard)
- ✅ Miễn phí hoàn toàn

---

## 📋 **Bước 1: Deploy Backend (Đã xong)**

Backend đã deploy tại: `https://ai-language-tutor-api-brqj.onrender.com`

---

## 📋 **Bước 2: Deploy Frontend trên Render**

### **Cách 1: Dùng render.yaml (Khuyến nghị)**

1. Vào: https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect repo: `taituan12346790/lang_prj`
4. Render sẽ tự động đọc `render.yaml` và tạo **2 services**:
   - ✅ `ai-language-tutor-api` (Backend - đã có)
   - ✅ `ai-language-tutor-frontend` (Frontend - mới)
5. Click **"Apply"**

---

### **Cách 2: Manual (Nếu Blueprint không hoạt động)**

1. Vào: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo: `taituan12346790/lang_prj`
4. Điền thông tin:

```yaml
Name: ai-language-tutor-frontend
Region: Singapore
Branch: master
Runtime: Python 3

Build Command:
pip install streamlit httpx

Start Command:
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

Environment Variables:
API_BASE_URL = https://ai-language-tutor-api-brqj.onrender.com
```

5. Click **"Create Web Service"**

---

## 🎯 **Kết quả:**

Sau khi deploy xong, bạn sẽ có:

```
✅ Backend API:  https://ai-language-tutor-api-brqj.onrender.com
✅ Frontend UI:  https://ai-language-tutor-frontend.onrender.com
```

**→ Người dùng chỉ cần vào Frontend URL!**

---

## 📊 **Cấu trúc:**

```
┌─────────────────────────────────────────────┐
│  👤 NGƯỜI DÙNG                              │
│     ↓                                       │
│  🌐 ai-language-tutor-frontend             │
│     .onrender.com                           │
│     (Render - Streamlit Frontend)           │
└─────────────────────────────────────────────┘
                    ↓ API Calls
┌─────────────────────────────────────────────┐
│  ⚙️  ai-language-tutor-api-brqj            │
│      .onrender.com                          │
│     (Render - FastAPI Backend)              │
└─────────────────────────────────────────────┘
                    ↓ Database
┌─────────────────────────────────────────────┐
│  🗄️  Neon.tech PostgreSQL                  │
└─────────────────────────────────────────────┘
```

---

## ⏱️ **Timeline:**

- Deploy Backend: ✅ Done
- Deploy Frontend: ~5 phút
- **Total:** ~5 phút

---

## 💰 **Chi phí:**

```
Backend:  Free (Render)
Frontend: Free (Render)
Database: Free (Neon.tech)
───────────────────────
TOTAL:    $0/month
```

---

## 🔧 **Troubleshooting:**

### **Nếu Streamlit không start:**

Thêm flag `--server.headless=true` vào Start Command:
```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### **Nếu CORS error:**

Backend `app/main.py` đã config CORS cho tất cả origins:
```python
allow_origins=["*"]
```

---

## ✅ **Checklist:**

- [x] Backend deployed
- [x] Database migrated
- [ ] Frontend deployed ← **Làm bước này**
- [ ] Test frontend URL
- [ ] Test login/register
- [ ] Test AI chat

---

**Giờ chỉ cần deploy frontend service trên Render là xong!** 🎉
