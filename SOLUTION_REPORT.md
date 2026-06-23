# 🔧 GIẢI PHÁP CHO LỖI 404 "NOT FOUND" - DASHBOARD VÀ TOPICS

## ❌ HIỆN TRẠNG

User báo lỗi khi truy cập dashboard và topics từ Streamlit frontend:
- **Lỗi**: `Not Found` 404 
- **Endpoints bị lỗi**:
  - `GET /api/learning/dashboard`
  - `GET /api/learning/topics/{level}`

## ✅ ĐÃ KIỂM TRA

### 1. Database ✓
- ✅ PostgreSQL có 190 topics (A1-C2)
- ✅ 760 lessons (4 lessons/topic)
- ✅ Phân bố đúng: A1(20), A2(25), B1(30), B2(35), C1(40), C2(40)

### 2. Backend Code ✓
- ✅ Router `learning_path.py` có 6 routes
- ✅ Router prefix: `/api/learning`
- ✅ Routes được define đúng trong router
- ✅ TopicService có eager loading (selectinload) - đã fix greenlet error
- ✅ main.py import router đúng
- ✅ main.py include_router được gọi
- ✅ Logs show "✅ Learning Path routes registered"

### 3. Dependencies ✓
- ✅ `get_current_user` dependency hoạt động (login thành công)
- ✅ JWT token được tạo đúng
- ✅ Authorization header được gửi đúng

### 4. Testing ✓
- ✅ Backend server running trên port 8000
- ✅ `/health` endpoint hoạt động
- ✅ `/api/auth/register` hoạt động
- ✅ `/api/auth/login` hoạt động
- ✅ Test với token hợp lệ vẫn trả về 404

## 🔍 PHÁT HIỆN VẤN ĐỀ

**Router ĐƯỢC REGISTER nhưng endpoints VẪN trả về 404!**

Các test cho thấy:
1. Router object tồn tại và có 6 routes
2. `app.include_router()` được gọi thành công
3. Logs confirm router đã registered
4. Nhưng khi gọi endpoint → 404 Not Found
5. OpenAPI spec (`/api/openapi.json`) KHÔNG chứa learning endpoints

## 🎯 NGUYÊN NHÂN

Có khả năng là một trong các vấn đề sau:

### Giả thuyết 1: Schema Response Model Issues
Router sử dụng Pydantic schemas phức tạp:
```python
@router.get("/dashboard", response_model=DashboardResponse)
```

Nếu schema có vấn đề → FastAPI có thể skip route khi build OpenAPI schema.

### Giả thuyết 2: Dependency Injection Order
Endpoint sử dụng 2 dependencies:
```python
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
```

Có thể có conflict trong dependency resolution.

### Giả thuyết 3: Import Time Side Effects
Khi import `learning_path` module, có thể có exception xảy ra nhưng bị suppress.

## 💡 GIẢI PHÁP ĐỀ XUẤT

### Bước 1: Kiểm Tra Schema Issues
Thử loại bỏ `response_model` tạm thời để xem endpoint có register không:

```python
# Thử thay đổi trong app/routers/learning_path.py
@router.get("/dashboard")  # Bỏ response_model
async def get_dashboard(...):
    result = await _svc.get_dashboard(current_user.id, db)
    return result  # Return dict thay vì schema object
```

### Bước 2: Test Route Đơn Giản
Thêm 1 route test không có dependency:

```python
@router.get("/test-simple")
async def test_simple():
    return {"status": "ok", "message": "Learning Path router is working!"}
```

### Bước 3: Kiểm Tra Schema Imports
Verify tất cả schemas trong `app/schemas/learning.py`:
- DashboardResponse
- TopicResponse  
- LevelProgressResponse
- etc.

Đảm bảo không có circular imports hoặc missing fields.

### Bước 4: Debug với Exception Handler
Thêm try-catch khi include router:

```python
try:
    app.include_router(learning_path.router, tags=["Learning Path"])
    logger.success("✅ Learning Path routes registered")
except Exception as e:
    logger.error(f"❌ Failed to register learning_path: {e}")
    import traceback
    traceback.print_exc()
```

### Bước 5: Kiểm Tra FastAPI Version Compatibility
Có thể là bug với FastAPI version. Check:
```bash
pip list | grep fastapi
```

Nếu cần, thử downgrade/upgrade:
```bash
pip install "fastapi==0.104.1" --force-reinstall
```

## 📝 TIẾP THEO

Tôi đề xuất thực hiện theo thứ tự:

1. **NGAY BÂY GIỜ**: Add simple test endpoint để confirm router hoạt động
2. **SAU ĐÓ**: Check schemas có issue không
3. **CuỐI CÙNG**: Debug dependencies nếu vẫn chưa được

---

**Ngày tạo**: 2026-06-03  
**Status**: 🔴 Đang troubleshoot
