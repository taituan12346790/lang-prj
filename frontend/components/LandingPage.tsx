'use client';

import { useState } from 'react';
import { BookOpen, Globe, Zap, Users, ArrowRight } from 'lucide-react';

interface LandingPageProps {
  onStart: () => void;
}

export default function LandingPage({ onStart }: LandingPageProps) {
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');
  const [selectedLevel, setSelectedLevel] = useState<'beginner' | 'intermediate' | 'advanced' | ''>('');

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'ja', name: 'Japanese' },
    { code: 'zh', name: 'Chinese' },
  ];

  const levels = [
    { value: 'beginner', label: 'Beginner', icon: '🌱' },
    { value: 'intermediate', label: 'Intermediate', icon: '🚀' },
    { value: 'advanced', label: 'Advanced', icon: '🏆' },
  ];

  const handleStart = () => {
    if (selectedLanguage && selectedLevel) {
      onStart();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fadeIn">
        <div className="flex justify-center mb-6">
          <Globe size={64} className="text-white drop-shadow-lg" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 drop-shadow-lg">
          AI Language Tutor
        </h1>
        <p className="text-xl text-white/90 drop-shadow-md">
          Learn any language with personalized AI guidance
        </p>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
        {[
          { icon: Zap, title: 'Fast Learning', desc: 'Accelerated language acquisition' },
          { icon: BookOpen, title: 'Smart Lessons', desc: 'Personalized learning paths' },
          { icon: Users, title: 'Interactive', desc: 'Real-time conversation practice' },
        ].map((feature, i) => {
          const Icon = feature.icon;
          return (
            <div
              key={i}
              className="bg-white/10 backdrop-blur-md rounded-xl p-6 text-white transform hover:scale-105 transition-transform"
            >
              <Icon size={32} className="mb-3" />
              <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
              <p className="text-sm text-white/80">{feature.desc}</p>
            </div>
          );
        })}
      </div>

      {/* Selection Cards */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 shadow-2xl">
        {/* Language Selection */}
        <div className="mb-8">
          <label className="text-white font-bold text-lg mb-4 block">
            Choose a Language
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => setSelectedLanguage(lang.code)}
                className={`p-3 rounded-lg font-medium transition-all ${
                  selectedLanguage === lang.code
                    ? 'bg-white text-primary shadow-lg scale-105'
                    : 'bg-white/20 text-white hover:bg-white/30'
                }`}
              >
                {lang.name}
              </button>
            ))}
          </div>
        </div>

        {/* Level Selection */}
        <div className="mb-8">
          <label className="text-white font-bold text-lg mb-4 block">
            Select Your Level
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {levels.map((level) => (
              <button
                key={level.value}
                onClick={() => setSelectedLevel(level.value as any)}
                className={`p-4 rounded-lg font-medium transition-all flex items-center justify-center space-x-2 ${
                  selectedLevel === level.value
                    ? 'bg-white text-primary shadow-lg scale-105'
                    : 'bg-white/20 text-white hover:bg-white/30'
                }`}
              >
                <span>{level.icon}</span>
                <span>{level.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Start Button */}
        <button
          onClick={handleStart}
          disabled={!selectedLanguage || !selectedLevel}
          className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-dark font-bold py-3 px-6 rounded-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 group"
        >
          <span>Start Learning</span>
          <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
}
