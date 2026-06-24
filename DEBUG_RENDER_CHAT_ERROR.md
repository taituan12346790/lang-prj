# 🔍 DEBUG RENDER CHAT ERROR - Hướng dẫn kiểm tra lỗi

## ✅ Đã làm gì?

### Commit `0f20f24` - Cải thiện error logging:

1. **Trong `app/routers/chat.py`**:
   - ✅ Thêm `logger.exception(e)` để log full traceback
   - ✅ Thêm detail message trong HTTPException để thấy error message
   
2. **Trong `app/llm/llm_client.py`**:
   - ✅ Thêm `print(f"🔍 DEBUG: Using model: {self.model}")` 
   - ✅ Thêm `print(f"❌ LLM error: {e}")` khi có lỗi
   - ✅ Re-raise exception để error được catch ở router
   - ✅ Model vẫn là `openai/gpt-oss-120b` (đã revert lại)

## 🎯 Bước tiếp theo: Kiểm tra Render Logs

### 1. Truy cập Render Dashboard
   - Đăng nhập vào https://dashboard.render.com
   - Chọn service **Backend API** (không phải Frontend)

### 2. Xem Logs
   - Click vào tab **Logs** ở menu bên trái
   - Đợi deploy mới hoàn tất (commit `0f20f24`)
   - Thử gửi chat message từ frontend

### 3. Tìm kiếm trong logs

Sau khi gửi chat, tìm các dòng log này:

#### ✅ Logs bình thường (nếu hoạt động):
```
🔍 DEBUG: Using model: openai/gpt-oss-120b
✅ Loaded X messages from DB for session...
✅ Learning context loaded: ...
```

#### ❌ Logs lỗi (cần tìm):
```
❌ LLM error: ...
Chat error: ...
Traceback (most recent call last):
  ...
```

## 🔎 Các lỗi phổ biến cần check

### A. Lỗi Groq API
```
AuthenticationError: Invalid API key
ModelNotFoundError: Model 'openai/gpt-oss-120b' not found
RateLimitError: Rate limit exceeded
```

**Cách fix**: 
- Check GROQ_API_KEY trong Render Environment
- Verify model name đúng với Groq docs

### B. Lỗi Database Connection
```
could not connect to server
asyncpg.exceptions.PostgresError
ConnectionRefusedError
```

**Cách fix**:
- Check DATABASE_URL trong Render Environment
- Verify Neon database có allow connections từ Render không
- Check Neon database có đang suspend không (free tier)

### C. Lỗi Timeout
```
asyncio.TimeoutError
TimeoutError: Query timeout
Request timeout
```

**Cách fix**:
- Tăng timeout trong Render service settings
- Check database performance trên Neon

### D. Lỗi Import/Module
```
ModuleNotFoundError: No module named 'X'
ImportError: cannot import name 'Y'
```

**Cách fix**:
- Check `requirements.txt` có đầy đủ dependencies chưa
- Re-deploy từ Render Dashboard

## 📋 Checklist môi trường Render

### Environment Variables cần có:
- [ ] `GROQ_API_KEY` - API key từ Groq
- [ ] `DATABASE_URL` - Connection string từ Neon
- [ ] `SECRET_KEY` - Secret key cho JWT
- [ ] `ALGORITHM=HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- [ ] `GOOGLE_CLIENT_ID` (optional)
- [ ] `GOOGLE_CLIENT_SECRET` (optional)
- [ ] `FRONTEND_URLS` - Frontend URL của Render
- [ ] `BACKEND_URL` - Backend URL của Render

### Cách kiểm tra Environment Variables:
1. Render Dashboard → Backend Service
2. Tab **Environment** ở menu bên trái
3. Xem danh sách variables có đầy đủ không

## 🆘 Nếu vẫn không thấy lỗi

### Option 1: Thêm logging mạnh hơn
Chạy commands này ở local:

```bash
# Thêm logging vào learning_service.py
git add .
git commit -m "Add more debug logging"
git push origin master
```

### Option 2: Test trực tiếp API endpoint
Dùng curl hoặc Postman để test:

```bash
curl -X POST https://your-backend.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_input": "Hello",
    "session_id": "test-123"
  }'
```

### Option 3: Check Render service status
1. Render Dashboard → Backend Service
2. Tab **Events** - xem có error trong quá trình deploy không
3. Tab **Metrics** - xem CPU/Memory có spike không

## 📝 Ghi chú

**Tại sao localhost work nhưng Render fail?**

Có thể do:
1. ❌ Environment variables khác nhau
2. ❌ Database connection settings khác nhau (Neon có thể block connections)
3. ❌ Network timeout khác nhau
4. ❌ Python version khác nhau
5. ❌ Dependencies version conflict

**Next steps**:
1. ✅ Xem Render logs để tìm error message cụ thể
2. ✅ Share logs với tôi để analyze
3. ✅ Fix based on error type

---

## 🎯 ACTION ITEMS CHO BẠN:

### Bước 1: Đợi deploy xong
- Check Render Dashboard → Events
- Đợi đến khi thấy "Deploy live"

### Bước 2: Test chat
- Mở frontend trên Render
- Thử gửi 1 chat message
- Nếu lỗi → sang bước 3

### Bước 3: Copy logs
- Vào Render Dashboard → Backend Service → Logs
- Tìm dòng có "❌" hoặc "ERROR" hoặc "Traceback"
- Copy toàn bộ error message (khoảng 20-30 dòng)
- Share với tôi

### Bước 4: Tôi sẽ fix dựa trên logs
- Dựa vào error message cụ thể
- Sửa code hoặc environment variables
- Push fix lên Render

---

**Tóm tắt**: Giờ code đã có logging đầy đủ. Bạn chỉ cần:
1. Đợi Render deploy xong
2. Test chat
3. Copy error logs từ Render
4. Share với tôi → Tôi sẽ fix ngay!
