# 🧪 HƯỚNG DẪN TEST UI CHANGES

## 🎯 Mục đích
Kiểm tra 2 cải tiến UI mới:
1. Chữ form đăng nhập màu đen dễ đọc
2. Chức năng logout hoạt động

---

## 🚀 CÁCH TEST

### Bước 1: Khởi động hệ thống

```bash
# Terminal 1: Backend (nếu chưa chạy)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
streamlit run streamlit_app.py
```

Browser tự động mở: **http://localhost:8501**

---

### Bước 2: Test Form Đăng Nhập

#### 2.1 Kiểm tra Input Text

1. Ở trang đăng nhập, click vào ô **Email**
2. Gõ: `test@example.com`

**✅ PASS nếu:**
- Chữ bạn gõ màu **ĐEN** (không phải trắng)
- Background ô input màu **TRẮNG** hoặc gần trắng
- Chữ rõ ràng, dễ đọc

**❌ FAIL nếu:**
- Chữ vẫn màu trắng
- Khó đọc

#### 2.2 Kiểm tra Password Field

1. Click vào ô **Mật khẩu**
2. Gõ: `testpass123`

**✅ PASS nếu:**
- Hiển thị dấu chấm đen `•••` (không phải trắng)
- Background trắng
- Dễ phân biệt

#### 2.3 Kiểm tra Tab "Đăng ký"

1. Click tab **"Đăng ký"**
2. Điền thông tin:
   - Email: `newuser@test.com`
   - Họ tên: `Test User`
   - Password: `password123`
   - Xác nhận: `password123`

**✅ PASS nếu:**
- Tất cả text input màu đen
- Select box (Tiếng mẹ đẻ, Học tiếng) có chữ đen

#### 2.4 Test Select Box

1. Click dropdown **"Tiếng mẹ đẻ"**
2. Chọn "vi"

**✅ PASS nếu:**
- Dropdown list có background trắng
- Chữ trong list màu đen
- Dễ đọc

---

### Bước 3: Test Logout

#### 3.1 Đăng nhập

1. Dùng tài khoản đã có hoặc đăng ký mới
2. Email: `test@example.com`
3. Password: `testpass123`
4. Click **"Đăng nhập"**

**✅ PASS nếu:**
- Chuyển đến Dashboard
- Sidebar xuất hiện bên trái

#### 3.2 Kiểm tra Sidebar

**Sidebar phải hiển thị:**

```
┌─────────────────────┐
│ 👤 Tài khoản        │
│ ──────────────────  │
│ Test User           │ ← Tên bạn
│ 📧 test@example.com │ ← Email bạn
│ 🎯 Level: A1        │ ← Level badge
│ ──────────────────  │
│ 📚 Điều hướng       │
│ [🏠 Dashboard]      │
│ [📖 Chủ đề học]     │
│ [💬 Chat AI]        │
│ ──────────────────  │
│ [🚪 Đăng xuất]      │ ← NÚT LOGOUT
└─────────────────────┘
```

**✅ PASS nếu:**
- Hiển thị đúng tên và email
- Level badge có màu (xanh lá cho A1)
- Các nút hiển thị rõ ràng

#### 3.3 Test Navigation

1. Click nút **"📖 Chủ đề học"**

**✅ PASS nếu:**
- Chuyển sang trang Topics List
- Sidebar vẫn hiển thị

2. Click nút **"🏠 Dashboard"**

**✅ PASS nếu:**
- Quay lại Dashboard
- Sidebar vẫn ở đó

#### 3.4 Test Logout Function

1. Ở bất kỳ page nào (Dashboard, Topics, etc.)
2. Click nút **"🚪 Đăng xuất"** trong sidebar

**✅ PASS nếu:**
- Hiển thị thông báo: "Đã đăng xuất thành công!"
- Tự động chuyển về trang Login
- Sidebar biến mất
- Không thể quay lại Dashboard bằng nút Back

**❌ FAIL nếu:**
- Không có gì xảy ra
- Vẫn ở trang cũ
- Có lỗi hiển thị

#### 3.5 Verify Logout Complete

1. Thử truy cập trực tiếp: change page to "dashboard" bằng cách gõ trong URL bar (nếu có)

**✅ PASS nếu:**
- Tự động redirect về Login
- Session đã cleared

2. Đăng nhập lại

**✅ PASS nếu:**
- Có thể login bình thường
- Sidebar hiển thị lại

---

### Bước 4: Test Trên Nhiều Pages

#### 4.1 Dashboard
- ✅ Sidebar có logout button

