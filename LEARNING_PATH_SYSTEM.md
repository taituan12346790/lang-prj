# 🎓 HỆ THỐNG LỘ TRÌNH HỌC TẬP - AI LANGUAGE TUTOR

## 📋 TỔNG QUAN

Hệ thống này cung cấp **lộ trình học tiếng Anh có cấu trúc** theo chuẩn CEFR từ A1 đến C2, với:
- ✅ **190 chủ đề học tập** chia theo 6 cấp độ
- ✅ **Mỗi chủ đề có 4 bài học**: Grammar → Vocabulary → Practice → Quiz
- ✅ **Hệ thống đánh giá tự động** với quiz scoring
- ✅ **Level-Up Test** khi đủ điều kiện
- ✅ **AI Tutor** hỗ trợ chat tự do

---

## 📊 CẤU TRÚC CHƯƠNG TRÌNH

Theo yêu cầu từ `can_bo_sung.txt`, hệ thống có:

| Level | Số Chủ Đề | Thời Gian Ước Tính |
|-------|-----------|-------------------|
| **A1** | 20 chủ đề | ~10 giờ học |
| **A2** | 25 chủ đề | ~12 giờ học |
| **B1** | 30 chủ đề | ~15 giờ học |
| **B2** | 35 chủ đề | ~18 giờ học |
| **C1** | 40 chủ đề | ~24 giờ học |
| **C2** | 40 chủ đề | ~24 giờ học |

**Tổng cộng**: 190 chủ đề ≈ **~100 giờ học nghiêm túc**

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

### 1. DATABASE SCHEMA

#### **Topics Table**
```python
- id (UUID)
- level (A1/A2/B1/B2/C1/C2)
- order (1, 2, 3...)
- name (tên tiếng Anh)
- name_vi (tên tiếng Việt)
- description / description_vi
- grammar_focus (mảng điểm ngữ pháp)
- vocabulary_tags (mảng tag)
- estimated_minutes (thời gian học)
- is_active (true/false)
```

#### **Lessons Table**
```python
- id (UUID)
- topic_id (FK → Topics)
- order (1=grammar, 2=vocabulary, 3=practice, 4=quiz)
- lesson_type (grammar/vocabulary/practice/quiz)
- title / title_vi
- content (JSONB - flexible structure)
```

#### **UserTopicProgress Table**
```python
- id (UUID)
- user_id (FK → Users)
- topic_id (FK → Topics)
- status (not_started / in_progress / completed)
- lesson_completed (0-4)
- quiz_score (0-100)
- quiz_attempts
- started_at / completed_at
```

### 2. BACKEND API

#### **Learning Path Endpoints**
```
GET  /api/learning/dashboard           → Dashboard với tiến độ
GET  /api/learning/topics/{level}      → Danh sách chủ đề theo level
GET  /api/learning/topic/{topic_id}    → Chi tiết chủ đề + lessons
GET  /api/learning/lesson/{lesson_id}  → Nội dung bài học đầy đủ
POST /api/learning/topic/{topic_id}/lesson/{order}/complete → Hoàn thành bài
```

#### **Quiz Endpoints**
```
GET  /api/quiz/topic/{topic_id}/questions → Lấy câu hỏi quiz
POST /api/quiz/topic/{topic_id}/submit    → Nộp bài + chấm điểm
```

#### **Test Endpoints**
```
GET  /api/test/placement/questions        → Placement test
POST /api/test/placement                  → Submit placement
GET  /api/test/level/{level}/questions    → Level-up test
POST /api/test/level-up                   → Submit level-up
```

### 3. FRONTEND (STREAMLIT)

#### **Các Trang Chính**

1. **Auth Page** (`page_auth`)
   - Đăng nhập / Đăng ký
   - Google OAuth
   - Backend status

2. **Placement Test** (`page_placement`)
   - Xác định trình độ ban đầu
   - 20-30 câu hỏi đa level
   - Tự động phân loại A1-C2

