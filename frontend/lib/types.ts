export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  feedback?: boolean;
  intent?: string;
}

export interface LearningSession {
  id: string;
  language: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  startedAt: Date;
  messagesCount: number;
}

export interface ChatState {
  messages: Message[];
  session: LearningSession | null;
  isLoading: boolean;
  error: string | null;
}

export interface BotResponse {
  text: string;
  intent: string;
  confidence: number;
}
