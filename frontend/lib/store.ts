import { create } from 'zustand';
import type { ChatState, Message, LearningSession } from './types';

interface ChatStore extends ChatState {
  addMessage: (message: Message) => void;
  setMessages: (messages: Message[]) => void;
  setSession: (session: LearningSession | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  session: null,
  isLoading: false,
  error: null,

  addMessage: (message: Message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setMessages: (messages: Message[]) =>
    set(() => ({
      messages,
    })),

  setSession: (session: LearningSession | null) =>
    set(() => ({
      session,
    })),

  setLoading: (isLoading: boolean) =>
    set(() => ({
      isLoading,
    })),

  setError: (error: string | null) =>
    set(() => ({
      error,
    })),

  clearMessages: () =>
    set(() => ({
      messages: [],
    })),
}));
