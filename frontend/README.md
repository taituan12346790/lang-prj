# AI Language Learning Agent - Next.js Frontend

Modern, responsive web interface for learning languages with AI tutoring powered by Rasa NLU.

## Features

- 🎯 **Real-time Chat Interface** - Live conversation with AI tutor via Socket.io
- 🌍 **Multi-language Support** - Learn English, Spanish, French, German, Japanese, Chinese
- 📊 **Skill Levels** - Beginner, Intermediate, Advanced learning paths
- 💬 **Message Feedback** - Rate bot responses to improve learning
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast & Smooth** - Optimized animations and interactions
- 🎨 **Modern UI** - Beautiful gradient design with Tailwind CSS

## Tech Stack

- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Real-time**: Socket.io Client
- **State Management**: Zustand
- **Icons**: Lucide React
- **Language**: TypeScript

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update .env.local with your backend URL
```

## Development

```bash
# Start development server
npm run dev

# Open browser
# http://localhost:3000
```

## Build & Deploy

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000      # Backend API URL
NEXT_PUBLIC_SOCKET_URL=http://localhost:8000   # Socket.io server URL
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   └── globals.css          # Global styles
├── components/
│   ├── ChatInterface.tsx    # Main chat component
│   ├── MessageBubble.tsx    # Individual message display
│   ├── LandingPage.tsx      # Welcome screen
│   └── LoadingDots.tsx      # Loading indicator
├── lib/
│   ├── types.ts             # TypeScript interfaces
│   ├── socket.ts            # Socket.io setup
│   └── store.ts             # Zustand state management
└── public/                  # Static assets
```

## Backend Integration

This frontend connects to a Rasa NLU + Node.js backend using Socket.io:

- **messageChannel**: User sends messages
- **replyChannel**: Receives bot responses

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## License

MIT
