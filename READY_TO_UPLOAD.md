# ✅ SẴN SÀNG UPLOAD LÊN GITHUB

## 📋 CHECKLIST HOÀN THÀNH

### ✅ Đã chuẩn bị
- [x] `.gitignore` - Đã ignore files nhạy cảm và backup
- [x] `.env.example` - Template cho environment variables
- [x] `alembic.ini` - Đã xóa password thật, thay bằng placeholder
- [x] `render.yaml` - Config deploy + auto migrations
- [x] `Procfile` - Start command cho Render
- [x] `runtime.txt` - Python version
- [x] `README.md` - Project documentation
- [x] `requirements.txt` - Backend dependencies
- [x] `requirements-frontend.txt` - Frontend dependencies

### ✅ Migrations
- [x] Dùng `migrations/` folder (KHÔNG phải `alembic/`)
- [x] `alembic/` đã được ignore trong `.gitignore`
- [x] `alembic.ini` trỏ đúng vào `migrations/`

### ✅ Security
- [x] File `.env` KHÔNG được upload (có trong `.gitignore`)
- [x] Password trong `alembic.ini` đã xóa
- [x] Các file báo cáo `.txt` đã ignore
- [x] Scripts tiện ích (vietnamize*.py, fix_*.py) đã ignore

---

## 🚀 COMMANDS ĐỂ UPLOAD

### Bước 1: Kiểm tra Git status
```bash
git status
```

**Kết quả mong đợi**: Không thấy `.env`, `*.txt` files, hay `alembic/` folder

### Bước 2: Check files sẽ được upload
```bash
git add --dry-run .
```

### Bước 3: Verify .env KHÔNG có trong git
```bash
git ls-files | grep .env
# Nên trả về rỗng hoặc chỉ .env.example
```

### Bước 4: Add files
```bash
git add .
```

### Bước 5: Commit
```bash
git commit -m "Initial commit: AI Language Tutor with Vietnamese content"
```

### Bước 6: Add remote (nếu chưa có)
```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
```

### Bước 7: Push
```bash
git branch -M main
git push -u origin main
```

---

## 📦 FILES SẼ ĐƯỢC UPLOAD

### ✅ Core Application
```
├── app/                          # Backend code
│   ├── api/
│   ├── core/
│   ├── data/                     # topics_data.py (Vietnamese)
│   ├── llm/
│   ├── memory/
│   ├── models/
│   ├── rag/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── tools/
├── migrations/                   # Database migrations
│   ├── versions/
│   ├── env.py
│   └── README
├── streamlit_app.py             # Frontend
├── requirements.txt
├── requirements-frontend.txt
└── alembic.ini
```

### ✅ Configuration
```
├── .env.example                 # Template (NO real secrets)
├── .gitignore
├── Procfile
├── render.yaml
├── runtime.txt
└── README.md
```

### ❌ FILES BỊ IGNORE (Sẽ KHÔNG upload)
```
├── .env                         # ← QUAN TRỌNG: Không upload!
├── alembic/                     # ← Backup cũ
├── *.txt files                  # ← Báo cáo thesis
├── vietnamize*.py               # ← Scripts tiện ích
├── fix_*.py
├── __pycache__/
└── *.log
```

---

## 🔍 SAU KHI UPLOAD - KIỂM TRA

### 1. Truy cập GitHub repo
```
https://github.com/<your-username>/<repo-name>
```

### 2. Verify các file quan trọng
- [ ] `app/data/topics_data.py` - Content Vietnamese
- [ ] `migrations/` folder có đầy đủ
- [ ] `.env.example` có (nhưng `.env` KHÔNG có)
- [ ] `README.md` hiển thị đúng
- [ ] `render.yaml` và `Procfile` có

### 3. Check NO sensitive data
```bash
# Search for potential secrets in GitHub
# Tìm "fechuwntt123" (password cũ)
# Tìm "gsk_" (GROQ API key prefix)
# Tìm "postgresql://postgres:" (database URLs)
```

### 4. Test clone fresh
```bash
cd ~/temp
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Check .env KHÔNG có
ls -la | grep .env
# Chỉ thấy .env.example

# Check alembic/ KHÔNG có
ls -la | grep alembic
# Chỉ thấy alembic.ini
```

---

## 🎯 TIẾP THEO: DEPLOY LÊN RENDER

### 1. Tạo database trên Neon.tech
Xem hướng dẫn: `NEON_SETUP.md`

### 2. Deploy backend lên Render
Xem hướng dẫn: `DEPLOY_RENDER_GUIDE.md`

### 3. Deploy frontend lên Streamlit Cloud
Xem hướng dẫn: `DEPLOY_RENDER_GUIDE.md` (mục Frontend)

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 🔐 Bảo mật
1. **ĐỪNG BAO GIỜ** commit file `.env` thật
2. **LUÔN** check `git status` trước khi push
3. **XÓA** mọi hardcoded passwords/API keys
4. **SỬ DỤNG** environment variables cho secrets

### 📏 Best practices
1. Commit message rõ ràng và mô tả đúng thay đổi
2. Test local trước khi push
3. Review changes với `git diff` trước commit
4. Keep Git history clean

### 🚫 Nếu đã ACCIDENTALLY upload .env

**BẮT BUỘC phải làm ngay:**

1. **Xóa file khỏi Git history**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

2. **THAY ĐỔI TẤT CẢ SECRETS**
- Generate secret key mới
- Rotate GROQ API key
- Thay database password
- Update all environment variables

3. **Verify cleanup**
```bash
git log --all --full-history -- .env
# Nên trả về empty
```

---

## ✅ DONE!

Sau khi upload xong:
- [x] Code đã lên GitHub
- [x] Không có sensitive data
- [x] Migrations đã setup đúng
- [ ] Ready to deploy to Render
- [ ] Ready to deploy to Streamlit Cloud

**Next step**: Follow `DEPLOY_RENDER_GUIDE.md` để deploy!

---

## 📞 Support

Nếu gặp vấn đề:
1. Check `.gitignore` có đúng
2. Review `git status` output
3. Verify no `.env` in repo
4. Check GitHub repo trực tiếp
