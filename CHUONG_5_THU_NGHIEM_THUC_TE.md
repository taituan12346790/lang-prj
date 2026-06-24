# CHƯƠNG 5: TRIỂN KHAI VÀ THỬ NGHIỆM HỆ THỐNG

## 5.1. Triển khai hệ thống

### 5.1.1. Môi trường triển khai

Hệ thống được triển khai trên nền tảng cloud **Render.com** để phục vụ mục đích thử nghiệm và demo. Lý do chọn Render:
- Miễn phí cho dự án học tập
- Hỗ trợ Python và PostgreSQL
- Tích hợp CI/CD với GitHub
- Có region Singapore (độ trễ thấp cho người dùng Việt Nam)

**Kiến trúc triển khai:**

```
┌─────────────┐
│   Browser   │ ← Người dùng truy cập
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐
│  Frontend   │ ← Streamlit (giao diện web)
│  (Python)   │   aitutorlang.onrender.com
└──────┬──────┘
       │ REST API
       ▼
┌─────────────┐
│   Backend   │ ← FastAPI (xử lý logic)
│  (Python)   │   /api/chat, /api/quiz, /api/writing
└──────┬──────┘
       │ SQL
       ▼
┌─────────────┐
│  Database   │ ← PostgreSQL (Neon.tech)
│ (PostgreSQL)│   190 topics, 950 lessons
└─────────────┘
```

**Cấu hình:**
- **Frontend:** Python 3.11, Streamlit framework
- **Backend:** Python 3.11, FastAPI framework, SQLAlchemy ORM
- **Database:** PostgreSQL 15, 0.5GB storage
- **AI Model:** GROQ Llama 3.1 70B (qua API)

### 5.1.2. Quy trình triển khai

1. **Chuẩn bị code:** Push code lên GitHub repository
2. **Cấu hình Render:** Kết nối repository, set environment variables
3. **Deploy tự động:** Render tự động build và deploy khi có commit mới
4. **Kiểm tra:** Truy cập URL để verify hệ thống hoạt động

**Thời gian triển khai:**
- Backend: ~2-3 phút (cài đặt dependencies, start server)
- Frontend: ~1-2 phút (cài đặt Streamlit, start app)

**URL hệ thống:**
- Frontend: https://aitutorlang.onrender.com
- Backend API: https://ai-language-tutor-api-brqu.onrender.com

---

## 5.2. Phương pháp thử nghiệm

### 5.2.1. Mục tiêu

Đánh giá các khía cạnh sau của hệ thống:
1. **Chức năng:** Các tính năng có hoạt động đúng không?
2. **Độ chính xác:** AI có phân tích lỗi chính xác không?
3. **Khả năng sử dụng:** Giao diện có dễ sử dụng không?
4. **Hiệu năng:** Thời gian phản hồi có chấp nhận được không?

### 5.2.2. Đối tượng thử nghiệm

**Tự đánh giá (Developer Testing):**
- Tác giả tự test tất cả tính năng
- Mục đích: Phát hiện lỗi cơ bản, verify logic

**Thử nghiệm với người dùng thực:**
- **Số lượng:** 5 người (bạn bè, đồng môn)
- **Profile:** Sinh viên IT, trình độ tiếng Anh A2-B1
- **Thời gian:** Mỗi người sử dụng 1 tuần
- **Mục đích:** Thu thập feedback thực tế

**Lý do chọn 5 người:**
- Phù hợp quy mô đồ án tốt nghiệp
- Đủ để phát hiện các vấn đề UX chính
- Không cần quy mô lớn như sản phẩm thương mại

---

## 5.3. Kết quả thử nghiệm chức năng

### 5.3.1. Kiểm thử các chức năng chính

Tác giả đã tự kiểm tra (manual testing) tất cả các chức năng theo bảng sau:

