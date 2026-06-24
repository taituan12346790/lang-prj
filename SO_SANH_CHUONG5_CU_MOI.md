# SO SÁNH CHƯƠNG 5: BẢN CŨ vs BẢN HỌC THUẬT

## TÓM TẮT THAY ĐỔI

### 1. VĂN PHONG

| BẢN CŨ (chuong5_an_toan.txt) | BẢN MỚI (chuong5_hoc_thuat_final.txt) |
|---|---|
| ❌ "tác giả đã chuẩn bị 20 câu" | ✅ "Một tập dữ liệu gồm 20 câu được chuẩn bị" |
| ❌ "tác giả thực hiện thử nghiệm" | ✅ "Quá trình thử nghiệm được thực hiện" |
| ❌ "cho thấy tiềm năng ứng dụng" | ✅ "Kết quả chỉ phản ánh khả năng hoạt động bước đầu" |
| ❌ "hệ thống xây dựng thành công" | ✅ "Hệ thống hoàn thành các chức năng đã thiết kế" |
| ❌ "Nhìn chung, kết quả cho thấy..." | ✅ "Kết quả cho thấy... Tuy nhiên..." |

---

### 2. XỬ LÝ SỐ LIỆU

#### A. "85% ACCURACY"

**Bản cũ:**
> "AI Tutor đạt độ chính xác 85% trong việc phát hiện và phân tích lỗi"

**Bản mới:**
> "Trên tập dữ liệu thử nghiệm, hệ thống phát hiện đúng 17 trong số 20 câu... Cần lưu ý rằng quy mô mẫu (n=20) còn nhỏ và chưa đủ để đưa ra kết luận mang tính thống kê. Kết quả này chỉ phản ánh khả năng hoạt động bước đầu..."

**Thay đổi:**
- ❌ Không gọi là "độ chính xác 85%"
- ✅ Nói "phát hiện đúng 17/20"
- ✅ Thêm disclaimer về quy mô mẫu
- ✅ Nhấn mạnh "chỉ phản ánh bước đầu"

---

#### B. "±1.9 ĐIỂM CHÊNH LỆCH"

**Bản cũ:**
> "AI Writing Assessment có độ chênh lệch trung bình ±1.9 điểm so với tự đánh giá, cho thấy hệ thống hoạt động tương đối nhất quán"

**Bản mới:**
> "Kết quả cho thấy độ chênh lệch trung bình là ±1.9 điểm... Cần lưu ý rằng phương pháp so sánh này có nhiều hạn chế. Thứ nhất, quy mô mẫu nhỏ (n=10)... Thứ hai, việc so sánh với đánh giá ban đầu thay vì với đánh giá của nhiều chuyên gia... Thứ ba, không có ground truth rõ ràng... Do đó, kết quả này chỉ cho thấy AI Agent có khả năng thực hiện chức năng chấm điểm, nhưng chưa đủ cơ sở để khẳng định về độ chính xác hay tính nhất quán"

**Thay đổi:**
- ❌ Không khẳng định "độ nhất quán"
- ✅ Liệt kê 3 hạn chế của phương pháp
- ✅ Kết luận hạn chế: "chỉ cho thấy có khả năng", "chưa đủ cơ sở khẳng định"

---

#### C. RESPONSE TIME

**Bản cũ:**
> "Tuy nhiên, thời gian này vẫn nằm trong ngưỡng chấp nhận được đối với các ứng dụng AI"

**Bản mới:**
> "Các số liệu này chỉ phản ánh thời gian phản hồi trong điều kiện single user và không đại diện cho hiệu năng khi có nhiều người dùng đồng thời. Ngoài ra, thời gian phản hồi phụ thuộc nhiều vào độ trễ mạng, tốc độ xử lý của dịch vụ Groq API và trạng thái server tại thời điểm đo."

**Thay đổi:**
- ❌ Bỏ câu "chấp nhận được" (mang tính đánh giá chủ quan)
- ✅ Thêm disclaimer về điều kiện đo
- ✅ Nhấn mạnh các yếu tố ảnh hưởng

---

### 3. LOẠI BỎ NỘI DUNG KHÔNG CÓ BẰNG CHỨNG

#### Bản cũ có, Bản mới BỎ/SỬA:

| Nội dung cũ | Lý do | Xử lý |
|---|---|---|
| "Đây là kết quả chấp nhận được đối với hệ thống nguyên mẫu" | Chủ quan | ❌ BỎ |
| "cho thấy tiềm năng ứng dụng trong thực tế" | Vượt quá bằng chứng | ❌ BỎ |
| "hiệu quả hơn so với mô hình chatbot hỏi đáp đơn thuần" | Không có so sánh thực tế | ❌ BỎ |
| "hệ thống đáp ứng được yêu cầu" | Khẳng định quá mức | ✅ SỬA → "thực hiện được các chức năng trong phạm vi thử nghiệm" |

---

### 4. BỔ SUNG DISCLAIMER VÀ HẠN CHẾ

**Bản cũ:**
- Phần "Hạn chế" có 5 đoạn
- Văn phong vẫn còn lạc quan

**Bản mới:**
- Phần "Hạn chế" có 7 đoạn chi tiết
- Nhấn mạnh hạn chế ở MỌI phần kết quả
- Thêm disclaimer ngay sau MỖI bảng số liệu

**Ví dụ cụ thể:**

