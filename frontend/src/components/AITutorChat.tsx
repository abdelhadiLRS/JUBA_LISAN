'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const AITutorChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'مرحباً! أنا مدرسك الذكي. كيف يمكنني مساعدتك في تعلم اللغة اليوم؟',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('العربية');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          language: selectedLanguage,
          level: 'متوسط',
          context: 'conversation_practice'
        })
      });

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="juba-card bg-white dark:bg-slate-800 flex flex-col h-[600px]">
      {/* Header */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
              <span className="text-white text-xl">🤖</span>
            </div>
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white">المدرس الذكي</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">متصل الآن</p>
            </div>
          </div>
          
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="px-3 py-2 rounded-lg bg-slate-100 dark:bg-slate-700 text-sm text-slate-900 dark:text-white border-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="العربية">العربية</option>
            <option value="الإنجليزية">الإنجليزية</option>
            <option value="الألمانية">الألمانية</option>
            <option value="الفرنسية">الفرنسية</option>
            <option value="الإسبانية">الإسبانية</option>
          </select>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-br-md'
                  : 'bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-white rounded-bl-md'
              }`}
            >
              <p className="text-sm">{message.content}</p>
              <p className={`text-xs mt-2 ${
                message.role === 'user' ? 'text-amber-100' : 'text-slate-500 dark:text-slate-400'
              }`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </motion.div>
        ))}

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-slate-100 dark:bg-slate-700 p-4 rounded-2xl rounded-bl-md">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="اكتب رسالتك هنا..."
            className="flex-1 px-4 py-3 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-white border-none focus:ring-2 focus:ring-amber-500 placeholder-slate-500"
            disabled={isLoading}
          />
          <motion.button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: isLoading ? 1 : 1.05 }}
            whileTap={{ scale: isLoading ? 1 : 0.95 }}
          >
            📤
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default AITutorChat;
