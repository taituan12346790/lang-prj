'use client';

import { useEffect, useState } from 'react';
import ChatInterface from '@/components/ChatInterface';
import LandingPage from '@/components/LandingPage';

export default function Home() {
  const [isClient, setIsClient] = useState(false);
  const [isLearning, setIsLearning] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) return null;

  return (
    <main className="w-full h-screen">
      {!isLearning ? (
        <LandingPage onStart={() => setIsLearning(true)} />
      ) : (
        <ChatInterface onExit={() => setIsLearning(false)} />
      )}
    </main>
  );
}
