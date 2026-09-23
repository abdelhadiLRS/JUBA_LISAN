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
    <div className="juba-card flex h-[600px] flex-col overflow-hidden">
      {/* Header */}
      <div className="border-b-2 border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--juba-yellow)] shadow-[3px_3px_0_var(--juba-ink)]">
              <span className="text-xl">🤖</span>
            </div>
            <div>
              <h3 className="font-bold text-[var(--juba-text)]">المدرس الذكي</h3>
              <p className="text-xs text-[var(--juba-muted)]">متصل الآن</p>
            </div>
          </div>
          
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="rounded-xl border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] px-3 py-2 text-sm text-[var(--juba-text)] outline-none focus:border-[var(--juba-primary)] focus:ring-2 focus:ring-[var(--juba-primary)]/20"
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
      <div className="flex-1 space-y-4 overflow-y-auto bg-[var(--juba-bg)] p-4">
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
                message.role === 'user' ? 'text-[var(--juba-mint)]' : 'text-[var(--juba-muted)]'
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
            <div className="rounded-2xl rounded-bl-md border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] p-4">
              <div className="flex gap-2">
                <div className="h-2 w-2 animate-bounce rounded-full bg-[var(--juba-primary)]" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input */}
      <div className="border-t-2 border-[var(--juba-border)] bg-[var(--juba-surface)] p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="اكتب رسالتك هنا..."
            className="juba-input flex-1"
            disabled={isLoading}
          />
          <motion.button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="juba-primary-button min-h-12 px-6"
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