3. **Dashboard** (`page_dashboard`)
   - Hiển thị level hiện tại
   - Tiến độ % (hoàn thành / đang học / chưa bắt đầu)
   - Điểm quiz trung bình
   - Chủ đề đang học / tiếp theo
   - **Level-Up banner** khi đủ điều kiện

4. **Topics List** (`page_topics`)
   - Danh sách tất cả chủ đề theo level
   - Trạng thái: ✅ Completed / 🔵 In Progress / ⬜ Not Started
   - Điểm quiz / tiến độ bài học

5. **Topic Detail** (`page_topic`)
   - 4 bài học theo thứ tự:
     - 1️⃣ Grammar (Ngữ pháp)
     - 2️⃣ Vocabulary (Từ vựng)
     - 3️⃣ Practice (Luyện tập)
     - 4️⃣ Quiz (Kiểm tra)
   - **Mở khóa tuần tự**: Bài 2 chỉ mở khi hoàn thành Bài 1

6. **Lesson View** (`page_lesson`)
   - **Grammar**: Giải thích + ví dụ + notes
   - **Vocabulary**: Flashcards với pronunciation
   - **Practice**: Bài tập điền chỗ trống / trắc nghiệm
   - Nút "✅ Hoàn thành bài này" → update tiến độ

7. **Quiz** (`page_quiz`)
   - 10 câu hỏi trắc nghiệm
   - Progress bar
   - Submit → tự động chấm điểm

8. **Quiz Result** (`page_quiz_result`)
   - Điểm số (%) + Pass/Fail
   - ≥70% = Pass → hoàn thành chủ đề
   - Chi tiết từng câu (đúng/sai + giải thích)
   - Cho phép làm lại quiz

9. **Chat** (`page_chat`)
   - Chat tự do với AI Tutor
   - Có thể hỏi về ngữ pháp / luyện hội thoại
   - Luôn có sẵn giữa các chủ đề

10. **Level-Up Test** (`page_levelup`)
    - Chỉ hiện khi đủ điều kiện:
      - ✅ Hoàn thành ≥75% chủ đề
      - ✅ Điểm quiz trung bình ≥70%
    - 20-30 câu hỏi nâng cao
    - Pass (≥75%) → nâng lên level tiếp theo

---

## 🔄 QUI TRÌNH HỌC TẬP

### **Sau khi đăng nhập**

```
1. Làm Placement Test → Xác định level (A1-C2)
                ↓
2. Dashboard hiển thị:
   - Level hiện tại: A1
   - Tiến độ: 0/20 chủ đề (0%)
   - Chủ đề tiếp theo: "Greetings & Introductions"
                ↓
3. Bấm "Bắt đầu học" → Topic Detail
                ↓
4. Học tuần tự 4 bài:
   📖 Bài 1: Grammar → 🔤 Bài 2: Vocabulary 
              ↓                    ↓
   ✏️ Bài 3: Practice → 📝 Bài 4: Quiz
                ↓
5. Quiz ≥70% → ✅ Chủ đề hoàn thành
                ↓
6. Quay lại Dashboard → Chủ đề tiếp theo tự động mở
                ↓
7. Lặp lại cho 20 chủ đề A1...
                ↓
8. Khi hoàn thành 15/20 chủ đề (75%) + điểm TB ≥70%
   → 🏆 Hiện nút "Level-Up Test"
                ↓
9. Làm Level-Up Test → Pass → Nâng lên A2
                ↓
10. Tiếp tục với 25 chủ đề A2...
```

### **Tùy chọn bổ sung**
- 💬 **Chat với AI Tutor** bất cứ lúc nào để:
  - Hỏi thêm về ngữ pháp
  - Luyện hội thoại
  - Ôn lại chủ đề đã học
  
---

## 📈 ĐIỀU KIỆN LEVEL-UP

### **Công Thức Kiểm Tra**

```python
can_level_up = (
    completed_topics / total_topics >= 0.75    # ≥75% hoàn thành
    AND
    average_quiz_score >= 70                    # Điểm TB ≥70%
)
```

