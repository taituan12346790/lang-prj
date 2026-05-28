'use client';

import { formatDistanceToNow } from 'date-fns';
import { ThumbsUp, ThumbsDown } from 'lucide-react';
import type { Message } from '@/lib/types';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} items-end space-x-2`}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex-shrink-0" />
      )}
      <div className="flex flex-col">
        <div className={`message-bubble ${isUser ? 'user' : 'bot'}`}>
          <p className="break-words whitespace-pre-wrap">{message.text}</p>
          {message.intent && !isUser && (
            <p className="text-xs opacity-75 mt-1 italic">
              Intent: {message.intent}
            </p>
          )}
        </div>
        <span className="text-xs text-gray-400 mt-1 px-2">
          {formatDistanceToNow(message.timestamp, { addSuffix: true })}
        </span>
      </div>
      {!isUser && !message.feedback && message.intent && (
        <div className="flex space-x-1">
          <button
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
            title="Helpful"
          >
            <ThumbsUp size={16} className="text-green-600" />
          </button>
          <button
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
            title="Not helpful"
          >
            <ThumbsDown size={16} className="text-red-600" />
          </button>
        </div>
      )}
    </div>
  );
}
