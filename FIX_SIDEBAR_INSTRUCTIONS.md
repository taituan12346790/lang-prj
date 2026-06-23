# 🔧 HƯỚNG DẪN FIX SIDEBAR - THỰC HIỆN NGAY

## ⚠️ QUAN TRỌNG: PHẢI RESTART STREAMLIT

Code mới đã được update nhưng **Streamlit cần RESTART** để load code mới.

---

## 🚀 CÁCH 1: RESTART STREAMLIT (KHUYÊN DÙNG)

### Bước 1: Stop Streamlit hiện tại
Tìm terminal đang chạy Streamlit, nhấn:
```
Ctrl + C
```

### Bước 2: Chờ process stop
Đợi 2-3 giây cho đến khi thấy command prompt trở lại

### Bước 3: Start lại Streamlit
```bash
python -m streamlit run streamlit_app.py --server.port 8501
```

### Bước 4: Mở browser
- URL: http://localhost:8501
- Nhấn `Ctrl + Shift + R` để hard refresh

---

## 🎯 CÁCH 2: NẾU KHÔNG TÌM THẤY TERMINAL

### Kill tất cả Python processes:
```bash
taskkill /F /IM python.exe
```

### Start lại backend và frontend:
```bash
# Terminal 1 - Backend:
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend:
python -m streamlit run streamlit_app.py --server.port 8501
```

---

## ✅ SAU KHI RESTART

Bạn sẽ thấy:

### 1. **Debug info trong sidebar** (góc trên bên trái):
```
🔍 Debug: page=dashboard
```

Nếu **THẤY** dòng này → Sidebar đang hoạt động! ✅

Nếu **KHÔNG THẤY** → Báo tôi ngay, có vấn đề khác

### 2. **Sidebar luôn hiện**
- Kể cả khi session expire
- Kể cả khi user = None
- Sẽ show warning nếu session mất

### 3. **Debug token status** (cuối sidebar):
```
🔍 Token: ✅  (hoặc ❌)
```

---

## 🔍 KIỂM TRA SIDEBAR CÓ BỊ COLLAPSE KHÔNG

### Dấu hiệu sidebar bị collapse:
1. Góc **trên cùng bên trái** có mũi tên `>` nhỏ
2. Click vào mũi tên đó → sidebar xuất hiện trở lại

### Keyboard shortcut:
Nhấn phím `[` (ngoặc vuông mở) để toggle sidebar

---

## 🐛 NẾU VẪN KHÔNG THẤY SIDEBAR

Hãy cho tôi biết:

1. **Sau khi restart Streamlit:**
   - Có thấy dòng `🔍 Debug: page=...` trong sidebar không?
   - Nếu KHÔNG thấy → chụp màn hình toàn bộ app gửi tôi

2. **Sidebar bị mất ở page nào?**
   - Dashboard? Topics? Lesson? Quiz? Chat?

3. **Console có lỗi không?**
   - Nhấn F12 → tab Console
   - Chụp màn hình lỗi (nếu có)

4. **Sidebar mất sau hành động gì?**
   - Click button nào?
   - Navigate đến đâu?

---

## 📝 THAY ĐỔI ĐÃ LÀM

1. ✅ Thêm debug info hiển thị page hiện tại
2. ✅ Thêm debug info hiển thị token status
3. ✅ Sidebar LUÔN render, không bao giờ skip
4. ✅ Đổi text "Reload" → "Quay về đăng nhập" rõ ràng hơn

---

## 🎯 ACTION NGAY BÂY GIỜ:

1. **RESTART STREAMLIT** (Ctrl+C rồi chạy lại)
2. **Hard refresh browser** (Ctrl+Shift+R)
3. **Kiểm tra có thấy debug info không**
4. **Báo kết quả cho tôi**

RESTART LÀ QUAN TRỌNG NHẤT! ⚡