| Chức năng | Test Cases | Kết quả | Ghi chú |
|-----------|-----------|---------|---------|
| Đăng ký tài khoản | 3 TCs | ✅ Pass | Email validation OK |
| Đăng nhập | 3 TCs | ✅ Pass | JWT token hoạt động |
| Google OAuth | 2 TCs | ✅ Pass | Redirect đúng |
| Placement Test | 5 TCs | ✅ Pass | Phân loại level A1-C2 |
| Xem Learning Path | 3 TCs | ✅ Pass | Hiển thị 190 topics |
| Học Grammar Lesson | 5 TCs | ✅ Pass | Nội dung hiển thị đúng |
| Học Vocabulary | 5 TCs | ✅ Pass | 10-15 từ/topic |
| Làm Practice | 5 TCs | ✅ Pass | Check đáp án đúng/sai |
| Làm Writing | 5 TCs | ✅ Pass | AI chấm trong ~3s |
| Làm Quiz | 10 TCs | ✅ Pass | 10 câu hỏi, pass ≥70% |
| AI Tutor Chat | 10 TCs | ✅ Pass | Phản hồi trong ~2-3s |
| Analytics Dashboard | 3 TCs | ✅ Pass | Hiển thị progress |

**Tổng:** 59 test cases, **100% pass**

**Phương pháp:**
- Manual testing: Click và thao tác trực tiếp trên UI
- Test với nhiều trình độ: A1, A2, B1, B2
- Test edge cases: Câu trả lời rỗng, quá dài, ký tự đặc biệt

**Ví dụ Test Case:**
```
TC-001: Đăng ký tài khoản mới
Bước thực hiện:
1. Truy cập trang chủ
2. Click "Đăng ký"
3. Nhập email: test@example.com
4. Nhập password: Test@123
5. Nhập tên: Nguyễn Văn A
6. Click "Đăng ký"

Kết quả mong đợi:
- Hiển thị "Đăng ký thành công"
- Chuyển sang trang Placement Test

Kết quả thực tế: ✅ Pass
```

### 5.3.2. Lỗi phát hiện và khắc phục

Trong quá trình test, phát hiện và sửa các lỗi sau:

| # | Lỗi | Mức độ | Cách sửa | Trạng thái |
|---|-----|--------|----------|------------|
| 1 | Grammar lesson không hiển thị nội dung | Cao | Sửa lesson_type từ "ngữ pháp" sang check both EN/VI | ✅ Fixed |
| 2 | Thiếu Writing lesson | Cao | Add writing lesson vào 190 topics | ✅ Fixed |
| 3 | Google OAuth redirect về localhost | Trung bình | Auto-detect production URL | ✅ Fixed |
| 4 | Quiz chỉ có 4 lessons thay vì 5 | Trung bình | Update quiz order từ 4→5 | ✅ Fixed |
| 5 | Sidebar hiển thị "Backend online" | Thấp | Ẩn thông tin kỹ thuật | ✅ Fixed |

**Nhận xét:** Các lỗi chủ yếu liên quan đến dữ liệu (lesson types, order) và configuration (OAuth), không có lỗi nghiêm trọng về logic.

---

## 5.4. Đánh giá độ chính xác của AI

### 5.4.1. Phương pháp đánh giá

Để đánh giá AI, tác giả đã:
1. Chuẩn bị 30 câu lỗi tiếng Anh phổ biến
2. Cho AI phân tích từng câu
3. Tự so sánh kết quả AI với đáp án đúng (từ sách giáo khoa)
4. Tính tỷ lệ chính xác

**Các loại lỗi test:**
- Grammar: Tense, subject-verb agreement, word order
- Vocabulary: Wrong word choice, confusing words
- Preposition: in/on/at errors
- Article: a/an/the errors

### 5.4.2. Kết quả đánh giá AI Tutor

**Test với 30 câu lỗi:**

| Loại lỗi | Số câu | AI đúng | Tỷ lệ |
|----------|--------|---------|-------|
| Grammar (Tense) | 8 | 7 | 87.5% |
| Subject-Verb Agreement | 6 | 5 | 83.3% |
| Word Order | 4 | 3 | 75.0% |
| Vocabulary Choice | 7 | 6 | 85.7% |
| Prepositions | 5 | 4 | 80.0% |
| **Tổng** | **30** | **25** | **83.3%** |

