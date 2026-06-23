# MỤC LỤC LUẬN VĂN TỐT NGHIỆP
## "XÂY DỰNG AI AGENT HỖ TRỢ HỌC NGOẠI NGỮ"

---

## PHẦN MỞ ĐẦU

### Lời cam đoan
### Lời cảm ơn
### Mục lục
### Danh mục các ký hiệu, chữ viết tắt
### Danh mục các bảng biểu
### Danh mục các hình vẽ, đồ thị

---

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI

### 1.1. Đặt vấn đề
- 1.1.1. Bối cảnh và động lực nghiên cứu
- 1.1.2. Thực trạng học ngoại ngữ hiện nay
- 1.1.3. Những thách thức trong việc học ngoại ngữ

### 1.2. Mục tiêu nghiên cứu
- 1.2.1. Mục tiêu chính
- 1.2.2. Mục tiêu cụ thể

### 1.3. Phạm vi và đối tượng nghiên cứu
- 1.3.1. Đối tượng người học (CEFR A1-C2)
- 1.3.2. Nội dung học (Grammar, Vocabulary, Writing, Practice)
- 1.3.3. Ngôn ngữ mục tiêu (Tiếng Anh)

### 1.4. Phương pháp nghiên cứu
- 1.4.1. Nghiên cứu lý thuyết
- 1.4.2. Phân tích và thiết kế hệ thống
- 1.4.3. Triển khai và thử nghiệm

### 1.5. Ý nghĩa khoa học và thực tiễn
- 1.5.1. Ý nghĩa khoa học
- 1.5.2. Ý nghĩa thực tiễn

### 1.6. Kết cấu luận văn

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

### 2.1. Tổng quan về AI Agent
- 2.1.1. Định nghĩa AI Agent
- 2.1.2. Các loại AI Agent
- 2.1.3. Kiến trúc của AI Agent
- 2.1.4. Ứng dụng AI Agent trong giáo dục

### 2.2. Large Language Models (LLMs)
- 2.2.1. Giới thiệu về LLMs
- 2.2.2. GPT-4 và các mô hình tương tự
- 2.2.3. Prompt Engineering
- 2.2.4. Ứng dụng LLMs trong giảng dạy ngôn ngữ

### 2.3. Phương pháp giảng dạy ngoại ngữ
- 2.3.1. Khung năng lực CEFR (Common European Framework of Reference)
- 2.3.2. Personalized Learning (Học tập cá nhân hóa)
- 2.3.3. Adaptive Learning (Học tập thích ứng)
- 2.3.4. Feedback và Error Correction trong học ngôn ngữ

### 2.4. Công nghệ xây dựng hệ thống
- 2.4.1. Backend Framework: FastAPI
- 2.4.2. Frontend Framework: Streamlit
- 2.4.3. Database: PostgreSQL
- 2.4.4. ORM: SQLAlchemy
- 2.4.5. AI Services: OpenAI API

### 2.5. Các nghiên cứu liên quan
- 2.5.1. Tổng quan các hệ thống AI hỗ trợ học ngoại ngữ
- 2.5.2. So sánh với các giải pháp hiện có
- 2.5.3. Điểm mới của đề tài

---

## CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

### 3.1. Phân tích yêu cầu hệ thống
- 3.1.1. Yêu cầu chức năng (Functional Requirements)
  - Quản lý người dùng và phân cấp
  - Learning Path (Lộ trình học tập theo CEFR)
  - AI Tutor (Trợ lý AI cá nhân hóa)
  - **Hệ thống đánh giá đa dạng:**
    - Placement Test (Kiểm tra đầu vào)
    - Level-up Test (Kiểm tra nâng cấp trình độ)
    - Quiz per Topic (Kiểm tra theo chủ đề)
    - Writing Assessment (Đánh giá bài viết với rubric chi tiết)
    - Practice Exercises (Bài tập thực hành tự động)
  - Error Analysis và Practice Generation
  - Analytics và Progress Tracking
- 3.1.2. Yêu cầu phi chức năng (Non-functional Requirements)
  - Performance (Hiệu suất)
  - Scalability (Khả năng mở rộng)
  - Security (Bảo mật)
  - Usability (Tính khả dụng)