### **Ví dụ Level A1**
- Tổng: 20 chủ đề
- Cần hoàn thành: 15 chủ đề (75%)
- Điểm quiz trung bình: ≥70%
- Khi đủ → Hiện nút "🏆 Làm bài kiểm tra nâng cấp"

### **Level-Up Test**
- 20-30 câu hỏi tổng hợp level hiện tại
- Yêu cầu: ≥75% để pass
- Pass → Nâng level + reset progress
- Fail → Giữ nguyên level + gợi ý ôn tập

---

## 🎯 MỤC TIÊU HỌC TẬP THEO LEVEL

### **A1 – Beginner**
- Giao tiếp cơ bản
- Giới thiệu bản thân
- Hỏi đường, mua sắm
- **Ngữ pháp**: To be, Present Simple, Have/Has, Can
- **Từ vựng**: 500-800 từ

### **A2 – Elementary**
- Giao tiếp thường ngày
- Kể trải nghiệm đơn giản
- Du lịch, sức khỏe
- **Ngữ pháp**: Past Simple, Future, Comparisons
- **Từ vựng**: 1000-1500 từ

### **B1 – Intermediate**
- Hoạt động độc lập
- Trình bày ý kiến
- Giải quyết vấn đề
- **Ngữ pháp**: Present Perfect, Conditionals, Passive
- **Từ vựng**: 2000-2500 từ

### **B2 – Upper Intermediate**
- Học tập và làm việc hiệu quả
- Tranh luận, thuyết phục
- Viết essay, báo cáo
- **Ngữ pháp**: Perfect Continuous, Mixed Conditionals, Reported Speech
- **Từ vựng**: 3000-4000 từ

### **C1 – Advanced**
- Sử dụng ngôn ngữ linh hoạt
- Học thuật và nghề nghiệp
- Phân tích, đàm phán
- **Ngữ pháp**: Inversion, Cleft Sentences, Hedging
- **Từ vựng**: 5000-7000 từ

### **C2 – Mastery**
- Gần như người bản ngữ có học thức
- Hùng biện, viết luận văn
- Phân tích sâu, nghiên cứu
- **Ngữ pháp**: Advanced Rhetoric, Pragmatics
- **Từ vựng**: 8000-10000+ từ

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

### **Backend**
- **FastAPI** (Python async)
- **PostgreSQL** (database)
- **SQLAlchemy** (ORM async)
- **Pydantic** (validation)
- **JWT** (authentication)

### **Frontend**
- **Streamlit** (rapid UI)
- **httpx** (HTTP client)
- **Custom CSS** (styling)

### **AI Components**
- **LangChain** (agentic workflow)
- **OpenAI GPT** (chat tutor)
- **RAG System** (retrieval từ grammar books)

---

## 📂 CẤU TRÚC FILE QUAN TRỌNG

```
lang_prj/
├── app/
│   ├── data/
│   │   └── topics_data.py          ← 190 topics (A1-C2)
│   ├── models/
│   │   ├── topic.py                ← Topic model
│   │   ├── lesson.py               ← Lesson model
│   │   └── user_topic_progress.py  ← Progress tracking
│   ├── services/
│   │   └── topic_service.py        ← Business logic
│   ├── routers/
│   │   ├── learning_path.py        ← Learning API
│   │   └── quiz.py                 ← Quiz API
│   └── main.py                     ← FastAPI app
│
├── streamlit_app.py                ← Frontend UI (1350 lines)
├── can_bo_sung.txt                 ← Requirement doc
├── y_tuong_moi.txt                 ← System design doc
└── LEARNING_PATH_SYSTEM.md         ← This file

```

---

## 🚀 HƯỚNG DẪN CHẠY HỆ THỐNG

### **1. Khởi động Backend**
```bash
cd d:\lang_prj
python -m uvicorn app.main:app --reload
```
Backend chạy tại: `http://127.0.0.1:8000`

### **2. Khởi động Frontend**
```bash
streamlit run streamlit_app.py
```
Frontend chạy tại: `http://localhost:8501`