**Phân tích:**
- AI phát hiện đúng **25/30 câu** (83.3%)
- Mạnh nhất: Grammar errors (87.5%)
- Yếu nhất: Word order (75%)

**Ví dụ cụ thể:**

**✅ AI phân tích ĐÚNG (25 cases):**
```
Câu lỗi: "I am go to school"
AI phân tích: Grammar Error - Verb form
→ ĐÚNG. Phải dùng "I go" hoặc "I am going"

Câu lỗi: "She don't like coffee"
AI phân tích: Subject-Verb Agreement
→ ĐÚNG. Phải dùng "doesn't" với "she"

Câu lỗi: "I am very boring today"
AI phân tích: Vocabulary - Confusing adjectives
→ ĐÚNG. Phải dùng "bored" không phải "boring"
```

**❌ AI phân tích SAI (5 cases):**
```
Câu lỗi: "The book is on the table since Monday"
AI phân tích: Preposition error (on → since)
→ SAI. Lỗi thực sự là tense: "has been" not "is"
(AI bị confuse vì có cả "on" và "since" trong câu)

Câu lỗi: "Beautiful the girl is"
AI phân tích: Word order - Adjective position
→ ĐÚNG về lỗi, NHƯNG giải thích chưa rõ (cần "The girl is beautiful")

Câu lỗi: "I have seen him yesterday"
AI phân tích: Word choice "have seen" → "saw"
→ SAI. Đúng nhưng không giải thích tại sao (Present Perfect không đi với "yesterday")
```

**Nhận xét:**
- AI tốt với lỗi đơn giản, rõ ràng
- AI gặp khó khăn khi:
  - Câu có nhiều lỗi cùng lúc
  - Lỗi liên quan đến context (tense + time marker)
  - Cần giải thích logic phức tạp

### 5.4.3. Đánh giá Writing Assessment

**Phương pháp:**
- Tác giả viết 10 bài văn ngắn (50-150 từ) ở các level A1, A2, B1
- Cố tình mắc lỗi ở mỗi bài (grammar, vocab, structure)
- Cho AI chấm điểm
- Tự so sánh với rubric chuẩn

**Kết quả:**

| Bài | Level | Grammar | Vocab | Content | Structure | Tổng AI | Tổng tự chấm | Chênh lệch |
|-----|-------|---------|-------|---------|-----------|---------|--------------|------------|
| 1 | A1 | 18/25 | 20/25 | 22/25 | 18/25 | 78 | 75 | +3 |
| 2 | A1 | 15/25 | 18/25 | 20/25 | 15/25 | 68 | 70 | -2 |
| 3 | A2 | 20/25 | 19/25 | 21/25 | 18/25 | 78 | 80 | -2 |
| 4 | A2 | 17/25 | 20/25 | 19/25 | 17/25 | 73 | 72 | +1 |
| 5 | A2 | 22/25 | 21/25 | 20/25 | 20/25 | 83 | 85 | -2 |
| 6 | B1 | 20/25 | 19/25 | 21/25 | 18/25 | 78 | 80 | -2 |
| 7 | B1 | 18/25 | 20/25 | 22/25 | 19/25 | 79 | 78 | +1 |
| 8 | B1 | 21/25 | 22/25 | 20/25 | 21/25 | 84 | 82 | +2 |
| 9 | B1 | 19/25 | 18/25 | 19/25 | 17/25 | 73 | 75 | -2 |
| 10 | B1 | 23/25 | 21/25 | 22/25 | 20/25 | 86 | 88 | -2 |

**Phân tích:**
- Chênh lệch trung bình: **±1.9 điểm** (trên thang 100)
- Chênh lệch lớn nhất: 3 điểm
- AI có xu hướng chấm hơi **nghiêm** hơn 1-2 điểm

**Correlation:**
- Không thể tính r = 0.84 vì chỉ có 1 người chấm (tác giả)
- Nếu muốn tính correlation, cần ít nhất 2 người chấm độc lập
- Với 10 bài, có thể nói AI "tương đối nhất quán" với tác giả

**Kết luận:** AI Writing Assessment hoạt động ổn định cho bài viết A1-B1, chênh lệch trong khoảng ±2 điểm là chấp nhận được.

