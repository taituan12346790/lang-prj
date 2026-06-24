# ✅ CHECKLIST DEBUG RENDER CHAT ERROR

## 🎯 TÓM TẮT TÌNH HUỐNG
- ✅ Localhost: Hoạt động bình thường
- ❌ Render: Lỗi "Lỗi API: Lỗi khi xử lý chat"
- ✅ Đã push commit `0f20f24` với improved logging
- ✅ Model `openai/gpt-oss-120b` được confirm là đúng

---

## 📋 BƯỚC 1: KIỂM TRA DEPLOY STATUS

### Render Dashboard → Backend Service → Events
- [ ] Deploy status: "Deploy live" (xanh)
- [ ] Không có error trong build process
- [ ] Service đang "Running"

**Nếu deploy chưa xong**: Đợi 2-3 phút rồi refresh

---

## 📋 BƯỚC 2: TEST CHAT VÀ LẤY LOGS

### A. Test từ Frontend
1. Mở frontend Render URL
2. Đăng nhập
3. Gửi 1 chat message đơn giản: "Hello"
4. Chờ response

### B. Lấy logs ngay lập tức
1. Render Dashboard → Backend Service → **Logs**
2. Scroll xuống cuối (logs mới nhất)
3. Tìm các dòng có:
   - `🔍 DEBUG: Using model:`
   - `❌` (emoji X đỏ)
   - `ERROR`
   - `Traceback`
   - `Chat error:`

### C. Copy logs cần thiết
Copy khoảng **20-30 dòng** xung quanh error, ví dụ:

```
[timestamp] 🔍 DEBUG: Using model: openai/gpt-oss-120b
[timestamp] ✅ Loaded 5 messages from DB for session...
[timestamp] ❌ LLM error: Model 'openai/gpt-oss-120b' not found
[timestamp] Chat error: Model 'openai/gpt-oss-120b' not found
[timestamp] Traceback (most recent call last):
  File "/app/routers/chat.py", line XX
  ...
```

---

## 📋 BƯỚC 3: CHECK ENVIRONMENT VARIABLES

### Render Dashboard → Backend Service → Environment

Verify các variables này có đúng không:

### ✅ Required Variables:
- [ ] `GROQ_API_KEY` = `gsk_IiohONM...` (bạn đã có)
- [ ] `DATABASE_URL` = `postgresql+asyncpg://...@...neon.tech/...`
- [ ] `SECRET_KEY` = (bất kỳ string dài nào)
- [ ] `ALGORITHM` = `HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`

### ⚠️ Optional (nhưng nên có):
- [ ] `DEBUG` = `False` (trên production)
- [ ] `ENVIRONMENT` = `production`
- [ ] `LOG_LEVEL` = `INFO`
- [ ] `BACKEND_URL` = URL backend Render của bạn
- [ ] `FRONTEND_URLS` = `["https://your-frontend.onrender.com"]`

### ⚠️ Google OAuth (optional):
- [ ] `GOOGLE_CLIENT_ID`
- [ ] `GOOGLE_CLIENT_SECRET`
- [ ] `GOOGLE_REDIRECT_URI` = `https://your-backend.onrender.com/auth/google/callback`

**Lưu ý**: `DATABASE_URL` phải dùng `postgresql+asyncpg://` chứ không phải `postgresql://`

---

## 📋 BƯỚC 4: CHECK NEON DATABASE

### Neon Dashboard → Your Database

- [ ] Database status: "Active" (không bị suspend)
- [ ] Connection pooling: Enabled
- [ ] Compute: Running

### Test connection từ Render:
Nếu muốn test database connection, có thể SSH vào Render service:

```bash
# Trong Render Shell (nếu có)
python -c "from app.core.database import engine; print('DB OK')"
```

---

## 📋 BƯỚC 5: COMMON ERRORS & FIXES

### ❌ Error: "Model 'openai/gpt-oss-120b' not found"
**Nghĩa là**: Groq không nhận ra model này
**Fix**: 
1. Chạy local test: `python test_groq_connection.py`
2. Nếu local fail → model name sai
3. Check Groq docs: https://console.groq.com/docs/models

### ❌ Error: "Invalid API key" / "Authentication failed"
**Nghĩa là**: GROQ_API_KEY sai hoặc không có
**Fix**:
1. Copy lại API key từ Groq Console
2. Update trong Render Environment variables
3. Redeploy

### ❌ Error: "could not connect to server" / "PostgresError"
**Nghĩa là**: Không kết nối được database
**Fix**:
1. Check DATABASE_URL có đúng format `postgresql+asyncpg://...`
2. Check Neon database có đang active không
3. Check Neon có whitelist IP của Render không (usually auto)

### ❌ Error: "Timeout" / "TimeoutError"
**Nghĩa là**: Request quá lâu
**Fix**:
1. Check Groq API status: https://status.groq.com/
2. Tăng timeout trong Render settings
3. Optimize database queries

### ❌ Error: "ModuleNotFoundError"
**Nghĩa là**: Thiếu dependencies
**Fix**:
1. Check `requirements.txt` có đầy đủ không
2. Manually trigger redeploy từ Render

---

## 🆘 BƯỚC 6: GỬI THÔNG TIN CHO TÔI

### Khi gửi cho tôi, bao gồm:

1. **Error logs từ Render** (20-30 dòng)
2. **Screenshot Environment variables** (có thể blur secret values)
3. **Kết quả chạy local test**:
   ```bash
   python test_groq_connection.py
   ```
4. **Backend URL của bạn trên Render**

### Tôi sẽ:
- ✅ Phân tích error cụ thể
- ✅ Sửa code nếu cần
- ✅ Hoặc hướng dẫn fix environment variables
- ✅ Push fix lên Render

---

## 🎯 QUICK ACTIONS

### Action 1: Test local trước
```bash
cd d:\lang_prj
python test_groq_connection.py
```

Nếu local fail → Vấn đề ở model name hoặc API key
Nếu local OK → Vấn đề ở Render environment

### Action 2: Check logs ngay
1. Render Dashboard
2. Backend Service
3. Logs tab
4. Copy error về cho tôi

### Action 3: Verify environment
1. So sánh `.env` local vs Render Environment
2. Đảm bảo DATABASE_URL format đúng: `postgresql+asyncpg://...`

---

## 📝 NOTES

**Tại sao cần logs?**
- Code đã có logging đầy đủ (commit `0f20f24`)
- Logs sẽ cho biết chính xác lỗi ở đâu
- Không có logs = không thể fix chính xác

**Tôi có thể test gì khi chưa có logs?**
- Test Groq connection local: `python test_groq_connection.py`
- Test database connection local
- Verify environment variables

**Làm sao biết deploy xong?**
- Render Events tab có "Deploy live"
- Logs có dòng mới xuất hiện
- Service status = "Running"

---

## ✅ SUMMARY

1. ✅ Code đã có logging → Chờ deploy
2. ✅ Deploy xong → Test chat
3. ✅ Copy logs → Gửi cho tôi
4. ✅ Tôi analyze → Fix ngay!

**Timeline dự kiến**:
- Deploy: 2-5 phút
- Test + get logs: 1 phút
- Tôi analyze: 2 phút
- Fix: 5-10 phút
- **Total: ~15-20 phút có thể fix xong!**
