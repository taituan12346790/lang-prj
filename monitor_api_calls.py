"""
Monitor API calls by tracking all LLM generate_async calls
Run this to see EXACTLY where each API call happens
"""

# Read the production logs and analyze them
log_text = """
INFO:     74.220.52.6:0 - "GET /api/chat/sessions?limit=10 HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/learning/context HTTP/1.1" 200 OK
2026-07-13 16:21:47.787 | INFO     | app.services.topic_service:set_active_context:564 - ✅ Set active context for b88f3b13-1cb7-4dee-a636-b712e314421c: topic=db7be349-19c2-478c-9078-fed35b653a64, lesson=3, mode=normal
INFO:     74.220.52.6:0 - "POST /api/learning/activate-context HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/analytics/dashboard HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/learning/context HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/learning/context HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/learning/context HTTP/1.1" 200 OK
2026-07-13 16:21:49.400 | INFO     | app.routers.chat:chat_with_ai:27 - 🔵 CHAT REQUEST START: user=b88f3b13-1cb7-4dee-a636-b712e314421c, input=Chào bạn! Tôi đang học chủ đề 'Mua sắm & Giá cả', ...
2026-07-13 16:21:49.400 | INFO     | app.routers.chat:chat_with_ai:31 - 🔵 Loading learning service...
2026-07-13 16:21:53.114 | INFO     | app.routers.chat:chat_with_ai:34 - 🔵 Processing chat with learning service...
2026-07-13 16:21:53.114 | INFO     | app.services.learning_service:process:632 - 🔵 PROCESS START: user=b88f3b13..., input_len=157
2026-07-13 16:21:53.115 | INFO     | app.services.learning_service:process:649 - 🔵 Getting active topic for user b88f3b13...
2026-07-13 16:21:53.215 | INFO     | app.services.learning_service:process:651 - 🔵 Active topic: db7be349-19c2-478c-9078-fed35b653a64
2026-07-13 16:21:53.215 | INFO     | app.services.learning_service:process:660 - 🔵 Building initial state...
2026-07-13 16:21:53.216 | INFO     | app.services.learning_service:process:684 - 🔵 Invoking LangGraph...
2026-07-13 16:21:54.428 | INFO     | app.services.learning_service:_build_analytics_context_async:596 - Level-up eligibility for b88f3b13-1cb7-4dee-a636-b712e314421c: False
2026-07-13 16:21:54.428 | INFO     | app.services.learning_service:_build_analytics_context_async:612 - Analytics context built for b88f3b13-1cb7-4dee-a636-b712e314421c: 0 weak skills, 7 due reviews, eligible=False
2026-07-13 16:21:55.120 | INFO     | app.services.learning_service:_build_learning_context_dict:555 - Built learning context for b88f3b13-1cb7-4dee-a636-b712e314421c: Shopping & Prices (2/5 lessons)
2026-07-13 16:21:55.120 | INFO     | app.services.learning_service:_load_memory_node:121 - ✅ Learning context loaded: Shopping & Prices
2026-07-13 16:21:55.203 | INFO     | app.core.strategy:decide:146 - [Strategy] User=b88f3b13-1cb7-4dee-a636-b712e314421c | Mode=exercise | InputType=general
2026-07-13 16:21:55.606 | DEBUG    | app.agents.exercise_agent:execute:48 - ExerciseAgent executing exercise generation
ExerciseGenerator failed after 3 attempts
2026-07-13 16:21:59.289 | DEBUG    | app.agents.exercise_agent:execute:58 - ExerciseAgent completed task successfully
2026-07-13 16:21:59.289 | INFO     | app.core.pipeline:_execute_tools_node:197 - Tools executed: ['exercise']
2026-07-13 16:21:59.300 | INFO     | app.core.pipeline:_generate_response_node:238 - ✅ Learning context IS included in prompt
2026-07-13 16:21:59.300 | INFO     | app.core.pipeline:_generate_response_node:241 -    Topic: Mua sắm & Giá cả, Lesson: Practice: Shopping Dialogues
2026-07-13 16:21:59.300 | INFO     | app.core.pipeline:_generate_response_node:250 - 🔧 Tool results included in prompt: ['exercise']
🔍 DEBUG: Using model: openai/gpt-oss-120b
2026-07-13 16:22:02.500 | INFO     | app.core.pipeline:_generate_response_node:264 - Response generated | Length: 2865
2026-07-13 16:22:02.509 | WARNING  | app.core.pipeline:_validate_output_node:387 - ❌ Output validation failed: language_drift
2026-07-13 16:22:02.617 | INFO     | app.core.reflector_enhanced:_analyze_conversation:198 - ⏭️  Skipping LLM conversation analysis (disabled to save tokens)
2026-07-13 16:22:02.622 | INFO     | app.core.reflector_enhanced:_update_topic_skills:261 - Updated skills for user b88f3b13-1cb7-4dee-a636-b712e314421c on topic db7be349-19c2-478c-9078-fed35b653a64: weak=0, strong=0
2026-07-13 16:22:02.622 | INFO     | app.core.reflector_enhanced:reflect_and_update:160 - Reflector updated 1 topics for user b88f3b13-1cb7-4dee-a636-b712e314421c
2026-07-13 16:22:02.706 | INFO     | app.services.learning_service:_orchestrate_node:234 - Orchestrator suggested 1 actions for b88f3b13-1cb7-4dee-a636-b712e314421c
2026-07-13 16:22:02.802 | INFO     | app.services.learning_service:_update_memory_node:255 - 🧠 B2: Passing reflection analysis to memory: {'weak_skills': [], 'strong_skills': [], 'topics_discussed': [], 'engagement': 'medium'}
2026-07-13 16:22:02.833 | DEBUG    | app.services.conversation_service:save_message:50 - ✅ Message saved: session=451ed614..., role=user
2026-07-13 16:22:02.847 | DEBUG    | app.services.conversation_service:save_message:50 - ✅ Message saved: session=451ed614..., role=assistant
2026-07-13 16:22:02.847 | INFO     | app.services.learning_service:_save_conversation_to_db:399 - ✅ Saved conversation for b88f3b13-1cb7-4dee-a636-b712e314421c to DB (session: 451ed614...)
2026-07-13 16:22:02.903 | DEBUG    | app.services.chat_learning_service:record_activity:54 - No activity to record for session 451ed614-6a49-47a5-a291-a7056329f6b0
2026-07-13 16:22:02.908 | INFO     | app.services.learning_service:process:686 - 🔵 LangGraph completed
2026-07-13 16:22:02.916 | INFO     | app.routers.chat:chat_with_ai:46 - 🔵 Learning service returned: success=True
2026-07-13 16:22:02.916 | INFO     | app.routers.chat:chat_with_ai:65 - 🟢 CHAT REQUEST SUCCESS: response_length=2865
INFO:     74.220.52.6:0 - "POST /api/chat/ HTTP/1.1" 200 OK
INFO:     74.220.52.6:0 - "GET /api/chat/sessions?limit=10 HTTP/1.1" 200 OK
"""