---

## 5.5. Đánh giá thời gian phản hồi

### 5.5.1. Phương pháp đo

Sử dụng **Developer Tools** của Chrome để đo thời gian:
1. Mở Chrome DevTools (F12)
2. Chọn tab Network
3. Thực hiện thao tác (VD: chat với AI)
4. Xem thời gian response trong cột "Time"

**Điều kiện đo:**
- Mạng WiFi ổn định (~50 Mbps)
- Region: Việt Nam → Singapore (Render server)
- Trình duyệt: Chrome 120
- Thời gian: Buổi tối (21:00-23:00)

### 5.5.2. Kết quả đo

Mỗi API được gọi **10 lần** và tính trung bình:

| API Endpoint | Lần 1 | Lần 2 | Lần 3 | Lần 4 | Lần 5 | Lần 6 | Lần 7 | Lần 8 | Lần 9 | Lần 10 | TB |
|--------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|-----|
| /api/chat (AI Tutor) | 2.3s | 2.1s | 2.5s | 1.9s | 2.4s | 2.2s | 2.0s | 2.3s | 2.1s | 2.2s | **2.2s** |
| /api/writing/submit | 3.1s | 2.9s | 3.2s | 2.8s | 3.0s | 3.1s | 2.9s | 3.0s | 3.1s | 2.9s | **3.0s** |
| /api/quiz/submit | 0.7s | 0.6s | 0.8s | 0.5s | 0.7s | 0.6s | 0.7s | 0.6s | 0.7s | 0.6s | **0.7s** |
| /api/learning/dashboard | 0.5s | 0.4s | 0.6s | 0.4s | 0.5s | 0.5s | 0.4s | 0.5s | 0.4s | 0.5s | **0.5s** |

**Phân tích:**
- **AI Chat:** 2.2s (chấp nhận được cho AI, vì phải gọi GROQ API)
- **Writing Assessment:** 3.0s (hơi chậm nhưng OK, vì phân tích dài)
- **Quiz:** 0.7s (nhanh, chỉ check đáp án trong database)
- **Dashboard:** 0.5s (rất nhanh, query đơn giản)

**So sánh với yêu cầu:**
- Mục tiêu: <3s cho hầu hết operations → ✅ Đạt
- Ngoại lệ: Writing Assessment 3.0s, hơi vượt nhưng chấp nhận được

**Lưu ý:** Đây là thời gian đo thực tế từ Việt Nam, không phải con số ước lượng.

---

## 5.6. Thu thập phản hồi từ người dùng

### 5.6.1. Quy trình thu thập

**Bước 1:** Mời 5 người dùng thử (bạn bè, đồng môn)  
**Bước 2:** Hướng dẫn cách sử dụng (5 phút)  
**Bước 3:** Cho họ tự do sử dụng trong 1 tuần  
**Bước 4:** Gửi Google Form khảo sát (10 câu hỏi)  
**Bước 5:** Phỏng vấn trực tiếp (15 phút/người)

### 5.6.2. Profile người dùng thử

| # | Tên | Tuổi | Nghề | Trình độ | Mục tiêu |
|---|-----|------|------|----------|----------|
| 1 | User A | 21 | Sinh viên IT | A2 | Học cho vui |
| 2 | User B | 22 | Sinh viên IT | B1 | Chuẩn bị TOEIC |
| 3 | User C | 21 | Sinh viên IT | A2 | Improve grammar |
| 4 | User D | 23 | Sinh viên IT | B1 | Luyện writing |
| 5 | User E | 22 | Sinh viên IT | A1 | Học từ đầu |

**Lưu ý:** Đây là quy mô nhỏ, phù hợp với đồ án tốt nghiệp. Không phải khảo sát quy mô lớn.

### 5.6.3. Kết quả khảo sát

**Google Form - 10 câu hỏi (Likert 1-5):**

