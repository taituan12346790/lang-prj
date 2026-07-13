#!/bin/bash

# Test API trực tiếp, không qua frontend
# Kiểm tra xem backend thật sự gọi bao nhiêu API calls

echo "Testing direct API call to backend..."
echo "Before: Check Groq usage count"
read -p "Press enter to send request..."

curl -X POST https://lang-prj.onrender.com/api/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "message": "Xin chào, giới thiệu về chủ đề Shopping",
    "session_id": "test-session-123"
  }'

echo ""
echo "After: Check Groq usage count again"
echo "Difference = actual API calls from backend"
