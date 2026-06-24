# ⚠️ REMINDER: SWITCH BACK TO GPT-OSS-120B

## 🔴 QUAN TRỌNG:

**Sau 12 tiếng (khi Groq reset quota), nhớ đổi lại model về `openai/gpt-oss-120b`!**

---

## 📅 Thông tin:

- **Thời điểm đổi sang llama3**: 2026-06-24 12:30 (UTC+7)
- **Thời điểm cần đổi lại**: 2026-06-25 00:00+ (sau khi Groq reset quota)
- **Model hiện tại**: `llama3-70b-8192` (TẠM THỜI)
- **Model gốc**: `openai/gpt-oss-120b` (PHẢI ĐỔI LẠI)

---

## 🔧 Cách đổi lại:

### File: `app/llm/llm_client.py`

**Dòng 11 - Đổi từ:**
```python
def __init__(self, model="llama3-70b-8192", temperature=0.7, max_tokens=1500):  # TEMP
```

**Đổi thành:**
```python
def __init__(self, model="openai/gpt-oss-120b", temperature=0.7, max_tokens=1500):
```

### Commands:

```bash
# 1. Edit file
code app/llm/llm_client.py
# Sửa dòng 11

# 2. Commit & push
git add app/llm/llm_client.py
git commit -m "chore: Switch back to openai/gpt-oss-120b after rate limit reset"
git push origin master

# 3. Đợi Render deploy (2-3 phút)

# 4. Test chat → Done!
```

---

## 📊 So sánh models:

| Feature | llama3-70b-8192 | openai/gpt-oss-120b |
|---------|-----------------|---------------------|
| Params | 70B | 120B |
| Context | 8192 tokens | Unknown |
| Quality | Tốt | Rất tốt |
| Speed | Nhanh | Trung bình |
| Groq Quota | Separate | 1000/day |

---

## ⏰ CHECKLIST:

- [x] Đã đổi sang llama3-70b-8192
- [x] Commit: `temp: Switch to llama3-70b-8192 to avoid rate limit`
- [ ] **ĐỢI 12 TIẾNG**
- [ ] **ĐỔI LẠI openai/gpt-oss-120b**
- [ ] Test chat với model gốc
- [ ] Delete file này

---

## 🚨 LƯU Ý:

**KHÔNG ĐƯỢC QUÊN ĐỔI LẠI!**

Model `llama3-70b-8192` chỉ dùng TẠM THỜI để tránh rate limit.

Model gốc `openai/gpt-oss-120b` phải được dùng cho production!

---

**Set reminder/alarm ngay bây giờ!** ⏰