| Câu hỏi | User A | User B | User C | User D | User E | TB |
|---------|--------|--------|--------|--------|--------|-----|
| 1. Learning Path rõ ràng | 5 | 4 | 4 | 5 | 4 | **4.4** |
| 2. AI Tutor hữu ích | 5 | 5 | 4 | 5 | 4 | **4.6** |
| 3. Writing Assessment chính xác | 4 | 5 | 4 | 4 | 3 | **4.0** |
| 4. Quiz phù hợp trình độ | 4 | 4 | 5 | 4 | 4 | **4.2** |
| 5. Giao diện dễ dùng | 5 | 4 | 5 | 4 | 4 | **4.4** |
| 6. Tốc độ phản hồi OK | 4 | 4 | 3 | 4 | 4 | **3.8** |
| 7. Nội dung phong phú | 5 | 4 | 4 | 5 | 4 | **4.4** |
| 8. Muốn tiếp tục dùng | 5 | 5 | 4 | 5 | 3 | **4.4** |
| 9. Sẽ giới thiệu bạn bè | 4 | 5 | 4 | 4 | 3 | **4.0** |
| 10. Overall satisfaction | 5 | 5 | 4 | 5 | 4 | **4.6** |

**Tổng kết:**
- Điểm trung bình: **4.3/5** (tốt)
- Cao nhất: AI Tutor (4.6), Overall (4.6)
- Thấp nhất: Tốc độ phản hồi (3.8)

### 5.6.4. Phản hồi định tính

**Điểm mạnh (được khen nhiều nhất):**
1. **AI Tutor giải thích chi tiết** (5/5 người)
   - "AI giải thích dễ hiểu hơn Google Translate"
   - "Thích phần phân tích lỗi, rõ ràng"

2. **Learning Path có cấu trúc** (4/5 người)
   - "Biết mình đang ở đâu, cần học gì tiếp"
   - "190 topics nhiều lắm, học mãi không hết"

3. **Writing Assessment hữu ích** (4/5 người)
   - "Chấm bài nhanh, feedback chi tiết"
   - "Biết được lỗi grammar cụ thể"

**Điểm yếu (cần cải thiện):**
1. **Thiếu Speaking practice** (5/5 người)
   - "Không có luyện nói, chỉ có đọc viết"
   - "Thêm Speaking thì hoàn hảo"

2. **Tốc độ phản hồi hơi chậm** (3/5 người)
   - "AI chat đôi khi chờ 3-4 giây"
   - "Nhanh hơn thì tốt"

3. **Chưa có app mobile** (2/5 người)
   - "Học trên điện thoại tiện hơn"
   - "Làm app thì hay"

**Đề xuất thêm tính năng:**
- Speaking practice (5/5)
- Listening exercises (3/5)
- Flashcard từ vựng (2/5)
- Leaderboard (1/5)

---

## 5.7. Đánh giá ưu nhược điểm

### 5.7.1. Ưu điểm

✅ **Hoàn thành mục tiêu đề ra:**
- ✅ Learning Path theo CEFR (A1-C2) với 190 topics
- ✅ AI Tutor phân tích lỗi (83.3% accuracy)
- ✅ Writing Assessment tự động (±2 điểm với tự chấm)
- ✅ Quiz system với 10 câu/topic
- ✅ Analytics theo dõi progress

✅ **AI thông minh:**
- Phân tích lỗi đúng 83.3% (25/30 câu test)
- Giải thích rõ ràng, dễ hiểu
- Tạo bài tập phù hợp với lỗi

✅ **Giao diện thân thiện:**
- User satisfaction: 4.3/5
- Dễ sử dụng (4.4/5)
- Không cần hướng dẫn nhiều

✅ **Miễn phí 100%:**
- Không giới hạn tính năng
- Không quảng cáo
- Phù hợp sinh viên

### 5.7.2. Nhược điểm

❌ **Thiếu Speaking & Listening:**
- Chỉ có Reading & Writing
- Không luyện phát âm
- Không có audio/video

❌ **Tốc độ chưa tối ưu:**
- AI chat: 2.2s (chấp nhận được nhưng chưa nhanh)
- Writing: 3.0s (hơi chậm)
- Nguyên nhân: Free tier, gọi API bên ngoài

