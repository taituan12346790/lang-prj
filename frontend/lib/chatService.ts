// src/lib/chatService.ts
import api from './api';

export const sendMessageToAI = async (
  message: string, 
  sessionId?: string
): Promise<string> => {
  try {
    const response = await api.post('/backend/chat', { 
      message, 
      sessionId 
    });
    
    // Linh hoạt với nhiều cách backend trả về
    return response.data.reply || 
           response.data.content || 
           response.data.message || 
           response.data;
  } catch (error: any) {
    console.error('Chat API Error:', error);
    throw new Error(
      error.response?.data?.detail || 
      error.message || 
      'Không thể kết nối với AI Tutor. Vui lòng kiểm tra backend.'
    );
  }
};