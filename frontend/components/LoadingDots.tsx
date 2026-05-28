'use client';

export default function LoadingDots() {
  return (
    <div className="flex justify-start">
      <div className="message-bubble bot flex items-center space-x-1">
        <span className="inline-block">AI is thinking</span>
        <div className="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
}
