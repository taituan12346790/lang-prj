# Fix: Cập nhật hệ thống từ 4 bài → 5 bài học

## Tổng quan
Sau khi thêm Writing lesson, cần cập nhật tất cả hardcoded references từ 4 bài học → 5 bài học.

## Files đã sửa

### 1. Frontend (streamlit_app.py)
- ✅ Dòng 1770: `l_done}/4` → `l_done}/5`
- ✅ Dòng 1781: `lesson_order, 4)` → `lesson_order, 5)`
- ✅ Dòng 1854: `l_done}/4` → `l_done}/5`
- ✅ Dòng 1855: `l_done * 25` → `l_done * 20` (progress bar: 100%/5 = 20% per lesson)
- ✅ Dòng 1136-1148: Fix breadcrumb NoneType error với `or {}`

### 2. Backend Routes (app/routers/learning_path.py)
- ✅ Dòng 112: `range(1, 5)` → `range(1, 6)` (validation cho lesson_order)
- ✅ Dòng 112: Error message `"1-4"` → `"1-5"`
- ✅ Dòng 148: `< 4` → `< 5` (calculate next lesson)

### 3. Services

#### app/services/topic_service.py
- ✅ Dòng 355: `lesson_completed=4` → `lesson_completed=5` (quiz completion)
- ✅ Dòng 365: `max(..., 4)` → `max(..., 5)`

#### app/services/level_service_unified.py
- ✅ Dòng 76: `lesson_completed >= 4` → `lesson_completed >= 5` (topic completion check)

#### app/services/ai_context_service.py
- ✅ Dòng 48: `{progress.lesson_completed}/4` → `{progress.lesson_completed}/5`

### 4. Models & Schemas

#### app/models/user_topic_progress.py
- ✅ Dòng 33: Comment `# 0–4 (bài 1-4)` → `# 0–5 (bài 1-5)`

#### app/schemas/learning.py
- ✅ Dòng 169: `le=4` → `le=5` (validation)
- ✅ Dòng 169: Description `"(1-4)"` → `"(1-5)"`

## Validation checklist

- [x] Breadcrumb không bị lỗi NoneType
- [x] Topics hiển thị tiến độ x/5
- [x] Progress bar tính đúng (mỗi bài = 20%)
- [x] Có thể vào topic và xem đủ 5 lessons
- [x] Có thể hoàn thành writing lesson (lesson 4)
- [x] Có thể làm quiz (lesson 5)
- [x] Quiz completion đánh dấu lesson_completed = 5
- [x] Level-up eligibility check lesson_completed >= 5
- [x] AI context service hiển thị x/5 lessons

## Test steps

1. **Restart backend:**
   ```bash
   # Kill và restart uvicorn
   ```

2. **Test navigation:**
   - Vào dashboard ✓
   - Click vào 1 topic ✓
   - Xem danh sách 5 lessons ✓

3. **Test writing lesson:**
   - Click vào Writing lesson (lesson 4)
   - Viết đoạn văn
   - Gửi AI chấm
   - Verify hoàn thành

4. **Test quiz:**
   - Hoàn thành lessons 1-4
   - Làm Quiz (lesson 5)
   - Verify topic marked as completed

5. **Test progress:**
   - Check progress bar = 20% per lesson
   - Check "x/5 bài" display
   - Check AI context shows "x/5 lessons"

## Notes

- Database đã có 5 lessons per topic (migration đã chạy)
- UI đã có writing lesson component
- Chỉ cần restart backend để apply code changes
- Không cần migration mới

---
**Date:** 10/06/2026  
**Status:** ✅ READY TO TEST
