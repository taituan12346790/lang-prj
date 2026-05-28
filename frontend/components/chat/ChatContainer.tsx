// src/components/chat/ChatContainer.tsx
'use client';

import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import { Message } from '@/types/chat';
import { useChatStore } from '@/store/chatStore';
import { sendMessageToAI } from '@/lib/chatService';
import { ScrollArea } from '@/components/ui/scroll-area';

export default function ChatContainer() {
  const { 
    sessionId, 
    messages, 
    isLoading, 
    addMessage, 
    setIsLoading 
  } = useChatStore();

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (input: string) => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    addMessage(userMessage);
    setIsLoading(true);

    try {
      const reply = await sendMessageToAI(input, sessionId);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: reply,
        timestamp: new Date().toISOString(),
      };

      addMessage(assistantMessage);
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ ${error.message}`,
        timestamp: new Date().toISOString(),
      };
      addMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-950">
      <div className="border-b p-4 bg-white dark:bg-gray-900">
        <div className="max-w-3xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="font-semibold text-lg">AI Language Tutor</h1>
            <p className="text-sm text-green-600">● Online</p>
          </div>
          <div className="text-xs text-gray-500">ID: {sessionId.slice(0, 8)}...</div>
        </div>
      </div>

      <ScrollArea className="flex-1 p-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 py-20">
              Chào mừng bạn! Hãy gửi tin nhắn để bắt đầu buổi học hôm nay.
            </div>
          )}
          
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <span className="animate-pulse">🤖</span>
              </div>
              <div className="bg-gray-100 dark:bg-gray-800 rounded-2xl px-5 py-3 text-sm">
                AI Tutor đang suy nghĩ...
              </div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>

      <InputArea onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}