### 3.2. Phân tích các tác nhân (Use Case Analysis)
- 3.2.1. Sơ đồ Use Case tổng quát
- 3.2.2. Use Case: Đăng ký và Placement Test
- 3.2.3. Use Case: Học qua Learning Path
- 3.2.4. Use Case: Làm Quiz theo Topic
- 3.2.5. Use Case: Tương tác với AI Tutor
- 3.2.6. Use Case: Làm Practice Exercises và nhận phản hồi
- 3.2.7. Use Case: Viết bài và được chấm tự động
- 3.2.8. Use Case: Level-up Test
- 3.2.9. Use Case: Theo dõi tiến độ học tập

### 3.3. Thiết kế kiến trúc hệ thống
- 3.3.1. Kiến trúc tổng quát (3-tier Architecture)
- 3.3.2. Presentation Layer (Frontend)
- 3.3.3. Business Logic Layer (Backend API)
- 3.3.4. Data Layer (Database)
- 3.3.5. AI Services Integration
- 3.3.6. Sơ đồ luồng dữ liệu (Data Flow Diagram)

### 3.4. Thiết kế cơ sở dữ liệu
- 3.4.1. Mô hình quan hệ thực thể (ER Diagram)
- 3.4.2. Bảng Users và User Profiles
- 3.4.3. Bảng Topics và Lessons
- 3.4.4. Bảng User Progress và Learning Sessions
- 3.4.5. Bảng Chat Conversations và Messages
- 3.4.6. Bảng Writings và AI Feedback
- 3.4.7. Bảng AI Exercises và Submissions
- 3.4.8. Bảng Analytics và Error Logs

### 3.5. Thiết kế AI Agent
- 3.5.1. Kiến trúc AI Agent
- 3.5.2. Intent Classification (Phân loại mục đích)
- 3.5.3. Context Management (Quản lý ngữ cảnh)
- 3.5.4. Error Analyzer (Phân tích lỗi)
- 3.5.5. Practice Generator (Tạo bài tập)
- 3.5.6. Writing Assessor (Đánh giá bài viết)
- 3.5.7. Feedback Generator (Tạo phản hồi)

### 3.6. Thiết kế giao diện người dùng
- 3.6.1. Nguyên tắc thiết kế UI/UX
- 3.6.2. Wireframes các màn hình chính
  - Màn hình Dashboard
  - Màn hình Topic và Lesson
  - Màn hình AI Chat
  - Màn hình Writing
  - Màn hình Analytics
- 3.6.3. Design System và Theme

---

## CHƯƠNG 4: XÂY DỰNG VÀ TRIỂN KHAI HỆ THỐNG

### 4.1. Môi trường phát triển
- 4.1.1. Công cụ và thư viện sử dụng
- 4.1.2. Cấu hình môi trường development
- 4.1.3. Version Control với Git

### 4.2. Xây dựng Backend
- 4.2.1. Cấu trúc dự án Backend
- 4.2.2. Xây dựng Database Models
- 4.2.3. Xây dựng API Endpoints
  - Authentication API
  - Learning Path API
  - Chat API
  - Writing API
  - Quiz API
  - Analytics API
- 4.2.4. Database Migration với Alembic
- 4.2.5. Authentication và Authorization

### 4.3. Xây dựng AI Services
- 4.3.1. Tích hợp OpenAI API
- 4.3.2. Prompt Engineering cho các chức năng
  - Chat prompt
  - Error analysis prompt
  - Writing assessment prompt
  - Exercise generation prompt
- 4.3.3. Context Management Service
- 4.3.4. Error Analyzer Service
- 4.3.5. Writing Service với Rubric Scoring
- 4.3.6. Practice Generator Service

### 4.4. Xây dựng Frontend
- 4.4.1. Cấu trúc dự án Frontend (Streamlit)
- 4.4.2. Custom CSS và Theming
- 4.4.3. Xây dựng các trang chính
  - Authentication Page
  - Dashboard Page
  - Topic & Lesson Pages
  - Chat Page (AI Tutor)
  - Writing Page
  - Quiz Page
  - Analytics Page
- 4.4.4. State Management
- 4.4.5. API Integration

### 4.5. Xây dựng tính năng nổi bật
- 4.5.1. Learning Path theo CEFR (190 topics x 5 lessons)
- 4.5.2. AI Tutor Mode với Error Analysis
- 4.5.3. Writing Assessment với Detailed Scoring
- 4.5.4. Adaptive Quiz System
- 4.5.5. Analytics Dashboard
- 4.5.6. Chat Learning Activities Tracking

### 4.6. Testing và Quality Assurance
- 4.6.1. Unit Testing
- 4.6.2. Integration Testing
- 4.6.3. User Acceptance Testing
- 4.6.4. Bug Fixing và Optimization

