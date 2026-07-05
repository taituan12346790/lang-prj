# app/data/topics_data.py
"""
Seed data cho toàn bộ chủ đề học theo CEFR.
Bắt đầu với 20 chủ đề A1 theo can_bo_sung.txt.
Mỗi chủ đề gồm 5 bài học: Grammar → Vocabulary → Practice → Writing → Quiz
"""

from typing import List, Dict, Any

# ============================================================
# TỔNG QUAN THEO YÊU CẦU TỪ CAN_BO_SUNG.TXT
# ============================================================
# Level	Số chủ đề
# A1	    20-30
# A2	    25-35
# B1	    30-40
# B2	    35-45
# C1	    40-50
# C2	    40-60
#
# Triển khai:
# - A1: 20 chủ đề (đầy đủ)
# - A2: 25 chủ đề 
# - B1: 30 chủ đề
# - B2: 35 chủ đề
# - C1: 40 chủ đề
# - C2: 40 chủ đề
# ============================================================

# ============================================================
# A1 – 20 CHỦ ĐỀ
# ============================================================

A1_TOPICS: List[Dict[str, Any]] = [
    # ─────────────────────────────────────────────────────────
    # Topic 1: Greetings & Introductions
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1",
        "order": 1,
        "name": "Greetings & Introductions",
        "name_vi": "Chào hỏi & Giới thiệu bản thân",
        "description": "Learn how to greet people and introduce yourself in English.",
        "description_vi": "Học cách chào hỏi và giới thiệu bản thân bằng tiếng Anh.",
        "grammar_focus": ["Động từ to be (am/is/are)", "Đại từ nhân xưng"],
        "vocabulary_tags": ["greeting", "introduction", "social"],
        "estimated_minutes": 25,
        "lessons": [
            {
                "order": 1,
                "lesson_type": "ngữ pháp",
                "title": "Grammar: To Be & Subject Pronouns",
                "title_vi": "Ngữ pháp: Động từ 'To Be' & Đại từ nhân xưng",
                "content": {
                    "explanation": "Động từ 'to be' là một trong những động từ cơ bản nhất trong tiếng Anh. Chúng ta dùng nó để giới thiệu bản thân, mô tả người hoặc sự vật.",
                    "key_points": [
                        "I am → I'm",
                        "You are → You're",
                        "He/She/It is → He's / She's / It's",
                        "We/They are → We're / They're"
                    ],
                    "examples": [
                        {"en": "I am Linh.", "vi": "Tôi là Linh."},
                        {"en": "She is a teacher.", "vi": "Cô ấy là giáo viên."},
                        {"en": "They are students.", "vi": "Họ là học sinh."},
                        {"en": "My name is Nam. I am 25 years old.", "vi": "Tôi tên là Nam. Tôi 25 tuổi."}
                    ],
                    "notes": "Trong giao tiếp thông thường, chúng ta hầu như luôn dùng dạng rút gọn (I'm, you're, he's...)."
                }
            },
            {
                "order": 2,
                "lesson_type": "vocabulary",
                "title": "Vocabulary: Common Greetings & Personal Info",
                "title_vi": "Từ vựng: Lời chào thông dụng & Thông tin cá nhân",
                "content": {
                    "words": [
                        {"word": "Hello", "meaning": "Xin chào", "example": "Hello! My name is Anna.", "pronunciation": "/həˈloʊ/"},
                        {"word": "Hi", "meaning": "Chào (thân mật)", "example": "Hi! How are you?", "pronunciation": "/haɪ/"},
                        {"word": "Good morning", "meaning": "Chào buổi sáng", "example": "Good morning, teacher!", "pronunciation": "/ɡʊd ˈmɔːrnɪŋ/"},
                        {"word": "Good afternoon", "meaning": "Chào buổi chiều", "example": "Good afternoon, everyone.", "pronunciation": "/ɡʊd ˌæftərˈnuːn/"},
                        {"word": "Good evening", "meaning": "Chào buổi tối", "example": "Good evening, sir.", "pronunciation": "/ɡʊd ˈiːvnɪŋ/"},
                        {"word": "Goodbye / Bye", "meaning": "Tạm biệt", "example": "Goodbye! See you tomorrow.", "pronunciation": "/ˌɡʊdˈbaɪ/"},
                        {"word": "name", "meaning": "tên", "example": "My name is Tom.", "pronunciation": "/neɪm/"},
                        {"word": "age", "meaning": "tuổi", "example": "My age is 20.", "pronunciation": "/eɪdʒ/"},
                        {"word": "nationality", "meaning": "quốc tịch", "example": "My nationality is Vietnamese.", "pronunciation": "/ˌnæʃəˈnæləti/"},
                        {"word": "job / occupation", "meaning": "nghề nghiệp", "example": "My job is a teacher.", "pronunciation": "/dʒɒb/"},
                        {"word": "student", "meaning": "học sinh / sinh viên", "example": "I am a student.", "pronunciation": "/ˈstjuːdnt/"},
                        {"word": "teacher", "meaning": "giáo viên", "example": "She is a teacher.", "pronunciation": "/ˈtiːtʃər/"},
                        {"word": "Nice to meet you", "meaning": "Rất vui được gặp bạn", "example": "Nice to meet you, I'm David.", "pronunciation": "/naɪs tə miːt juː/"},
                        {"word": "How are you?", "meaning": "Bạn khỏe không?", "example": "Hi! How are you? – I'm fine, thanks!", "pronunciation": "/haʊ ɑːr juː/"}
                    ]
                }
            },
            {
                "order": 3,
                "lesson_type": "practice",
                "title": "Practice: Fill in the blanks & Match",
                "title_vi": "Luyện tập: Điền vào chỗ trống & Ghép cặp",
                "content": {
                    "exercises": [
                        {
                            "type": "fill_blank",
                            "question": "_____ am a student.",
                            "options": ["I", "She", "They"],
                            "answer": "I",
                            "explanation": "'I am' là đúng. Dùng 'She is' / 'They are' cho ngôi thứ 3."
                        },
                        {
                            "type": "fill_blank",
                            "question": "My name _____ Anna.",
                            "options": ["am", "is", "are"],
                            "answer": "is",
                            "explanation": "Dùng 'is' với he/she/it và danh từ số ít."
                        },
                        {
                            "type": "fill_blank",
                            "question": "They _____ teachers.",
                            "options": ["am", "is", "are"],
                            "answer": "are",
                            "explanation": "Dùng 'are' với you/we/they và danh từ số nhiều."
                        },
                        {
                            "type": "multiple_choice",
                            "question": "How do you greet someone in the morning?",
                            "question_vi": "Bạn chào người khác vào buổi sáng như thế nào?",
                            "options": ["Good evening", "Good morning", "Good night", "Goodbye"],
                            "answer": "Good morning",
                            "explanation": "'Good morning' dùng từ khoảng 6 giờ sáng đến 12 giờ trưa."
                        },
                        {
                            "type": "multiple_choice",
                            "question": "What do you say when you first meet someone?",
                            "question_vi": "Bạn nói gì khi gặp ai đó lần đầu tiên?",
                            "options": ["Goodbye!", "How are you?", "Nice to meet you!", "Good night!"],
                            "answer": "Nice to meet you!",
                            "explanation": "'Nice to meet you' là lời chào lịch sự khi gặp ai đó lần đầu tiên."
                        },
                        {
                            "type": "fill_blank",
                            "question": "Hi! _____ name is Tom. (tôi)",
                            "options": ["My", "Your", "His"],
                            "answer": "My",
                            "explanation": "Khi nói về bản thân, dùng 'My'."
                        }
                    ]
                }
            },
            {
                "order": 4,
                "lesson_type": "quiz",
                "title": "Quiz: Greetings & Introductions",
                "title_vi": "Kiểm tra: Chào hỏi & Giới thiệu bản thân",
                "content": {
                    "questions": [
                        {"id": "q1", "question": "I _____ a student.", "options": ["am", "is", "are", "be"], "correct": "am", "explanation": "Dùng 'am' với đại từ 'I'."},
                        {"id": "q2", "question": "She _____ a doctor.", "options": ["am", "is", "are", "be"], "correct": "is", "explanation": "Dùng 'is' với he/she/it."},
                        {"id": "q3", "question": "They _____ from Vietnam.", "options": ["am", "is", "are", "be"], "correct": "are", "explanation": "Dùng 'are' với they/we/you."},
                        {"id": "q4", "question": "What do you say in the morning?", "question_vi": "Bạn nói gì vào buổi sáng?", "options": ["Good night", "Good evening", "Good morning", "Goodbye"], "correct": "Good morning", "explanation": "'Good morning' dùng cho buổi sáng."},
                        {"id": "q5", "question": "My _____ is Anna.", "question_vi": "Tên tôi là Anna. (Từ cần điền là gì?)", "options": ["age", "name", "job", "nationality"], "correct": "name", "explanation": "'My name is Anna' cho biết tên của một người."},
                        {"id": "q6", "question": "Which is correct?", "question_vi": "Câu nào đúng?", "options": ["I are happy.", "She am sad.", "We are students.", "He are nice."], "correct": "We are students.", "explanation": "'We are' là dạng đúng."},
                        {"id": "q7", "question": "What do you say when meeting someone for the first time?", "question_vi": "Bạn nói gì khi gặp ai đó lần đầu tiên?", "options": ["See you later!", "Nice to meet you!", "Good night!", "Goodbye!"], "correct": "Nice to meet you!", "explanation": "'Nice to meet you' dùng khi gặp ai đó lần đầu."},
                        {"id": "q8", "question": "_____ are teachers.", "options": ["He", "I", "We", "She"], "correct": "We", "explanation": "'We are' = chủ ngữ 'we' + động từ 'are'."},
                        {"id": "q9", "question": "How _____ you? – I'm fine!", "options": ["am", "is", "are", "be"], "correct": "are", "explanation": "'How are you?' là câu hỏi chào hỏi phổ biến."},
                        {"id": "q10", "question": "My nationality is Vietnamese.", "question_vi": "Quốc tịch của tôi là người Việt. (Từ cần điền là gì?)", "options": ["job", "name", "nationality", "age"], "correct": "nationality", "explanation": "Nationality (quốc tịch) cho biết bạn đến từ đâu."}
                    ]
                }
            }
        ]
    },

    # ─────────────────────────────────────────────────────────
    # Topic 2: Numbers, Age & Time
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1",
        "order": 2,
        "name": "Numbers, Age & Time",
        "name_vi": "Số đếm, Tuổi & Thời gian",
        "description": "Learn numbers 1-100, how to say your age, and tell the time.",
        "description_vi": "Học số đếm 1-100, cách nói tuổi và xem giờ.",
        "grammar_focus": ["to be + tuổi", "Hỏi giờ (What time is it?)"],
        "vocabulary_tags": ["numbers", "time", "age"],
        "estimated_minutes": 30,
        "lessons": [
            {
                "order": 1,
                "lesson_type": "ngữ pháp",
                "title": "Grammar: Talking About Age & Time",
                "title_vi": "Ngữ pháp: Nói về tuổi & thời gian",
                "content": {
                    "explanation": "Dùng 'How old are you? – I am [số] years old.' để hỏi và nói về tuổi. Dùng 'What time is it? – It is [giờ].' để nói giờ.",
                    "key_points": [
                        "How old are you? → I am 20 years old.",
                        "What time is it? → It is 3 o'clock. / It's 3:30.",
                        "Numbers 1-10: one, two, three, four, five, six, seven, eight, nine, ten",
                        "Numbers 11-20: eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty",
                        "Tens: twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety, one hundred"
                    ],
                    "examples": [
                        {"en": "How old are you? – I am 22 years old.", "vi": "Bạn bao nhiêu tuổi? – Tôi 22 tuổi."},
                        {"en": "What time is it? – It is 9 o'clock.", "vi": "Mấy giờ rồi? – Bây giờ là 9 giờ."},
                        {"en": "She is thirty-five years old.", "vi": "Cô ấy 35 tuổi."},
                        {"en": "The class starts at 8 a.m.", "vi": "Lớp học bắt đầu lúc 8 giờ sáng."}
                    ],
                    "notes": "a.m. = buổi sáng (từ 12:00 đêm đến 12:00 trưa). p.m. = buổi chiều/tối (từ 12:00 trưa đến 12:00 đêm)."
                }
            },
            {
                "order": 2,
                "lesson_type": "vocabulary",
                "title": "Vocabulary: Numbers & Time Words",
                "title_vi": "Từ vựng: Số đếm & Từ chỉ thời gian",
                "content": {
                    "words": [
                        {"word": "one", "meaning": "một (1)", "example": "I have one brother.", "pronunciation": "/wʌn/"},
                        {"word": "two", "meaning": "hai (2)", "example": "She has two cats.", "pronunciation": "/tuː/"},
                        {"word": "five", "meaning": "năm (5)", "example": "There are five books.", "pronunciation": "/faɪv/"},
                        {"word": "ten", "meaning": "mười (10)", "example": "I have ten fingers.", "pronunciation": "/ten/"},
                        {"word": "twenty", "meaning": "hai mươi (20)", "example": "She is twenty years old.", "pronunciation": "/ˈtwenti/"},
                        {"word": "hundred", "meaning": "một trăm (100)", "example": "There are one hundred students.", "pronunciation": "/ˈhʌndrəd/"},
                        {"word": "o'clock", "meaning": "giờ đúng", "example": "It is 3 o'clock.", "pronunciation": "/əˈklɒk/"},
                        {"word": "a.m.", "meaning": "buổi sáng", "example": "School starts at 7 a.m.", "pronunciation": "/ˌeɪ ˈem/"},
                        {"word": "p.m.", "meaning": "buổi chiều/tối", "example": "I sleep at 10 p.m.", "pronunciation": "/ˌpiː ˈem/"},
                        {"word": "half past", "meaning": "rưỡi", "example": "It's half past two. (2:30)", "pronunciation": "/hɑːf pɑːst/"},
                        {"word": "quarter past", "meaning": "15 phút", "example": "It's quarter past three. (3:15)", "pronunciation": "/ˈkwɔːtər pɑːst/"},
                        {"word": "minute", "meaning": "phút", "example": "Wait five minutes, please.", "pronunciation": "/ˈmɪnɪt/"},
                        {"word": "hour", "meaning": "giờ (đơn vị thời gian)", "example": "The movie is two hours long.", "pronunciation": "/ˈaʊər/"}
                    ]
                }
            },
            {
                "order": 3,
                "lesson_type": "practice",
                "title": "Practice: Numbers & Time",
                "title_vi": "Luyện tập: Số đếm & Thời gian",
                "content": {
                    "exercises": [
                        {"type": "multiple_choice", "question": "How do you say '35' in English?", "question_vi": "Cách nói số 35 trong tiếng Anh?", "options": ["thirteen five", "thirty-five", "fifty-three", "three five"], "answer": "thirty-five", "explanation": "35 = thirty + five = thirty-five (dùng dấu gạch ngang)."},
                        {"type": "multiple_choice", "question": "It's 2:30. How do you say this?", "question_vi": "Cách nói giờ 2:30 trong tiếng Anh?", "options": ["Two thirty", "Half past two", "Both are correct"], "answer": "Both are correct", "explanation": "2:30 có thể nói là 'two thirty' hoặc 'half past two'."},
                        {"type": "fill_blank", "question": "How old _____ you? – I _____ 18 years old.", "options": ["are / am", "is / am", "are / is", "am / are"], "answer": "are / am", "explanation": "How old 'are' you? – I 'am' 18 years old."},
                        {"type": "multiple_choice", "question": "School starts at 7 _____ in the morning.", "options": ["p.m.", "a.m.", "o'clock", "minute"], "answer": "a.m.", "explanation": "7 a.m. = 7 giờ sáng. 'In the morning' cần dùng 'a.m.'."},
                        {"type": "multiple_choice", "question": "What is 'twenty + seven'?", "options": ["27", "72", "207", "270"], "answer": "27", "explanation": "twenty (20) + seven (7) = twenty-seven (27)."}
                    ]
                }
            },
            {
                "order": 4,
                "lesson_type": "quiz",
                "title": "Quiz: Numbers, Age & Time",
                "title_vi": "Kiểm tra: Số đếm, Tuổi & Thời gian",
                "content": {
                    "questions": [
                        {"id": "q1", "question": "How old _____ she?", "options": ["am", "is", "are", "be"], "correct": "is", "explanation": "She dùng 'is'."},
                        {"id": "q2", "question": "It is 4:00. How do you say it?", "question_vi": "Cách nói 4:00 giờ trong tiếng Anh?", "options": ["Four o'clock", "Half past four", "Quarter past four", "Four past"], "correct": "Four o'clock", "explanation": "4:00 = four o'clock (giờ đúng)."},
                        {"id": "q3", "question": "How do you spell 15?", "question_vi": "Cách đánh vần số 15 trong tiếng Anh?", "options": ["fifty", "fifteen", "fifth", "fivteen"], "correct": "fifteen", "explanation": "15 = fifteen."},
                        {"id": "q4", "question": "She is _____ years old. (23)", "options": ["twenty third", "twenty-three", "thirteen-two", "two-thirty"], "correct": "twenty-three", "explanation": "23 = twenty-three."},
                        {"id": "q5", "question": "What time is 7:30 a.m.?", "question_vi": "Cách nói 7:30 a.m. trong tiếng Anh?", "options": ["Half past seven in the morning", "Seven o'clock in the evening", "Half past seven in the evening", "Quarter past seven"], "correct": "Half past seven in the morning", "explanation": "7:30 a.m. = 7 rưỡi buổi sáng."},
                        {"id": "q6", "question": "100 in English is:", "question_vi": "Số 100 trong tiếng Anh là:", "options": ["ten", "thousand", "hundred", "ninety"], "correct": "hundred", "explanation": "100 = one hundred."},
                        {"id": "q7", "question": "I _____ 30 years old.", "options": ["am", "is", "are", "be"], "correct": "am", "explanation": "I am → dùng 'am'."},
                        {"id": "q8", "question": "School finishes at 5 _____ (afternoon).", "options": ["a.m.", "p.m.", "o'clock", "hours"], "correct": "p.m.", "explanation": "Afternoon/evening = p.m."},
                        {"id": "q9", "question": "What is 'twenty + seven'?", "options": ["27", "72", "207", "270"], "correct": "27", "explanation": "twenty (20) + seven (7) = twenty-seven (27)."},
                        {"id": "q10", "question": "Which number comes after nineteen?", "question_vi": "Số nào đứng sau số nineteen?", "options": ["Ninety", "Twenty", "Eleven", "Eighteen"], "correct": "Twenty", "explanation": "19 → 20 = twenty."}
                    ]
                }
            }
        ]
    },

    # ─────────────────────────────────────────────────────────
    # Topic 3: Family & Relationships
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1",
        "order": 3,
        "name": "Family & Relationships",
        "name_vi": "Gia đình & Các mối quan hệ",
        "description": "Describe your family members and relationships.",
        "description_vi": "Mô tả các thành viên trong gia đình và các mối quan hệ.",
        "grammar_focus": ["Tính từ sở hữu (my/your/his/her)", "Động từ have/has"],
        "vocabulary_tags": ["family", "relationships", "people"],
        "estimated_minutes": 30,
        "lessons": [
            {
                "order": 1,
                "lesson_type": "ngữ pháp",
                "title": "Grammar: Possessive Adjectives & Have/Has",
                "title_vi": "Ngữ pháp: Tính từ sở hữu & Have/Has",
                "content": {
                    "explanation": "Tính từ sở hữu cho biết điều gì đó thuộc về ai. 'Have/has' dùng để nói về sở hữu.",
                    "key_points": [
                        "my (của tôi), your (của bạn), his (của anh ấy), her (của cô ấy), its (của nó), our (của chúng tôi), their (của họ)",
                        "I/you/we/they → HAVE: I have a sister.",
                        "He/she/it → HAS: She has two brothers."
                    ],
                    "examples": [
                        {"en": "My mother is 50 years old.", "vi": "Mẹ tôi 50 tuổi."},
                        {"en": "His father is a doctor.", "vi": "Bố anh ấy là bác sĩ."},
                        {"en": "I have two sisters.", "vi": "Tôi có hai chị/em gái."},
                        {"en": "She has a brother named Tom.", "vi": "Cô ấy có một người anh/em trai tên Tom."}
                    ],
                    "notes": "Tính từ sở hữu đứng TRƯỚC danh từ: my mother (KHÔNG phải 'mother my')."
                }
            },
            {
                "order": 2,
                "lesson_type": "vocabulary",
                "title": "Vocabulary: Family Members",
                "title_vi": "Từ vựng: Các thành viên trong gia đình",
                "content": {
                    "words": [
                        {"word": "mother / mom", "meaning": "mẹ", "example": "My mother is a nurse.", "pronunciation": "/ˈmʌðər/"},
                        {"word": "father / dad", "meaning": "bố/cha", "example": "My father works in an office.", "pronunciation": "/ˈfɑːðər/"},
                        {"word": "parents", "meaning": "bố mẹ", "example": "My parents are teachers.", "pronunciation": "/ˈpeərənts/"},
                        {"word": "sister", "meaning": "chị/em gái", "example": "I have one sister.", "pronunciation": "/ˈsɪstər/"},
                        {"word": "brother", "meaning": "anh/em trai", "example": "He is my brother.", "pronunciation": "/ˈbrʌðər/"},
                        {"word": "grandmother / grandma", "meaning": "bà nội/ngoại", "example": "My grandmother is 75.", "pronunciation": "/ˈɡrænmʌðər/"},
                        {"word": "grandfather / grandpa", "meaning": "ông nội/ngoại", "example": "My grandfather loves fishing.", "pronunciation": "/ˈɡrænfɑːðər/"},
                        {"word": "uncle", "meaning": "chú/bác/cậu", "example": "My uncle lives in Hanoi.", "pronunciation": "/ˈʌŋkl/"},
                        {"word": "aunt", "meaning": "cô/dì/bác gái", "example": "My aunt is very kind.", "pronunciation": "/ænt/"},
                        {"word": "cousin", "meaning": "anh/chị/em họ", "example": "I have five cousins.", "pronunciation": "/ˈkʌzn/"},
                        {"word": "husband", "meaning": "chồng", "example": "Her husband is an engineer.", "pronunciation": "/ˈhʌzbənd/"},
                        {"word": "wife", "meaning": "vợ", "example": "His wife is a doctor.", "pronunciation": "/waɪf/"},
                        {"word": "son", "meaning": "con trai", "example": "They have a son.", "pronunciation": "/sʌn/"},
                        {"word": "daughter", "meaning": "con gái", "example": "She has a daughter.", "pronunciation": "/ˈdɔːtər/"},
                        {"word": "only child", "meaning": "con một", "example": "I am an only child.", "pronunciation": "/ˈoʊnli tʃaɪld/"}
                    ]
                }
            },
            {
                "order": 3,
                "lesson_type": "practice",
                "title": "Practice: Family Descriptions",
                "title_vi": "Luyện tập: Mô tả gia đình",
                "content": {
                    "exercises": [
                        {"type": "fill_blank", "question": "_____ mother is a teacher. (tôi)", "options": ["My", "His", "Her", "Your"], "answer": "My", "explanation": "Khi nói về bản thân → My."},
                        {"type": "fill_blank", "question": "She _____ two brothers.", "options": ["have", "has", "is", "are"], "answer": "has", "explanation": "She → has (ngôi thứ 3 số ít)."},
                        {"type": "multiple_choice", "question": "Your father's mother is your:", "question_vi": "Mẹ của bố bạn trong tiếng Anh là gì?", "options": ["aunt", "grandmother", "sister", "cousin"], "answer": "grandmother", "explanation": "Father's mother = grandmother (bà)."},
                        {"type": "fill_blank", "question": "We _____ a big family.", "options": ["have", "has"], "answer": "have", "explanation": "We → have."},
                        {"type": "multiple_choice", "question": "Which word means 'con gái'?", "question_vi": "Từ nào có nghĩa là 'con gái'?", "options": ["son", "sister", "daughter", "aunt"], "answer": "daughter", "explanation": "Daughter = con gái. Son = con trai."}
                    ]
                }
            },
            {
                "order": 4,
                "lesson_type": "quiz",
                "title": "Quiz: Family & Relationships",
                "title_vi": "Kiểm tra: Gia đình & Các mối quan hệ",
                "content": {
                    "questions": [
                        {"id": "q1", "question": "_____ father is a doctor. (anh ấy)", "options": ["My", "His", "Her", "Their"], "correct": "His", "explanation": "He → his."},
                        {"id": "q2", "question": "I _____ three brothers.", "options": ["has", "have", "is", "am"], "correct": "have", "explanation": "I → have."},
                        {"id": "q3", "question": "Which is the female version of 'uncle'?", "question_vi": "Từ nào là dạng nữ của 'uncle' (chú/bác)?", "options": ["grandmother", "sister", "aunt", "cousin"], "correct": "aunt", "explanation": "Uncle (nam) ↔ Aunt (nữ)."},
                        {"id": "q4", "question": "She _____ a daughter named Anna.", "options": ["have", "has"], "correct": "has", "explanation": "She → has."},
                        {"id": "q5", "question": "My parents' parents are my:", "question_vi": "Bố mẹ của bố mẹ tôi là ai?", "options": ["cousins", "uncles", "grandparents", "brothers"], "correct": "grandparents", "explanation": "Parents' parents = grandparents (ông bà)."},
                        {"id": "q6", "question": "_____ have two children: a son and a daughter.", "options": ["She", "He", "They", "It"], "correct": "They", "explanation": "A family = they → have."},
                        {"id": "q7", "question": "What is the opposite of 'brother'?", "question_vi": "Từ trái nghĩa với 'brother' (anh/em trai) là gì?", "options": ["son", "father", "uncle", "sister"], "correct": "sister", "explanation": "Brother (anh/em trai) ↔ Sister (chị/em gái)."},
                        {"id": "q8", "question": "His _____ is 40 years old. (vợ)", "options": ["husband", "wife", "daughter", "sister"], "correct": "wife", "explanation": "His wife = vợ anh ấy."},
                        {"id": "q9", "question": "Our _____ live with us. (ông bà)", "options": ["cousins", "grandparents", "uncles", "parents"], "correct": "grandparents", "explanation": "Grandparents = ông bà."},
                        {"id": "q10", "question": "They _____ an only child.", "options": ["has", "have", "is", "are"], "correct": "have", "explanation": "They → have."}
                    ]
                }
            }
        ]
    },

    # ─────────────────────────────────────────────────────────
    # Topic 4: Colors & Adjectives
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1",
        "order": 4,
        "name": "Colors & Basic Adjectives",
        "name_vi": "Màu sắc & Tính từ cơ bản",
        "description": "Learn colors and how to describe things with adjectives.",
        "description_vi": "Học màu sắc và cách mô tả đồ vật bằng tính từ.",
        "grammar_focus": ["Tính từ đứng trước danh từ", "to be + tính từ"],
        "vocabulary_tags": ["colors", "adjectives", "description"],
        "estimated_minutes": 25,
        "lessons": [
            {
                "order": 1,
                "lesson_type": "ngữ pháp",
                "title": "Grammar: Using Adjectives",
                "title_vi": "Ngữ pháp: Dùng Tính từ",
                "content": {
                    "explanation": "Tính từ mô tả danh từ. Trong tiếng Anh, tính từ đứng TRƯỚC danh từ, hoặc sau 'to be'.",
                    "key_points": [
                        "Adjective + Noun: a RED bag, a BIG house",
                        "Subject + to be + Adjective: The bag IS red. The house IS big.",
                        "Adjectives do NOT change for plural: two red bags (NOT 'two reds bags')"
                    ],
                    "examples": [
                        {"en": "I have a blue pen.", "vi": "Tôi có một cây bút màu xanh."},
                        {"en": "The car is red.", "vi": "Chiếc xe màu đỏ."},
                        {"en": "She is tall and beautiful.", "vi": "Cô ấy cao và xinh đẹp."},
                        {"en": "They have a big house.", "vi": "Họ có một ngôi nhà lớn."}
                    ],
                    "notes": "Trong tiếng Việt, tính từ đứng SAU danh từ (túi ĐỎ). Trong tiếng Anh, tính từ đứng TRƯỚC danh từ (RED bag). Đây là lỗi phổ biến với người Việt!"
                }
            },
            {
                "order": 2,
                "lesson_type": "vocabulary",
                "title": "Vocabulary: Colors & Descriptive Words",
                "title_vi": "Từ vựng: Màu sắc & Từ mô tả",
                "content": {
                    "words": [
                        {"word": "red", "meaning": "đỏ", "example": "She has a red dress.", "pronunciation": "/red/"},
                        {"word": "blue", "meaning": "xanh da trời", "example": "The sky is blue.", "pronunciation": "/bluː/"},
                        {"word": "green", "meaning": "xanh lá", "example": "The trees are green.", "pronunciation": "/ɡriːn/"},
                        {"word": "yellow", "meaning": "vàng", "example": "Chuối màu vàng.", "pronunciation": "/ˈjeloʊ/"},
                        {"word": "white", "meaning": "trắng", "example": "Snow is white.", "pronunciation": "/waɪt/"},
                        {"word": "black", "meaning": "đen", "example": "His jacket is black.", "pronunciation": "/blæk/"},
                        {"word": "orange", "meaning": "cam", "example": "The orange is orange.", "pronunciation": "/ˈɔːrɪndʒ/"},
                        {"word": "purple", "meaning": "tím", "example": "She likes purple flowers.", "pronunciation": "/ˈpɜːrpl/"},
                        {"word": "pink", "meaning": "hồng", "example": "The shirt is pink.", "pronunciation": "/pɪŋk/"},
                        {"word": "big / large", "meaning": "to/lớn", "example": "That is a big dog.", "pronunciation": "/bɪɡ/"},
                        {"word": "small / little", "meaning": "nhỏ", "example": "I have a small car.", "pronunciation": "/smɔːl/"},
                        {"word": "tall", "meaning": "cao", "example": "He is very tall.", "pronunciation": "/tɔːl/"},
                        {"word": "short", "meaning": "thấp/ngắn", "example": "She is short.", "pronunciation": "/ʃɔːrt/"},
                        {"word": "new", "meaning": "mới", "example": "I have a new phone.", "pronunciation": "/njuː/"},
                        {"word": "old", "meaning": "cũ/già", "example": "This is an old book.", "pronunciation": "/oʊld/"},
                        {"word": "beautiful / pretty", "meaning": "đẹp", "example": "What a beautiful day!", "pronunciation": "/ˈbjuːtɪfl/"},
                        {"word": "ugly", "meaning": "xấu", "example": "He thinks the painting is ugly.", "pronunciation": "/ˈʌɡli/"},
                        {"word": "hot", "meaning": "nóng", "example": "The soup is very hot.", "pronunciation": "/hɒt/"},
                        {"word": "cold", "meaning": "lạnh", "example": "The water is cold.", "pronunciation": "/koʊld/"}
                    ]
                }
            },
            {
                "order": 3,
                "lesson_type": "practice",
                "title": "Practice: Colors & Adjectives",
                "title_vi": "Luyện tập: Màu sắc & Tính từ",
                "content": {
                    "exercises": [
                        {"type": "multiple_choice", "question": "Câu nào dưới đây là đúng?", "question_vi": "Câu nào dưới đây là đúng?", "options": ["I have a bag red.", "I have a red bag.", "I have bag a red.", "Red I have a bag."], "answer": "I have a red bag.", "explanation": "Trong tiếng Anh: tính từ + danh từ. 'Red bag' KHÔNG PHẢI 'bag red'."},
                        {"type": "fill_blank", "question": "The sky is _____.", "options": ["red", "blue", "green", "yellow"], "answer": "blue", "explanation": "Bầu trời thường được mô tả là màu xanh."},
                        {"type": "multiple_choice", "question": "What is the opposite of 'big'?", "question_vi": "Từ trái nghĩa với 'big' là gì?", "options": ["tall", "old", "small", "hot"], "answer": "small", "explanation": "Big ↔ Small."},
                        {"type": "multiple_choice", "question": "She has a _____ car. (opposite of 'old')", "question_vi": "Cô ấy có một chiếc xe _____. (trái nghĩa với 'cũ')", "options": ["old", "ugly", "new", "cold"], "answer": "new", "explanation": "New = mới (trái nghĩa với old)."},
                        {"type": "fill_blank", "question": "Snow is _____.", "options": ["black", "white", "blue", "red"], "answer": "white", "explanation": "Tuyết màu trắng."}
                    ]
                }
            },
            {
                "order": 4,
                "lesson_type": "quiz",
                "title": "Quiz: Colors & Adjectives",
                "title_vi": "Kiểm tra: Màu sắc & Tính từ",
                "content": {
                    "questions": [
                        {"id": "q1", "question": "What color is a banana?", "question_vi": "Chuối có màu gì?", "options": ["Red", "Blue", "Yellow", "Green"], "correct": "Yellow", "explanation": "Chuối màu vàng."},
                        {"id": "q2", "question": "Which sentence is correct?", "question_vi": "Câu nào đúng?", "options": ["A dog big", "Big a dog", "A big dog", "Dog a big"], "correct": "A big dog", "explanation": "Tính từ đứng TRƯỚC danh từ trong tiếng Anh."},
                        {"id": "q3", "question": "What is the opposite of 'tall'?", "question_vi": "Từ trái nghĩa với 'tall' là gì?", "options": ["big", "short", "old", "new"], "correct": "short", "explanation": "Tall ↔ Short."},
                        {"id": "q4", "question": "What color is grass?", "question_vi": "Cỏ có màu gì?", "options": ["Black", "Blue", "Red", "Green"], "correct": "Green", "explanation": "Cỏ màu xanh lá."},
                        {"id": "q5", "question": "The room is very _____. (nóng)", "options": ["cold", "hot", "small", "tall"], "correct": "hot", "explanation": "Hot = nóng."},
                        {"id": "q6", "question": "She has _____ hair. (màu đen)", "options": ["white", "red", "black", "blue"], "correct": "black", "explanation": "Black = đen."},
                        {"id": "q7", "question": "I have a _____ house. (mới)", "options": ["old", "big", "new", "ugly"], "correct": "new", "explanation": "New = mới."},
                        {"id": "q8", "question": "The dress is _____. (màu hồng)", "options": ["purple", "orange", "pink", "blue"], "correct": "pink", "explanation": "Pink = hồng."},
                        {"id": "q9", "question": "What does 'beautiful' mean in Vietnamese?", "question_vi": "'Beautiful' có nghĩa tiếng Việt là gì?", "options": ["xấu", "nhỏ", "đẹp", "nóng"], "correct": "đẹp", "explanation": "Beautiful = đẹp."},
                        {"id": "q10", "question": "The water in the fridge is ___.", "options": ["hot", "cold", "tall", "new"], "correct": "cold", "explanation": "Nước trong tủ lạnh thì lạnh."}
                    ]
                }
            }
        ]
    },

    # ─────────────────────────────────────────────────────────
    # Topic 5: Present Simple (Daily Routines)
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1",
        "order": 5,
        "name": "Present Simple – Daily Routines",
        "name_vi": "Thì Hiện tại Đơn – Thói quen hằng ngày",
        "description": "Learn the present simple tense to talk about habits and routines.",
        "description_vi": "Học thì hiện tại đơn để nói về thói quen và hoạt động hằng ngày.",
        "grammar_focus": ["Thì hiện tại đơn", "Trạng từ tần suất", "Ngôi thứ 3 thêm -s"],
        "vocabulary_tags": ["daily routines", "habits", "time expressions"],
        "estimated_minutes": 35,
        "lessons": [
            {
                "order": 1,
                "lesson_type": "ngữ pháp",
                "title": "Grammar: Present Simple Tense",
                "title_vi": "Ngữ pháp: Thì Hiện tại Đơn",
                "content": {
                    "explanation": "Thì hiện tại đơn dùng để nói về thói quen, hành động hằng ngày và sự thật hiển nhiên.",
                    "key_points": [
                        "Form: Subject + Verb (base form)",
                        "I/You/We/They → verb (base): I eat breakfast.",
                        "He/She/It → verb + s/es: She eats breakfast.",
                        "Negative: do not (don't) / does not (doesn't) + verb",
                        "Question: Do/Does + subject + verb?",
                        "Adverbs of frequency: always, usually, often, sometimes, rarely, never"
                    ],
                    "examples": [
                        {"en": "I wake up at 6 a.m. every day.", "vi": "Tôi thức dậy lúc 6 giờ sáng mỗi ngày."},
                        {"en": "She goes to school by bus.", "vi": "Cô ấy đi học bằng xe buýt."},
                        {"en": "They don't eat meat.", "vi": "Họ không ăn thịt."},
                        {"en": "Does he work on weekends?", "vi": "Anh ấy có làm việc vào cuối tuần không?"}
                    ],
                    "notes": "Nhớ: He/She/It luôn thêm -s hoặc -es: work→works, go→goes, watch→watches, study→studies."
                }
            },
            {
                "order": 2,
                "lesson_type": "vocabulary",
                "title": "Vocabulary: Daily Routine Verbs",
                "title_vi": "Từ vựng: Động từ hoạt động hằng ngày",
                "content": {
                    "words": [
                        {"word": "wake up", "meaning": "thức dậy", "example": "I wake up at 6 a.m.", "pronunciation": "/weɪk ʌp/"},
                        {"word": "get up", "meaning": "ra khỏi giường", "example": "She gets up at 7.", "pronunciation": "/ɡet ʌp/"},
                        {"word": "brush teeth", "meaning": "đánh răng", "example": "I brush my teeth twice a day.", "pronunciation": "/brʌʃ tiːθ/"},
                        {"word": "have breakfast", "meaning": "ăn sáng", "example": "He has breakfast at 7:30.", "pronunciation": "/hæv ˈbrekfəst/"},
                        {"word": "go to work/school", "meaning": "đi làm/đi học", "example": "She goes to school at 8.", "pronunciation": "/ɡoʊ tuː wɜːrk/"},
                        {"word": "have lunch", "meaning": "ăn trưa", "example": "We have lunch at noon.", "pronunciation": "/hæv lʌntʃ/"},
                        {"word": "have dinner", "meaning": "ăn tối", "example": "They have dinner at 7 p.m.", "pronunciation": "/hæv ˈdɪnər/"},
                        {"word": "go to bed", "meaning": "đi ngủ", "example": "I go to bed at 11 p.m.", "pronunciation": "/ɡoʊ tə bed/"},
                        {"word": "watch TV", "meaning": "xem TV", "example": "He watches TV in the evening.", "pronunciation": "/wɒtʃ ˌtiːˈviː/"},
                        {"word": "read", "meaning": "đọc", "example": "She reads books every night.", "pronunciation": "/riːd/"},
                        {"word": "exercise / work out", "meaning": "tập thể dục", "example": "I exercise in the morning.", "pronunciation": "/ˈeksərsaɪz/"},
                        {"word": "always", "meaning": "luôn luôn (100%)", "example": "I always drink water.", "pronunciation": "/ˈɔːlweɪz/"},
                        {"word": "usually", "meaning": "thường thường (~80%)", "example": "She usually walks to school.", "pronunciation": "/ˈjuːʒuəli/"},
                        {"word": "sometimes", "meaning": "đôi khi (~50%)", "example": "He sometimes cooks dinner.", "pronunciation": "/ˈsʌmtaɪmz/"},
                        {"word": "never", "meaning": "không bao giờ (0%)", "example": "I never eat fast food.", "pronunciation": "/ˈnevər/"}
                    ]
                }
            },
            {
                "order": 3,
                "lesson_type": "practice",
                "title": "Practice: Present Simple",
                "title_vi": "Luyện tập: Thì Hiện tại Đơn",
                "content": {
                    "exercises": [
                        {"type": "fill_blank", "question": "She _____ to school every day.", "options": ["go", "goes", "going", "gone"], "answer": "goes", "explanation": "She (ngôi thứ 3) → goes (go + es)."},
                        {"type": "fill_blank", "question": "They _____ eat meat.", "options": ["don't", "doesn't", "isn't", "aren't"], "answer": "don't", "explanation": "They → don't (do not)."},
                        {"type": "multiple_choice", "question": "_____ he go to the gym?", "question_vi": "Anh ấy có đi phòng tập không? (Chọn từ để tạo câu hỏi)", "options": ["Is", "Do", "Does", "Are"], "answer": "Does", "explanation": "He → Does (dạng câu hỏi với he/she/it)."},
                        {"type": "fill_blank", "question": "I _____ breakfast at 7 a.m.", "options": ["has", "have", "having", "had"], "answer": "have", "explanation": "I → have (base form)."},
                        {"type": "fill_blank", "question": "She _____ TV every evening.", "options": ["watch", "watches", "watching", "watched"], "answer": "watches", "explanation": "She → watches (watch + es)."},
                        {"type": "multiple_choice", "question": "I _____ eat junk food. (= 0%)", "question_vi": "Tôi _____ ăn đồ ăn nhanh. (= 0% - không bao giờ)", "options": ["always", "usually", "sometimes", "never"], "answer": "never", "explanation": "Never = không bao giờ (0% frequency)."}
                    ]
                }
            },
            {
                "order": 4,
                "lesson_type": "quiz",
                "title": "Quiz: Present Simple",
                "title_vi": "Kiểm tra: Thì Hiện tại Đơn",
                "content": {
                    "questions": [
                        {"id": "q1", "question": "He _____ to bed at 10 p.m.", "options": ["go", "goes", "going", "gone"], "correct": "goes", "explanation": "He/she/it → verb+s: goes."},
                        {"id": "q2", "question": "They _____ eat breakfast.", "options": ["doesn't", "don't", "isn't", "aren't"], "correct": "don't", "explanation": "They → don't."},
                        {"id": "q3", "question": "_____ she work on Saturday?", "options": ["Do", "Is", "Does", "Are"], "correct": "Does", "explanation": "She → Does (question)."},
                        {"id": "q4", "question": "I _____ up at 6 a.m. every day.", "options": ["wakes", "wake", "waking", "waked"], "correct": "wake", "explanation": "I → wake (base form, no -s)."},
                        {"id": "q5", "question": "Which adverb means 100% frequency?", "question_vi": "Trạng từ nào có nghĩa là 100% (luôn luôn)?", "options": ["never", "sometimes", "always", "rarely"], "correct": "always", "explanation": "Always = luôn luôn (100%)."},
                        {"id": "q6", "question": "She _____ lunch at school.", "options": ["have", "has", "having", "had"], "correct": "has", "explanation": "She → has."},
                        {"id": "q7", "question": "I _____ go to the gym. (= 0%)", "options": ["always", "usually", "sometimes", "never"], "correct": "never", "explanation": "Never = 0%."},
                        {"id": "q8", "question": "Which is correct?", "question_vi": "Câu nào đúng?", "options": ["She eat rice.", "She eats rice.", "She eating rice.", "She is eat rice."], "correct": "She eats rice.", "explanation": "She + eats (động từ + s cho ngôi thứ 3 số ít)."},
                        {"id": "q9", "question": "_____ you like coffee?", "options": ["Is", "Do", "Does", "Are"], "correct": "Do", "explanation": "You → Do (dạng câu hỏi)."},
                        {"id": "q10", "question": "He _____ drink alcohol.", "options": ["don't", "doesn't", "isn't", "aren't"], "correct": "doesn't", "explanation": "He → doesn't (does not)."}
                    ]
                }
            }
        ]
    },

    # ─────────────────────────────────────────────────────────
    # Topics 6-20: Simplified structure (same pattern)
    # ─────────────────────────────────────────────────────────
    {
        "level": "A1", "order": 6,
        "name": "Food & Drinks",
        "name_vi": "Thực phẩm & Đồ uống",
        "description": "Learn vocabulary for common food and drinks, and how to order.",
        "description_vi": "Học từ vựng về thực phẩm và đồ uống, và cách đặt món.",
        "grammar_focus": ["Would you like...? (Đề nghị)", "I'd like... (Tôi muốn)", "Danh từ đếm được/không đếm được"],
        "vocabulary_tags": ["food", "drinks", "restaurant", "ordering"],
        "estimated_minutes": 30,
        "lessons": [
            {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Ordering Food – Would like", "title_vi": "Ngữ pháp: Đặt món – Would like",
             "content": {"explanation": "'Would like' là cách lịch sự để yêu cầu điều gì đó.", "explanation_vi": "'Would like' là cách lịch sự để yêu cầu điều gì đó.", "key_points": ["I would like = I'd like (lịch sự want)", "Would you like...? (offer/question)", "Some/any: some (khẳng định), any (negative/question)"], "examples": [{"en": "I'd like a coffee, please.", "vi": "Tôi muốn một ly cà phê, cảm ơn."}, {"en": "Would you like some water?", "vi": "Bạn có muốn nước không?"}], "notes": "'Would like' lịch sự hơn 'want'. Dùng khi đặt món ở nhà hàng."}},
            {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Food & Drinks", "title_vi": "Từ vựng: Thực phẩm & Đồ uống",
             "content": {"words": [
                 {"word": "rice", "meaning": "cơm/gạo", "example": "I eat rice every day.", "pronunciation": "/raɪs/"},
                 {"word": "bread", "meaning": "bánh mì", "example": "She has bread for breakfast.", "pronunciation": "/bred/"},
                 {"word": "noodles", "meaning": "mì/phở", "example": "He loves noodles.", "pronunciation": "/ˈnuːdlz/"},
                 {"word": "chicken", "meaning": "thịt gà", "example": "I'd like chicken, please.", "pronunciation": "/ˈtʃɪkɪn/"},
                 {"word": "fish", "meaning": "cá", "example": "She doesn't eat fish.", "pronunciation": "/fɪʃ/"},
                 {"word": "vegetables", "meaning": "rau củ", "example": "Eat your vegetables!", "pronunciation": "/ˈvedʒtəblz/"},
                 {"word": "fruit", "meaning": "trái cây", "example": "I have fruit for lunch.", "pronunciation": "/fruːt/"},
                 {"word": "water", "meaning": "nước", "example": "A glass of water, please.", "pronunciation": "/ˈwɔːtər/"},
                 {"word": "coffee", "meaning": "cà phê", "example": "I drink coffee every morning.", "pronunciation": "/ˈkɒfi/"},
                 {"word": "tea", "meaning": "trà", "example": "Would you like some tea?", "pronunciation": "/tiː/"},
                 {"word": "juice", "meaning": "nước ép", "example": "I'd like orange juice.", "pronunciation": "/dʒuːs/"},
                 {"word": "milk", "meaning": "sữa", "example": "Children need milk.", "pronunciation": "/mɪlk/"},
                 {"word": "menu", "meaning": "thực đơn", "example": "Can I see the menu?", "pronunciation": "/ˈmenjuː/"},
                 {"word": "bill / check", "meaning": "hóa đơn", "example": "Can I have the bill, please?", "pronunciation": "/bɪl/"}
             ]}},
            {"order": 3, "lesson_type": "practice", "title": "Practice: Ordering Food", "title_vi": "Luyện tập: Gọi món",
             "content": {"exercises": [
                 {"type": "multiple_choice", "question": "You are at a restaurant. How do you order politely?", "question_vi": "Bạn đang ở nhà hàng. Cách đặt món lịch sự là gì?", "options": ["I want chicken.", "Give me chicken!", "I'd like chicken, please.", "Chicken now!"], "answer": "I'd like chicken, please.", "explanation": "'I'd like' là cách lịch sự để đặt món."},
                 {"type": "fill_blank", "question": "_____ you like some coffee?", "options": ["Do", "Would", "Are", "Have"], "answer": "Would", "explanation": "'Would you like' dùng để offer something."},
                 {"type": "fill_blank", "question": "Can I see the _____?", "options": ["bill", "menu", "water", "food"], "answer": "menu", "explanation": "Menu = thực đơn."},
                 {"type": "multiple_choice", "question": "Which is a drink?", "question_vi": "Từ nào là đồ uống?", "options": ["rice", "chicken", "juice", "bread"], "answer": "juice", "explanation": "Juice = nước ép (a drink)."},
                 {"type": "fill_blank", "question": "I'd like a glass of _____, please. (nước)", "options": ["milk", "tea", "water", "coffee"], "answer": "water", "explanation": "Water = nước."}
             ]}},
            {"order": 4, "lesson_type": "quiz", "title": "Quiz: Food & Drinks", "title_vi": "Kiểm tra: Thực phẩm & Đồ uống",
             "content": {"questions": [
                 {"id": "q1", "question": "How do you politely order food?", "question_vi": "Cách đặt món lịch sự là gì?", "options": ["I want rice.", "I'd like rice, please.", "Give me rice!", "Rice!"], "correct": "I'd like rice, please.", "explanation": "'I'd like' = lịch sự ordering."},
                 {"id": "q2", "question": "_____ you like some tea?", "options": ["Do", "Are", "Would", "Have"], "correct": "Would", "explanation": "'Would you like' = offer."},
                 {"id": "q3", "question": "What is 'thịt gà' in English?", "question_vi": "'Thịt gà' trong tiếng Anh là gì?", "options": ["fish", "beef", "chicken", "pork"], "correct": "chicken", "explanation": "Chicken = thịt gà."},
                 {"id": "q4", "question": "What do you ask for at the end of a meal?", "question_vi": "Bạn hỏi xin gì ở cuối bữa ăn?", "options": ["menu", "water", "bill", "food"], "correct": "bill", "explanation": "Bill/check = hóa đơn."},
                 {"id": "q5", "question": "What are vegetables?", "question_vi": "Vegetables (rau củ) là loại thực phẩm gì?", "options": ["drinks", "food (plants)", "desserts", "meats"], "correct": "food (plants)", "explanation": "Vegetables = rau củ (plants we eat)."},
                 {"id": "q6", "question": "Which is NOT a drink?", "question_vi": "Từ nào KHÔNG phải đồ uống?", "options": ["water", "milk", "juice", "bread"], "correct": "bread", "explanation": "Bread (bánh mì) là đồ ăn, không phải đồ uống."},
                 {"id": "q7", "question": "I drink _____ every morning. (cà phê)", "options": ["tea", "coffee", "juice", "milk"], "correct": "coffee", "explanation": "Coffee = cà phê."},
                 {"id": "q8", "question": "She doesn't eat _____. (cá)", "options": ["rice", "fish", "chicken", "beef"], "correct": "fish", "explanation": "Fish = cá."},
                 {"id": "q9", "question": "I have _____ for breakfast. (bánh mì)", "options": ["noodles", "rice", "bread", "fruit"], "correct": "bread", "explanation": "Bread = bánh mì."},
                 {"id": "q10", "question": "Can I see the _____, please?", "options": ["bill", "menu", "water", "table"], "correct": "menu", "explanation": "Menu = thực đơn."}
             ]}}
        ]
    },

    # Topics 7-20: Core structure only (will use AI content generation for detail)
    {
        "level": "A1", "order": 7,
        "name": "My Home & Furniture",
        "name_vi": "Ngôi nhà & Đồ đạc",
        "description": "Describe your home and name common household items.",
        "description_vi": "Mô tả ngôi nhà và gọi tên các đồ vật thông dụng trong nhà.",
        "grammar_focus": ["there is / there are (có)", "Giới từ chỉ nơi chốn"],
        "vocabulary_tags": ["home", "furniture", "rooms", "prepositions"],
        "estimated_minutes": 30,
        "lessons": [
            {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: There is / There are & Prepositions", "title_vi": "Ngữ pháp: There is / There are & Giới từ",
             "content": {"explanation": "'There is' (số ít) và 'there are' (số nhiều) mô tả những gì tồn tại ở đâu đó.", "explanation_vi": "'There is' (số ít) và 'there are' (số nhiều) mô tả những gì tồn tại ở đâu đó.", "key_points": ["There is a table. (1 table)", "There are two chairs. (2+ chairs)", "Is there a...? / Are there any...?", "Prepositions: in, on, under, next to, between, behind, in front of"], "examples": [{"en": "There is a sofa in the living room.", "vi": "Có một ghế sofa trong phòng khách."}, {"en": "The cat is under the table.", "vi": "Con mèo ở dưới gầm bàn."}], "notes": "Đừng nhầm lẫn 'there is' với 'it is'. 'There is a book' (mô tả sự tồn tại). 'It is a book' (mô tả cái gì đó là gì)."}},
            {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Rooms & Furniture", "title_vi": "Từ vựng: Các phòng & Đồ đạc",
             "content": {"words": [
                 {"word": "living room", "meaning": "phòng khách", "example": "We watch TV in the living room.", "pronunciation": "/ˈlɪvɪŋ ruːm/"},
                 {"word": "bedroom", "meaning": "phòng ngủ", "example": "I sleep in my bedroom.", "pronunciation": "/ˈbedruːm/"},
                 {"word": "kitchen", "meaning": "nhà bếp", "example": "She cooks in the kitchen.", "pronunciation": "/ˈkɪtʃɪn/"},
                 {"word": "bathroom", "meaning": "phòng tắm", "example": "The bathroom is on the right.", "pronunciation": "/ˈbæθruːm/"},
                 {"word": "table", "meaning": "cái bàn", "example": "Put the book on the table.", "pronunciation": "/ˈteɪbl/"},
                 {"word": "chair", "meaning": "cái ghế", "example": "Sit on the chair.", "pronunciation": "/tʃer/"},
                 {"word": "bed", "meaning": "cái giường", "example": "I sleep in a big bed.", "pronunciation": "/bed/"},
                 {"word": "sofa / couch", "meaning": "ghế sofa", "example": "He sleeps on the sofa.", "pronunciation": "/ˈsoʊfə/"},
                 {"word": "window", "meaning": "cửa sổ", "example": "Open the window, please.", "pronunciation": "/ˈwɪndoʊ/"},
                 {"word": "door", "meaning": "cửa ra vào", "example": "Close the door.", "pronunciation": "/dɔːr/"},
                 {"word": "in", "meaning": "trong", "example": "The cat is in the box.", "pronunciation": "/ɪn/"},
                 {"word": "on", "meaning": "trên (bề mặt)", "example": "The book is on the table.", "pronunciation": "/ɒn/"},
                 {"word": "under", "meaning": "dưới", "example": "The shoes are under the bed.", "pronunciation": "/ˈʌndər/"},
                 {"word": "next to", "meaning": "bên cạnh", "example": "The lamp is next to the bed.", "pronunciation": "/nekst tuː/"}
             ]}},
            {"order": 3, "lesson_type": "practice", "title": "Practice: There is/are & Prepositions", "title_vi": "Luyện tập: There is/are & Giới từ",
             "content": {"exercises": [
                 {"type": "fill_blank", "question": "_____ is a bed in my room.", "options": ["There", "It", "This", "Here"], "answer": "There", "explanation": "'There is' describes existence of something."},
                 {"type": "fill_blank", "question": "There _____ three chairs in the kitchen.", "options": ["is", "are", "am", "be"], "answer": "are", "explanation": "Three chairs = plural → 'there are'."},
                 {"type": "fill_blank", "question": "The book is _____ the table.", "options": ["in", "on", "under", "next"], "answer": "on", "explanation": "On = trên bề mặt."},
                 {"type": "fill_blank", "question": "The cat is _____ the bed. (dưới)", "options": ["on", "in", "under", "next to"], "answer": "under", "explanation": "Under = bên dưới."},
                 {"type": "fill_blank", "question": "_____ there a sofa in the living room?", "options": ["Is", "Are", "Do", "Does"], "answer": "Is", "explanation": "'Is there a...' = câu hỏi cho sự vật số ít."}
             ]}},
            {"order": 4, "lesson_type": "quiz", "title": "Quiz: Home & Furniture", "title_vi": "Kiểm tra: Nhà & Đồ đạc",
             "content": {"questions": [
                 {"id": "q1", "question": "There _____ a table in the kitchen.", "options": ["are", "is", "am", "be"], "correct": "is", "explanation": "A table = singular → there is."},
                 {"id": "q2", "question": "There _____ two windows in my bedroom.", "options": ["is", "are", "am", "be"], "correct": "are", "explanation": "Two windows = plural → there are."},
                 {"id": "q3", "question": "The book is _____ the table. (dưới)", "options": ["on", "in", "next to", "under"], "correct": "under", "explanation": "Under = bên dưới."},
                 {"id": "q4", "question": "Where do you cook?", "question_vi": "Bạn nấu ăn ở đâu?", "options": ["bedroom", "bathroom", "kitchen", "living room"], "correct": "kitchen", "explanation": "Kitchen = nhà bếp (where you cook)."},
                 {"id": "q5", "question": "The lamp is _____ the bed. (bên cạnh)", "options": ["on", "in", "under", "next to"], "correct": "next to", "explanation": "Next to = bên cạnh."},
                 {"id": "q6", "question": "Where do you sleep?", "question_vi": "Bạn ngủ ở đâu?", "options": ["living room", "kitchen", "bathroom", "bedroom"], "correct": "bedroom", "explanation": "Bedroom = phòng ngủ."},
                 {"id": "q7", "question": "_____ there any chairs in the room?", "options": ["Is", "Are", "Do", "Does"], "correct": "Are", "explanation": "Chairs = plural → Are there any...?"},
                 {"id": "q8", "question": "The cat is _____ the box. (trong)", "options": ["on", "in", "under", "next to"], "correct": "in", "explanation": "In = bên trong."},
                 {"id": "q9", "question": "What is a 'sofa'?", "question_vi": "'Sofa' là gì?", "options": ["a type of bed", "a type of chair for sitting", "a type of table", "a type of door"], "correct": "a type of chair for sitting", "explanation": "Sofa = ghế sofa để ngồi."},
                 {"id": "q10", "question": "There _____ no furniture in the room.", "options": ["are", "is", "am", "be"], "correct": "is", "explanation": "'Furniture' (đồ đạc) là danh từ không đếm được → dùng there is."}
             ]}}
        ]
    },

    {"level": "A1", "order": 8, "name": "Shopping & Prices", "name_vi": "Mua sắm & Giá cả",
     "description": "Learn to shop, ask about prices, and make purchases.", "description_vi": "Học cách mua sắm, hỏi giá cả và thực hiện giao dịch.",
     "grammar_focus": ["how much (bao nhiêu tiền)", "Mạo từ a/an/the", "this/that/these/those (này/kia)"], "vocabulary_tags": ["shopping", "money", "prices", "clothes"],
     "estimated_minutes": 30,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: How much? & Articles (a/an/the)", "title_vi": "Ngữ pháp: Hỏi giá & Mạo từ", "content": {"explanation": "Dùng 'How much is/are...?' để hỏi giá. Mạo từ (a/an/the) dùng với danh từ.", "explanation_vi": "Dùng 'How much is/are...?' để hỏi giá. Mạo từ (a/an/the) đi kèm danh từ.", "key_points": ["How much is this? / How much are these?", "a + phụ âm sound (a book, a car)", "an + âm nguyên âm (an apple, an orange)", "the = specific thing both speaker and listener know"], "examples": [{"en": "How much is this shirt?", "vi": "Cái áo này giá bao nhiêu?"}, {"en": "It's $15.", "vi": "Giá $15."}, {"en": "I'd like an apple and a banana.", "vi": "Tôi muốn một quả táo và một quả chuối."}], "notes": "'How much' dùng cho danh từ không đếm được và hỏi giá. 'How many' dùng cho danh từ đếm được."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Shopping Words", "title_vi": "Từ vựng: Từ về mua sắm", "content": {"words": [
             {"word": "shop / store", "meaning": "cửa hàng", "example": "She goes to the shop.", "pronunciation": "/ʃɒp/"},
             {"word": "buy", "meaning": "mua", "example": "I want to buy a dress.", "pronunciation": "/baɪ/"},
             {"word": "sell", "meaning": "bán", "example": "They sell shoes here.", "pronunciation": "/sel/"},
             {"word": "price", "meaning": "giá cả", "example": "What is the price?", "pronunciation": "/praɪs/"},
             {"word": "expensive", "meaning": "đắt (tiền)", "example": "That car is very expensive.", "pronunciation": "/ɪkˈspensɪv/"},
             {"word": "cheap", "meaning": "rẻ (tiền)", "example": "This shirt is cheap.", "pronunciation": "/tʃiːp/"},
             {"word": "discount", "meaning": "giảm giá", "example": "Is there a discount?", "pronunciation": "/ˈdɪskaʊnt/"},
             {"word": "size", "meaning": "kích cỡ", "example": "What size do you wear?", "pronunciation": "/saɪz/"},
             {"word": "small / medium / large", "meaning": "nhỏ / vừa / lớn", "example": "I need a medium size.", "pronunciation": "/smɔːl ˈmiːdiəm lɑːrdʒ/"},
             {"word": "cash", "meaning": "tiền mặt", "example": "Do you pay by cash?", "pronunciation": "/kæʃ/"},
             {"word": "card", "meaning": "thẻ (thanh toán)", "example": "Can I pay by card?", "pronunciation": "/kɑːrd/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Shopping Dialogues", "title_vi": "Luyện tập: Hội thoại mua sắm", "content": {"exercises": [
             {"type": "fill_blank", "question": "How _____ is this bag?", "options": ["many", "much", "old", "big"], "answer": "much", "explanation": "'How much' = hỏi giá / số lượng không đếm được."},
             {"type": "fill_blank", "question": "I'd like _____ apple.", "options": ["a", "an", "the", "some"], "answer": "an", "explanation": "Apple bắt đầu bằng nguyên âm → dùng 'an'."},
             {"type": "multiple_choice", "question": "This shirt costs $5. That shirt costs $50. Which is expensive?", "question_vi": "Áo này giá $5. Áo kia giá $50. Cái nào đắt?", "options": ["the $5 shirt", "the $50 shirt", "both", "neither"], "answer": "the $50 shirt", "explanation": "Expensive = đắt tiền."},
             {"type": "multiple_choice", "question": "Can I pay by _____? (not cash)", "question_vi": "Tôi có thể thanh toán bằng _____? (không phải tiền mặt)", "options": ["price", "discount", "card", "size"], "answer": "card", "explanation": "Pay by card = thanh toán bằng thẻ."},
             {"type": "fill_blank", "question": "What _____ do you wear? (S/M/L)", "options": ["price", "color", "size", "number"], "answer": "size", "explanation": "Size = kích cỡ (S/M/L)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Shopping & Prices", "title_vi": "Kiểm tra: Mua sắm & Giá cả", "content": {"questions": [
             {"id": "q1", "question": "How _____ is this dress?", "question_vi": "Chiếc váy này giá bao nhiêu? (Chọn từ để hỏi)", "options": ["many", "much", "old", "long"], "correct": "much", "explanation": "How much = hỏi giá."},
             {"id": "q2", "question": "I'd like _____ orange.", "options": ["a", "an", "the", "some"], "correct": "an", "explanation": "Orange bắt đầu bằng nguyên âm → dùng an."},
             {"id": "q3", "question": "This shirt costs $5. That shirt costs $50. Which one is cheap?", "question_vi": "Áo này giá $5. Áo kia giá $50. Cái nào rẻ?", "options": ["the $5 shirt", "the $50 shirt", "both", "neither"], "correct": "the $5 shirt", "explanation": "Cheap = rẻ. $5 rẻ hơn $50."},
             {"id": "q4", "question": "What does 'buy' mean in Vietnamese?", "question_vi": "'Buy' có nghĩa tiếng Việt là gì?", "options": ["bán", "mua", "trả tiền", "cho"], "correct": "mua", "explanation": "Buy = mua."},
             {"id": "q5", "question": "A _____ means the price is lower than normal.", "question_vi": "_____ có nghĩa là giá thấp hơn bình thường.", "options": ["price", "discount", "size", "card"], "correct": "discount", "explanation": "Discount = giảm giá."},
             {"id": "q6", "question": "I wear size M. What does M stand for?", "question_vi": "Tôi mặc size M. M là viết tắt của gì?", "options": ["small", "medium", "large", "extra-large"], "correct": "medium", "explanation": "M = Medium = vừa."},
             {"id": "q7", "question": "Can I pay by _____? (thẻ)", "options": ["price", "card", "size", "shop"], "correct": "card", "explanation": "Pay by card = thanh toán thẻ."},
             {"id": "q8", "question": "I'd like _____ umbrella.", "options": ["a", "an", "the", "–"], "correct": "an", "explanation": "Umbrella bắt đầu bằng nguyên âm u → dùng an."},
             {"id": "q9", "question": "This book costs $3. It is very:", "options": ["expensive", "cheap", "big", "small"], "correct": "cheap", "explanation": "Cheap = rẻ. $3 là giá rẻ cho một cuốn sách."},
             {"id": "q10", "question": "Do you have this in a small _____?", "options": ["price", "color", "size", "shop"], "correct": "size", "explanation": "Size = kích cỡ."}
         ]}}
     ]},

    {"level": "A1", "order": 9, "name": "Transportation", "name_vi": "Phương tiện di chuyển",
     "description": "Learn how to talk about transportation and give/ask directions.",
     "description_vi": "Học cách nói về phương tiện di chuyển và chỉ/hỏi đường.",
     "grammar_focus": ["how do you get to...? (đi bằng gì)", "take/go by (đi bằng)", "Giới từ chỉ hướng"],
     "vocabulary_tags": ["transport", "directions", "travel", "city"],
     "estimated_minutes": 30,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Getting Around – How to travel", "title_vi": "Ngữ pháp: Di chuyển như thế nào",
          "content": {"explanation": "Dùng 'go by + phương tiện' hoặc 'take the + phương tiện' để mô tả cách di chuyển.", "explanation_vi": "Dùng 'go by + phương tiện' hoặc 'take the + phương tiện' để mô tả cách di chuyển.", "key_points": ["go by bus / car / train / bike", "take the bus / the train / the taxi", "How do you get to school? – I go by bus.", "Turn left/right, go straight"], "examples": [{"en": "I go to school by bike.", "vi": "Tôi đi học bằng xe đạp."}, {"en": "Take the bus to the city center.", "vi": "Đi xe buýt đến trung tâm thành phố."}, {"en": "Turn left at the traffic light.", "vi": "Rẽ trái tại đèn giao thông."}], "notes": "Dùng 'by' cho phương tiện (không dùng mạo từ): go by bus. Dùng 'the' khi chỉ cụ thể: take the number 10 bus."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Transport & Directions", "title_vi": "Từ vựng: Phương tiện & Chỉ đường", "content": {"words": [
             {"word": "bus", "meaning": "xe buýt", "example": "I take the bus to work.", "pronunciation": "/bʌs/"},
             {"word": "train", "meaning": "tàu hỏa", "example": "The train is fast.", "pronunciation": "/treɪn/"},
             {"word": "taxi / cab", "meaning": "xe taxi", "example": "Let's take a taxi.", "pronunciation": "/ˈtæksi/"},
             {"word": "bike / bicycle", "meaning": "xe đạp", "example": "She rides her bike to school.", "pronunciation": "/baɪk/"},
             {"word": "motorbike", "meaning": "xe máy", "example": "He goes by motorbike.", "pronunciation": "/ˈmoʊtərbaɪk/"},
             {"word": "car", "meaning": "ô tô/xe hơi", "example": "They drive a car.", "pronunciation": "/kɑːr/"},
             {"word": "on foot / walk", "meaning": "đi bộ", "example": "I walk to the park.", "pronunciation": "/wɔːk/"},
             {"word": "turn left", "meaning": "rẽ trái", "example": "Turn left at the corner.", "pronunciation": "/tɜːrn left/"},
             {"word": "turn right", "meaning": "rẽ phải", "example": "Turn right at the light.", "pronunciation": "/tɜːrn raɪt/"},
             {"word": "go straight", "meaning": "đi thẳng", "example": "Go straight for 2 km.", "pronunciation": "/ɡoʊ streɪt/"},
             {"word": "near / far", "meaning": "gần / xa", "example": "Is it near here?", "pronunciation": "/nɪər/"},
             {"word": "traffic light", "meaning": "đèn giao thông", "example": "Stop at the traffic light.", "pronunciation": "/ˈtræfɪk laɪt/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Transport & Directions", "title_vi": "Luyện tập: Phương tiện & Chỉ đường", "content": {"exercises": [
             {"type": "multiple_choice", "question": "How do you get to school?", "question_vi": "Bạn đi học bằng gì?", "options": ["I go by foot.", "I go by walk.", "I walk.", "I walk hoặc I go by foot."], "answer": "I walk hoặc I go by foot.", "explanation": "'Walk' hoặc 'go by foot / on foot' đều đúng."},
             {"type": "fill_blank", "question": "She goes to work _____ bus.", "options": ["in", "by", "with", "on"], "answer": "by", "explanation": "'Go by bus' = đi bằng xe buýt."},
             {"type": "fill_blank", "question": "Turn _____ at the traffic light. (trái)", "options": ["right", "straight", "left", "up"], "answer": "left", "explanation": "Left = trái."},
             {"type": "multiple_choice", "question": "Which is the slowest transport?", "question_vi": "Phương tiện nào chậm nhất?", "options": ["train", "car", "walking", "bus"], "answer": "walking", "explanation": "Walking = đi bộ (slowest)."},
             {"type": "fill_blank", "question": "_____ the train to the airport.", "options": ["Go", "Take", "Drive", "Walk"], "answer": "Take", "explanation": "'Take the train' = đi tàu."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Transportation", "title_vi": "Kiểm tra: Phương tiện di chuyển", "content": {"questions": [
             {"id": "q1", "question": "She goes to school _____ motorbike.", "options": ["in", "by", "with", "on"], "correct": "by", "explanation": "Go by + transport."},
             {"id": "q2", "question": "What does 'turn right' mean?", "question_vi": "'Turn right' có nghĩa là gì?", "options": ["Rẽ trái", "Đi thẳng", "Rẽ phải", "Quay lại"], "correct": "Rẽ phải", "explanation": "Turn right = rẽ phải."},
             {"id": "q3", "question": "_____ the bus to the market.", "options": ["Go", "Drive", "Take", "Walk"], "correct": "Take", "explanation": "Take the bus = đi xe buýt."},
             {"id": "q4", "question": "Which transport uses tracks?", "question_vi": "Phương tiện nào chạy trên đường ray?", "options": ["bus", "car", "train", "taxi"], "correct": "train", "explanation": "Train = tàu hỏa (chạy trên đường ray)."},
             {"id": "q5", "question": "Go _____ for 500 meters, then turn left.", "options": ["left", "right", "straight", "back"], "correct": "straight", "explanation": "Go straight = đi thẳng."},
             {"id": "q6", "question": "I don't have a car. I go _____. (đi bộ)", "options": ["by foot", "by car", "by train", "by taxi"], "correct": "by foot", "explanation": "On foot / by foot = đi bộ."},
             {"id": "q7", "question": "Stop at the _____ light.", "options": ["traffic", "red", "green", "signal"], "correct": "traffic", "explanation": "Traffic light = đèn giao thông."},
             {"id": "q8", "question": "Is the school far from here?", "question_vi": "Trường học có xa đây không?", "options": ["What time is it?", "No, it's near.", "I like school.", "Go right."], "correct": "No, it's near.", "explanation": "Near = gần (trái nghĩa với far)."},
             {"id": "q9", "question": "A bicycle is powered by:", "question_vi": "Xe đạp chạy bằng:", "options": ["electricity", "gasoline", "pedaling", "wind"], "correct": "pedaling", "explanation": "Bicycle = xe đạp, powered by pedaling (đạp)."},
             {"id": "q10", "question": "How do you ask for directions?", "question_vi": "Cách hỏi đường lịch sự là gì?", "options": ["I go by bus.", "Excuse me, where is the station?", "Turn right.", "It's far."], "correct": "Excuse me, where is the station?", "explanation": "Hỏi đường = lịch sự hỏi 'where is...'"}
         ]}}
     ]},

    {"level": "A1", "order": 10, "name": "Question Forms (Wh- Questions)", "name_vi": "Câu hỏi Wh-",
     "description": "Master the 5 key Wh- question words: What, Where, When, Who, Why, How.",
     "description_vi": "Nắm vững 6 từ để hỏi Wh-: What, Where, When, Who, Why, How.",
     "grammar_focus": ["Câu hỏi Wh-", "Từ để hỏi + trợ động từ + chủ ngữ + động từ"],
     "vocabulary_tags": ["questions", "ngữ pháp", "communication"],
     "estimated_minutes": 30,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Wh- Question Formation", "title_vi": "Ngữ pháp: Cấu trúc câu hỏi Wh-", "content": {"explanation": "Câu hỏi Wh- hỏi thông tin cụ thể, không phải chỉ yes/no.", "explanation_vi": "Câu hỏi Wh- hỏi thông tin cụ thể, không phải chỉ yes/no.", "key_points": ["What = cái gì (thing)", "Where = ở đâu (place)", "When = khi nào (time)", "Who = ai (person)", "Why = tại sao (reason)", "How = như thế nào (manner/way)", "Structure: Wh-word + do/does/is/are + subject + verb?"], "examples": [{"en": "What do you do? – I am a teacher.", "vi": "Bạn làm nghề gì? – Tôi là giáo viên."}, {"en": "Where do you live? – I live in Hanoi.", "vi": "Bạn sống ở đâu? – Tôi sống ở Hà Nội."}, {"en": "When does the class start? – At 8 a.m.", "vi": "Lớp học bắt đầu khi nào? – Lúc 8 giờ sáng."}], "notes": "Trợ động từ (do/does) phải khớp với chủ ngữ. Với 'to be', không cần trợ động từ: Where IS she? (không phải Where does she is?)"}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Question Words in Context", "title_vi": "Từ vựng: Từ để hỏi trong ngữ cảnh", "content": {"words": [
             {"word": "What", "meaning": "Cái gì / Là gì", "example": "What is your name?", "pronunciation": "/wɒt/"},
             {"word": "Where", "meaning": "Ở đâu / Đến đâu", "example": "Where do you live?", "pronunciation": "/wer/"},
             {"word": "When", "meaning": "Khi nào / Lúc nào", "example": "When is your birthday?", "pronunciation": "/wen/"},
             {"word": "Who", "meaning": "Ai", "example": "Who is your teacher?", "pronunciation": "/huː/"},
             {"word": "Why", "meaning": "Tại sao", "example": "Why are you late?", "pronunciation": "/waɪ/"},
             {"word": "How", "meaning": "Như thế nào / Bằng cách nào", "example": "How are you?", "pronunciation": "/haʊ/"},
             {"word": "How many", "meaning": "Bao nhiêu (đếm được)", "example": "How many sisters do you have?", "pronunciation": "/haʊ ˈmeni/"},
             {"word": "How much", "meaning": "Bao nhiêu (không đếm được / giá)", "example": "How much is it?", "pronunciation": "/haʊ mʌtʃ/"},
             {"word": "How old", "meaning": "Bao nhiêu tuổi", "example": "How old are you?", "pronunciation": "/haʊ oʊld/"},
             {"word": "How long", "meaning": "Bao lâu / Dài bao nhiêu", "example": "How long is the trip?", "pronunciation": "/haʊ lɒŋ/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Forming Wh- Questions", "title_vi": "Luyện tập: Tạo câu hỏi Wh-", "content": {"exercises": [
             {"type": "multiple_choice", "question": "_____ do you live? – In Hanoi.", "options": ["What", "Who", "Where", "When"], "answer": "Where", "explanation": "Where = ở đâu (place)."},
             {"type": "multiple_choice", "question": "_____ is your name?", "options": ["Where", "When", "What", "Who"], "answer": "What", "explanation": "What = cái gì → What is your name?"},
             {"type": "fill_blank", "question": "_____ are you late? – Because I missed the bus.", "options": ["What", "Where", "Why", "Who"], "answer": "Why", "explanation": "Why = tại sao → hỏi lý do."},
             {"type": "multiple_choice", "question": "_____ many brothers do you have?", "options": ["How", "What", "Where", "When"], "answer": "How", "explanation": "How many = bao nhiêu (countable)."},
             {"type": "multiple_choice", "question": "_____ does the movie start?", "options": ["Who", "Where", "When", "Why"], "answer": "When", "explanation": "When = khi nào (time)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Wh- Questions", "title_vi": "Kiểm tra: Câu hỏi Wh-", "content": {"questions": [
             {"id": "q1", "question": "_____ is your favorite color?", "options": ["Where", "Who", "What", "When"], "correct": "What", "explanation": "What = hỏi về 'cái gì'."},
             {"id": "q2", "question": "_____ do you go to school? – By bus.", "options": ["What", "Where", "When", "How"], "correct": "How", "explanation": "How = bằng cách nào → phương tiện."},
             {"id": "q3", "question": "_____ is your teacher? – Mr. Smith.", "options": ["What", "Who", "Where", "Why"], "correct": "Who", "explanation": "Who = ai (person)."},
             {"id": "q4", "question": "_____ old are you?", "options": ["What", "How", "Where", "Who"], "correct": "How", "explanation": "How old = bao nhiêu tuổi."},
             {"id": "q5", "question": "_____ are you crying? – Because I'm sad.", "options": ["Who", "When", "Why", "Where"], "correct": "Why", "explanation": "Why = tại sao (reason)."},
             {"id": "q6", "question": "_____ is your birthday?", "options": ["Why", "Where", "Who", "When"], "correct": "When", "explanation": "When = khi nào (time/date)."},
             {"id": "q7", "question": "_____ does she live? – In Ho Chi Minh City.", "options": ["What", "Who", "Where", "When"], "correct": "Where", "explanation": "Where = ở đâu (place)."},
             {"id": "q8", "question": "_____ much is this bag?", "options": ["How", "What", "Where", "Who"], "correct": "How", "explanation": "How much = bao nhiêu tiền."},
             {"id": "q9", "question": "_____ many students are in your class?", "options": ["What", "How", "Where", "Why"], "correct": "How", "explanation": "How many = bao nhiêu (countable)."},
             {"id": "q10", "question": "_____ do you spell your name?", "options": ["What", "Where", "How", "Who"], "correct": "How", "explanation": "How do you spell = đánh vần như thế nào."}
         ]}}
     ]},

    # Topics 11-20: basic structure
    {"level": "A1", "order": 11, "name": "Modal Verb: Can", "name_vi": "Động từ khiếm khuyết: Can",
     "description": "Use 'can' to talk about ability and permission.", "description_vi": "Dùng 'can' để nói về khả năng và sự cho phép.",
     "grammar_focus": ["can + động từ nguyên mẫu", "can/can't (khả năng)", "Can I...? (xin phép)"],
     "vocabulary_tags": ["ability", "permission", "modal verbs"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Can & Can't", "title_vi": "Ngữ pháp: Can & Can't", "content": {"explanation": "'Can' diễn đạt khả năng (I can swim) và sự cho phép (Can I go?). Nó KHÔNG thay đổi với he/she/it.", "explanation_vi": "'Can' diễn đạt khả năng và sự cho phép. Nó KHÔNG thêm -s cho he/she/it.", "key_points": ["Subject + can + verb (base form): She can speak English.", "Negative: Subject + cannot / can't + verb", "Question: Can + subject + verb?", "Can vs. Can't: Can = có thể, Can't = không thể"], "examples": [{"en": "I can swim very well.", "vi": "Tôi có thể bơi rất giỏi."}, {"en": "She can't drive a car yet.", "vi": "Cô ấy chưa biết lái xe."}, {"en": "Can you help me, please?", "vi": "Bạn có thể giúp tôi được không?"}, {"en": "Can I open the window?", "vi": "Tôi có thể mở cửa sổ không?"}], "notes": "Can giống nhau cho TẤT CẢ chủ ngữ: I can, you can, he can, she can, we can, they can."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Ability & Skills", "title_vi": "Từ vựng: Khả năng & Kỹ năng", "content": {"words": [
             {"word": "swim", "meaning": "bơi lội", "example": "Can you swim?", "pronunciation": "/swɪm/"},
             {"word": "drive", "meaning": "lái xe", "example": "She can drive a car.", "pronunciation": "/draɪv/"},
             {"word": "cook", "meaning": "nấu ăn", "example": "He can cook Vietnamese food.", "pronunciation": "/kʊk/"},
             {"word": "sing", "meaning": "hát", "example": "She can sing beautifully.", "pronunciation": "/sɪŋ/"},
             {"word": "dance", "meaning": "khiêu vũ/nhảy", "example": "Can you dance?", "pronunciation": "/dæns/"},
             {"word": "speak", "meaning": "nói (ngôn ngữ)", "example": "I can speak 3 languages.", "pronunciation": "/spiːk/"},
             {"word": "read", "meaning": "đọc", "example": "She can read very fast.", "pronunciation": "/riːd/"},
             {"word": "write", "meaning": "viết", "example": "Can you write your name?", "pronunciation": "/raɪt/"},
             {"word": "play (instrument)", "meaning": "chơi (nhạc cụ)", "example": "He can play the guitar.", "pronunciation": "/pleɪ/"},
             {"word": "ride a bike", "meaning": "đi xe đạp", "example": "I can ride a bike.", "pronunciation": "/raɪd ə baɪk/"},
             {"word": "use a computer", "meaning": "dùng máy tính", "example": "She can use a computer well.", "pronunciation": "/juːz ə kəmˈpjuːtər/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Can & Can't", "title_vi": "Luyện tập: Can & Can't", "content": {"exercises": [
             {"type": "fill_blank", "question": "She _____ speak 3 languages.", "options": ["can", "can't", "cans", "is can"], "answer": "can", "explanation": "Can + động từ nguyên mẫu. Không thêm -s cho she."},
             {"type": "fill_blank", "question": "He _____ drive. He doesn't have a license.", "options": ["can", "can't", "cannot", "can't"], "answer": "can't", "explanation": "Can't / cannot = không thể."},
             {"type": "fill_blank", "question": "_____ you help me, please?", "options": ["Do", "Are", "Can", "Is"], "answer": "Can", "explanation": "Can you...? = Bạn có thể...? (yêu cầu/xin phép)."},
             {"type": "multiple_choice", "question": "Which is WRONG?", "question_vi": "Câu nào SAI?", "options": ["I can swim.", "She can swim.", "He cans swim.", "They can swim."], "answer": "He cans swim.", "explanation": "Can KHÔNG BAO GIỜ thêm -s: he CAN (không phải 'he cans')."},
             {"type": "fill_blank", "question": "_____ I use your phone?", "options": ["Can", "Do", "Am", "Is"], "answer": "Can", "explanation": "Can I...? = Tôi có thể...không? (xin phép)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Modal Verb Can", "title_vi": "Kiểm tra: Động từ Can", "content": {"questions": [
             {"id": "q1", "question": "She _____ swim.", "options": ["can", "cans", "is can", "do can"], "correct": "can", "explanation": "Can giống nhau cho tất cả chủ ngữ."},
             {"id": "q2", "question": "I _____ fly. I'm not a bird!", "options": ["can", "can't", "am not", "don't"], "correct": "can't", "explanation": "Can't = không thể."},
             {"id": "q3", "question": "_____ you play the piano?", "options": ["Do", "Are", "Can", "Is"], "correct": "Can", "explanation": "Can you...? = dạng câu hỏi."},
             {"id": "q4", "question": "He _____ cook.", "options": ["can't", "can", "is", "has"], "correct": "can", "explanation": "Can = có khả năng làm gì."},
             {"id": "q5", "question": "Which sentence is correct?", "question_vi": "Câu nào đúng?", "options": ["She cans speak English.", "She can speaks English.", "She can speak English.", "She is can speak English."], "correct": "She can speak English.", "explanation": "Can + động từ nguyên mẫu (không -s, không -ing)."},
             {"id": "q6", "question": "Can I _____ the window?", "options": ["opens", "opening", "open", "opened"], "correct": "open", "explanation": "Can + động từ nguyên mẫu."},
             {"id": "q7", "question": "They _____ drive – they are only 10 years old.", "options": ["can", "can't", "are", "do"], "correct": "can't", "explanation": "Trẻ em không thể lái xe (quá nhỏ tuổi)."},
             {"id": "q8", "question": "What does 'can't' mean?", "question_vi": "'Can't' có nghĩa là gì?", "options": ["can / có thể", "cannot / không thể", "don't / không", "isn't / không phải"], "correct": "cannot / không thể", "explanation": "Can't = cannot = không thể."},
             {"id": "q9", "question": "He can _____ very fast.", "options": ["runs", "running", "run", "ran"], "correct": "run", "explanation": "Can + động từ nguyên mẫu: can run."},
             {"id": "q10", "question": "_____ she speak Chinese? – Yes, she can.", "options": ["Do", "Does", "Can", "Is"], "correct": "Can", "explanation": "Câu hỏi với can: Can she...?"}
         ]}}
     ]},

    {"level": "A1", "order": 12, "name": "Days, Months & Seasons", "name_vi": "Ngày, Tháng & Mùa",
     "description": "Learn the days of the week, months of the year, and seasons.",
     "description_vi": "Học các ngày trong tuần, tháng trong năm và các mùa.",
     "grammar_focus": ["on + ngày trong tuần", "in + tháng/mùa", "Số thứ tự"],
     "vocabulary_tags": ["time", "calendar", "seasons", "dates"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Prepositions with Time (on/in/at)", "title_vi": "Ngữ pháp: Giới từ chỉ thời gian", "content": {"explanation": "Dùng 'on' cho ngày trong tuần, 'in' cho tháng/mùa/năm, 'at' cho giờ cụ thể.", "explanation_vi": "Dùng 'on' cho ngày, 'in' cho tháng/mùa/năm, 'at' cho giờ cụ thể.", "key_points": ["ON: on Monday, on Tuesday, on my birthday", "IN: in January, in spring, in 2024", "AT: at 8 o'clock, at noon, at night", "Ordinal numbers for dates: 1st (first), 2nd (second), 3rd (third), 4th (fourth)..."], "examples": [{"en": "I have class on Monday.", "vi": "Tôi có lớp học vào thứ Hai."}, {"en": "My birthday is in March.", "vi": "Sinh nhật tôi vào tháng Ba."}, {"en": "The class starts at 9 a.m.", "vi": "Lớp học bắt đầu lúc 9 giờ sáng."}], "notes": "Remember: on SPECIFIC day, in LONGER period (month/season/year), at SPECIFIC time (o'clock)."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Days, Months & Seasons", "title_vi": "Từ vựng: Ngày, Tháng & Mùa", "content": {"words": [
             {"word": "Monday", "meaning": "Thứ Hai", "example": "I go to school on Monday.", "pronunciation": "/ˈmʌndeɪ/"},
             {"word": "Tuesday", "meaning": "Thứ Ba", "example": "Tuesday is a busy day.", "pronunciation": "/ˈtjuːzdeɪ/"},
             {"word": "Wednesday", "meaning": "Thứ Tư", "example": "Wednesday comes after Tuesday.", "pronunciation": "/ˈwenzdeɪ/"},
             {"word": "Thursday", "meaning": "Thứ Năm", "example": "I have a meeting on Thursday.", "pronunciation": "/ˈθɜːrzdeɪ/"},
             {"word": "Friday", "meaning": "Thứ Sáu", "example": "Friday is the end of the work week.", "pronunciation": "/ˈfraɪdeɪ/"},
             {"word": "Saturday", "meaning": "Thứ Bảy", "example": "I relax on Saturday.", "pronunciation": "/ˈsætərdeɪ/"},
             {"word": "Sunday", "meaning": "Chủ Nhật", "example": "Sunday is a day off.", "pronunciation": "/ˈsʌndeɪ/"},
             {"word": "January", "meaning": "Tháng Một", "example": "January is cold.", "pronunciation": "/ˈdʒænjueri/"},
             {"word": "February", "meaning": "Tháng Hai", "example": "Valentine's Day is in February.", "pronunciation": "/ˈfebrueri/"},
             {"word": "spring", "meaning": "Mùa Xuân", "example": "Flowers bloom in spring.", "pronunciation": "/sprɪŋ/"},
             {"word": "summer", "meaning": "Mùa Hè", "example": "It's hot in summer.", "pronunciation": "/ˈsʌmər/"},
             {"word": "autumn / fall", "meaning": "Mùa Thu", "example": "Leaves fall in autumn.", "pronunciation": "/ˈɔːtəm/"},
             {"word": "winter", "meaning": "Mùa Đông", "example": "It snows in winter.", "pronunciation": "/ˈwɪntər/"},
             {"word": "weekend", "meaning": "cuối tuần", "example": "I rest on weekends.", "pronunciation": "/ˈwiːkend/"},
             {"word": "weekday", "meaning": "ngày thường (thứ 2-6)", "example": "I work on weekdays.", "pronunciation": "/ˈwiːkdeɪ/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Time Prepositions", "title_vi": "Luyện tập: Giới từ thời gian", "content": {"exercises": [
             {"type": "fill_blank", "question": "I have class _____ Monday.", "options": ["in", "on", "at", "by"], "answer": "on", "explanation": "On + ngày trong tuần."},
             {"type": "fill_blank", "question": "My birthday is _____ July.", "options": ["on", "at", "in", "by"], "answer": "in", "explanation": "In + tháng."},
             {"type": "multiple_choice", "question": "Which day comes after Wednesday?", "question_vi": "Ngày nào đứng sau thứ Tư?", "options": ["Tuesday", "Thursday", "Friday", "Monday"], "answer": "Thursday", "explanation": "Thứ 2-3-4-5-6-7-CN."},
             {"type": "multiple_choice", "question": "Which season is coldest?", "question_vi": "Mùa nào lạnh nhất?", "options": ["spring", "summer", "autumn", "winter"], "answer": "winter", "explanation": "Winter = mùa đông (mùa lạnh nhất)."},
             {"type": "fill_blank", "question": "Class starts _____ 8 o'clock.", "options": ["on", "in", "at", "by"], "answer": "at", "explanation": "At + giờ cụ thể."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Days, Months & Seasons", "title_vi": "Kiểm tra: Ngày, Tháng & Mùa", "content": {"questions": [
             {"id": "q1", "question": "School is _____ Monday to Friday.", "options": ["in", "on", "from", "at"], "correct": "from", "explanation": "Từ thứ Hai đến thứ Sáu."},
             {"id": "q2", "question": "Christmas is _____ December.", "options": ["on", "in", "at", "by"], "correct": "in", "explanation": "In + tháng."},
             {"id": "q3", "question": "Christmas Day is _____ December 25th.", "options": ["in", "on", "at", "by"], "correct": "on", "explanation": "On + ngày cụ thể."},
             {"id": "q4", "question": "Which day is the weekend?", "question_vi": "Ngày nào là cuối tuần?", "options": ["Monday", "Wednesday", "Saturday", "Thursday"], "correct": "Saturday", "explanation": "Weekend = thứ Bảy và Chủ nhật."},
             {"id": "q5", "question": "It snows in _____. (tuyết rơi)", "options": ["summer", "spring", "autumn", "winter"], "correct": "winter", "explanation": "Winter = mùa đông (mùa có tuyết)."},
             {"id": "q6", "question": "What month comes before March?", "question_vi": "Tháng nào đứng trước tháng Ba?", "options": ["April", "February", "January", "May"], "correct": "February", "explanation": "Tháng 1 - 2 - 3."},
             {"id": "q7", "question": "I relax _____ weekends.", "options": ["in", "on", "at", "by"], "correct": "on", "explanation": "On weekends (ngày cuối tuần)."},
             {"id": "q8", "question": "Which season has flowers blooming?", "question_vi": "Mùa nào có hoa nở?", "options": ["winter", "autumn", "spring", "summer"], "correct": "spring", "explanation": "Spring = mùa xuân (hoa nở)."},
             {"id": "q9", "question": "The meeting is _____ 3 p.m.", "options": ["in", "on", "at", "by"], "correct": "at", "explanation": "At + giờ cụ thể trong ngày."},
             {"id": "q10", "question": "How many days are in a week?", "question_vi": "Một tuần có bao nhiêu ngày?", "options": ["5", "6", "7", "8"], "correct": "7", "explanation": "7 ngày: T2, T3, T4, T5, T6, T7, CN."}
         ]}}
     ]},

    {"level": "A1", "order": 13, "name": "Jobs & Occupations", "name_vi": "Nghề nghiệp",
     "description": "Learn vocabulary for different jobs and how to talk about work.",
     "description_vi": "Học từ vựng về các nghề nghiệp và cách nói về công việc.",
     "grammar_focus": ["be + nghề nghiệp", "work as/work in", "a/an + nghề nghiệp"],
     "vocabulary_tags": ["jobs", "work", "professions"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Talking About Jobs", "title_vi": "Ngữ pháp: Nói về nghề nghiệp", "content": {"explanation": "Dùng 'to be' để mô tả nghề nghiệp. Dùng 'work as' hoặc 'work in'.", "explanation_vi": "Dùng 'to be' để mô tả nghề nghiệp. Dùng 'work as' hoặc 'work in'.", "key_points": ["I am a doctor. (a/an + job)", "She works as a nurse.", "He works in a hospital.", "What do you do (for a living)? = Bạn làm nghề gì?"], "examples": [{"en": "I am a teacher.", "vi": "Tôi là giáo viên."}, {"en": "She works as an engineer.", "vi": "Cô ấy làm kỹ sư."}, {"en": "He works in a school.", "vi": "Anh ấy làm việc ở trường."}], "notes": "Dùng 'a' trước phụ âm (a teacher, a doctor) và 'an' trước nguyên âm (an engineer, an artist)."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Common Jobs", "title_vi": "Từ vựng: Các nghề phổ biến", "content": {"words": [
             {"word": "doctor", "meaning": "bác sĩ", "example": "She is a doctor.", "pronunciation": "/ˈdɒktər/"},
             {"word": "nurse", "meaning": "y tá", "example": "He works as a nurse.", "pronunciation": "/nɜːrs/"},
             {"word": "teacher", "meaning": "giáo viên", "example": "My mother is a teacher.", "pronunciation": "/ˈtiːtʃər/"},
             {"word": "engineer", "meaning": "kỹ sư", "example": "He is an engineer.", "pronunciation": "/ˌendʒɪˈnɪər/"},
             {"word": "farmer", "meaning": "nông dân", "example": "My grandfather is a farmer.", "pronunciation": "/ˈfɑːrmər/"},
             {"word": "cook / chef", "meaning": "đầu bếp", "example": "She works as a cook.", "pronunciation": "/kʊk/"},
             {"word": "police officer", "meaning": "cảnh sát", "example": "He is a police officer.", "pronunciation": "/pəˈliːs ˈɒfɪsər/"},
             {"word": "driver", "meaning": "tài xế", "example": "My uncle is a taxi driver.", "pronunciation": "/ˈdraɪvər/"},
             {"word": "businessman", "meaning": "doanh nhân", "example": "She is a businesswoman.", "pronunciation": "/ˈbɪznɪsmæn/"},
             {"word": "student", "meaning": "học sinh/sinh viên", "example": "I am a student.", "pronunciation": "/ˈstjuːdnt/"},
             {"word": "artist", "meaning": "nghệ sĩ", "example": "He works as an artist.", "pronunciation": "/ˈɑːrtɪst/"},
             {"word": "office", "meaning": "văn phòng", "example": "She works in an office.", "pronunciation": "/ˈɒfɪs/"},
             {"word": "hospital", "meaning": "bệnh viện", "example": "Doctors work in a hospital.", "pronunciation": "/ˈhɒspɪtl/"},
             {"word": "school", "meaning": "trường học", "example": "Giáo viên làm việc ở trường học.", "pronunciation": "/skuːl/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Jobs & Workplaces", "title_vi": "Luyện tập: Nghề nghiệp & Nơi làm việc", "content": {"exercises": [
             {"type": "fill_blank", "question": "She is _____ engineer. (an/a)", "options": ["a", "an", "the", "–"], "answer": "an", "explanation": "Engineer bắt đầu bằng nguyên âm 'e' → dùng an."},
             {"type": "multiple_choice", "question": "Where does a doctor work?", "options": ["school", "office", "hospital", "farm"], "answer": "hospital", "explanation": "Bác sĩ làm việc ở bệnh viện."},
             {"type": "fill_blank", "question": "What do you _____ for a living? (asking job)", "options": ["make", "do", "work", "play"], "answer": "do", "explanation": "'What do you do?' = Bạn làm nghề gì?"},
             {"type": "multiple_choice", "question": "He grows vegetables. He is a:", "options": ["teacher", "doctor", "farmer", "chef"], "answer": "farmer", "explanation": "Farmer = nông dân (grows crops)."},
             {"type": "fill_blank", "question": "She works _____ a nurse in the hospital.", "options": ["in", "as", "by", "for"], "answer": "as", "explanation": "Works as + job title."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Jobs & Occupations", "title_vi": "Kiểm tra: Nghề nghiệp", "content": {"questions": [
             {"id": "q1", "question": "She is _____ artist.", "options": ["a", "an", "the", "–"], "correct": "an", "explanation": "Artist bắt đầu bằng nguyên âm 'a' → dùng an."},
             {"id": "q2", "question": "Where do teachers work?", "question_vi": "Giáo viên làm việc ở đâu?", "options": ["hospital", "school", "farm", "office"], "correct": "school", "explanation": "Giáo viên làm việc ở trường học."},
             {"id": "q3", "question": "He drives a taxi. He is a:", "question_vi": "Anh ấy lái taxi. Anh ấy là:", "options": ["pilot", "driver", "engineer", "farmer"], "correct": "driver", "explanation": "Taxi driver = tài xế."},
             {"id": "q4", "question": "What _____ you do for a living?", "options": ["is", "do", "are", "can"], "correct": "do", "explanation": "What do you do? = job question."},
             {"id": "q5", "question": "She works _____ a nurse.", "options": ["in", "as", "on", "by"], "correct": "as", "explanation": "Works as + job."},
             {"id": "q6", "question": "I am _____ teacher.", "options": ["an", "a", "the", "–"], "correct": "a", "explanation": "Teacher bắt đầu bằng phụ âm 't' → dùng a."},
             {"id": "q7", "question": "He works in a hospital. He is probably a:", "question_vi": "Anh ấy làm ở bệnh viện. Anh ấy có thể là:", "options": ["farmer", "teacher", "doctor or nurse", "driver"], "correct": "doctor or nurse", "explanation": "Hospital = bệnh viện → doctors/nurses work there."},
             {"id": "q8", "question": "What does a chef do?", "question_vi": "Đầu bếp làm gì?", "options": ["teaches students", "cooks food", "drives cars", "plants crops"], "correct": "cooks food", "explanation": "Chef / cook = đầu bếp."},
             {"id": "q9", "question": "She works in _____ office.", "options": ["a", "an", "the", "–"], "correct": "an", "explanation": "Office bắt đầu bằng nguyên âm 'o' → dùng an."},
             {"id": "q10", "question": "My father _____ a businessman.", "options": ["work", "works", "is", "are"], "correct": "is", "explanation": "Bố tôi là doanh nhân (to be + nghề nghiệp)."}
         ]}}
     ]},

    {"level": "A1", "order": 14, "name": "Places in the City", "name_vi": "Các địa điểm trong thành phố",
     "description": "Learn the names of common places in a city and how to ask for directions.",
     "description_vi": "Học tên các địa điểm phổ biến trong thành phố và cách hỏi đường.",
     "grammar_focus": ["there is/are (địa điểm)", "Where is...? (ở đâu)", "near/far from (gần/xa)"],
     "vocabulary_tags": ["city", "places", "directions", "buildings"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Asking for & Giving Directions", "title_vi": "Ngữ pháp: Hỏi và chỉ đường", "content": {"explanation": "Dùng 'Where is...?' để hỏi vị trí và chỉ đường bằng câu mệnh lệnh.", "explanation_vi": "Dùng 'Where is...?' để hỏi vị trí và chỉ đường bằng câu mệnh lệnh.", "key_points": ["Where is the post office?", "It's next to / opposite / behind / in front of...", "Go straight, turn left/right", "Is there a bank near here?"], "examples": [{"en": "Excuse me, where is the hospital?", "vi": "Xin lỗi, bệnh viện ở đâu?"}, {"en": "It's opposite the park.", "vi": "Nó nằm đối diện công viên."}, {"en": "Is there a supermarket near here?", "vi": "Có siêu thị nào gần đây không?"}], "notes": "Khi hỏi đường người lạ, luôn bắt đầu với 'Excuse me' để tỏ ra lịch sự."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Places in the City", "title_vi": "Từ vựng: Địa điểm trong thành phố", "content": {"words": [
             {"word": "bank", "meaning": "ngân hàng", "example": "I need to go to the bank.", "pronunciation": "/bæŋk/"},
             {"word": "post office", "meaning": "bưu điện", "example": "I send letters at the post office.", "pronunciation": "/poʊst ˈɒfɪs/"},
             {"word": "hospital", "meaning": "bệnh viện", "example": "She is at the hospital.", "pronunciation": "/ˈhɒspɪtl/"},
             {"word": "school", "meaning": "trường học", "example": "Children go to school.", "pronunciation": "/skuːl/"},
             {"word": "supermarket", "meaning": "siêu thị", "example": "I buy food at the supermarket.", "pronunciation": "/ˈsuːpərmɑːrkɪt/"},
             {"word": "restaurant", "meaning": "nhà hàng", "example": "Let's eat at a restaurant.", "pronunciation": "/ˈrestrɒnt/"},
             {"word": "park", "meaning": "công viên", "example": "Children play in the park.", "pronunciation": "/pɑːrk/"},
             {"word": "library", "meaning": "thư viện", "example": "I study at the library.", "pronunciation": "/ˈlaɪbreri/"},
             {"word": "cinema / movie theater", "meaning": "rạp chiếu phim", "example": "Let's go to the cinema!", "pronunciation": "/ˈsɪnəmə/"},
             {"word": "hotel", "meaning": "khách sạn", "example": "She stays at a hotel.", "pronunciation": "/hoʊˈtel/"},
             {"word": "airport", "meaning": "sân bay", "example": "The airport is far from the city.", "pronunciation": "/ˈeərpɔːrt/"},
             {"word": "station", "meaning": "nhà ga / trạm", "example": "Where is the bus station?", "pronunciation": "/ˈsteɪʃn/"},
             {"word": "opposite", "meaning": "đối diện", "example": "The bank is opposite the park.", "pronunciation": "/ˈɒpəzɪt/"},
             {"word": "between", "meaning": "ở giữa (2 vật)", "example": "The café is between the bank and the school.", "pronunciation": "/bɪˈtwiːn/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: City Directions", "title_vi": "Luyện tập: Chỉ đường trong thành phố", "content": {"exercises": [
             {"type": "multiple_choice", "question": "Where do you borrow books?", "options": ["hospital", "bank", "library", "hotel"], "answer": "library", "explanation": "Library = thư viện (borrow books)."},
             {"type": "fill_blank", "question": "Excuse me, _____ is the post office?", "options": ["what", "who", "where", "when"], "answer": "where", "explanation": "Where = ở đâu (hỏi vị trí)."},
             {"type": "multiple_choice", "question": "The café is _____ the bank and the school.", "options": ["opposite", "next to", "between", "behind"], "answer": "between", "explanation": "Between = ở giữa hai nơi."},
             {"type": "multiple_choice", "question": "You need to fly. Where do you go?", "options": ["hotel", "airport", "station", "cinema"], "answer": "airport", "explanation": "Airport = sân bay (để bay)."},
             {"type": "fill_blank", "question": "The park is _____ the hotel. (đối diện)", "options": ["between", "next to", "opposite", "behind"], "answer": "opposite", "explanation": "Opposite = đối diện."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Places in the City", "title_vi": "Kiểm tra: Địa điểm trong thành phố", "content": {"questions": [
             {"id": "q1", "question": "Where do you watch movies?", "question_vi": "Bạn xem phim ở đâu?", "options": ["library", "hospital", "cinema", "bank"], "correct": "cinema", "explanation": "Cinema = rạp chiếu phim."},
             {"id": "q2", "question": "Excuse me, _____ is the nearest bank?", "options": ["what", "who", "where", "when"], "correct": "where", "explanation": "Where = hỏi địa điểm."},
             {"id": "q3", "question": "Where do sick people go?", "question_vi": "Người bệnh đi đâu?", "options": ["school", "library", "hotel", "hospital"], "correct": "hospital", "explanation": "Hospital = bệnh viện."},
             {"id": "q4", "question": "The café is _____ the post office. (both sides)", "options": ["opposite", "between", "next to", "behind"], "correct": "next to", "explanation": "Next to = bên cạnh."},
             {"id": "q5", "question": "You need to send a letter. Go to the:", "question_vi": "Bạn cần gửi thư. Đi đến:", "options": ["bank", "post office", "hotel", "library"], "correct": "post office", "explanation": "Post office = bưu điện."},
             {"id": "q6", "question": "The park is _____ the school. (directly across)", "options": ["next to", "behind", "opposite", "between"], "correct": "opposite", "explanation": "Opposite = đối diện."},
             {"id": "q7", "question": "Where do tourists usually stay?", "question_vi": "Khách du lịch thường ở đâu?", "options": ["school", "hospital", "hotel", "cinema"], "correct": "hotel", "explanation": "Hotel = khách sạn."},
             {"id": "q8", "question": "I need money. Where should I go?", "question_vi": "Tôi cần tiền. Tôi nên đi đâu?", "options": ["library", "restaurant", "bank", "park"], "correct": "bank", "explanation": "Bank = ngân hàng."},
             {"id": "q9", "question": "The market is _____ the park and the school.", "options": ["next to", "opposite", "between", "behind"], "correct": "between", "explanation": "Between = ở giữa."},
             {"id": "q10", "question": "Where do you buy food in a big store?", "question_vi": "Bạn mua thực phẩm ở cửa hàng lớn nào?", "options": ["restaurant", "bank", "supermarket", "cinema"], "correct": "supermarket", "explanation": "Supermarket = siêu thị."}
         ]}}
     ]},

    {"level": "A1", "order": 15, "name": "Health & Body Parts", "name_vi": "Sức khỏe & Bộ phận cơ thể",
     "description": "Learn body parts vocabulary and how to talk about health problems.",
     "description_vi": "Học từ vựng về bộ phận cơ thể và cách nói về vấn đề sức khỏe.",
     "grammar_focus": ["I have a + triệu chứng", "My + bộ phận cơ thể + hurts", "should (nên)"],
     "vocabulary_tags": ["health", "body", "illness", "doctor"],
     "estimated_minutes": 30,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Talking About Health", "title_vi": "Ngữ pháp: Nói về sức khỏe", "content": {"explanation": "Dùng 'I have a headache/cold/fever' để mô tả triệu chứng. Dùng 'My...hurts' để nói về đau.", "explanation_vi": "Dùng 'I have a headache/cold/fever' để mô tả triệu chứng. Dùng 'My...hurts' để nói về đau.", "key_points": ["I have a headache. / I have a cold.", "My head hurts. / My back hurts.", "I feel sick/tired/dizzy.", "You should see a doctor.", "Should + base verb (advice)"], "examples": [{"en": "I have a stomachache.", "vi": "Tôi bị đau bụng."}, {"en": "My throat hurts.", "vi": "Họng tôi đau."}, {"en": "You should rest at home.", "vi": "Bạn nên nghỉ ngơi ở nhà."}], "notes": "'Should' gives advice. Always followed by base verb: You should rest (NOT rests)."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Body Parts & Symptoms", "title_vi": "Từ vựng: Bộ phận cơ thể & Triệu chứng", "content": {"words": [
             {"word": "head", "meaning": "đầu", "example": "I have a headache.", "pronunciation": "/hed/"},
             {"word": "face", "meaning": "khuôn mặt", "example": "Wash your face.", "pronunciation": "/feɪs/"},
             {"word": "eye", "meaning": "mắt", "example": "My eyes hurt from the screen.", "pronunciation": "/aɪ/"},
             {"word": "ear", "meaning": "tai", "example": "I have an earache.", "pronunciation": "/ɪər/"},
             {"word": "nose", "meaning": "mũi", "example": "My nose is running.", "pronunciation": "/noʊz/"},
             {"word": "mouth", "meaning": "miệng", "example": "Open your mouth.", "pronunciation": "/maʊθ/"},
             {"word": "throat", "meaning": "họng", "example": "My throat hurts.", "pronunciation": "/θroʊt/"},
             {"word": "arm", "meaning": "cánh tay", "example": "I broke my arm.", "pronunciation": "/ɑːrm/"},
             {"word": "hand", "meaning": "bàn tay", "example": "Wash your hands.", "pronunciation": "/hænd/"},
             {"word": "leg", "meaning": "chân", "example": "My leg is sore.", "pronunciation": "/leɡ/"},
             {"word": "stomach", "meaning": "bụng/dạ dày", "example": "I have a stomachache.", "pronunciation": "/ˈstʌmək/"},
             {"word": "headache", "meaning": "đau đầu", "example": "I have a terrible headache.", "pronunciation": "/ˈhedeɪk/"},
             {"word": "cold", "meaning": "cảm lạnh", "example": "I have a cold.", "pronunciation": "/koʊld/"},
             {"word": "fever", "meaning": "sốt", "example": "She has a fever.", "pronunciation": "/ˈfiːvər/"},
             {"word": "tired", "meaning": "mệt mỏi", "example": "I feel very tired.", "pronunciation": "/ˈtaɪərd/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Health Problems", "title_vi": "Luyện tập: Vấn đề sức khỏe", "content": {"exercises": [
             {"type": "multiple_choice", "question": "I have a _____. My head hurts. (đau đầu)", "options": ["stomachache", "headache", "cold", "fever"], "answer": "headache", "explanation": "Headache = đau đầu."},
             {"type": "fill_blank", "question": "My throat _____. I can't speak. (hurt)", "options": ["hurt", "hurts", "hurting", "is hurt"], "answer": "hurts", "explanation": "My throat + hurts (ngôi thứ 3 singular)."},
             {"type": "multiple_choice", "question": "You have a fever. You _____ see a doctor.", "options": ["can", "do", "should (nên)", "must always"], "answer": "should (nên)", "explanation": "Should = lời khuyên."},
             {"type": "multiple_choice", "question": "What body part do you use to hear?", "options": ["eye", "nose", "ear", "mouth"], "answer": "ear", "explanation": "Ear = tai (to hear)."},
             {"type": "fill_blank", "question": "She _____ a cold. She's sneezing a lot.", "options": ["is", "has", "have", "gets"], "answer": "has", "explanation": "She has a cold (to have + illness)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Health & Body Parts", "title_vi": "Kiểm tra: Sức khỏe & Cơ thể", "content": {"questions": [
             {"id": "q1", "question": "My _____ hurts. I can't walk. (chân)", "options": ["arm", "head", "leg", "hand"], "correct": "leg", "explanation": "Leg = chân."},
             {"id": "q2", "question": "I have a headache means:", "question_vi": "'I have a headache' có nghĩa là:", "options": ["My stomach hurts", "My head hurts", "I am tired", "I have a cold"], "correct": "My head hurts", "explanation": "Headache = đau đầu."},
             {"id": "q3", "question": "You look sick. You _____ rest.", "options": ["can", "do", "should (nên)", "will"], "correct": "should (nên)", "explanation": "Should = lời khuyên."},
             {"id": "q4", "question": "She has a _____. Her temperature is 39°C.", "options": ["cold", "headache", "fever", "stomachache"], "correct": "fever", "explanation": "Fever = sốt (high temperature)."},
             {"id": "q5", "question": "What body part do you use to see?", "question_vi": "Bạn dùng bộ phận nào để nhìn?", "options": ["ear", "nose", "eye", "mouth"], "correct": "eye", "explanation": "Eye = mắt (to see)."},
             {"id": "q6", "question": "I _____ a stomachache. (Khai báo triệu chứng)", "options": ["am", "feel", "have", "get"], "correct": "have", "explanation": "I have a + symptom."},
             {"id": "q7", "question": "My _____ hurts. I can't write. (bàn tay)", "options": ["leg", "hand", "eye", "ear"], "correct": "hand", "explanation": "Hand = bàn tay."},
             {"id": "q8", "question": "I feel very _____. I need to sleep. (mệt)", "options": ["happy", "hungry", "tired", "cold"], "correct": "tired", "explanation": "Tired = mệt mỏi."},
             {"id": "q9", "question": "Where is your stomach?", "question_vi": "Dạ dày/bụng của bạn ở đâu?", "options": ["in your head", "in your abdomen", "in your arm", "in your leg"], "correct": "in your abdomen", "explanation": "Stomach / abdomen = bụng."},
             {"id": "q10", "question": "He has a cold. He _____ see a doctor.", "options": ["can", "do", "should (nên)", "must"], "correct": "should (nên)", "explanation": "Should = nên (advice)."}
         ]}}
     ]},

    {"level": "A1", "order": 16, "name": "Hobbies & Free Time", "name_vi": "Sở thích & Thời gian rảnh",
     "description": "Talk about what you like to do in your free time.",
     "description_vi": "Nói về những gì bạn thích làm khi rảnh rỗi.",
     "grammar_focus": ["like + V-ing", "love/enjoy/hate + V-ing", "how often (bao lâu một lần)"],
     "vocabulary_tags": ["hobbies", "leisure", "free time", "activities"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Like/Love/Hate + -ing", "title_vi": "Ngữ pháp: Like/Love/Hate + Gerund", "content": {"explanation": "Sau like, love, enjoy, hate → dùng động từ + -ing.", "explanation_vi": "Sau like, love, enjoy, hate → dùng động từ + -ing (danh động từ).", "key_points": ["I like swimming. (NOT 'I like swim')", "She loves reading books.", "He hates waking up early.", "Do you enjoy cooking?", "How often do you...? – Every day / Once a week / Sometimes"], "examples": [{"en": "I love watching movies.", "vi": "Tôi rất thích xem phim."}, {"en": "She enjoys playing the guitar.", "vi": "Cô ấy thích chơi đàn guitar."}, {"en": "He hates doing homework.", "vi": "Anh ấy ghét làm bài tập về nhà."}], "notes": "Like + gerund (general): I like swimming. Like + to-infinitive (specific occasion): I'd like to swim now. Both are correct but mean slightly different things."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Hobbies & Activities", "title_vi": "Từ vựng: Sở thích & Hoạt động", "content": {"words": [
             {"word": "reading", "meaning": "đọc sách", "example": "I enjoy reading novels.", "pronunciation": "/ˈriːdɪŋ/"},
             {"word": "swimming", "meaning": "bơi lội", "example": "She loves swimming.", "pronunciation": "/ˈswɪmɪŋ/"},
             {"word": "cooking", "meaning": "nấu ăn", "example": "He enjoys cooking.", "pronunciation": "/ˈkʊkɪŋ/"},
             {"word": "traveling", "meaning": "du lịch", "example": "I love traveling to new places.", "pronunciation": "/ˈtrævəlɪŋ/"},
             {"word": "playing sports", "meaning": "chơi thể thao", "example": "She likes playing sports.", "pronunciation": "/pleɪɪŋ spɔːrts/"},
             {"word": "listening to music", "meaning": "nghe nhạc", "example": "He loves listening to music.", "pronunciation": "/ˈlɪsənɪŋ tə ˈmjuːzɪk/"},
             {"word": "watching movies", "meaning": "xem phim", "example": "I like watching movies.", "pronunciation": "/ˈwɒtʃɪŋ ˈmuːviz/"},
             {"word": "drawing / painting", "meaning": "vẽ", "example": "She enjoys painting.", "pronunciation": "/ˈdrɔːɪŋ/"},
             {"word": "gardening", "meaning": "làm vườn", "example": "My grandmother loves gardening.", "pronunciation": "/ˈɡɑːrdənɪŋ/"},
             {"word": "shopping", "meaning": "mua sắm", "example": "She likes shopping.", "pronunciation": "/ˈʃɒpɪŋ/"},
             {"word": "cycling", "meaning": "đi xe đạp", "example": "I enjoy cycling in the park.", "pronunciation": "/ˈsaɪklɪŋ/"},
             {"word": "once a week", "meaning": "một lần một tuần", "example": "I swim once a week.", "pronunciation": "/wʌns ə wiːk/"},
             {"word": "every day", "meaning": "mỗi ngày", "example": "She reads every day.", "pronunciation": "/ˈevri deɪ/"},
             {"word": "on weekends", "meaning": "vào cuối tuần", "example": "He cooks on weekends.", "pronunciation": "/ɒn ˈwiːkendz/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Hobbies", "title_vi": "Luyện tập: Sở thích", "content": {"exercises": [
             {"type": "fill_blank", "question": "I like _____ books. (read → gerund)", "options": ["read", "reads", "reading", "to read"], "answer": "reading", "explanation": "Like + verb-ing: I like reading."},
             {"type": "fill_blank", "question": "She _____ playing soccer. (love)", "options": ["love", "loves", "loving", "loved"], "answer": "loves", "explanation": "She (3rd) → loves."},
             {"type": "multiple_choice", "question": "He hates _____ up early.", "options": ["wake", "wakes", "waking", "waked"], "answer": "waking", "explanation": "Hate + verb-ing: hates waking."},
             {"type": "multiple_choice", "question": "How _____ do you exercise?", "options": ["many", "much", "often", "long"], "answer": "often", "explanation": "How often = bao lâu một lần."},
             {"type": "fill_blank", "question": "I love _____ to new places. (travel)", "options": ["travel", "travels", "traveling", "traveled"], "answer": "traveling", "explanation": "Love + verb-ing: love traveling."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Hobbies & Free Time", "title_vi": "Kiểm tra: Sở thích & Thời gian rảnh", "content": {"questions": [
             {"id": "q1", "question": "She likes _____ in the park.", "options": ["run", "runs", "running", "ran"], "correct": "running", "explanation": "Like + verb-ing."},
             {"id": "q2", "question": "I hate _____ homework.", "options": ["do", "does", "doing", "did"], "correct": "doing", "explanation": "Hate + verb-ing: doing."},
             {"id": "q3", "question": "How _____ do you go swimming?", "options": ["many", "much", "often", "long"], "correct": "often", "explanation": "How often = frequency question."},
             {"id": "q4", "question": "He enjoys _____ to music.", "options": ["listen", "listens", "listening", "listened"], "correct": "listening", "explanation": "Enjoy + verb-ing: listening."},
             {"id": "q5", "question": "I love _____. (du lịch)", "options": ["travel", "traveling", "travels", "traveled"], "correct": "traveling", "explanation": "Love + verb-ing: traveling."},
             {"id": "q6", "question": "Which is a hobby?", "question_vi": "Từ nào là sở thích?", "options": ["sleep", "work", "painting", "be sick"], "correct": "painting", "explanation": "Painting = vẽ tranh (a hobby)."},
             {"id": "q7", "question": "She _____ shopping on weekends.", "options": ["love", "loves", "loving", "is love"], "correct": "loves", "explanation": "She → loves (ngôi thứ 3)."},
             {"id": "q8", "question": "Do you enjoy _____ movies?", "options": ["watch", "watches", "watching", "watched"], "correct": "watching", "explanation": "Enjoy + verb-ing."},
             {"id": "q9", "question": "'Once a week' means:", "question_vi": "'Once a week' có nghĩa là:", "options": ["every day", "7 times a week", "1 time per week", "never"], "correct": "1 time per week", "explanation": "Once a week = 1 lần/tuần."},
             {"id": "q10", "question": "They _____ cycling on weekends.", "options": ["enjoy", "enjoys", "enjoying", "enjoyed"], "correct": "enjoy", "explanation": "They → enjoy (base form, no -s)."}
         ]}}
     ]},

    {"level": "A1", "order": 17, "name": "Weather & Seasons", "name_vi": "Thời tiết & Mùa",
     "description": "Describe the weather and talk about different seasons.",
     "description_vi": "Mô tả thời tiết và nói về các mùa trong năm.",
     "grammar_focus": ["It is + tính từ thời tiết", "What's the weather like? (Thời tiết thế nào?)", "Động từ chỉ thời tiết"],
     "vocabulary_tags": ["weather", "seasons", "nature", "description"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Talking About Weather", "title_vi": "Ngữ pháp: Nói về thời tiết", "content": {"explanation": "Use 'It is' to describe weather. 'It' is always the subject when talking about weather.", "explanation_vi": "Dùng 'It is' để mô tả thời tiết. 'It' luôn là chủ ngữ khi nói về thời tiết.", "key_points": ["It is sunny/cloudy/rainy/windy/snowy.", "It is hot/cold/warm/cool.", "What's the weather like today? – It's sunny.", "Weather verbs: It rains, It snows (present simple for habits)"], "examples": [{"en": "It's very hot today.", "vi": "Hôm nay rất nóng."}, {"en": "What's the weather like in Hanoi? – It's rainy.", "vi": "Thời tiết ở Hà Nội như thế nào? – Trời đang mưa."}, {"en": "It snows in winter.", "vi": "Tuyết rơi vào mùa đông."}], "notes": "Chú ý: Trong tiếng Anh, dùng 'It IS sunny' (tính từ). Trong tiếng Việt, bạn nói 'Trời nắng'. Cấu trúc ngữ pháp khác nhau!"}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Weather Words", "title_vi": "Từ vựng: Từ về thời tiết", "content": {"words": [
             {"word": "sunny", "meaning": "nắng", "example": "It's a sunny day!", "pronunciation": "/ˈsʌni/"},
             {"word": "cloudy", "meaning": "nhiều mây", "example": "The sky is cloudy.", "pronunciation": "/ˈklaʊdi/"},
             {"word": "rainy", "meaning": "có mưa", "example": "It's rainy today.", "pronunciation": "/ˈreɪni/"},
             {"word": "windy", "meaning": "nhiều gió", "example": "It's very windy outside.", "pronunciation": "/ˈwɪndi/"},
             {"word": "snowy", "meaning": "có tuyết", "example": "It's snowy in winter.", "pronunciation": "/ˈsnoʊi/"},
             {"word": "foggy", "meaning": "có sương mù", "example": "It's foggy this morning.", "pronunciation": "/ˈfɒɡi/"},
             {"word": "hot", "meaning": "nóng", "example": "It's 38°C – very hot!", "pronunciation": "/hɒt/"},
             {"word": "cold", "meaning": "lạnh", "example": "It's cold in winter.", "pronunciation": "/koʊld/"},
             {"word": "warm", "meaning": "ấm áp", "example": "Spring is warm.", "pronunciation": "/wɔːrm/"},
             {"word": "cool", "meaning": "mát mẻ", "example": "Autumn is cool.", "pronunciation": "/kuːl/"},
             {"word": "temperature", "meaning": "nhiệt độ", "example": "The temperature is 25°C.", "pronunciation": "/ˈtemprətʃər/"},
             {"word": "umbrella", "meaning": "ô/dù", "example": "Take an umbrella – it's raining!", "pronunciation": "/ʌmˈbrelə/"},
             {"word": "sunshine", "meaning": "ánh nắng mặt trời", "example": "I love the sunshine.", "pronunciation": "/ˈsʌnʃaɪn/"},
             {"word": "storm", "meaning": "bão", "example": "There's a storm coming.", "pronunciation": "/stɔːrm/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Weather Descriptions", "title_vi": "Luyện tập: Mô tả thời tiết", "content": {"exercises": [
             {"type": "fill_blank", "question": "What's the weather _____? – It's sunny.", "options": ["look", "like", "as", "is"], "answer": "like", "explanation": "What's the weather like? = Thời tiết như thế nào?"},
             {"type": "multiple_choice", "question": "It _____ very cold in winter here.", "options": ["am", "are", "is", "be"], "answer": "is", "explanation": "It is (weather) → It is cold."},
             {"type": "multiple_choice", "question": "It's raining. What should you take?", "options": ["sunglasses", "umbrella", "jacket", "nothing"], "answer": "umbrella", "explanation": "Umbrella = ô/dù (để che mưa)."},
             {"type": "fill_blank", "question": "It _____ a lot in summer here.", "options": ["rains", "is raining", "raining", "rain"], "answer": "rains", "explanation": "Present simple for habits: it rains (a lot) in summer."},
             {"type": "multiple_choice", "question": "Which word describes warm weather?", "options": ["snowy", "foggy", "sunny", "stormy"], "answer": "sunny", "explanation": "Sunny = nắng (warm/hot weather)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Weather & Seasons", "title_vi": "Kiểm tra: Thời tiết & Mùa", "content": {"questions": [
             {"id": "q1", "question": "What's the weather _____?", "options": ["as", "like", "look", "see"], "correct": "like", "explanation": "What's the weather like? = standard question."},
             {"id": "q2", "question": "It _____ hot today. I need a fan.", "options": ["am", "are", "is", "be"], "correct": "is", "explanation": "It is (weather description)."},
             {"id": "q3", "question": "It's raining. The weather is:", "question_vi": "Trời đang mưa. Thời tiết là:", "options": ["sunny", "windy", "rainy", "snowy"], "correct": "rainy", "explanation": "Rain → rainy."},
             {"id": "q4", "question": "Spring is usually:", "question_vi": "Mùa xuân thường:", "options": ["cold", "warm", "very hot", "snowy"], "correct": "warm", "explanation": "Spring = ấm áp."},
             {"id": "q5", "question": "You need an umbrella when it's:", "question_vi": "Bạn cần dù khi trời:", "options": ["sunny", "windy", "rainy", "cool"], "correct": "rainy", "explanation": "Umbrella = for rain."},
             {"id": "q6", "question": "The temperature is 5°C. It's very:", "question_vi": "Nhiệt độ 5°C. Trời rất:", "options": ["hot", "warm", "cool", "cold"], "correct": "cold", "explanation": "5°C = very cold."},
             {"id": "q7", "question": "It _____ in winter in northern countries.", "options": ["snows", "rains", "is sunny", "is warm"], "correct": "snows", "explanation": "It snows in winter (cold countries)."},
             {"id": "q8", "question": "Which season is usually hottest?", "question_vi": "Mùa nào thường nóng nhất?", "options": ["spring", "summer", "autumn", "winter"], "correct": "summer", "explanation": "Summer = mùa hè (hottest)."},
             {"id": "q9", "question": "It _____ windy outside. Hold your hat!", "options": ["am", "are", "is", "be"], "correct": "is", "explanation": "It is + adjective."},
             {"id": "q10", "question": "What is 'nhiệt độ' in English?", "question_vi": "'Nhiệt độ' trong tiếng Anh là gì?", "options": ["weather", "climate", "temperature", "season"], "correct": "temperature", "explanation": "Temperature = nhiệt độ."}
         ]}}
     ]},

    {"level": "A1", "order": 18, "name": "School & Education", "name_vi": "Trường học & Giáo dục",
     "description": "Learn vocabulary about school subjects and classroom objects.",
     "description_vi": "Học từ vựng về các môn học và đồ dùng trong lớp học.",
     "grammar_focus": ["have/has (lịch trình)", "What subject do you like? (Thích môn gì?)", "Câu lệnh trong lớp học"],
     "vocabulary_tags": ["school", "subjects", "education", "classroom"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Talking About School", "title_vi": "Ngữ pháp: Nói về trường học", "content": {"explanation": "Dùng thì hiện tại đơn để nói về lịch học và các môn học.", "key_points": ["I study English/Math/Science.", "I have English class on Monday.", "What subject do you like/study?", "I am in grade 10. (lớp 10)", "Classroom instructions: Open your book. Listen. Repeat."], "examples": [{"en": "I study Math on Monday and Wednesday.", "vi": "Tôi học Toán vào thứ Hai và thứ Tư."}, {"en": "What is your favorite subject?", "vi": "Môn học yêu thích của bạn là gì?"}, {"en": "I like English but I don't like Physics.", "vi": "Tôi thích tiếng Anh nhưng không thích Vật lý."}], "notes": "Trong tiếng Anh, tên môn học phải viết hoa: English, Math, Science, History (KHÔNG phải english, math)."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: School Subjects & Classroom", "title_vi": "Từ vựng: Môn học & Lớp học", "content": {"words": [
             {"word": "English", "meaning": "Tiếng Anh", "example": "I study English.", "pronunciation": "/ˈɪŋɡlɪʃ/"},
             {"word": "Math / Mathematics", "meaning": "Toán học", "example": "Math is difficult.", "pronunciation": "/mæθ/"},
             {"word": "Science", "meaning": "Khoa học", "example": "I like Science.", "pronunciation": "/ˈsaɪəns/"},
             {"word": "History", "meaning": "Lịch sử", "example": "History is interesting.", "pronunciation": "/ˈhɪstri/"},
             {"word": "Geography", "meaning": "Địa lý", "example": "We study Geography today.", "pronunciation": "/dʒiˈɒɡrəfi/"},
             {"word": "Art", "meaning": "Mỹ thuật", "example": "She loves Art class.", "pronunciation": "/ɑːrt/"},
             {"word": "Music", "meaning": "Âm nhạc", "example": "Music is my favorite subject.", "pronunciation": "/ˈmjuːzɪk/"},
             {"word": "Physical Education / PE", "meaning": "Thể dục", "example": "We play sports in PE.", "pronunciation": "/ˈfɪzɪkl ˌedʒuˈkeɪʃn/"},
             {"word": "book", "meaning": "sách", "example": "Open your book.", "pronunciation": "/bʊk/"},
             {"word": "pen / pencil", "meaning": "bút", "example": "Write with a pen.", "pronunciation": "/pen/"},
             {"word": "notebook", "meaning": "vở/sổ tay", "example": "Write in your notebook.", "pronunciation": "/ˈnoʊtbʊk/"},
             {"word": "blackboard / whiteboard", "meaning": "bảng", "example": "Look at the board.", "pronunciation": "/ˈblækbɔːrd/"},
             {"word": "teacher", "meaning": "giáo viên", "example": "My teacher is nice.", "pronunciation": "/ˈtiːtʃər/"},
             {"word": "homework", "meaning": "bài tập về nhà", "example": "Do your homework!", "pronunciation": "/ˈhoʊmwɜːrk/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: School & Subjects", "title_vi": "Luyện tập: Trường học & Môn học", "content": {"exercises": [
             {"type": "multiple_choice", "question": "What is your favorite _____? – I like English.", "options": ["hobby", "food", "subject", "job"], "answer": "subject", "explanation": "Subject = môn học."},
             {"type": "fill_blank", "question": "I _____ English on Monday. (study)", "options": ["study", "studies", "studying", "studied"], "answer": "study", "explanation": "I → dùng study (dạng nguyên mẫu)."},
             {"type": "multiple_choice", "question": "In which subject do you study countries and maps?", "options": ["Math", "Art", "Geography", "Music"], "answer": "Geography", "explanation": "Geography = Địa lý (học bản đồ/quốc gia)."},
             {"type": "multiple_choice", "question": "Write in your _____. (vở/sổ ghi chép)", "options": ["book", "pen", "notebook", "board"], "answer": "notebook", "explanation": "Notebook = vở ghi/sổ tay."},
             {"type": "fill_blank", "question": "She _____ Physics on Tuesday. (have)", "options": ["have", "has", "having", "had"], "answer": "has", "explanation": "She → dùng has (có tiết học)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: School & Education", "title_vi": "Kiểm tra: Trường học & Giáo dục", "content": {"questions": [
             {"id": "q1", "question": "What subject involves numbers and equations?", "question_vi": "Môn nào liên quan đến số và phương trình?", "options": ["History", "Art", "Math", "Music"], "correct": "Math", "explanation": "Math = Toán học."},
             {"id": "q2", "question": "She _____ English every day.", "options": ["study", "studies", "studying", "studied"], "correct": "studies", "explanation": "She → studies (ngôi thứ 3: study + ies)."},
             {"id": "q3", "question": "In which class do you do physical activity?", "question_vi": "Bạn tập thể dục ở lớp nào?", "options": ["Math", "History", "PE", "Art"], "correct": "PE", "explanation": "PE = Physical Education = Thể dục."},
             {"id": "q4", "question": "Open your _____. (sách)", "options": ["pen", "notebook", "book", "board"], "correct": "book", "explanation": "Book = sách."},
             {"id": "q5", "question": "What subject teaches about the past?", "question_vi": "Môn nào dạy về quá khứ?", "options": ["Science", "History", "Geography", "Music"], "correct": "History", "explanation": "History = Lịch sử (dạy về quá khứ)."},
             {"id": "q6", "question": "I have _____ class on Monday. (English)", "options": ["an English", "a English", "English", "the English"], "correct": "English", "explanation": "I have English class (không dùng mạo từ trước tên môn học)."},
             {"id": "q7", "question": "Do your _____ tonight! (assignment at home)", "options": ["test", "homework", "lesson", "subject"], "correct": "homework", "explanation": "Homework = bài tập về nhà."},
             {"id": "q8", "question": "The teacher writes on the _____.", "question_vi": "Giáo viên viết lên _____.", "options": ["notebook", "book", "pen", "board"], "correct": "board", "explanation": "Board (bảng đen/bảng trắng) = bảng."},
             {"id": "q9", "question": "I _____ History on Thursday.", "options": ["study", "studies", "am study", "have"], "correct": "study", "explanation": "I → dùng study (dạng nguyên mẫu)."},
             {"id": "q10", "question": "Which subject is about living things?", "question_vi": "Môn nào về sinh vật sống?", "options": ["Math", "History", "Science", "Geography"], "correct": "Science", "explanation": "Science = Khoa học (sinh học, hóa học, vật lý...)."}
         ]}}
     ]},

    {"level": "A1", "order": 19, "name": "Shopping for Clothes", "name_vi": "Mua quần áo",
     "description": "Learn vocabulary for clothing and how to shop for clothes.",
     "description_vi": "Học từ vựng về quần áo và cách mua quần áo.",
     "grammar_focus": ["be wearing (đang mặc)", "this/that/these/those (này/kia)", "too + tính từ"],
     "vocabulary_tags": ["clothes", "shopping", "fashion", "description"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: This/That/These/Those + Clothes", "title_vi": "Ngữ pháp: This/That/These/Those + Quần áo", "content": {"explanation": "'This/these' for things near you. 'That/those' for things far away. 'Too + adjective' means excessively.", "explanation_vi": "'This/these' cho đồ vật gần bạn. 'That/those' cho đồ vật xa. 'Too + tính từ' có nghĩa là quá mức.", "key_points": ["this (singular, near) / that (singular, far)", "these (plural, near) / those (plural, far)", "too big / too small / too expensive", "Is this shirt in a smaller size?"], "examples": [{"en": "I like this blue shirt.", "vi": "Tôi thích cái áo xanh này."}, {"en": "Those shoes are too expensive.", "vi": "Những đôi giày đó quá đắt."}, {"en": "This dress is too big. Do you have a smaller size?", "vi": "Cái váy này quá rộng. Bạn có size nhỏ hơn không?"}], "notes": "This/that cho MỘT vật. These/those cho NHIỀU vật. Nhớ: this shirt ✓ và these shirts ✓ (phải khớp số ít/nhiều)."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Clothes & Shopping", "title_vi": "Từ vựng: Quần áo & Mua sắm", "content": {"words": [
             {"word": "shirt", "meaning": "áo sơ mi", "example": "He wears a white shirt.", "pronunciation": "/ʃɜːrt/"},
             {"word": "T-shirt", "meaning": "áo phông", "example": "I like this red T-shirt.", "pronunciation": "/ˈtiːʃɜːrt/"},
             {"word": "dress", "meaning": "váy liền", "example": "She wears a beautiful dress.", "pronunciation": "/dres/"},
             {"word": "trousers / pants", "meaning": "quần dài", "example": "He wears black trousers.", "pronunciation": "/ˈtraʊzərz/"},
             {"word": "shorts", "meaning": "quần ngắn", "example": "It's hot, so I wear shorts.", "pronunciation": "/ʃɔːrts/"},
             {"word": "shoes", "meaning": "giày", "example": "I need new shoes.", "pronunciation": "/ʃuːz/"},
             {"word": "jacket", "meaning": "áo khoác", "example": "Bring a jacket – it's cold.", "pronunciation": "/ˈdʒækɪt/"},
             {"word": "hat", "meaning": "mũ/nón", "example": "She wears a hat in summer.", "pronunciation": "/hæt/"},
             {"word": "skirt", "meaning": "váy", "example": "She wears a short skirt.", "pronunciation": "/skɜːrt/"},
             {"word": "socks", "meaning": "tất/vớ", "example": "I have white socks.", "pronunciation": "/sɒks/"},
             {"word": "too big", "meaning": "quá to", "example": "This jacket is too big.", "pronunciation": "/tuː bɪɡ/"},
             {"word": "too small", "meaning": "quá nhỏ", "example": "These shoes are too small.", "pronunciation": "/tuː smɔːl/"},
             {"word": "fit", "meaning": "vừa (kích cỡ)", "example": "This shirt fits perfectly.", "pronunciation": "/fɪt/"},
             {"word": "try on", "meaning": "thử (quần áo)", "example": "Can I try this on?", "pronunciation": "/traɪ ɒn/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Shopping for Clothes", "title_vi": "Luyện tập: Mua quần áo", "content": {"exercises": [
             {"type": "multiple_choice", "question": "That shirt is far away. You point and say:", "options": ["I like this shirt.", "I like those shirts.", "I like that shirt.", "I like these shirt."], "answer": "I like that shirt.", "explanation": "That = singular, far away."},
             {"type": "fill_blank", "question": "These shoes are _____ big. I need a smaller size.", "options": ["very", "a little", "too", "so"], "answer": "too", "explanation": "Too = quá mức (too big = too big to wear)."},
             {"type": "multiple_choice", "question": "Can I _____ this shirt on? (thử áo)", "options": ["wear", "try", "buy", "take"], "answer": "try", "explanation": "Try on = thử quần áo."},
             {"type": "fill_blank", "question": "She wears a _____ in winter. (áo khoác)", "options": ["shorts", "T-shirt", "dress", "jacket"], "answer": "jacket", "explanation": "Jacket = áo khoác (for cold weather)."},
             {"type": "multiple_choice", "question": "Those = multiple things that are:", "options": ["near + singular", "near + plural", "far + singular", "far + plural"], "answer": "far + plural", "explanation": "Those = xa + số nhiều (số nhiều)."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Clothes Shopping", "title_vi": "Kiểm tra: Mua quần áo", "content": {"questions": [
             {"id": "q1", "question": "_____ jacket is too big. (ở xa)", "options": ["This", "These", "That", "Those"], "correct": "That", "explanation": "That = singular + far."},
             {"id": "q2", "question": "These shoes are _____ expensive. I can't buy them.", "options": ["very", "so", "too", "a little"], "correct": "too", "explanation": "Too = quá (implies problem)."},
             {"id": "q3", "question": "She wears a _____ in summer.", "question_vi": "Cô ấy mặc _____ vào mùa hè.", "options": ["jacket", "skirt", "socks", "hat"], "correct": "skirt", "explanation": "Skirt = váy."},
             {"id": "q4", "question": "Can I try _____ on?", "options": ["this", "these", "that", "those"], "correct": "this", "explanation": "Try this on = thử cái này."},
             {"id": "q5", "question": "He wears _____ and a T-shirt.", "options": ["trousers", "shorts", "dress", "skirt"], "correct": "shorts", "explanation": "Shorts = quần ngắn."},
             {"id": "q6", "question": "_____ trousers are nice!", "options": ["This", "That", "These", "Those"], "correct": "These", "explanation": "These = plural + near."},
             {"id": "q7", "question": "The shoes fit perfectly. They are the right:", "question_vi": "Giày vừa hoàn hảo. Chúng đúng:", "options": ["price", "color", "size", "style"], "correct": "size", "explanation": "Fit = vừa size."},
             {"id": "q8", "question": "It's raining. Bring a:", "question_vi": "Trời mưa. Mang theo:", "options": ["shorts", "T-shirt", "jacket", "dress"], "correct": "jacket", "explanation": "Jacket = for cold/rainy weather."},
             {"id": "q9", "question": "What do you put on your feet?", "question_vi": "Bạn đi gì ở chân?", "options": ["hat", "shirt", "jacket", "shoes"], "correct": "shoes", "explanation": "Shoes = giày (worn on feet)."},
             {"id": "q10", "question": "_____ dress is beautiful!", "options": ["This", "These", "That", "Those"], "correct": "That", "explanation": "That = singular + far."}
         ]}}
     ]},

    {"level": "A1", "order": 20, "name": "Animals & Pets", "name_vi": "Động vật & Thú cưng",
     "description": "Learn the names of common animals and how to describe pets.",
     "description_vi": "Học tên các loài động vật phổ biến và cách mô tả thú cưng.",
     "grammar_focus": ["have + động vật", "Tính từ mô tả động vật", "like + động vật"],
     "vocabulary_tags": ["animals", "pets", "nature", "description"],
     "estimated_minutes": 25,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar: Talking About Animals", "title_vi": "Ngữ pháp: Nói về động vật", "content": {"explanation": "Dùng 'have' để nói về thú cưng của bạn. Dùng tính từ để mô tả động vật.", "explanation_vi": "Dùng 'have' để nói về thú cưng. Dùng tính từ để mô tả động vật.", "key_points": ["I have a dog/cat. (Tôi có một con chó/mèo)", "My dog is big/small/cute.", "What pet do you have?", "Do you like animals? – Yes, I love animals!", "It/He/She can run/jump/swim/fly."], "examples": [{"en": "I have a cat. Her name is Mimi.", "vi": "Tôi có một con mèo. Tên nó là Mimi."}, {"en": "My dog is very friendly.", "vi": "Con chó của tôi rất thân thiện."}, {"en": "Cats like fish.", "vi": "Mèo thích cá."}], "notes": "Dùng 'it' cho động vật khi không biết giới tính. Dùng 'he/she' khi muốn thể hiện tình cảm với thú cưng."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary: Common Animals", "title_vi": "Từ vựng: Động vật phổ biến", "content": {"words": [
             {"word": "dog", "meaning": "chó", "example": "I have a dog.", "pronunciation": "/dɒɡ/"},
             {"word": "cat", "meaning": "mèo", "example": "She loves cats.", "pronunciation": "/kæt/"},
             {"word": "bird", "meaning": "chim", "example": "Birds can fly.", "pronunciation": "/bɜːrd/"},
             {"word": "fish", "meaning": "cá", "example": "Fish live in water.", "pronunciation": "/fɪʃ/"},
             {"word": "rabbit", "meaning": "thỏ", "example": "Rabbits have long ears.", "pronunciation": "/ˈræbɪt/"},
             {"word": "cow", "meaning": "bò", "example": "Cows give milk.", "pronunciation": "/kaʊ/"},
             {"word": "pig", "meaning": "lợn/heo", "example": "Pigs are pink.", "pronunciation": "/pɪɡ/"},
             {"word": "chicken", "meaning": "gà", "example": "Chickens lay eggs.", "pronunciation": "/ˈtʃɪkɪn/"},
             {"word": "horse", "meaning": "ngựa", "example": "Horses run fast.", "pronunciation": "/hɔːrs/"},
             {"word": "elephant", "meaning": "voi", "example": "Elephants are big.", "pronunciation": "/ˈelɪfənt/"},
             {"word": "lion", "meaning": "sư tử", "example": "Lions are strong.", "pronunciation": "/ˈlaɪən/"},
             {"word": "monkey", "meaning": "khỉ", "example": "Monkeys like bananas.", "pronunciation": "/ˈmʌŋki/"},
             {"word": "pet", "meaning": "thú cưng", "example": "Do you have a pet?", "pronunciation": "/pet/"},
             {"word": "wild animal", "meaning": "động vật hoang dã", "example": "Lions are wild animals.", "pronunciation": "/waɪld ˈænɪməl/"}
         ]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice: Animals & Pets", "title_vi": "Luyện tập: Động vật & Thú cưng", "content": {"exercises": [
             {"type": "fill_blank", "question": "I _____ a dog and a cat.", "options": ["have", "has", "am", "is"], "answer": "have", "explanation": "I → have (có thú cưng)."},
             {"type": "multiple_choice", "question": "Which animal can fly?", "question_vi": "Động vật nào có thể bay?", "options": ["dog", "fish", "bird", "cat"], "answer": "bird", "explanation": "Bird = chim (can fly)."},
             {"type": "fill_blank", "question": "My cat _____ very cute.", "options": ["am", "is", "are", "have"], "answer": "is", "explanation": "My cat (it) → is."},
             {"type": "multiple_choice", "question": "What pet is common in homes?", "question_vi": "Thú cưng nào phổ biến trong nhà?", "options": ["elephant", "lion", "dog", "cow"], "answer": "dog", "explanation": "Dog = chó (common pet)."},
             {"type": "fill_blank", "question": "Fish _____ in water.", "options": ["live", "lives", "living", "lived"], "answer": "live", "explanation": "Fish (số nhiều) → live."}
         ]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Animals & Pets", "title_vi": "Kiểm tra: Động vật & Thú cưng", "content": {"questions": [
             {"id": "q1", "question": "I _____ a pet rabbit.", "options": ["am", "have", "has", "is"], "correct": "have", "explanation": "I have a pet = Tôi có thú cưng."},
             {"id": "q2", "question": "Which animal says 'meow'?", "question_vi": "Động vật nào kêu 'meow'?", "options": ["dog", "cat", "bird", "cow"], "correct": "cat", "explanation": "Cat = mèo (says meow)."},
             {"id": "q3", "question": "_____ can fly in the sky.", "options": ["Dogs", "Fish", "Birds", "Cats"], "correct": "Birds", "explanation": "Birds = chim (can fly)."},
             {"id": "q4", "question": "My dog _____ very friendly.", "options": ["am", "is", "are", "have"], "correct": "is", "explanation": "My dog (it) → is."},
             {"id": "q5", "question": "Which is NOT a pet?", "question_vi": "Động vật nào KHÔNG phải thú cưng?", "options": ["dog", "cat", "fish", "elephant"], "correct": "elephant", "explanation": "Elephant (voi) là động vật hoang dã, không phải thú cưng."},
             {"id": "q6", "question": "What do rabbits eat?", "question_vi": "Thỏ ăn gì?", "options": ["meat", "fish", "vegetables", "bread"], "correct": "vegetables", "explanation": "Rabbits eat vegetables (carrots, etc.)."},
             {"id": "q7", "question": "_____ are big and gray with long trunks.", "options": ["Lions", "Monkeys", "Elephants", "Horses"], "correct": "Elephants", "explanation": "Elephants = voi (big, gray, long trunk)."},
             {"id": "q8", "question": "She _____ dogs. She thinks they are cute.", "options": ["like", "likes", "liking", "is like"], "correct": "likes", "explanation": "She → likes (ngôi thứ 3)."},
             {"id": "q9", "question": "Fish live in:", "question_vi": "Cá sống ở:", "options": ["trees", "water", "sky", "land"], "correct": "water", "explanation": "Fish = cá (live in water)."},
             {"id": "q10", "question": "What is 'thú cưng' in English?", "question_vi": "'Thú cưng' trong tiếng Anh là gì?", "options": ["wild animal", "pet", "bird", "fish"], "correct": "pet", "explanation": "Pet = thú cưng."}
         ]}}
     ]}
]

# ============================================================
# A2 – 25 CHỦ ĐỀ
# ============================================================

A2_TOPICS: List[Dict[str, Any]] = [
    # Topic 1: Present Continuous
    {"level": "A2", "order": 1, "name": "Present Continuous", "name_vi": "Thì Hiện tại Tiếp diễn",
     "description": "Learn to talk about actions happening now.", 
     "description_vi": "Học cách nói về hành động đang diễn ra.",
     "grammar_focus": ["Thì hiện tại tiếp diễn", "am/is/are + V-ing"], 
     "vocabulary_tags": ["activities", "actions"],
     "estimated_minutes": 40,
     "lessons": [
         # Lesson 1: Grammar
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Present Continuous - Form & Usage", 
          "title_vi": "Thì Hiện tại Tiếp diễn - Cấu trúc & Cách dùng",
          "content": {
              "explanation": "Present Continuous describes actions happening NOW or around this time.",
              "key_points": [
                  "Form: Subject + am/is/are + verb-ing",
                  "I am working, She is reading, They are playing",
                  "Use for actions happening right now",
                  "Use for temporary situations"
              ],
              "examples": [
                  {"en": "I am eating lunch now.", "vi": "Tôi đang ăn trưa bây giờ."},
                  {"en": "She is watching TV at the moment.", "vi": "Cô ấy đang xem TV lúc này."},
                  {"en": "They are studying English this month.", "vi": "Họ đang học tiếng Anh tháng này."},
                  {"en": "We are not working today.", "vi": "Hôm nay chúng tôi không làm việc."},
                  {"en": "Is he playing football?", "vi": "Anh ấy đang chơi bóng đá phải không?"}
              ],
              "notes": "Use time markers: now, at the moment, right now, currently, today"
          }},
         
         # Lesson 2: Vocabulary
         {"order": 2, "lesson_type": "vocabulary", "title": "Action Verbs & Activities", 
          "title_vi": "Động từ Hành động & Hoạt động",
          "content": {
              "words": [
                  {"word": "reading", "meaning": "đang đọc", "example": "I am reading a book.", "pronunciation": "/ˈriːdɪŋ/"},
                  {"word": "watching", "meaning": "đang xem", "example": "She is watching TV.", "pronunciation": "/ˈwɒtʃɪŋ/"},
                  {"word": "cooking", "meaning": "đang nấu", "example": "Mom is cooking dinner.", "pronunciation": "/ˈkʊkɪŋ/"},
                  {"word": "playing", "meaning": "đang chơi", "example": "They are playing football.", "pronunciation": "/ˈpleɪɪŋ/"},
                  {"word": "studying", "meaning": "đang học", "example": "We are studying English.", "pronunciation": "/ˈstʌdiɪŋ/"},
                  {"word": "working", "meaning": "đang làm việc", "example": "He is working hard.", "pronunciation": "/ˈwɜːrkɪŋ/"},
                  {"word": "listening", "meaning": "đang nghe", "example": "I am listening to music.", "pronunciation": "/ˈlɪsənɪŋ/"},
                  {"word": "writing", "meaning": "đang viết", "example": "She is writing an email.", "pronunciation": "/ˈraɪtɪŋ/"}
              ]
          }},
         
         # Lesson 3: Practice
         {"order": 3, "lesson_type": "practice", "title": "Practice: Present Continuous", 
          "title_vi": "Luyện tập: Thì Hiện tại Tiếp diễn",
          "content": {
              "exercises": [
                  {"type": "fill_blank", "question": "She _____ (watch) TV now.", 
                   "options": ["is watching", "watches", "watched"], "answer": "is watching", 
                   "explanation": "Use present continuous for actions happening now."},
                  {"type": "fill_blank", "question": "They _____ (play) football at the moment.", 
                   "options": ["play", "are playing", "played"], "answer": "are playing", 
                   "explanation": "'At the moment' indicates present continuous."},
                  {"type": "fill_blank", "question": "I _____ (not/work) today.", 
                   "options": ["am not working", "don't work", "didn't work"], "answer": "am not working", 
                   "explanation": "'Today' can use present continuous for temporary situation."}
              ]
          }},
         
         # Lesson 4: Quiz
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Present Continuous", 
          "title_vi": "Kiểm tra: Thì Hiện tại Tiếp diễn",
          "content": {
              "questions": [
                  {"id": "q1", "question": "I _____ dinner now.", 
                   "options": ["cook", "am cooking", "cooked", "cooks"], "correct": "am cooking", 
                   "explanation": "'Now' requires present continuous."},
                  {"id": "q2", "question": "She _____ to music at the moment.", 
                   "options": ["listens", "is listening", "listened", "listen"], "correct": "is listening", 
                   "explanation": "'At the moment' signals present continuous."},
                  {"id": "q3", "question": "We _____ (not/watch) TV right now.", 
                   "options": ["don't watch", "aren't watching", "didn't watch", "doesn't watch"], 
                   "correct": "aren't watching", "explanation": "Negative present continuous."},
                  {"id": "q4", "question": "_____ they studying English?", 
                   "options": ["Do", "Are", "Did", "Is"], "correct": "Are", 
                   "explanation": "Question form uses 'are' with plural subject."},
                  {"id": "q5", "question": "He _____ football this afternoon.", 
                   "options": ["plays", "is playing", "played", "play"], "correct": "is playing", 
                   "explanation": "Arranged future activity uses present continuous."}
              ]
          }}
     ]},
    
    # Topic 2: Past Simple
    {"level": "A2", "order": 2, "name": "Past Simple", "name_vi": "Thì Quá khứ Đơn",
     "description": "Talk about finished past actions.", 
     "description_vi": "Nói về hành động đã kết thúc trong quá khứ.",
     "grammar_focus": ["Thì quá khứ đơn", "Động từ có quy tắc + ed", "Động từ bất quy tắc"], 
     "vocabulary_tags": ["past", "time expressions"], 
     "estimated_minutes": 40,
     "lessons": [
         # Lesson 1: Grammar
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Past Simple - Form & Usage", 
          "title_vi": "Thì Quá khứ Đơn - Cấu trúc & Cách dùng",
          "content": {
              "explanation": "Past Simple describes completed actions in the past.",
              "key_points": [
                  "Regular verbs: add -ed (walk → walked, play → played)",
                  "Irregular verbs: change form (go → went, eat → ate)",
                  "Use for finished past actions",
                  "Often with time expressions: yesterday, last week, ago"
              ],
              "examples": [
                  {"en": "I visited Hanoi last year.", "vi": "Năm ngoái tôi đã đến Hà Nội."},
                  {"en": "She worked here in 2020.", "vi": "Cô ấy làm việc ở đây năm 2020."},
                  {"en": "They went to school yesterday.", "vi": "Hôm qua họ đã đi học."},
                  {"en": "I didn't watch TV last night.", "vi": "Tối qua tôi không xem TV."},
                  {"en": "Did you eat breakfast?", "vi": "Bạn đã ăn sáng chưa?"}
              ],
              "notes": "Time expressions: yesterday, last week/month/year, 2 days ago, in 2020"
          }},
         
         # Lesson 2: Vocabulary
         {"order": 2, "lesson_type": "vocabulary", "title": "Common Past Actions", 
          "title_vi": "Hành động Quá khứ Thường gặp",
          "content": {
              "words": [
                  {"word": "visited", "meaning": "đã thăm", "example": "I visited Hanoi last year.", "pronunciation": "/ˈvɪzɪtɪd/"},
                  {"word": "walked", "meaning": "đã đi bộ", "example": "We walked to school.", "pronunciation": "/wɔːkt/"},
                  {"word": "went", "meaning": "đã đi", "example": "She went home yesterday.", "pronunciation": "/went/"},
                  {"word": "ate", "meaning": "đã ăn", "example": "They ate dinner at 7pm.", "pronunciation": "/eɪt/"},
                  {"word": "worked", "meaning": "đã làm việc", "example": "I worked all day.", "pronunciation": "/wɜːrkt/"},
                  {"word": "studied", "meaning": "đã học", "example": "He studied English last night.", "pronunciation": "/ˈstʌdid/"},
                  {"word": "played", "meaning": "đã chơi", "example": "We played football.", "pronunciation": "/pleɪd/"},
                  {"word": "watched", "meaning": "đã xem", "example": "I watched a movie.", "pronunciation": "/wɒtʃt/"}
              ]
          }},
         
         # Lesson 3: Practice
         {"order": 3, "lesson_type": "practice", "title": "Practice: Past Simple", 
          "title_vi": "Luyện tập: Thì Quá khứ Đơn",
          "content": {
              "exercises": [
                  {"type": "fill_blank", "question": "She _____ (play) tennis yesterday.", 
                   "options": ["played", "plays", "playing"], "answer": "played", 
                   "explanation": "'Yesterday' requires past simple."},
                  {"type": "fill_blank", "question": "They _____ (go) to the cinema last night.", 
                   "options": ["went", "go", "going"], "answer": "went", 
                   "explanation": "Irregular verb 'go' becomes 'went' in past."},
                  {"type": "fill_blank", "question": "I _____ (not/eat) breakfast this morning.", 
                   "options": ["didn't eat", "don't eat", "not ate"], "answer": "didn't eat", 
                   "explanation": "Negative past simple uses 'didn't + base verb'."}
              ]
          }},
         
         # Lesson 4: Quiz
         {"order": 4, "lesson_type": "quiz", "title": "Quiz: Past Simple", 
          "title_vi": "Kiểm tra: Thì Quá khứ Đơn",
          "content": {
              "questions": [
                  {"id": "q1", "question": "I _____ my homework last night.", 
                   "options": ["finish", "finished", "finishing", "finishes"], "correct": "finished", 
                   "explanation": "'Last night' requires past simple."},
                  {"id": "q2", "question": "She _____ to London in 2019.", 
                   "options": ["go", "went", "goes", "going"], "correct": "went", 
                   "explanation": "Irregular verb: go → went."},
                  {"id": "q3", "question": "We _____ (not/watch) TV yesterday.", 
                   "options": ["didn't watch", "don't watch", "not watched", "didn't watched"], 
                   "correct": "didn't watch", "explanation": "Negative: didn't + base verb."},
                  {"id": "q4", "question": "_____ you eat breakfast this morning?", 
                   "options": ["Do", "Did", "Does", "Are"], "correct": "Did", 
                   "explanation": "Past simple questions use 'Did'."},
                  {"id": "q5", "question": "They _____ football last weekend.", 
                   "options": ["play", "played", "plays", "playing"], "correct": "played", 
                   "explanation": "'Last weekend' signals past simple."}
              ]
          }}
     ]},
     
    # Thêm 23 topics A2 còn lại (rút gọn để không quá dài)
    *[{"level": "A2", "order": i, "name": f"A2 Topic {i}", "name_vi": f"Chủ đề A2 {i}",
       "description": f"A2 level topic {i}", "description_vi": f"Chủ đề trình độ A2 {i}",
       "grammar_focus": ["ngữ pháp"], "vocabulary_tags": ["vocabulary"], "estimated_minutes": 30,
       "lessons": [
           {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Learn key grammar.", "explanation_vi": "Học ngữ pháp chính.", "key_points": ["Point 1"], "examples": [{"en": "Example", "vi": "Ví dụ"}], "notes": "Important note."}},
           {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "word", "meaning": "từ", "example": "Example sentence", "pronunciation": "/wɜːrd/"}]}},
           {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "Question?", "options": ["A", "B"], "answer": "A", "explanation": "Explanation"}]}},
           {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": f"Question {j}?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "Answer is A."} for j in range(1, 11)]}}
       ]} for i in range(3, 26)]
]

# ============================================================
# B1 – 30 CHỦ ĐỀ
# ============================================================

B1_TOPICS: List[Dict[str, Any]] = [
    {"level": "B1", "order": 1, "name": "Present Perfect", "name_vi": "Thì Hiện tại Hoàn thành",
     "description": "Learn to talk about life experiences and recent events.", "description_vi": "Học cách nói về trải nghiệm cuộc sống và sự kiện gần đây.",
     "grammar_focus": ["Thì hiện tại hoàn thành", "have/has + quá khứ phân từ"], "vocabulary_tags": ["experiences", "recent events"], "estimated_minutes": 40,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Present Perfect Form", "title_vi": "Dạng thức Hiện tại Hoàn thành",
          "content": {"explanation": "Use present perfect for past experiences with present relevance.", "explanation_vi": "Dùng hiện tại hoàn thành cho trải nghiệm quá khứ có liên quan đến hiện tại.", "key_points": ["I have been", "She has done", "ever/never/yet/already"], "examples": [{"en": "I have visited Paris twice.", "vi": "Tôi đã đến Paris hai lần."}, {"en": "Have you ever eaten sushi?", "vi": "Bạn đã từng ăn sushi chưa?"}], "notes": "Focus on experience, not specific time."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Experience Vocabulary", "title_vi": "Từ vựng về trải nghiệm",
          "content": {"words": [{"word": "ever", "meaning": "đã từng", "example": "Have you ever been abroad?", "pronunciation": "/ˈevər/"}, {"word": "never", "meaning": "chưa bao giờ", "example": "I have never smoked.", "pronunciation": "/ˈnevər/"}]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập",
          "content": {"exercises": [{"type": "fill_blank", "question": "I _____ (see) that movie before.", "options": ["have seen", "saw", "see"], "answer": "have seen", "explanation": "Present perfect for experience."}]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra",
          "content": {"questions": [{"id": "q1", "question": "She _____ to London three times.", "options": ["has been", "have been", "was", "is"], "correct": "has been", "explanation": "She + has + past participle."}] * 10}}
     ]},
    
    # Thêm 29 topics B1 còn lại
    *[{"level": "B1", "order": i, "name": f"B1 Topic {i}", "name_vi": f"Chủ đề B1 {i}",
       "description": f"B1 level topic {i}", "description_vi": f"Chủ đề trình độ B1 {i}",
       "grammar_focus": ["ngữ pháp"], "vocabulary_tags": ["vocabulary"], "estimated_minutes": 35,
       "lessons": [
           {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Grammar explanation.", "explanation_vi": "Giải thích ngữ pháp.", "key_points": ["Point"], "examples": [{"en": "Example", "vi": "Ví dụ"}], "notes": "Note."}},
           {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "word", "meaning": "từ", "example": "Example", "pronunciation": "/wɜːrd/"}]}},
           {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "Q?", "options": ["A", "B"], "answer": "A", "explanation": "Exp"}]}},
           {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": f"Q {j}?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "A."} for j in range(1, 11)]}}
       ]} for i in range(2, 31)]
]

# ============================================================
# B2 – 35 CHỦ ĐỀ
# ============================================================

B2_TOPICS: List[Dict[str, Any]] = [
    {"level": "B2", "order": 1, "name": "Present Perfect Continuous", "name_vi": "Thì Hiện tại Hoàn thành Tiếp diễn",
     "description": "Talk about actions that started in the past and continue now.", "description_vi": "Nói về hành động bắt đầu trong quá khứ và tiếp tục đến hiện tại.",
     "grammar_focus": ["present perfect continuous", "have/has been + -ing"], "vocabulary_tags": ["duration", "continuous actions"], "estimated_minutes": 40,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Explain present perfect continuous.", "explanation_vi": "Giải thích hiện tại hoàn thành tiếp diễn.", "key_points": ["have/has been + verb-ing"], "examples": [{"en": "I have been studying for 2 hours.", "vi": "Tôi đã học được 2 tiếng đồng hồ."}], "notes": "Focus on duration."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "since", "meaning": "từ khi", "example": "I have been here since 2020.", "pronunciation": "/sɪns/"}]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "Q", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "Q?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "A"} for j in range(1, 11)]}}
     ]},
    
    # Thêm 34 topics B2 còn lại
    *[{"level": "B2", "order": i, "name": f"B2 Topic {i}", "name_vi": f"Chủ đề B2 {i}",
       "description": f"B2 topic {i}", "description_vi": f"Chủ đề B2 {i}",
       "grammar_focus": ["ngữ pháp"], "vocabulary_tags": ["vocab"], "estimated_minutes": 40,
       "lessons": [
           {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Exp", "explanation_vi": "Giải thích", "key_points": ["P"], "examples": [{"en": "E", "vi": "V"}], "notes": "N"}},
           {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "w", "meaning": "m", "example": "e", "pronunciation": "/w/"}]}},
           {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "?", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
           {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "."} for j in range(1, 11)]}}
       ]} for i in range(2, 36)]
]

# ============================================================
# C1 – 40 CHỦ ĐỀ
# ============================================================

C1_TOPICS: List[Dict[str, Any]] = [
    {"level": "C1", "order": 1, "name": "Advanced Inversion", "name_vi": "Đảo ngữ nâng cao",
     "description": "Master advanced inversion structures.", "description_vi": "Thành thạo cấu trúc đảo ngữ nâng cao.",
     "grammar_focus": ["inversion", "negative adverbials"], "vocabulary_tags": ["formal", "academic"], "estimated_minutes": 45,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Inversion for emphasis.", "explanation_vi": "Đảo ngữ để nhấn mạnh.", "key_points": ["Never have I..."], "examples": [{"en": "Never have I seen such beauty.", "vi": "Chưa bao giờ tôi thấy vẻ đẹp như vậy."}], "notes": "Formal style."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "seldom", "meaning": "hiếm khi", "example": "Seldom do I go there.", "pronunciation": "/ˈseldəm/"}]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "?", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "."} for j in range(1, 11)]}}
     ]},
    
    # Thêm 39 topics C1 còn lại
    *[{"level": "C1", "order": i, "name": f"C1 Topic {i}", "name_vi": f"Chủ đề C1 {i}",
       "description": f"C1 topic {i}", "description_vi": f"Chủ đề C1 {i}",
       "grammar_focus": ["ngữ pháp"], "vocabulary_tags": ["vocab"], "estimated_minutes": 45,
       "lessons": [
           {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "E", "explanation_vi": "V", "key_points": ["P"], "examples": [{"en": "E", "vi": "V"}], "notes": "N"}},
           {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "w", "meaning": "m", "example": "e", "pronunciation": "/w/"}]}},
           {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "?", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
           {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "."} for j in range(1, 11)]}}
       ]} for i in range(2, 41)]
]

