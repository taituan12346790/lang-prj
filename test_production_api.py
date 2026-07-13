"""
Test production API directly
"""
import requests
import json

# Test production endpoint
url = "https://lang-prj.onrender.com/api/learning/topics?level=A1"

try:
    print("🌐 Testing production API...")
    print(f"URL: {url}\n")
    
    response = requests.get(url, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Response length: {len(response.text)} chars")
        print(f"First 200 chars: {response.text[:200]}\n")
        
        try:
            topics = response.json()
            
            # Find Topic 20
            topic_20 = None
            for topic in topics:
                if topic.get('order') == 20:
                    topic_20 = topic
                    break
            
            if topic_20:
                print("\n" + "=" * 60)
                print("TOPIC 20 FROM PRODUCTION API:")
                print("=" * 60)
                print(f"Name: {topic_20.get('name')}")
                print(f"Name (VI): {topic_20.get('name_vi')}")
                print(f"Description: {topic_20.get('description')}")
                print(f"Description (VI): {topic_20.get('description_vi')}")
                print(f"Number of lessons: {len(topic_20.get('lessons', []))}")
                print("\nLessons:")
                for lesson in topic_20.get('lessons', []):
                    print(f"  {lesson.get('order')}. [{lesson.get('lesson_type')}] {lesson.get('title')}")
                print("=" * 60)
            else:
                print("❌ Topic 20 not found in response")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print(f"Response is not valid JSON")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print("⏰ Request timeout - Server might be restarting")
except Exception as e:
    print(f"❌ Error: {e}")
