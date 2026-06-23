"""
Test question data for all CEFR levels (A1-C2) and placement test
Extracted from test_mau.txt
"""

from app.schemas.test import Level, SkillType
from typing import List, Dict

# ==================== A1 LEVEL TEST ====================
A1_TEST_QUESTIONS = [
    # Grammar Part (10 questions)
    {
        "question_id": "a1_g_1",
        "question": "I ___ a student.",
        "options": ["am", "is", "are", "be"],
        "correct_answer": "am",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_2",
        "question": "She ___ in Hanoi.",
        "options": ["live", "lives", "living", "lived"],
        "correct_answer": "lives",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_3",
        "question": "___ you like coffee?",
        "options": ["Do", "Does", "Is", "Are"],
        "correct_answer": "Do",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_4",
        "question": "They ___ TV every evening.",
        "options": ["watches", "watch", "watched", "watching"],
        "correct_answer": "watch",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_5",
        "question": "My father ___ a car.",
        "options": ["have", "has", "having", "had"],
        "correct_answer": "has",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_6",
        "question": "We ___ to school on Sundays.",
        "options": ["don't go", "doesn't go", "not go", "aren't go"],
        "correct_answer": "don't go",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_7",
        "question": "There ___ two books on the table.",
        "options": ["is", "am", "are", "be"],
        "correct_answer": "are",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_8",
        "question": "I can ___ English.",
        "options": ["speaks", "speak", "speaking", "spoke"],
        "correct_answer": "speak",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_9",
        "question": "She ___ happy today.",
        "options": ["am", "are", "is", "be"],
        "correct_answer": "is",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    {
        "question_id": "a1_g_10",
        "question": "What ___ your name?",
        "options": ["are", "is", "do", "does"],
        "correct_answer": "is",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A1
    },
    # Vocabulary Part (10 questions)
    {
        "question_id": "a1_v_1",
        "question": "A doctor works in a ___.",
        "options": ["school", "hospital", "bank", "hotel"],
        "correct_answer": "hospital",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_2",
        "question": "Which word is a colour?",
        "options": ["Blue", "Bread", "Table", "Chair"],
        "correct_answer": "Blue",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_3",
        "question": "A cat is an ___.",
        "options": ["animal", "fruit", "job", "country"],
        "correct_answer": "animal",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_4",
        "question": "Opposite of \"hot\" is:",
        "options": ["warm", "cool", "cold", "sunny"],
        "correct_answer": "cold",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_5",
        "question": "We use a ___ to write.",
        "options": ["pen", "plate", "shoe", "cup"],
        "correct_answer": "pen",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_6",
        "question": "Breakfast is eaten in the ___.",
        "options": ["afternoon", "evening", "night", "morning"],
        "correct_answer": "morning",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_7",
        "question": "How many days are there in a week?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_8",
        "question": "Which word is a fruit?",
        "options": ["Apple", "Potato", "Onion", "Carrot"],
        "correct_answer": "Apple",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_9",
        "question": "A teacher works at a ___.",
        "options": ["school", "hospital", "factory", "airport"],
        "correct_answer": "school",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    {
        "question_id": "a1_v_10",
        "question": "The opposite of \"big\" is:",
        "options": ["long", "tall", "small", "old"],
        "correct_answer": "small",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A1
    },
    # Reading Part (10 questions)
    {
        "question_id": "a1_r_1",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nHow old is Anna?",
        "options": ["20", "21", "22", "23"],
        "correct_answer": "22",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_2",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nWhere does she live?",
        "options": ["Paris", "London", "Rome", "Berlin"],
        "correct_answer": "London",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_3",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nWhere does she work?",
        "options": ["Hospital", "School", "Office", "Shop"],
        "correct_answer": "Office",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_4",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nHow does she go to work?",
        "options": ["Car", "Train", "Bike", "Bus"],
        "correct_answer": "Bus",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_5",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nWhat does she like doing after work?",
        "options": ["Swimming", "Reading books", "Cooking", "Dancing"],
        "correct_answer": "Reading books",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_6",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nWhen does she visit her friends?",
        "options": ["Monday", "Tuesday", "Weekends", "Friday"],
        "correct_answer": "Weekends",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_7",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nAnna works in a ___ office.",
        "options": ["big", "small", "new", "old"],
        "correct_answer": "small",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_8",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nAnna likes listening to ___.",
        "options": ["podcasts", "radio", "music", "news"],
        "correct_answer": "music",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_9",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nThe text is mainly about:",
        "options": ["Anna's job and daily life", "Anna's holiday", "Anna's family", "Anna's school"],
        "correct_answer": "Anna's job and daily life",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
    {
        "question_id": "a1_r_10",
        "question": "Anna is 22 years old. She lives in London. She works in a small office. Every morning, she goes to work by bus. After work, she likes reading books and listening to music. At weekends, she visits her friends.\n\nWhich statement is TRUE?",
        "options": ["Anna lives in Paris.", "Anna goes to work by train.", "Anna is 22 years old.", "Anna works in a hospital."],
        "correct_answer": "Anna is 22 years old.",
        "skill_type": SkillType.READING,
        "level": Level.A1
    },
]

# Answer key for A1
A1_ANSWER_KEY = {
    "a1_g_1": "am", "a1_g_2": "lives", "a1_g_3": "Do", "a1_g_4": "watch", "a1_g_5": "has",
    "a1_g_6": "don't go", "a1_g_7": "are", "a1_g_8": "speak", "a1_g_9": "is", "a1_g_10": "is",
    "a1_v_1": "hospital", "a1_v_2": "Blue", "a1_v_3": "animal", "a1_v_4": "cold", "a1_v_5": "pen",
    "a1_v_6": "morning", "a1_v_7": "7", "a1_v_8": "Apple", "a1_v_9": "school", "a1_v_10": "small",
    "a1_r_1": "22", "a1_r_2": "London", "a1_r_3": "Office", "a1_r_4": "Bus", "a1_r_5": "Reading books",
    "a1_r_6": "Weekends", "a1_r_7": "small", "a1_r_8": "music", "a1_r_9": "Anna's job and daily life",
    "a1_r_10": "Anna is 22 years old.",
}

# ==================== A2 LEVEL TEST ====================
A2_TEST_QUESTIONS = [
    {
        "question_id": "a2_g_1",
        "question": "If I ___ you were coming, I would have prepared dinner.",
        "options": ["knew", "had known", "know", "would know"],
        "correct_answer": "had known",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A2
    },
    {
        "question_id": "a2_g_2",
        "question": "By the time you arrive, I ___ dinner.",
        "options": ["will finish", "will have finished", "am finishing", "have finished"],
        "correct_answer": "will have finished",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A2
    },
    {
        "question_id": "a2_g_3",
        "question": "She said she ___ to London before.",
        "options": ["has gone", "had gone", "went", "was going"],
        "correct_answer": "had gone",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A2
    },
    {
        "question_id": "a2_g_4",
        "question": "The book ___ by many students.",
        "options": ["is read", "are read", "reads", "is reading"],
        "correct_answer": "is read",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A2
    },
    {
        "question_id": "a2_g_5",
        "question": "I wish I ___ taller.",
        "options": ["am", "was", "were", "have been"],
        "correct_answer": "were",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.A2
    },
    {
        "question_id": "a2_v_1",
        "question": "A person who designs buildings is called an ___.",
        "options": ["engineer", "architect", "mechanic", "surgeon"],
        "correct_answer": "architect",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A2
    },
    {
        "question_id": "a2_v_2",
        "question": "The ___ of the mountain was covered with snow.",
        "options": ["peak", "foot", "side", "base"],
        "correct_answer": "peak",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A2
    },
    {
        "question_id": "a2_v_3",
        "question": "She has a strong ___ for music.",
        "options": ["passion", "emotion", "feeling", "mood"],
        "correct_answer": "passion",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.A2
    },
    {
        "question_id": "a2_r_1",
        "question": "Mark Johnson has been a pilot for 20 years. He started his career with a small airline in Texas, but now he flies international routes. Every month, Mark travels to more than 10 different countries. He enjoys meeting people from different cultures, but his favorite part of the job is landing safely with 300 passengers.\n\nWhere did Mark start his pilot career?",
        "options": ["London", "Texas", "New York", "Tokyo"],
        "correct_answer": "Texas",
        "skill_type": SkillType.READING,
        "level": Level.A2
    },
    {
        "question_id": "a2_r_2",
        "question": "Mark Johnson has been a pilot for 20 years. He started his career with a small airline in Texas, but now he flies international routes. Every month, Mark travels to more than 10 different countries. He enjoys meeting people from different cultures, but his favorite part of the job is landing safely with 300 passengers.\n\nHow many countries does Mark visit each month?",
        "options": ["5", "10", "More than 10", "20"],
        "correct_answer": "More than 10",
        "skill_type": SkillType.READING,
        "level": Level.A2
    },
]

A2_ANSWER_KEY = {
    "a2_g_1": "had known", "a2_g_2": "will have finished", "a2_g_3": "had gone", 
    "a2_g_4": "is read", "a2_g_5": "were",
    "a2_v_1": "architect", "a2_v_2": "peak", "a2_v_3": "passion",
    "a2_r_1": "Texas", "a2_r_2": "More than 10",
}

# ==================== B1 LEVEL TEST ====================
B1_TEST_QUESTIONS = [
    {
        "question_id": "b1_g_1",
        "question": "Unless you study harder, you ___ the exam.",
        "options": ["won't pass", "don't pass", "wouldn't pass", "haven't passed"],
        "correct_answer": "won't pass",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.B1
    },
    {
        "question_id": "b1_g_2",
        "question": "The project ___ completed by next Friday.",
        "options": ["will be", "is being", "has been", "is"],
        "correct_answer": "will be",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.B1
    },
    {
        "question_id": "b1_g_3",
        "question": "Despite ___ hard, they didn't win the competition.",
        "options": ["work", "working", "having worked", "worked"],
        "correct_answer": "working",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.B1
    },
    {
        "question_id": "b1_v_1",
        "question": "The company decided to ___ the new product due to lack of funds.",
        "options": ["postpone", "promote", "progress", "produce"],
        "correct_answer": "postpone",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.B1
    },
    {
        "question_id": "b1_v_2",
        "question": "Her ___ to social media has affected her productivity.",
        "options": ["addiction", "habit", "tradition", "custom"],
        "correct_answer": "addiction",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.B1
    },
    {
        "question_id": "b1_r_1",
        "question": "The invention of the internet revolutionized the way people communicate. Today, billions of people use email, social media, and messaging apps to stay connected. However, experts warn that excessive screen time can lead to mental health problems, particularly among young people. Society must find a balance between the benefits of technology and the need for face-to-face interaction.\n\nAccording to the text, what has the internet revolutionized?",
        "options": ["Transportation", "Communication", "Education", "Business"],
        "correct_answer": "Communication",
        "skill_type": SkillType.READING,
        "level": Level.B1
    },
    {
        "question_id": "b1_r_2",
        "question": "The invention of the internet revolutionized the way people communicate. Today, billions of people use email, social media, and messaging apps to stay connected. However, experts warn that excessive screen time can lead to mental health problems, particularly among young people. Society must find a balance between the benefits of technology and the need for face-to-face interaction.\n\nWhat is mentioned as a concern about excessive screen time?",
        "options": ["Loss of money", "Mental health problems", "Loss of jobs", "Poor grades"],
        "correct_answer": "Mental health problems",
        "skill_type": SkillType.READING,
        "level": Level.B1
    },
]

B1_ANSWER_KEY = {
    "b1_g_1": "won't pass", "b1_g_2": "will be", "b1_g_3": "working",
    "b1_v_1": "postpone", "b1_v_2": "addiction",
    "b1_r_1": "Communication", "b1_r_2": "Mental health problems",
}

# ==================== B2 LEVEL TEST ====================
B2_TEST_QUESTIONS = [
    {
        "question_id": "b2_g_1",
        "question": "It is imperative that he ___ this report before the deadline.",
        "options": ["completes", "complete", "completed", "will complete"],
        "correct_answer": "complete",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.B2
    },
    {
        "question_id": "b2_g_2",
        "question": "Had she known about the consequences, she ___ a different decision.",
        "options": ["would make", "would have made", "makes", "has made"],
        "correct_answer": "would have made",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.B2
    },
    {
        "question_id": "b2_v_1",
        "question": "The government's ___ to reduce pollution has resulted in stricter environmental regulations.",
        "options": ["commitment", "promise", "intention", "goal"],
        "correct_answer": "commitment",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.B2
    },
    {
        "question_id": "b2_r_1",
        "question": "Globalization has brought unprecedented opportunities for international trade and cultural exchange. Nevertheless, it has also created significant challenges, including economic inequality, cultural homogenization, and environmental degradation. Policymakers must navigate this complex landscape to maximize benefits while minimizing potential harms.\n\nWhich of the following best captures the author's tone?",
        "options": ["Optimistic", "Pessimistic", "Balanced", "Indifferent"],
        "correct_answer": "Balanced",
        "skill_type": SkillType.READING,
        "level": Level.B2
    },
]

B2_ANSWER_KEY = {
    "b2_g_1": "complete", "b2_g_2": "would have made",
    "b2_v_1": "commitment",
    "b2_r_1": "Balanced",
}

# ==================== C1 LEVEL TEST ====================
C1_TEST_QUESTIONS = [
    {
        "question_id": "c1_g_1",
        "question": "The researcher's findings, ___ were groundbreaking, revolutionized the field.",
        "options": ["which", "that", "what", "whom"],
        "correct_answer": "which",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.C1
    },
    {
        "question_id": "c1_v_1",
        "question": "The author's ___ use of metaphor enhanced the literary quality of the novel.",
        "options": ["judicious", "frivolous", "hasty", "reckless"],
        "correct_answer": "judicious",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.C1
    },
    {
        "question_id": "c1_r_1",
        "question": "Postmodern philosophy challenges the notion of absolute truth, asserting that meaning is socially constructed and context-dependent. This epistemological stance has profound implications for fields ranging from literature to science, fundamentally altering how we understand knowledge production.\n\nWhat is the primary argument of postmodern philosophy?",
        "options": ["Truth is absolute", "Meaning is socially constructed", "Knowledge is unchanging", "Context is irrelevant"],
        "correct_answer": "Meaning is socially constructed",
        "skill_type": SkillType.READING,
        "level": Level.C1
    },
]

C1_ANSWER_KEY = {
    "c1_g_1": "which",
    "c1_v_1": "judicious",
    "c1_r_1": "Meaning is socially constructed",
}

# ==================== C2 LEVEL TEST ====================
C2_TEST_QUESTIONS = [
    {
        "question_id": "c2_g_1",
        "question": "The committee's decision was predicated on evidence that many construed as ___ at best.",
        "options": ["tenuous", "robust", "conclusive", "irrefutable"],
        "correct_answer": "tenuous",
        "skill_type": SkillType.GRAMMAR,
        "level": Level.C2
    },
    {
        "question_id": "c2_v_1",
        "question": "The author's ___ treatment of the subject matter demonstrates exceptional scholarly rigor.",
        "options": ["perfunctory", "assiduous", "desultory", "superficial"],
        "correct_answer": "assiduous",
        "skill_type": SkillType.VOCABULARY,
        "level": Level.C2
    },
    {
        "question_id": "c2_r_1",
        "question": "The interplay between determinism and free will remains one of philosophy's most intractable quandaries. Whilst compatibilists endeavor to reconcile these seemingly irreconcilable positions, hard determinists and libertarians maintain fundamentally divergent ontological commitments.\n\nWhat does the passage suggest about the debate between compatibilists and hard determinists?",
        "options": ["They agree on fundamental principles", "They hold fundamentally different positions", "Compatibilists have proven their point", "The debate is resolved"],
        "correct_answer": "They hold fundamentally different positions",
        "skill_type": SkillType.READING,
        "level": Level.C2
    },
]

C2_ANSWER_KEY = {
    "c2_g_1": "tenuous",
    "c2_v_1": "assiduous",
    "c2_r_1": "They hold fundamentally different positions",
}

# ==================== PLACEMENT TEST ====================
PLACEMENT_TEST_QUESTIONS = [
    # Mix of all levels (15 questions total - 5 easy, 5 medium, 5 hard)
    # Easy questions (A1-A2 level)
    {
        "question_id": "placement_1",
        "question": "I ___ a student.",
        "options": ["am", "is", "are", "be"],
        "correct_answer": "am",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_2",
        "question": "She ___ in London.",
        "options": ["live", "lives", "living", "lived"],
        "correct_answer": "lives",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_3",
        "question": "Which word is a colour?",
        "options": ["Blue", "Bread", "Table", "Chair"],
        "correct_answer": "Blue",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_4",
        "question": "A doctor works in a ___.",
        "options": ["school", "hospital", "bank", "hotel"],
        "correct_answer": "hospital",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_5",
        "question": "How old is Anna? Anna is 22 years old.",
        "options": ["20", "21", "22", "23"],
        "correct_answer": "22",
        "skill_type": SkillType.READING,
    },
    # Medium questions (B1-B2 level)
    {
        "question_id": "placement_6",
        "question": "Unless you study harder, you ___ the exam.",
        "options": ["won't pass", "don't pass", "wouldn't pass", "haven't passed"],
        "correct_answer": "won't pass",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_7",
        "question": "By the time you arrive, I ___ dinner.",
        "options": ["will finish", "will have finished", "am finishing", "have finished"],
        "correct_answer": "will have finished",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_8",
        "question": "The company decided to ___ the new product due to lack of funds.",
        "options": ["postpone", "promote", "progress", "produce"],
        "correct_answer": "postpone",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_9",
        "question": "Her ___ to social media has affected her productivity.",
        "options": ["addiction", "habit", "tradition", "custom"],
        "correct_answer": "addiction",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_10",
        "question": "The invention of the internet revolutionized the way people communicate. What has the internet revolutionized?",
        "options": ["Transportation", "Communication", "Education", "Business"],
        "correct_answer": "Communication",
        "skill_type": SkillType.READING,
    },
    # Hard questions (C1-C2 level)
    {
        "question_id": "placement_11",
        "question": "It is imperative that he ___ this report before the deadline.",
        "options": ["completes", "complete", "completed", "will complete"],
        "correct_answer": "complete",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_12",
        "question": "The researcher's findings, ___ were groundbreaking, revolutionized the field.",
        "options": ["which", "that", "what", "whom"],
        "correct_answer": "which",
        "skill_type": SkillType.GRAMMAR,
    },
    {
        "question_id": "placement_13",
        "question": "The author's ___ use of metaphor enhanced the literary quality of the novel.",
        "options": ["judicious", "frivolous", "hasty", "reckless"],
        "correct_answer": "judicious",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_14",
        "question": "The author's ___ treatment of the subject matter demonstrates exceptional scholarly rigor.",
        "options": ["perfunctory", "assiduous", "desultory", "superficial"],
        "correct_answer": "assiduous",
        "skill_type": SkillType.VOCABULARY,
    },
    {
        "question_id": "placement_15",
        "question": "Globalization has brought unprecedented opportunities but also challenges including inequality and cultural homogenization. Which best captures the author's tone?",
        "options": ["Optimistic", "Pessimistic", "Balanced", "Indifferent"],
        "correct_answer": "Balanced",
        "skill_type": SkillType.READING,
    },
]

PLACEMENT_ANSWER_KEY = {
    "placement_1": "am", "placement_2": "lives", "placement_3": "Blue", "placement_4": "hospital", "placement_5": "22",
    "placement_6": "won't pass", "placement_7": "will have finished", "placement_8": "postpone", "placement_9": "addiction", "placement_10": "Communication",
    "placement_11": "complete", "placement_12": "which", "placement_13": "judicious", "placement_14": "assiduous", "placement_15": "Balanced",
}

# ==================== HELPER FUNCTION ====================
def get_test_by_level(level: Level) -> tuple:
    """Get test questions and answer key by level"""
    if level == Level.A1:
        return A1_TEST_QUESTIONS, A1_ANSWER_KEY
    elif level == Level.A2:
        return A2_TEST_QUESTIONS, A2_ANSWER_KEY
    elif level == Level.B1:
        return B1_TEST_QUESTIONS, B1_ANSWER_KEY
    elif level == Level.B2:
        return B2_TEST_QUESTIONS, B2_ANSWER_KEY
    elif level == Level.C1:
        return C1_TEST_QUESTIONS, C1_ANSWER_KEY
    elif level == Level.C2:
        return C2_TEST_QUESTIONS, C2_ANSWER_KEY
    else:
        raise ValueError(f"Unknown level: {level}")

def get_placement_test() -> tuple:
    """Get placement test questions and answer key"""
    return PLACEMENT_TEST_QUESTIONS, PLACEMENT_ANSWER_KEY