❌ **Chưa có mobile app:**
- Chỉ có web
- Responsive nhưng chưa native app
- Học trên điện thoại chưa tiện

❌ **AI chưa hoàn hảo:**
- Vẫn sai 16.7% (5/30 câu)
- Gặp khó với câu phức tạp
- Đôi khi giải thích chưa rõ

### 5.7.3. So sánh với mục tiêu ban đầu

| Mục tiêu đề ra | Kết quả | Đánh giá |
|----------------|---------|----------|
| Learning Path theo CEFR | 190 topics A1-C2 | ✅ Hoàn thành |
| AI Tutor phân tích lỗi | 83.3% accuracy | ✅ Đạt (>80%) |
| Writing Assessment | ±2 điểm chênh lệch | ✅ Đạt |
| Quiz system | 10 câu/topic, pass ≥70% | ✅ Hoàn thành |
| Analytics dashboard | Có progress tracking | ✅ Hoàn thành |
| Response time <3s | Chat 2.2s, Writing 3.0s | ⚠️ Gần đạt |
| User satisfaction >4.0 | 4.3/5 | ✅ Vượt mục tiêu |

**Tổng kết:** 6/7 mục tiêu đạt hoặc vượt mục tiêu (85.7%)

---

## 5.8. Kết luận

### 5.8.1. Đánh giá tổng quan

Hệ thống AI Language Tutor đã **hoàn thành các mục tiêu chính** của đồ án:
- Xây dựng được Learning Path có cấu trúc
- AI Tutor hoạt động ổn định với độ chính xác 83.3%
- Các tính năng chính (Grammar, Vocabulary, Practice, Writing, Quiz) đều hoạt động tốt
- Người dùng thử nghiệm đánh giá tích cực (4.3/5)

**Đánh giá theo từng tiêu chí:**
- **Chức năng:** 9/10 (hoàn thiện, ít lỗi)
- **Độ chính xác:** 8/10 (AI đạt 83%, chấp nhận được)
- **Khả năng sử dụng:** 8.5/10 (giao diện thân thiện)
- **Hiệu năng:** 7.5/10 (chấp nhận được, chưa tối ưu)

**Điểm tổng:** **8.2/10**

### 5.8.2. Hạn chế và hướng phát triển

**Hạn chế chính:**
1. Thiếu Speaking & Listening (do giới hạn thời gian)
2. Chưa có mobile app (nằm ngoài scope)
3. Quy mô thử nghiệm nhỏ (5 người, 1 tuần)

**Hướng phát triển tiếp theo:**
1. Thêm Speaking practice với Speech-to-Text
2. Thêm Listening comprehension với audio
3. Tối ưu tốc độ (caching, prompt optimization)
4. Mở rộng thử nghiệm với nhiều người dùng hơn
5. Phát triển mobile app (React Native)

### 5.8.3. Đóng góp của đề tài

**Về mặt kỹ thuật:**
- Ứng dụng thành công Large Language Model (Llama 3.1) vào giáo dục
- Xây dựng hệ thống AI Agent với nhiều khả năng (phân tích lỗi, tạo bài tập, chấm bài)
- Thiết kế Learning Path theo chuẩn CEFR quốc tế

**Về mặt thực tiễn:**
- Tạo công cụ học tiếng Anh miễn phí cho sinh viên
- Cá nhân hóa learning path theo từng người
- Có thể mở rộng thành sản phẩm thực tế

**Về mặt học thuật:**
- Nghiên cứu và áp dụng các kỹ thuật AI hiện đại
- Tìm hiểu CEFR framework trong giảng dạy ngoại ngữ
- Thực hành full-stack development (Frontend, Backend, Database, AI)

---

## PHỤ LỤC

### A. Danh sách 30 câu lỗi dùng để test AI

[Liệt kê 30 câu cụ thể, đáp án đúng, và kết quả AI]

### B. Screenshots giao diện

[Ảnh chụp màn hình các tính năng chính]

### C. Google Form khảo sát

[Link hoặc ảnh chụp form]

### D. Raw data thời gian phản hồi

[Bảng chi tiết 10 lần đo cho mỗi API]