print("=" * 80)
print("ANALYZING PRODUCTION LOG FOR API CALLS")
print("=" * 80)

# Count API call indicators
debug_model_count = log_text.count("🔍 DEBUG: Using model")
exercise_failures = log_text.count("ExerciseGenerator failed after")

print(f"\n📊 API CALL ANALYSIS:")
print(f"   🔍 '🔍 DEBUG: Using model' appearances: {debug_model_count}")
print(f"   ❌ 'ExerciseGenerator failed after' appearances: {exercise_failures}")

print(f"\n🎯 EXPECTED API CALLS FOR THIS REQUEST:")
print(f"   1. ExerciseGenerator attempt (fails)")
print(f"   2. Pipeline generate_response_node (succeeds)")
print(f"   TOTAL: 2 calls")

print(f"\n📈 BUT USER REPORTS:")
print(f"   Jump from 657 → 695 calls = 38 CALLS!")

print(f"\n⚠️  DISCREPANCY:")
print(f"   Logged calls: {debug_model_count}")
print(f"   Actual calls: 38")
print(f"   MISSING: ~36 calls not being logged!")

print(f"\n🔍 POSSIBLE CAUSES:")
print(f"   1. ExerciseGenerator retries 3 times (max_retries=1 → should be 1 call)")
print(f"   2. Multiple concurrent users hitting API at same time")
print(f"   3. Frontend making multiple requests")
print(f"   4. API calls happening BEFORE the DEBUG log statement")
print(f"   5. Background workers/cron jobs calling APIs")

print(f"\n💡 RECOMMENDED INVESTIGATION:")
print(f"   1. Check Groq dashboard to see timestamp of API calls")
print(f"   2. Add logging BEFORE API call (not after)")
print(f"   3. Check if frontend sends multiple requests per click")
print(f"   4. Check for background tasks (celery, cron, etc.)")
print(f"   5. Verify only ONE user is testing (not multiple sessions)")

print("=" * 80)
