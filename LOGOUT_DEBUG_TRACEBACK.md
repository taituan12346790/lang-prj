# 🔍 DEBUG LOGOUT - TRACEBACK

## HƯỚNG DẪN

1. **Restart Streamlit**: Ctrl+C rồi chạy lại
2. **Refresh browser**: Ctrl+Shift+R
3. **Login**
4. **Click "Đăng xuất"** → **"Có, đăng xuất ngay"**
5. **Xem terminal Streamlit**

---

## TÌMCÁI GÌ

Terminal sẽ in:
```
🟠 _fetch_profile() called from:
  File "...", line XXX, in <function>
  ...
```

**Báo cho tôi**: Function/line nào gọi `_fetch_profile()`?

---

## EXPECTED

Nếu logout work, **KHÔNG CÓ** dòng `🟠 _fetch_profile()` sau logout.

Nếu vẫn có, biết được từ đâu được gọi thì có thể fix.

---

**RESTART STREAMLIT VÀ TEST NHÉ!**
