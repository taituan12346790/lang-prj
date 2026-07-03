# KẾ HOẠCH SỬA ERROR LOGGING (NẾU CÒN THỜI GIAN)

## 🔍 CHẨN ĐOÁN VẤN ĐỀ

### Bước 1: Kiểm tra database
```bash
# Kết nối PostgreSQL
psql -U your_username -d your_database

# Kiểm tra bảng có tồn tại không
\dt user_error_logs

# Nếu không có, chạy migration
cd d:\lang_prj
alembic upgrade head
```

### Bước 2: Test model
```python
# Tạo file test_error_log.py
import asyncio
from app.models.error_log import UserErrorLog
from app.core.database import get_db

async def test_create_error_log():
    async for db in get_db():
        error_log = UserErrorLog(
            user_id="some-uuid",  # Thay bằng UUID thực tế
            error_type="GRAMMAR_ERROR",
            skill_tag="present_simple",
            user_input="He go to school",
            correct_form="He goes to school",
            severity="HIGH",
            explanation="Thiếu -s cho ngôi thứ 3 số ít"
        )
        db.add(error_log)
        await db.commit()
        print("✅ Error log created successfully!")
        break

asyncio.run(test_create_error_log())
```

---

## ⚡ SỬA NHANH (30 PHÚT - 1 GIỜ)

### Option 1: Làm cho Demo hoạt động

**File cần sửa: `app/routers/quiz.py` hoặc `app/routers/learning.py`**

```python
from app.models.error_log import UserErrorLog
from app.services.error_service import ErrorService

@router.post("/submit-answer")
async def submit_answer(
    question_id: str,
    user_answer: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ... logic kiểm tra đáp án ...
    
    if user_answer != correct_answer:
        # LOG LỖI TẠI ĐÂY!
        error_service = ErrorService(db)
        await error_service.log_error(
            user_id=current_user.id,
            error_data={
                "error_type": "GRAMMAR_ERROR",  # Hoặc phân loại tự động
                "skill_tag": question.skill_tag,
                "user_input": user_answer,
                "correct_form": correct_answer,
                "question": question.text,
                "severity": "MEDIUM"
            }
        )
    
    return {"correct": user_answer == correct_answer}
```

### Option 2: Tạo Dummy Data cho Demo

```python
# create_dummy_errors.py
import asyncio
from datetime import datetime, timedelta
from app.models.error_log import UserErrorLog
from app.core.database import get_db

async def create_dummy_errors(user_id):
    async for db in get_db():
        errors = [
            {
                "error_type": "GRAMMAR_ERROR",
                "skill_tag": "present_simple",
                "user_input": "He go to school",
                "correct_form": "He goes to school",
                "severity": "HIGH",
                "created_at": datetime.now() - timedelta(days=5)
            },
            {
                "error_type": "GRAMMAR_ERROR",
                "skill_tag": "present_simple",
                "user_input": "She don't like apples",
                "correct_form": "She doesn't like apples",
                "severity": "HIGH",
                "created_at": datetime.now() - timedelta(days=3)
            },
            {
                "error_type": "VOCABULARY_ERROR",
                "skill_tag": "articles",
                "user_input": "I want to be teacher",
                "correct_form": "I want to be a teacher",
                "severity": "MEDIUM",
                "created_at": datetime.now() - timedelta(days=1)
            },
        ]
        
        for error_data in errors:
            error_log = UserErrorLog(user_id=user_id, **error_data)
            db.add(error_log)
        
        await db.commit()
        print(f"✅ Created {len(errors)} dummy error logs")
        break

# Chạy với user_id thật
asyncio.run(create_dummy_errors("your-user-uuid"))
```

---

## 📊 DASHBOARD QUERY (Cho Demo)

```python
# app/routers/analytics.py

@router.get("/error-stats")
async def get_error_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Query top errors
    query = """
        SELECT 
            skill_tag, 
            COUNT(*) as count,
            AVG(CASE WHEN severity='HIGH' THEN 3 
                     WHEN severity='MEDIUM' THEN 2 
                     ELSE 1 END) as avg_severity
        FROM user_error_logs
        WHERE user_id = :user_id
        GROUP BY skill_tag
        ORDER BY count DESC
        LIMIT 10
    """
    
    result = await db.execute(text(query), {"user_id": current_user.id})
    errors = result.fetchall()
    
    return {
        "top_errors": [
            {
                "skill": row[0],
                "count": row[1],
                "avg_severity": float(row[2])
            }
            for row in errors
        ]
    }
```

---

## 🎬 DEMO SCRIPT (NẾU SỬA XONG)

### Scenario 1: Live Demo
1. Đăng nhập vào hệ thống
2. Làm một bài tập → Trả lời SAI
3. Mở pgAdmin hoặc psql
4. Show query:
   ```sql
   SELECT error_type, skill_tag, created_at 
   FROM user_error_logs 
   WHERE user_id = 'current-user-id'
   ORDER BY created_at DESC 
   LIMIT 5;
   ```
5. "Đây là bằng chứng hệ thống đã log lỗi có cấu trúc!"

### Scenario 2: Show Code Only
1. Mở file `app/models/error_log.py`
2. Giải thích từng trường
3. Mở file `app/services/error_service.py`
4. Giải thích logic
5. "Đây là thiết kế, đang trong quá trình integrate"

---

## 🛡️ NẾU KHÔNG CÒN THỜI GIAN SỬA

**Dùng slide/diagram thay thế:**

```
┌─────────────────────────────────────────┐
│   ERROR LOGGING ARCHITECTURE            │
│                                          │
│  User Answer (Wrong)                     │
│         ↓                                │
│  Error Analyzer Agent                    │
│         ↓                                │
│  ┌──────────────────────────────┐       │
│  │ user_error_logs Table        │       │
│  ├──────────────────────────────┤       │
│  │ id (UUID)                    │       │
│  │ user_id                      │       │
│  │ error_type: GRAMMAR_ERROR    │       │
│  │ skill_tag: present_simple    │       │
│  │ user_input: "He go..."       │       │
│  │ correct_form: "He goes..."   │       │
│  │ severity: HIGH               │       │
│  │ explanation: "..."           │       │
│  │ created_at: timestamp        │       │
│  └──────────────────────────────┘       │
│         ↓                                │
│  Analytics Dashboard                     │
│  (Query by skill_tag, time range)       │
└─────────────────────────────────────────┘
```

**Nói:** 
> "Đây là architecture em đã thiết kế. Code đã có, đang trong quá trình debug integration. Đây là minh chứng rõ ràng không phải 'web + chatbot' đơn giản."

---

## ✅ CHECKLIST TRƯỚC PHẢN BIỆN

- [ ] Migration đã chạy: `alembic current` (xem có migration 003 không)
- [ ] Bảng đã tồn tại: `\dt user_error_logs` trong psql
- [ ] Model import OK: Không có lỗi khi chạy app
- [ ] Nếu không sửa kịp: Chuẩn bị diagram/slide backup
- [ ] Thuộc lòng cách giải thích "design vs implementation"

---

## 🎯 MỤC TIÊU TỐI THIỂU

**KHÔNG cần:**
- ❌ 100% features hoạt động
- ❌ Perfect integration

**CHỈ cần:**
- ✅ Chứng minh được ARCHITECTURE DESIGN
- ✅ Show được CODE ĐÃ VIẾT
- ✅ Giải thích được TẠI SAO thiết kế như vậy

**Remember:** 
> "Đồ án tốt nghiệp đánh giá khả năng THIẾT KẾ, không phải khả năng debug nhanh!"

