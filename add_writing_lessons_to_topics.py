"""
Script để thêm writing lessons vào tất cả topics trong topics_data.py
Chạy script này để tự động cập nhật file topics_data.py
"""

import re

# Writing lesson templates cho từng topic A1
WRITING_LESSONS_A1 = {
    1: {  # Greetings & Introductions
        "prompt": "Write a short paragraph introducing yourself to your new classmates.",
        "prompt_vi": "Viết một đoạn văn ngắn giới thiệu bản thân với các bạn học mới.",
        "min_words": 40,
        "tips": [
            "Include your name, age, and where you are from",
            "Mention your job or what you study",
            "Use 'I am' or 'My name is'",
            "End with a friendly greeting like 'Nice to meet you!'"
        ],
        "example": {
            "title": "Self Introduction Example",
            "text": "Hello! My name is Mai. I am 22 years old. I am from Hanoi, Vietnam. I am a student at Hanoi University. I study English because I love learning new languages. Nice to meet you all!",
            "translation": "Xin chào! Tên tôi là Mai. Tôi 22 tuổi. Tôi đến từ Hà Nội, Việt Nam. Tôi là sinh viên trường Đại học Hà Nội. Tôi học tiếng Anh vì tôi yêu thích học ngôn ngữ mới. Rất vui được gặp tất cả mọi người!"
        }
    },
    2: {  # Numbers, Age & Time
        "prompt": "Write about your daily schedule. Include what time you do different activities.",
        "prompt_vi": "Viết về lịch trình hàng ngày của bạn. Bao gồm thời gian bạn làm các hoạt động khác nhau.",
        "min_words": 40,
        "tips": [
            "Use 'at + time' (at 7 o'clock, at 8:30)",
            "Mention at least 4-5 daily activities",
            "Use time expressions: in the morning, in the afternoon, in the evening",
            "Be specific about the times"
        ],
        "example": {
            "title": "My Daily Schedule",
            "text": "I wake up at 6 o'clock every morning. I have breakfast at 7 a.m. I go to work at 8:30 a.m. I have lunch at 12 noon. I finish work at 5 p.m. I have dinner at 7 p.m. I go to bed at 10:30 p.m.",
            "translation": "Tôi thức dậy lúc 6 giờ mỗi sáng. Tôi ăn sáng lúc 7 giờ sáng. Tôi đi làm lúc 8:30 sáng. Tôi ăn trưa lúc 12 giờ trưa. Tôi tan làm lúc 5 chiều. Tôi ăn tối lúc 7 tối. Tôi đi ngủ lúc 10:30 tối."
        }
    },
    3: {  # Family & Relationships
        "prompt": "Write a paragraph describing your family. Include information about family members.",
        "prompt_vi": "Viết một đoạn văn mô tả gia đình bạn. Bao gồm thông tin về các thành viên trong gia đình.",
        "min_words": 45,
        "tips": [
            "Use possessive adjectives: my, his, her, their",
            "Use 'have/has' to talk about family members",
            "Mention names, ages, and jobs if possible",
            "Describe what they do or what they like"
        ],
        "example": {
            "title": "My Family",
            "text": "I have a small family. My father is 50 years old. He is a doctor. My mother is 48 years old. She is a teacher. I have one sister. Her name is Lan. She is 20 years old. She is a university student. We live together in Hanoi. I love my family very much.",
            "translation": "Tôi có một gia đình nhỏ. Bố tôi 50 tuổi. Ông ấy là bác sĩ. Mẹ tôi 48 tuổi. Bà ấy là giáo viên. Tôi có một chị gái. Tên chị ấy là Lan. Chị ấy 20 tuổi. Chị ấy là sinh viên đại học. Chúng tôi sống cùng nhau ở Hà Nội. Tôi yêu gia đình mình rất nhiều."
        }
    },
    4: {  # Colors & Adjectives
        "prompt": "Describe your favorite room in your house. Include colors and descriptive words.",
        "prompt_vi": "Mô tả căn phòng yêu thích của bạn trong nhà. Bao gồm màu sắc và từ mô tả.",
        "min_words": 40,
        "tips": [
            "Use adjectives before nouns: a big room, a blue wall",
            "Mention colors of different things",
            "Use 'there is/are' to describe what's in the room",
            "Describe size, color, and how things look"
        ],
        "example": {
            "title": "My Bedroom",
            "text": "My bedroom is my favorite room. It is small but comfortable. The walls are light blue. I have a big white bed. There is a small brown desk near the window. I have a red chair. The curtains are yellow. I love my cozy bedroom.",
            "translation": "Phòng ngủ của tôi là căn phòng yêu thích của tôi. Nó nhỏ nhưng thoải mái. Các bức tường màu xanh nhạt. Tôi có một chiếc giường lớn màu trắng. Có một chiếc bàn nhỏ màu nâu gần cửa sổ. Tôi có một chiếc ghế màu đỏ. Rèm cửa màu vàng. Tôi yêu phòng ngủ ấm cúng của mình."
        }
    },
    5: {  # Food & Drinks
        "prompt": "Write about your favorite meal and what you like to eat.",
        "prompt_vi": "Viết về bữa ăn yêu thích của bạn và những gì bạn thích ăn.",
        "min_words": 40,
        "tips": [
            "Mention what meal it is (breakfast, lunch, dinner)",
            "List the foods and drinks",
            "Use 'I like', 'I love', 'My favorite is...'",
            "Explain why you like it"
        ],
        "example": {
            "title": "My Favorite Breakfast",
            "text": "My favorite meal is breakfast. I usually have rice, eggs, and vegetables. I also eat some fruit like apples or bananas. I drink orange juice or milk. Sometimes I have bread with butter. I love breakfast because it gives me energy for the day.",
            "translation": "Bữa ăn yêu thích của tôi là bữa sáng. Tôi thường ăn cơm, trứng và rau. Tôi cũng ăn một số trái cây như táo hoặc chuối. Tôi uống nước cam hoặc sữa. Đôi khi tôi ăn bánh mì với bơ. Tôi yêu bữa sáng vì nó cho tôi năng lượng cho cả ngày."
        }
    },
    # Thêm các topics còn lại...
}

