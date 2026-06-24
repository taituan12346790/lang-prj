# ĐÁNH GIÁ CỦA GIẢNG VIÊN PHẢN BIỆN - CHƯƠNG 5

## 1. VẤN ĐỀ VĂN PHONG

### ❌ LỖI: Sử dụng ngôi thứ nhất
- "tác giả đã chuẩn bị 20 câu"
- "tác giả thực hiện thử nghiệm"
- "tác giả đã viết 10 bài văn"

### ✅ SỬA: Dùng câu bị động học thuật
- "Một tập dữ liệu gồm 20 câu được chuẩn bị..."
- "Quá trình thử nghiệm được thực hiện..."
- "10 bài văn mẫu được sử dụng trong thử nghiệm..."

---

### ❌ LỖI: Mang tính quảng bá
- "hệ thống xây dựng thành công"
- "cho thấy tiềm năng ứng dụng trong thực tế"
- "Đây là kết quả chấp nhận được"

### ✅ SỬA: Khách quan, có điều kiện
- "Hệ thống hoàn thành các chức năng đã thiết kế"
- "Kết quả bước đầu cho thấy khả năng hoạt động của hệ thống"
- "Trong phạm vi thử nghiệm, kết quả này phù hợp với mục tiêu đề ra"

---

## 2. SỐ LIỆU THIẾU CƠ SỞ KIỂM CHỨNG

### ⚠️ "54 test case → 54/54 đạt"

**Vấn đề:**
- Không nêu rõ test case là gì
- Tiêu chí "đạt" không rõ ràng
- Không có test case nào fail → Nghi ngờ test không đủ khó

**Cách xử lý:**
- Giữ lại NHƯNG bổ sung: "Các test case kiểm tra chức năng cơ bản..."
- Thêm disclaimer: "Kết quả này chỉ phản ánh khả năng hoạt động trong điều kiện kiểm thử, chưa đánh giá hiệu năng trong môi trường thực tế với tải cao"

---

### ⚠️ "85% accuracy với 20 câu test"

**Vấn đề:**
- Mẫu quá nhỏ (n=20) để khẳng định "độ chính xác"
- Không có confidence interval
- Không có phân tích thống kê
- 17/20 = 85% nhưng không có ý nghĩa thống kê

**Cách xử lý:**
→ KHÔNG NÊN gọi là "độ chính xác 85%"
→ NÊN viết: "Trên tập dữ liệu thử nghiệm gồm 20 câu, hệ thống phát hiện đúng 17 câu. Do quy mô mẫu hạn chế, kết quả này chỉ mang tính tham khảo và cần được đánh giá thêm trên tập dữ liệu lớn hơn."

---

### ⚠️ "±1.9 điểm chênh lệch" trong đánh giá bài viết

**Vấn đề:**
- So sánh AI với chính tác giả tự chấm
- Không có inter-rater reliability
- Không có ground truth
- n=10 quá nhỏ

**Cách xử lý:**
→ KHÔNG NÊN gọi là "độ nhất quán"
→ NÊN viết: "Trên 10 bài viết mẫu, kết quả chấm điểm của AI có chênh lệch trung bình ±1.9 điểm so với đánh giá ban đầu. Do phương pháp so sánh đơn giản và mẫu nhỏ, cần có nghiên cứu sâu hơn với nhiều chuyên gia đánh giá độc lập."

---

### ⚠️ "Thời gian phản hồi 2.2s, 3.0s, ..."

**Vấn đề:**
- Chỉ đo 10 lần
- Không có độ lệch chuẩn, min/max
- Không nêu rõ điều kiện đo (CPU, RAM, network)
- Không kiểm tra concurrent users

**Cách xử lý:**
→ GIỮ LẠI nhưng thêm disclaimer
→ Bổ sung: "Các số liệu đo được trong điều kiện single user, không đại diện cho hiệu năng khi có nhiều người dùng đồng thời"

---

## 3. KẾT LUẬN VƯỢT QUÁ BẰNG CHỨNG

### ❌ "Hệ thống xây dựng thành công một nền tảng..."
→ ✅ "Hệ thống hoàn thành các chức năng đã thiết kế..."

### ❌ "Cho thấy tiềm năng ứng dụng trong thực tế"
→ ✅ "Kết quả bước đầu cho thấy khả năng hoạt động của hệ thống"

### ❌ "Hệ thống đáp ứng được yêu cầu"
→ ✅ "Hệ thống thực hiện được các chức năng đã đề ra trong phạm vi thử nghiệm"

### ❌ "Hiệu quả hơn so với mô hình chatbot hỏi đáp đơn thuần"
→ ❌ BỎ HOÀN TOÀN (không có so sánh thực tế)

---

## 4. TRÙNG LẶP VỚI CHƯƠNG 4

### ❌ NÊN BỎ:
- "Frontend được xây dựng bằng Streamlit..."
- "Backend được phát triển bằng FastAPI..."
- "Việc triển khai các thành phần độc lập giúp..."

### ✅ CHỈ NÊN GIỮ:
- "Hệ thống được triển khai trên Render tại địa chỉ..."
- "Database sử dụng Neon.tech tại Singapore"

---

## 5. NỘI DUNG ĐỊNH TÍNH THIẾU BẰNG CHỨNG

### ⚠️ "Khả năng duy trì ngữ cảnh và cá nhân hóa"

**Vấn đề:** Không có phương pháp đo lường cụ thể

**Cách xử lý:**
→ Viết lại: "Trong quá trình thử nghiệm, hệ thống cho thấy khả năng sử dụng thông tin từ các tương tác trước để tạo phản hồi. Tuy nhiên, chưa có phương pháp đánh giá định lượng cho khía cạnh này."

---

## 6. KHUYẾN NGHỊ TỔNG THỂ

### PHẦN NÊN GIỮ:
✅ Functional testing (54 test case) - nhưng cần disclaimer
✅ 20 câu test phân tích lỗi - nhưng đổi thành "kết quả thử nghiệm bước đầu"
✅ 10 bài viết - nhưng không gọi là "độ chính xác"
✅ Response time - nhưng nêu rõ điều kiện đo

### PHẦN CẦN VIẾT LẠI HOÀN TOÀN:
🔄 Phần "Đánh giá kết quả đạt được" → Quá chủ quan
🔄 Phần "Khả năng duy trì ngữ cảnh" → Thiếu phương pháp đo
🔄 Mô tả môi trường triển khai → Trùng với Chương 4

### PHẦN NÊN BỎ:
❌ "Cho thấy tiềm năng ứng dụng"
❌ "Hiệu quả hơn chatbot đơn thuần"
❌ Các câu kết luận không có bằng chứng

---

## 7. CẤU TRÚC ĐỀ XUẤT MỚI

```
5.1. Môi trường thử nghiệm [VIẾT LẠI - ngắn gọn, không trùng Ch4]
5.2. Kiểm thử chức năng [GIỮ NGUYÊN + thêm disclaimer]
5.3. Thử nghiệm với AI Tutor [SỬA - thêm "bước đầu", "quy mô nhỏ"]
5.4. Thử nghiệm đánh giá bài viết [SỬA - bỏ "độ chính xác"]
5.5. Đo thời gian phản hồi [GIỮ + thêm điều kiện đo]
5.6. Thảo luận [SỬA - khách quan hơn]
5.7. Hạn chế [MỞ RỘNG - nhấn mạnh hạn chế hơn]
5.8. Hướng phát triển [GIỮ NGUYÊN]
5.9. Kết luận [SỬA - không khẳng định quá mức]
```
