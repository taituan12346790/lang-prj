import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Language Learning Agent',
  description: 'Learn languages with personalized AI tutoring',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 min-h-screen">
        <div className="min-h-screen flex items-center justify-center p-4">
          {children}
        </div>
      </body>
    </html>
  );
}
