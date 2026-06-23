'use client';

import { useState } from 'react';

interface Message {
  role: 'user' | 'ai';
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    // TODO: sau này thay bằng fetch gọi backend
    // Mock response (giả lập AI trả lời)
    setTimeout(() => {
      const aiMsg: Message = {
        role: 'ai',
        content: `Backend chưa sẵn sàng. Bạn vừa nói: "${input}". Đây là phản hồi mẫu.`
      };
      setMessages(prev => [...prev, aiMsg]);
      setLoading(false);
    }, 800);
  };

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto border rounded-lg p-4 mb-4 space-y-2 bg-white dark:bg-zinc-900">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10">
            Nhập tin nhắn để bắt đầu chat với AI Tutor
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg px-4 py-2 ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-zinc-700'}`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 dark:bg-zinc-700 rounded-lg px-4 py-2">...</div>
          </div>
        )}
      </div>
      <div className="flex gap-2">
        <textarea
          className="flex-1 border rounded-lg p-2 resize-none dark:bg-zinc-800 dark:border-zinc-700"
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder="Nhập câu hỏi của bạn..."
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium px-4 py-2 rounded-lg"
        >
          Gửi
        </button>
      </div>
    </div>
  );
}