#### 4.2 Topics List
1. Từ Dashboard, click **"Xem toàn bộ chủ đề"**
2. Check sidebar

**✅ PASS nếu:**
- Sidebar vẫn hiển thị
- Logout button vẫn ở đó

#### 4.3 Topic Detail
1. Click vào 1 topic bất kỳ
2. Check sidebar

**✅ PASS nếu:**
- Sidebar hiển thị
- Can logout

#### 4.4 Chat Page
1. Từ sidebar, click **"💬 Chat AI"**
2. Check sidebar

**✅ PASS nếu:**
- Sidebar hiển thị
- Logout works

---

## 📋 CHECKLIST TỔNG HỢP

### ✅ Form Input (Màu đen)
- [ ] Email input: chữ đen, bg trắng
- [ ] Password input: dots đen, bg trắng
- [ ] Họ tên input: chữ đen
- [ ] Select box: chữ đen trong dropdown
- [ ] Radio buttons: readable

### ✅ Sidebar & Logout
- [ ] Sidebar hiển thị sau login
- [ ] User name hiển thị đúng
- [ ] Email hiển thị đúng
- [ ] Level badge đúng màu
- [ ] Navigation buttons work
- [ ] Logout button xuất hiện
- [ ] Click logout → thông báo success
- [ ] Auto redirect to login
- [ ] Session cleared hoàn toàn
- [ ] Có thể login lại

### ✅ Cross-page Testing
- [ ] Dashboard có sidebar
- [ ] Topics có sidebar
- [ ] Topic detail có sidebar
- [ ] Lesson có sidebar
- [ ] Quiz có sidebar
- [ ] Chat có sidebar
- [ ] Logout works từ mọi page

---

## 🐛 TROUBLESHOOTING

### Vấn đề: Chữ vẫn màu trắng

**Giải pháp:**
1. Hard refresh: `Ctrl + Shift + R` (Windows) hoặc `Cmd + Shift + R` (Mac)
2. Clear browser cache
3. Restart Streamlit:
   ```bash
   # Ctrl+C để stop
   streamlit run streamlit_app.py
   ```

### Vấn đề: Sidebar không hiển thị

**Check:**
1. Đã login chưa?
2. Đang ở page nào? (Auth page không có sidebar)
3. Refresh page
4. Check console có lỗi không (F12)

### Vấn đề: Logout không work

**Debug:**
1. Check backend có chạy không
2. Check console logs (F12)
3. Thử manual: gõ trong Python console
   ```python
   st.session_state.access_token = None
   st.session_state.page = "auth"
   ```

### Vấn đề: Frontend bị crash

**Fix:**
```bash
# Stop all Python
Get-Process python | Stop-Process -Force

# Restart
streamlit run streamlit_app.py
```

---

## 📊 EXPECTED RESULTS

### Before vs After

| Feature | Before | After |
|---------|--------|-------|
| Input text color | ⚪ White (hard to read) | ⚫ Black (easy to read) |
| Input background | Dark (0.07 opacity) | Light (0.95 opacity) |
| Logout function | ❌ None | ✅ Working |
| Navigation | Manual | ✅ Sidebar buttons |
| UX Score | 5/10 | 9/10 |

---

## ✅ SUCCESS CRITERIA

**Test PASSED nếu:**

1. ✅ Tất cả input fields có chữ màu đen, dễ đọc
2. ✅ Sidebar hiển thị ở mọi authenticated pages
3. ✅ Logout button hoạt động
4. ✅ Click logout → clear session + redirect
5. ✅ Có thể login lại sau logout
6. ✅ Navigation buttons work
7. ✅ Không có console errors
8. ✅ Không có UI glitches

**Test FAILED nếu:**

1. ❌ Input vẫn màu trắng khó đọc
2. ❌ Sidebar không xuất hiện
3. ❌ Logout không làm gì cả
4. ❌ Crash khi logout
5. ❌ Session không clear
6. ❌ Console có errors

---

## 📸 SCREENSHOTS (Optional)

Chụp màn hình để verify:

1. **Login form** - showing black text
2. **Sidebar** - showing user info + logout
3. **After logout** - back to auth page
4. **Topics page** - sidebar still there

---

## 🎉 KẾT LUẬN

Nếu tất cả tests đều **PASS**:

✅ **Form inputs dễ đọc**  
✅ **Logout hoạt động hoàn hảo**  
✅ **UX cải thiện đáng kể**

Hệ thống sẵn sàng sử dụng!

---

**Thời gian test**: ~5-10 phút  
**Cần thiết bị**: Browser (Chrome/Edge/Firefox)  
**Level**: Beginner-friendly ✅
