#!/usr/bin/env python3
"""Translate all remaining English notes and explanations"""

with open('app/data/topics_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# All notes translations
translations = {
    # Shopping - Topic 8
    "'How much' is for uncountable nouns and asking prices. 'How many' is for countable nouns.":
        "'How much' dùng cho danh từ không đếm được và hỏi giá. 'How many' dùng cho danh từ đếm được.",
    
    # Transportation - Topic 9
    "Use 'by' for method of transport (no article): go by bus. Use 'the' when naming specific: take the number 10 bus.":
        "Dùng 'by' cho phương tiện (không dùng mạo từ): go by bus. Dùng 'the' khi chỉ cụ thể: take the number 10 bus.",
    
    # Questions - Topic 10
    "The auxiliary verb (do/does) must match the subject. With 'to be', no auxiliary needed: Where IS she? (not Where does she is?)":
        "Trợ động từ (do/does) phải khớp với chủ ngữ. Với 'to be', không cần trợ động từ: Where IS she? (không phải Where does she is?)",
    
    # Days/Months - Topic 12
    "Use 'on' for specific days, 'in' for months/years/seasons, 'at' for clock times.":
        "Dùng 'on' cho ngày cụ thể, 'in' cho tháng/năm/mùa, 'at' cho giờ.",
    
    # Jobs - Topic 13
    "Use 'a/an' before job names: He is a teacher. Don't use article when talking generally: Teachers work hard.":
        "Dùng 'a/an' trước tên nghề: He is a teacher. Không dùng mạo từ khi nói chung: Teachers work hard.",
    
    # Places - Topic 14
    "When asking strangers for directions, always start with 'Excuse me' to be lịch sự.":
        "Khi hỏi đường người lạ, luôn bắt đầu với 'Excuse me' để tỏ ra lịch sự.",
    
    # Hobbies - Topic 16
    "Remember: after 'like/love/enjoy/hate', always use verb + -ing (gerund), NOT infinitive.":
        "Nhớ: sau 'like/love/enjoy/hate', luôn dùng động từ + -ing (gerund), KHÔNG dùng to-infinitive.",
    
    # Weather - Topic 17
    "Notice: In English, we use 'It IS sunny' (adjective). In Vietnamese, you say 'Trời nắng' (sunny sky/weather). The grammar is different!":
        "Chú ý: Trong tiếng Anh, dùng 'It IS sunny' (tính từ). Trong tiếng Việt, bạn nói 'Trời nắng'. Cấu trúc ngữ pháp khác nhau!",
    
    # School - Topic 18
    "In English, we say 'study' for academic subjects and 'learn' for acquiring skills.":
        "Trong tiếng Anh, dùng 'study' cho môn học và 'learn' cho việc học kỹ năng.",
    
    # Clothes - Topic 19
    "This/that for ONE item. These/those for MULTIPLE items. Remember: this shirt ✓ but these shirts ✓ (match singular/plural).":
        "This/that cho MỘT vật. These/those cho NHIỀU vật. Nhớ: this shirt ✓ và these shirts ✓ (phải khớp số ít/nhiều).",
    
    # Review - Topic 20
    "Congratulations on completing A1! Keep practicing daily for best results.":
        "Chúc mừng bạn hoàn thành A1! Hãy luyện tập hàng ngày để đạt kết quả tốt nhất.",
    
    # Food - Topic 6
    "Some/any: 'some' in affirmative/offers, 'any' in negative/questions.":
        "Some/any: 'some' trong câu khẳng định/đề nghị, 'any' trong câu phủ định/nghi vấn.",
    
    # Home - Topic 7
    "'There is' for singular, 'There are' for plural. For questions: 'Is there...?' / 'Are there...?'":
        "'There is' cho số ít, 'There are' cho số nhiều. Câu hỏi: 'Is there...?' / 'Are there...?'",
}

# Apply translations
for eng, vie in translations.items():
    content = content.replace(eng, vie)

# Now translate remaining explanations found by checker
explanation_translations = {
    # Topic 2
    "Dùng 'How old are you? – I am [số] years old.' để hỏi và nói về tuổi. Dùng 'What time is it? – It is [giờ].' để nói giờ.":
        "Dùng 'How old are you? – I am [số] years old.' để hỏi và nói về tuổi. Dùng 'What time is it? – It is [giờ].' để nói giờ.",
    
    # Topic 7
    "'There is/are' describes existence or location of something.":
        "'There is/are' mô tả sự tồn tại hoặc vị trí của cái gì đó.",
    
    "On the table (trên bàn), under the chair (dưới ghế), next to (bên cạnh).":
        "On the table (trên bàn), under the chair (dưới ghế), next to (bên cạnh).",
    
    # Topic 17
    "Use 'It is + adjective' for weather: It is sunny. Use weather verbs: It rains, it snows.":
        "Dùng 'It is + tính từ' cho thời tiết: It is sunny. Dùng động từ chỉ thời tiết: It rains, it snows.",
    
    "It rains (present simple for facts/habits).":
        "It rains (thì hiện tại đơn cho sự thật/thói quen).",
    
    "Foggy = sương mù (reduced visibility).":
        "Foggy = sương mù (tầm nhìn kém).",
    
    "Spring = mùa xuân (first season).":
        "Spring = mùa xuân (mùa đầu tiên).",
    
    # Topic 18
    "Use 'have/has' to talk about schedule: I have Math on Monday.":
        "Dùng 'have/has' để nói về thời khóa biểu: I have Math on Monday.",
    
    "Art = Mỹ thuật (creative subject).":
        "Art = Mỹ thuật (môn sáng tạo).",
    
    # Topic 19
    "'Be wearing' describes what someone is wearing right now.":
        "'Be wearing' mô tả ai đó đang mặc gì.",
    
    "Too + adjective = quá (negative meaning): too big, too small, too expensive.":
        "Too + tính từ = quá (nghĩa tiêu cực): too big, too small, too expensive.",
    
    "Jeans = quần jean (always plural in English).":
        "Jeans = quần jean (luôn ở dạng số nhiều trong tiếng Anh).",
    
    # Topic 20
    "Review all A1 grammar points and identify common mistakes you still make.":
        "Ôn tập tất cả điểm ngữ pháp A1 và nhận diện lỗi phổ biến bạn vẫn mắc phải.",
}

for eng, vie in explanation_translations.items():
    content = content.replace(eng, vie)

with open('app/data/topics_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Translated {len(translations)} notes")
print(f"✓ Translated {len(explanation_translations)} explanations")
print(f"✓ Total: {len(translations) + len(explanation_translations)} items")
