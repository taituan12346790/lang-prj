"""
Add question_vi to practice lessons for all A1 topics
"""

import sys
sys.path.insert(0, '.')

from app.data.topics_data import A1_TOPICS

def check_practice_lessons():
    """Check which practice lessons need question_vi"""
    
    print("=" * 80)
    print("CHECKING PRACTICE LESSONS FOR QUESTION_VI")
    print("=" * 80)
    
    topics_need_update = []
    
    for topic in A1_TOPICS:
        topic_order = topic['order']
        topic_name = topic['name']
        
        # Find practice lesson
        practice_lesson = None
        for lesson in topic.get('lessons', []):
            if lesson.get('lesson_type') == 'practice':
                practice_lesson = lesson
                break
        
        if not practice_lesson:
            continue
        
        # Check exercises
        exercises = practice_lesson.get('content', {}).get('exercises', [])
        needs_update = False
        
        for ex in exercises:
            if ex.get('type') == 'multiple_choice':
                if 'question_vi' not in ex:
                    needs_update = True
                    break
        
        if needs_update:
            topics_need_update.append({
                'order': topic_order,
                'name': topic_name,
                'lesson': practice_lesson
            })
            print(f"📝 Topic {topic_order}: {topic_name}")
            print(f"   Practice lesson needs question_vi")
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {len(topics_need_update)}/20 topics need update")
    print("=" * 80)
    
    return topics_need_update

if __name__ == "__main__":
    check_practice_lessons()
