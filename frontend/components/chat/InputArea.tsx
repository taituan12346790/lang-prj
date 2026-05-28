// src/components/chat/InputArea.tsx
'use client';

import { Send, Mic, MicOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { useState, KeyboardEvent } from 'react';

interface InputAreaProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  onVoiceToggle?: () => void;
  isListening?: boolean;
}

export default function InputArea({
  onSend,
  isLoading,
  onVoiceToggle,
  isListening = false,
}: InputAreaProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSend(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
      <div className="max-w-3xl mx-auto">
        <div className="relative flex items-end gap-2">
          {onVoiceToggle && (
            <Button
              type="button"
              variant="outline"
              size="icon"
              onClick={onVoiceToggle}
              className={isListening ? 'text-red-500' : ''}
            >
              {isListening ? <MicOff size={20} /> : <Mic size={20} />}
            </Button>
          )}

          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Nhập tin nhắn của bạn... (Shift + Enter để xuống dòng)"
            className="min-h-[64px] max-h-[180px] resize-y pr-16"
            disabled={isLoading}
          />

          <Button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            size="icon"
            className="absolute bottom-3 right-3"
          >
            <Send size={20} />
          </Button>
        </div>

        <p className="text-center text-xs text-gray-500 mt-3">
          AI Language Tutor có thể mắc lỗi • Hãy kiểm tra thông tin quan trọng
        </p>
      </div>
    </div>
  );
}