### 4.7. Deployment
- 4.7.1. Chuẩn bị môi trường production
- 4.7.2. Database Migration
- 4.7.3. Environment Configuration
- 4.7.4. Monitoring và Logging

---

## CHƯƠNG 5: THỬ NGHIỆM VÀ ĐÁNH GIÁ

### 5.1. Kế hoạch thử nghiệm
- 5.1.1. Mục tiêu thử nghiệm
- 5.1.2. Phương pháp thử nghiệm
- 5.1.3. Đối tượng tham gia

### 5.2. Thử nghiệm chức năng
- 5.2.1. Test Learning Path
- 5.2.2. Test AI Tutor
- 5.2.3. Test Writing Assessment
- 5.2.4. Test Quiz System
- 5.2.5. Test Analytics

### 5.3. Đánh giá hiệu suất hệ thống
- 5.3.1. Response Time
- 5.3.2. Throughput
- 5.3.3. Accuracy của AI
- 5.3.4. User Experience Metrics

### 5.4. Khảo sát người dùng
- 5.4.1. Thiết kế bảng khảo sát
- 5.4.2. Thu thập dữ liệu
- 5.4.3. Phân tích kết quả

### 5.5. So sánh với các hệ thống tương tự
- 5.5.1. Tiêu chí so sánh
- 5.5.2. Phân tích ưu nhược điểm

### 5.6. Kết quả đạt được
- 5.6.1. Các chức năng đã triển khai
- 5.6.2. Hiệu quả học tập
- 5.6.3. Phản hồi người dùng

### 5.7. Hạn chế và hướng khắc phục
- 5.7.1. Hạn chế về mặt kỹ thuật
- 5.7.2. Hạn chế về dữ liệu và nội dung
- 5.7.3. Đề xuất cải tiến

---

## CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 6.1. Tổng kết đề tài
- 6.1.1. Những vấn đề đã giải quyết được
- 6.1.2. Những đóng góp chính
- 6.1.3. Bài học kinh nghiệm

### 6.2. Hướng phát triển
- 6.2.1. Mở rộng ngôn ngữ mục tiêu
- 6.2.2. Tích hợp Speech Recognition và TTS
- 6.2.3. Gamification và Social Learning
- 6.2.4. Mobile Application
- 6.2.5. Advanced Analytics với Machine Learning
- 6.2.6. Multi-modal Learning (Video, Audio, Reading)

### 6.3. Kết luận

---

## TÀI LIỆU THAM KHẢO

### Tài liệu tiếng Việt
### Tài liệu tiếng Anh
### Tài liệu trực tuyến

---

## PHỤ LỤC

### Phụ lục A: Mã nguồn chính
- A.1. Backend API Core
- A.2. AI Services
- A.3. Frontend Main Pages
- A.4. Database Models

### Phụ lục B: Giao diện hệ thống
- B.1. Screenshots các màn hình chính
- B.2. Flowchart các tính năng

### Phụ lục C: Kết quả khảo sát
- C.1. Bảng câu hỏi khảo sát
- C.2. Kết quả thống kê
- C.3. Biểu đồ phân tích

### Phụ lục D: Tài liệu kỹ thuật
- D.1. Database Schema
- D.2. API Documentation
- D.3. Deployment Guide

### Phụ lục E: Dữ liệu huấn luyện và Prompt Templates
- E.1. Sample Prompts cho các chức năng
- E.2. Rubric chi tiết cho Writing Assessment
- E.3. Error Analysis Rules

---

## GHI CHÚ

- Tổng số trang: khoảng 80-100 trang
- Font chữ: Times New Roman, 13pt
- Lề: Trái 3cm, Phải 2cm, Trên/Dưới 2cm
- Giãn dòng: 1.5

---

## ĐIỂM NỔI BẬT CỦA ĐỀ TÀI

1. **Learning Path cá nhân hóa**: 190 topics với 5 loại lesson (Grammar, Vocabulary, Practice, Writing, Quiz)
2. **AI Tutor thông minh**: Phân tích lỗi và tạo bài tập tự động
3. **Writing Assessment chi tiết**: Chấm điểm theo 4 tiêu chí (Grammar, Vocabulary, Content, Structure)
4. **Adaptive Learning**: Điều chỉnh nội dung dựa trên tiến độ và lỗi của người học
5. **Analytics Dashboard**: Theo dõi chi tiết tiến độ học tập
