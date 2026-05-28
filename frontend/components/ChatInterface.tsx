'use client';

import { useEffect, useRef, useState } from 'react';
import { Send, LogOut, MessageCircle } from 'lucide-react';
import { useChatStore } from '@/lib/store';
import { connectSocket, disconnectSocket, getSocket } from '@/lib/socket';
import type { Message } from '@/lib/types';
import MessageBubble from './MessageBubble';
import LoadingDots from './LoadingDots';

interface ChatInterfaceProps {
  onExit: () => void;
}

export default function ChatInterface({ onExit }: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const {
    messages,
    addMessage,
    setLoading,
    isLoading,
    error,
    setError,
  } = useChatStore();

  useEffect(() => {
    const socket = connectSocket();

    socket.on('reply', (data: { text: string; intent: string; confidence: number }) => {
      const botMessage: Message = {
        id: Math.random().toString(),
        text: data.text,
        sender: 'bot',
        timestamp: new Date(),
        intent: data.intent,
      };
      addMessage(botMessage);
      setLoading(false);
    });

    socket.on('error', (errorMsg: string) => {
      setError(errorMsg);
      setLoading(false);
    });

    return () => {
      socket.off('reply');
      socket.off('error');
    };
  }, [addMessage, setLoading, setError]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Math.random().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setLoading(true);
    setError(null);

    const socket = getSocket();
    if (socket) {
      socket.emit('message', { text: inputValue });
    }

    setInputValue('');
  };

  const handleExit = () => {
    disconnectSocket();
    onExit();
  };

  return (
    <div className="w-full max-w-2xl h-full md:h-auto md:max-h-screen chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="flex items-center space-x-3">
          <MessageCircle size={28} />
          <div>
            <h1 className="text-xl md:text-2xl font-bold">Language Tutor</h1>
            <p className="text-sm opacity-90">AI-powered language learning</p>
          </div>
        </div>
        <button
          onClick={handleExit}
          className="p-2 hover:bg-white/20 rounded-lg transition-colors"
          title="Exit"
        >
          <LogOut size={20} />
        </button>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-400">
            <MessageCircle size={48} className="mb-4 opacity-50" />
            <p>Start a conversation to learn!</p>
            <p className="text-sm mt-2">Ask me anything about your language learning journey.</p>
          </div>
        )}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && <LoadingDots />}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me something..."
            disabled={isLoading}
            className="flex-1 px-4 py-3 rounded-lg border-2 border-gray-200 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30 transition-all disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Send size={20} />
            <span className="hidden sm:inline">Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}