### **3. Workflow**
1. Đăng ký tài khoản mới
2. Làm Placement Test → xác định level
3. Dashboard hiển thị chủ đề đầu tiên
4. Học theo thứ tự: Grammar → Vocabulary → Practice → Quiz
5. Quiz pass (≥70%) → chủ đề hoàn thành
6. Tiếp tục với chủ đề tiếp theo
7. Đủ 75% → Level-Up Test
8. Pass → Nâng level tiếp theo

---

## 🎨 TÍNH NĂNG NỔI BẬT

### ✅ **Đã Triển Khai**

1. **Lộ trình có cấu trúc**
   - 190 chủ đề chia 6 level
   - Mỗi chủ đề 4 bài học
   - Mở khóa tuần tự

2. **Dashboard trực quan**
   - Tiến độ % theo level
   - Stats: hoàn thành / đang học / chưa bắt đầu
   - Điểm quiz trung bình

3. **Quiz tự động chấm**
   - 10 câu hỏi / topic
   - Tính điểm tự động
   - Feedback chi tiết
   - Cho phép làm lại

4. **Level-Up System**
   - Điều kiện rõ ràng (75% + 70%)
   - Level-Up Test khi đủ
   - Tự động nâng level

5. **AI Tutor Chat**
   - Chat tự do bất cứ lúc nào
   - Hỏi ngữ pháp
   - Luyện hội thoại

6. **Responsive UI**
   - Dark theme gradient
   - Progress bars
   - Cards với states
   - Icons trực quan

---

## 📊 THỐNG KÊ HỆ THỐNG

| Metric | Value |
|--------|-------|
| **Tổng Topics** | 190 |
| **Tổng Lessons** | 760 (190 × 4) |
| **Tổng Quiz Questions** | ~1,900 (10/topic) |
| **Lines of Code (Backend)** | ~3,000 |
| **Lines of Code (Frontend)** | ~1,350 |
| **Database Tables** | 12 |
| **API Endpoints** | 25+ |

---

## 🎯 ROADMAP TƯƠNG LAI

### **Phase 1: Content Enhancement** (Đề xuất)
- [ ] Bổ sung nội dung chi tiết cho topics A2-C2
- [ ] Thêm audio pronunciation cho vocabulary
- [ ] Thêm video lessons
- [ ] Thêm ví dụ thực tế hơn

### **Phase 2: Advanced Features**
- [ ] Spaced Repetition System (SRS)
- [ ] Flashcard drill mode
- [ ] Speaking practice với voice recognition
- [ ] Writing correction với AI
- [ ] Peer learning / forums

### **Phase 3: Gamification**
- [ ] Badges & achievements
- [ ] Leaderboard
- [ ] Streaks (chuỗi ngày học)
- [ ] Daily challenges

### **Phase 4: Mobile & Offline**
- [ ] React Native app
- [ ] Offline mode
- [ ] Push notifications
- [ ] Apple/Android stores

---

## 🤝 LỜI KẾT

Hệ thống **AI Language Tutor** hiện đã có:

✅ **Backend hoàn chỉnh** với 190 topics, API đầy đủ  
✅ **Frontend Streamlit** với tất cả tính năng cần thiết  
✅ **Learning path rõ ràng** từ A1 → C2  
✅ **Quiz & Level-up system** tự động  
✅ **AI Tutor chat** hỗ trợ 24/7  

Người dùng có thể:
1. Đăng nhập → Placement test → Xác định level
2. Học theo lộ trình có cấu trúc
3. Làm quiz sau mỗi chủ đề
4. Theo dõi tiến độ trực quan
5. Level-up khi đủ điều kiện
6. Chat tự do với AI Tutor

Hệ thống đã sẵn sàng cho việc **học tập thực tế** và có thể **mở rộng** dễ dàng trong tương lai! 🚀

---

**Tài liệu này được tạo ngày:** 2026-06-03  
**Phiên bản:** 1.0  
**Tác giả:** AI Language Tutor Development Team