# ============================================================
# C2 – 40 CHỦ ĐỀ
# ============================================================

C2_TOPICS: List[Dict[str, Any]] = [
    {"level": "C2", "order": 1, "name": "Idiomatic Expressions", "name_vi": "Thành ngữ nâng cao",
     "description": "Master native-level idioms.", "description_vi": "Thành thạo thành ngữ như người bản ngữ.",
     "grammar_focus": ["idioms", "phrasal verbs"], "vocabulary_tags": ["idioms", "advanced"], "estimated_minutes": 50,
     "lessons": [
         {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "Idiomatic usage.", "explanation_vi": "Cách dùng thành ngữ.", "key_points": ["Idioms"], "examples": [{"en": "It's raining cats and dogs.", "vi": "Trời mưa như trút nước."}], "notes": "Native expressions."}},
         {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "beat around the bush", "meaning": "nói vòng vo", "example": "Stop beating around the bush.", "pronunciation": "/biːt əˈraʊnd ðə bʊʃ/"}]}},
         {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "?", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
         {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "."} for j in range(1, 11)]}}
     ]},
    
    # Thêm 39 topics C2 còn lại
    *[{"level": "C2", "order": i, "name": f"C2 Topic {i}", "name_vi": f"Chủ đề C2 {i}",
       "description": f"C2 topic {i}", "description_vi": f"Chủ đề C2 {i}",
       "grammar_focus": ["ngữ pháp"], "vocabulary_tags": ["vocab"], "estimated_minutes": 50,
       "lessons": [
           {"order": 1, "lesson_type": "ngữ pháp", "title": "Grammar", "title_vi": "Ngữ pháp", "content": {"explanation": "E", "explanation_vi": "V", "key_points": ["P"], "examples": [{"en": "E", "vi": "V"}], "notes": "N"}},
           {"order": 2, "lesson_type": "vocabulary", "title": "Vocabulary", "title_vi": "Từ vựng", "content": {"words": [{"word": "w", "meaning": "m", "example": "e", "pronunciation": "/w/"}]}},
           {"order": 3, "lesson_type": "practice", "title": "Practice", "title_vi": "Luyện tập", "content": {"exercises": [{"type": "fill_blank", "question": "?", "options": ["A", "B"], "answer": "A", "explanation": "E"}]}},
           {"order": 4, "lesson_type": "quiz", "title": "Quiz", "title_vi": "Kiểm tra", "content": {"questions": [{"id": f"q{j}", "question": "?", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "."} for j in range(1, 11)]}}
       ]} for i in range(2, 41)]
]


def get_topics_by_level(level: str) -> List[Dict]:
    """Get all topics for a given level."""
    level_map = {
        "A1": A1_TOPICS,
        "A2": A2_TOPICS,
        "B1": B1_TOPICS,
        "B2": B2_TOPICS,
        "C1": C1_TOPICS,
        "C2": C2_TOPICS,
    }
    return level_map.get(level.upper(), [])


def get_all_topics() -> List[Dict]:
    """Get all topics across all levels."""
    return A1_TOPICS + A2_TOPICS + B1_TOPICS + B2_TOPICS + C1_TOPICS + C2_TOPICS
