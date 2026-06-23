# 🔍 DEBUG GOOGLE LOGIN - UPGRADED

## ✅ CODE MỚI ĐÃ THÊM

### 1. Auto-retry profile fetch
Nếu có token nhưng không có user → tự động fetch profile lại

### 2. Debug info chi tiết trong sidebar
Sidebar giờ sẽ hiện:
```
🔍 page=dashboard
🔍 token=✅
🔍 user=❌  ← NẾU THẤY DẤU X → ĐÂY LÀ VẤN ĐỀ
🔍 profile=❌
```

### 3. Button "Try Reload Profile"
Khi sidebar báo "Session expired", có nút để thử fetch profile lại

---

## 🚀 RESTART STREAMLIT (BẮT BUỘC!)

```bash
# Terminal đang chạy Streamlit:
Ctrl + C

# Chờ 3-5 giây

# Chạy lại:
python -m streamlit run streamlit_app.py --server.port 8501
```

---

## 🧪 TEST VÀ CHO TÔI BIẾT

### Bước 1: Sau khi restart, đăng nhập Google

### Bước 2: Xem sidebar, cho tôi biết CHÍNH XÁC:

```
🔍 page=?        ← Là gì? (dashboard, auth, topic...)
🔍 token=?       ← ✅ hay ❌?
🔍 user=?        ← ✅ hay ❌?  (QUAN TRỌNG!)
🔍 profile=?     ← ✅ hay ❌?
```

### Bước 3: Nếu thấy "⚠️ Session expired"

Sẽ có debug info như:
```
Debug: token=True, user=False, profile=True
```

**Cho tôi biết giá trị này!**

### Bước 4: Click "🔧 Try Reload Profile"

Xem có fix được không?

---

## 🎯 CÁC TRƯỜNG HỢP CÓ THỂ XẢY RA

### Case 1: token=✅, user=❌, profile=✅
**Nguyên nhân**: Profile fetch thành công nhưng không set user
**Fix**: Code mới đã sửa này, nhưng cần restart

### Case 2: token=✅, user=❌, profile=❌
**Nguyên nhân**: Profile API call failed (401, timeout, lỗi backend)
**Fix**: Cần check backend logs

### Case 3: token=❌, user=❌, profile=❌
**Nguyên nhân**: Token không được set từ Google callback
**Fix**: Cần check Google OAuth flow

---

## 📝 TERMINAL LOGS

### Sau khi restart, check terminal Streamlit xem có dòng này không:

```
✅ Profile loaded: your@email.com, user_id=...
```

Nếu thấy:
```
❌ Failed to fetch profile: [error message]
```

→ **CHỤP MÀN HÌNH VÀ GỬI TÔI**

---

## 🔧 NẾU VẪN LỖI

### Thử đăng nhập bằng email/password thay vì Google:

1. Đăng ký account mới (nếu chưa có)
2. Login bằng email/password
3. Xem sidebar có đầy đủ không?

Nếu email/password work nhưng Google không:
→ Vấn đề ở Google OAuth callback

Nếu cả 2 đều không work:
→ Vấn đề ở `_fetch_profile()` hoặc backend

---

## 🎯 THÔNG TIN CẦN GỬI TÔI

1. **Debug info từ sidebar:**
   ```
   🔍 page=?
   🔍 token=?
   🔍 user=?
   🔍 profile=?
   ```

2. **Terminal Streamlit có dòng nào:**
   - `✅ Profile loaded: ...`
   - `❌ Failed to fetch profile: ...`

3. **Browser console (F12) có lỗi không?**

4. **Thử email/password login có work không?**

---

## 🚨 NẾU BACKEND BỊ LỖI

Có thể backend crash, check terminal backend xem có lỗi không:

```bash
# Xem backend có chạy không:
curl http://127.0.0.1:8000/health
```

Nếu không respond → restart backend:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

**RESTART STREAMLIT NGAY VÀ GỬI TÔI DEBUG INFO!** 🔥

Với debug info chi tiết này tôi sẽ biết chính xác vấn đề ở đâu.