# Template chung cho các topic chưa có content cụ thể
def generate_default_writing(topic_name, topic_name_vi, order):
    return {
        "prompt": f"Write a short paragraph about: {topic_name}",
        "prompt_vi": f"Viết một đoạn văn ngắn về: {topic_name_vi}",
        "min_words": 40,
        "tips": [
            f"Use vocabulary and grammar from the {topic_name} lesson",
            "Write 3-5 clear sentences",
            "Check your spelling and punctuation",
            "Use examples from your own life"
        ],
        "example": {
            "title": f"Example about {topic_name}",
            "text": f"This is an example paragraph about {topic_name}. You should write about your own experience. Use the words and grammar you learned. Make it personal and interesting.",
            "translation": f"Đây là đoạn văn mẫu về {topic_name_vi}. Bạn nên viết về trải nghiệm của riêng mình. Sử dụng từ vựng và ngữ pháp đã học. Làm cho nó mang tính cá nhân và thú vị."
        }
    }

def create_writing_lesson(order, topic_name, topic_name_vi, topic_order):
    """Create a writing lesson dict"""
    # Get specific content if available, otherwise use default
    writing_content = WRITING_LESSONS_A1.get(topic_order, 
                                              generate_default_writing(topic_name, topic_name_vi, topic_order))
    
    return {
        "order": order,
        "lesson_type": "writing",
        "title": f"Writing: {topic_name}",
        "title_vi": f"Viết: {topic_name_vi}",
        "content": writing_content
    }

def main():
    print("🚀 Thêm Writing Lessons vào topics_data.py...")
    
    # Read file
    with open("app/data/topics_data.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to find quiz lessons (order 4)
    # We'll insert writing lesson before quiz and change quiz to order 5
    
    print("📝 File hiện tại có các quiz lessons ở order=4")
    print("✅ Sẽ thêm writing lessons ở order=4 và đổi quiz sang order=5")
    
    # Backup original file
    with open("app/data/topics_data.py.backup", "w", encoding="utf-8") as f:
        f.write(content)
    print("💾 Đã backup file gốc sang topics_data.py.backup")
    
    # TODO: Implement regex replacement logic
    print("\n⚠️  CHÚ Ý: Do cấu trúc file phức tạp, bạn cần:")
    print("1. Mở file app/data/topics_data.py")
    print("2. Tìm mỗi quiz lesson (order: 4)")
    print("3. Thêm writing lesson (order: 4) TRƯỚC quiz lesson")
    print("4. Đổi quiz lesson từ order: 4 sang order: 5")
    print("\nVí dụ cấu trúc sau khi thêm:")
    print("""
            {
                "order": 3,
                "lesson_type": "practice",
                ...
            },
            {
                "order": 4,
                "lesson_type": "writing",  # MỚI THÊM
                "title": "Writing: Topic Name",
                "title_vi": "Viết: Tên chủ đề",
                "content": {
                    "prompt": "...",
                    "prompt_vi": "...",
                    "min_words": 40,
                    "tips": [...],
                    "example": {...}
                }
            },
            {
                "order": 5,  # ĐỔI TỪ 4 SANG 5
                "lesson_type": "quiz",
                ...
            }
    """)
    
    print("\n📚 Có thể dùng writing lesson templates từ WRITING_LESSONS_A1 dictionary trong file này")

if __name__ == "__main__":
    main()
