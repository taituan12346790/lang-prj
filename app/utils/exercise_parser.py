# app/utils/exercise_parser.py
"""Parse exercises from AI response"""
import re
from typing import List, Dict, Any, Optional


def parse_exercises_from_response(ai_response: str) -> Optional[List[Dict[str, Any]]]:
    """
    Parse exercises from AI response.
    
    Expected format:
    4️⃣ Practice Exercises
    1️⃣ She _____ (watch) TV now.
    2️⃣ They _____ (play) football.
    ...
    
    Returns list of exercises with question and answer placeholder
    """
    
    # Check if response contains exercises section
    if "Practice Exercises" not in ai_response and "Bài tập" not in ai_response:
        return None
    
    # Find exercises section
    exercises_section = ""
    
    # Find start of exercises (after "Practice Exercises" or "Bài tập")
    start_markers = ["4️⃣ Practice Exercises", "4️⃣ **Practice Exercises**", "✏️", "Bài tập luyện tập"]
    start_idx = -1
    
    for marker in start_markers:
        idx = ai_response.find(marker)
        if idx != -1:
            start_idx = idx
            break
    
    if start_idx == -1:
        return None
    
    # Find end of exercises (before "Instructions" or "5️⃣")
    end_markers = ["5️⃣", "Instructions", "Hướng dẫn", "📩", "📮"]
    end_idx = len(ai_response)
    
    for marker in end_markers:
        idx = ai_response.find(marker, start_idx)
        if idx != -1 and idx < end_idx:
            end_idx = idx
    
    exercises_section = ai_response[start_idx:end_idx]
    
    # Parse individual exercises
    # Pattern: 1️⃣, 2️⃣, etc. followed by text with ___ and (verb)
    exercise_pattern = r'([1-5]️⃣)\s*(.+?)(?=\n[1-5]️⃣|\Z)'
    
    matches = re.findall(exercise_pattern, exercises_section, re.DOTALL)
    
    if not matches:
        return None
    
    exercises = []
    for number_emoji, text in matches:
        # Extract number
        number = ord(number_emoji[0]) - ord('0')  # Convert emoji to number
        
        # Clean text
        text = text.strip()
        
        # Try to extract verb/word in parentheses for correct answer
        verb_match = re.search(r'\(([^)]+)\)', text)
        verb = verb_match.group(1) if verb_match else ""
        
        exercises.append({
            "number": number,
            "question": text,
            "verb_hint": verb,  # The verb to conjugate
            "correct_answer": None  # Will be filled when user submits
        })
    
    # Only return if we found at least 3 exercises
    if len(exercises) >= 3:
        return exercises
    
    return None


def parse_user_answers(user_input: str, num_exercises: int = 5) -> List[Dict[str, Any]]:
    """
    Parse user answers from input like:
    "1 is watching 2 are playing 3 is reading 4 am writing 5 are listening"
    
    Returns: [{"number": 1, "answer": "is watching"}, ...]
    """
    
    # Pattern: number followed by text until next number
    pattern = r'(\d+)\s+([^\d]+?)(?=\s*\d+\s+|\Z)'
    
    matches = re.findall(pattern, user_input, re.DOTALL)
    
    answers = []
    for num_str, answer in matches:
        num = int(num_str)
        answer = answer.strip()
        
        if 1 <= num <= num_exercises:
            answers.append({
                "number": num,
                "answer": answer
            })
    
    return answers