Sau bảng 54 test case, bản mới thêm:
> "Tuy nhiên, kết quả này chỉ phản ánh khả năng hoạt động ở mức độ chức năng cơ bản. Các khía cạnh như hiệu năng khi có nhiều người dùng đồng thời, khả năng xử lý lỗi trong các tình huống phức tạp và độ ổn định trong thời gian dài vẫn chưa được đánh giá đầy đủ."

---

### 5. VIẾT LẠI HOÀN TOÀN

#### Phần "Đánh giá kết quả đạt được" → "Thảo luận"

**Bản cũ (6 đoạn, mang tính quảng bá):**
- "hệ thống xây dựng thành công"
- "Đây là kết quả chấp nhận được"
- "cho thấy tiềm năng ứng dụng"

**Bản mới (7 đoạn, phân tích khách quan):**
- Thảo luận từng phần kết quả
- Mỗi đoạn có cấu trúc: "Kết quả + Nhưng + Hạn chế"
- Kết thúc: "chưa đủ cơ sở để đưa ra kết luận mang tính thống kê"

---

#### Phần "Khả năng duy trì ngữ cảnh và cá nhân hóa"

**Bản cũ:**
> "Kết quả cho thấy hệ thống có khả năng tạo phản hồi phù hợp... AI Tutor duy trì được ngữ cảnh... Kết quả thực nghiệm cho thấy việc kết hợp AI Agent giúp hệ thống hỗ trợ hiệu quả hơn so với mô hình chatbot hỏi đáp đơn thuần."

**Bản mới:**
> "Trong quá trình thử nghiệm, hệ thống cho thấy khả năng sử dụng thông tin từ các tương tác trước đó... Tuy nhiên, chưa có phương pháp đánh giá định lượng cho khía cạnh này. Việc đo lường mức độ hiệu quả của cơ chế cá nhân hóa và khả năng duy trì ngữ cảnh cần được nghiên cứu thêm trong tương lai."

**Thay đổi:**
- ❌ Bỏ so sánh "hiệu quả hơn chatbot" (không có bằng chứng)
- ✅ Thừa nhận "chưa có phương pháp đánh giá định lượng"
- ✅ Nói "cần nghiên cứu thêm"

---

### 6. LOẠI BỎ TRÙNG LẶP VỚI CHƯƠNG 4

**Bản cũ:**
- Mô tả chi tiết Streamlit, FastAPI, PostgreSQL
- "Frontend được xây dựng bằng Streamlit..."
- "Backend được phát triển bằng FastAPI..."
- "Việc triển khai các thành phần độc lập giúp..."

**Bản mới:**
- Chỉ nêu deployment environment
- Tập trung vào: Render, URL, khu vực server
- Không lặp lại công nghệ đã nói ở Chương 4

---

### 7. KẾT LUẬN CHƯƠNG

**Bản cũ (3 đoạn):**
- Liệt kê thành tích (54/54, 85%, ±1.9, 2-3s)
- "Nhìn chung, kết quả thực nghiệm cho thấy..."
- "khẳng định tính khả thi"

**Bản mới (3 đoạn):**
- Tóm tắt phương pháp và kết quả
- "Tuy nhiên, tất cả các thử nghiệm đều được thực hiện trên quy mô nhỏ và với phương pháp đơn giản"
- "kết quả chỉ phản ánh khả năng hoạt động bước đầu và chưa đủ cơ sở để đưa ra kết luận mang tính thống kê"
- Nhấn mạnh hạn chế cần khắc phục

---

## ĐIỂM KHÁC BIỆT CỐT LÕI

| Khía cạnh | Bản cũ | Bản mới |
|---|---|---|
| **Văn phong** | Mang tính quảng bá | Khách quan, học thuật |
| **Ngôi** | "tác giả", "tôi" | Câu bị động |
| **Kết luận** | "thành công", "tiềm năng" | "bước đầu", "chưa đủ cơ sở" |
| **Số liệu** | Khẳng định "85% accuracy" | "17/20 câu + disclaimer" |
| **Hạn chế** | Nhắc qua | Nhấn mạnh ở MỌI phần |
| **So sánh** | "hiệu quả hơn chatbot" | Bỏ (không có bằng chứng) |
| **Tổng quan** | Lạc quan | Thực tế, trung thực |

---

## KẾT LUẬN

### Bản cũ (chuong5_an_toan.txt):
✅ Đã bỏ user survey
❌ Vẫn còn văn phong quảng bá
❌ Khẳng định quá mức (85% accuracy, tiềm năng ứng dụng)
❌ Thiếu disclaimer đầy đủ

### Bản mới (chuong5_hoc_thuat_final.txt):
✅ Văn phong học thuật chuẩn
✅ Khách quan, không quảng bá
✅ Mọi số liệu đều có disclaimer
✅ Nhấn mạnh hạn chế và phạm vi áp dụng
✅ Không khẳng định quá bằng chứng

---

## KHUYẾN NGHỊ

**Dùng file nào để nộp?**

→ **`chuong5_hoc_thuat_final.txt`** ← An toàn nhất cho bảo vệ

**Lý do:**
1. Giảng viên phản biện khó tìm ra lỗ hổng
2. Mọi khẳng định đều có điều kiện rõ ràng
3. Hạn chế được nêu trung thực
4. Không có nội dung vượt quá bằng chứng

**Khi bảo vệ:**
- Nhấn mạnh: "Đây là kết quả thử nghiệm BỘ ĐẦU trên quy mô NHỎ"
- Thừa nhận hạn chế: "Cần đánh giá thêm trên tập dữ liệu lớn hơn"
- Tránh khẳng định: "Chưa đủ cơ sở để kết luận về độ chính xác"
