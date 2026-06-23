# 📁 GIẢI THÍCH VỀ MIGRATIONS

## ❓ Tại sao có 2 folders?

Dự án của bạn có **2 folders migrations**:
1. ✅ `migrations/` - **Đang dùng** (chính thức)
2. ❌ `alembic/` - **Backup cũ** (không dùng nữa)

---

## 🔍 Kiểm tra config

Trong file `alembic.ini`:
```ini
script_location = migrations    # ← Dùng migrations/, KHÔNG phải alembic/
version_locations = %(script_location)s/versions
```

➡️ **Kết luận**: Hệ thống đang dùng `migrations/`, không phải `alembic/`

---

## 📦 Files trong mỗi folder

### ✅ `migrations/` (Chính thức - 9 files)
```
migrations/
├── versions/
│   ├── 001_learning_path.py
│   ├── 006_add_sprint_1_learning_context_columns.py
│   ├── 1d22be5d1e48_add_is_verified_to_users_table.py
│   ├── 4aaf052ec0bd_fix_conversation_role_to_string.py
│   ├── 4f6bf87597c2_add_quiz_analytics_and_error_logs.py
│   ├── 860e1ee93883_add_ai_exercises_tables.py
│   ├── c8e5271d513c_add_writing_lesson_to_all_topics.py
│   ├── d35debe1bece_add_user_writings_table.py
│   └── f6c7b58afddd_add_onboarding_completed_to_user_profile.py
├── env.py
├── README
└── script.py.mako
```

### ❌ `alembic/` (Backup cũ - 7 files)
```
alembic/
└── versions/
    ├── 002_add_quiz_analytics.py
    ├── 003_add_error_logs.py
    ├── 004_add_learning_context.py
    ├── 005_add_conversation_context.py
    ├── 006_add_sprint_1_learning_context_columns.py
    ├── 007_add_chat_learning_activities.py
    └── 008_add_writing_lesson.py
```

---

## 🎯 Nên upload gì lên GitHub?

### ✅ UPLOAD (Cần thiết)
- [x] `migrations/` - Folder chính thức
- [x] `alembic.ini` - Config file

### ❌ KHÔNG UPLOAD (Backup cũ)
- [ ] `alembic/` - Đã ignore trong `.gitignore`

---

## 🚨 QUAN TRỌNG: Database Migration khi deploy

Khi deploy lên Render:

### 1. Tạo database trước (Neon.tech)
```bash
# Tạo database trên Neon.tech
# Copy DATABASE_URL
```

### 2. Set environment variable trên Render
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

### 3. Run migrations
Render sẽ tự động chạy migrations khi build:

**Option A: Thêm vào `render.yaml`** (Tự động)
```yaml
buildCommand: |
  pip install -r requirements.txt
  alembic upgrade head
```

**Option B: Manual** (Sau khi deploy)
```bash
# SSH vào Render service
alembic upgrade head
```

---

## 📝 Commands để check migrations

### Check migration history
```bash
alembic history
```

### Check current version
```bash
alembic current
```

### Upgrade to latest
```bash
alembic upgrade head
```

### Downgrade một version
```bash
alembic downgrade -1
```

---

## ⚠️ Lưu ý về `alembic.ini`

File `alembic.ini` có hardcoded DATABASE_URL:
```ini
sqlalchemy.url = postgresql+asyncpg://postgres:fechuwntt123@localhost:5432/langprj_db
```

### 🔒 BẢO MẬT:
1. **ĐỪNG** commit password thật lên GitHub
2. **NÊN** thay bằng placeholder trước khi upload:

```ini
# TRƯỚC KHI UPLOAD, SỬA LẠI:
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/dbname
```

3. Khi deploy, Render sẽ dùng `DATABASE_URL` từ environment variables (không dùng file này)

---

## ✅ Checklist trước khi upload

- [ ] `migrations/` folder có đủ files
- [ ] `alembic.ini` đã remove password thật
- [ ] `alembic/` đã được ignore trong `.gitignore`
- [ ] Test locally: `alembic upgrade head` chạy được

---

## 🔄 Nếu cần merge migrations từ `alembic/` sang `migrations/`

Nếu có migration quan trọng trong `alembic/` chưa có trong `migrations/`:

1. Copy files từ `alembic/versions/` sang `migrations/versions/`
2. Check dependency giữa các migrations
3. Update revision IDs nếu cần
4. Test: `alembic upgrade head`

**Tuy nhiên**, dựa vào tên files, có vẻ đã được merge rồi:
- `alembic/002_add_quiz_analytics.py` → `migrations/4f6bf87597c2_add_quiz_analytics_and_error_logs.py`
- `alembic/008_add_writing_lesson.py` → `migrations/c8e5271d513c_add_writing_lesson_to_all_topics.py`

---

## 📚 Tài liệu tham khảo

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Render Database Migrations](https://render.com/docs/databases)
- [Neon.tech with Alembic](https://neon.tech/docs/guides/alembic)
