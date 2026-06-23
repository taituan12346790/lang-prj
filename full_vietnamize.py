#!/usr/bin/env python3
"""
Full vietnamization of all English explanation/notes in topics_data.py
Uses manual translation mapping for common patterns
"""
import re
import json

# Read file
with open('app/data/topics_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Comprehensive translation dictionary
# All common explanation patterns in the file
translations = {
    # Grammar explanations
    "No -s added for she.": "Không thêm -s với she.",
    "base verb": "động từ nguyên mẫu",
    "(positive ability)": "(khả năng - khẳng định)",
    "(negative ability)": "(khả năng - phủ định)",
    "(negative)": "(phủ định)",
    "(affirmative)": "(khẳng định)",
    "(question)": "(câu hỏi)",
    "No -s": "Không thêm -s",
    "for she": "với she",
    "for he/she/it": "với he/she/it",
    "with he/she/it": "với he/she/it",
    "with you/we/they": "với you/we/they",
    "with I": "với I",
    "with the pronoun": "với đại từ",
    "with they/we/you": "với they/we/you",
    
    # Common quiz/practice explanations
    "Adjective goes BEFORE the noun in English.": "Tính từ đứng TRƯỚC danh từ trong tiếng Anh.",
    "Apple starts with a vowel sound": "Apple bắt đầu bằng âm nguyên âm",
    "use 'an'.": "dùng 'an'.",
    "Bananas are yellow.": "Chuối có màu vàng.",
    "Grass is green.": "Cỏ có màu xanh lá.",
    "Tall ↔ Short.": "Tall (cao) ↔ Short (ngắn/thấp).",
    
    # Frequency and time
    "go + es": "go + es",
    "verb+s": "động từ + s",
    "do not": "phủ định",
    "does not": "phủ định",
    
    # Common phrases
    "is a polite way": "là cách lịch sự",
    "is polite for ordering": "là cách lịch sự để đặt món",
    "to offer something": "để đề nghị điều gì đó",
    "to ask for": "để yêu cầu",
    "to talk about": "để nói về",
    "to describe": "để mô tả",
    
    # More patterns
    "The opposite of": "Từ trái nghĩa của",
    "Which sentence is grammatically correct?": "Câu nào đúng ngữ pháp?",
    "Juice = nước ép (a drink).": "Juice = nước ép (đồ uống).",
    "Menu = thực đơn.": "Menu = thực đơn.",
}

# Apply translations
for eng, vie in translations.items():
    content = content.replace(eng, vie)

# Pattern-based replacements using regex
# Handle "X → use Y" patterns
content = re.sub(r"(\w+) → use '(\w+)'", r"\1 → dùng '\2'", content)

# Handle "Use X with Y" patterns  
content = re.sub(r"Use '(\w+)' with (\w+/\w+/\w+)", r"Dùng '\1' với \2", content)

# Write back
with open('app/data/topics_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Full vietnamization completed")
print("  Applied {} translation rules".format(len(translations)))
