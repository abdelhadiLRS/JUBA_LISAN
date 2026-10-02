'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, Send, Sparkles } from 'lucide-react';

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
      timestamp: new Date(),
    },
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
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
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
          context: 'conversation_practice',
        }),
      });

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
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
    <div className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm flex h-[600px] flex-col overflow-hidden">
      <div className="flex items-center justify-between border-b border-[var(--duo-line)] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] p-4 sm:p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-[10px] border border-[var(--duo-ink)] bg-[color-mix(in_srgb,var(--duo-yellow)_18%,transparent)] shadow-sm">
            <Bot className="h-5 w-5 text-[var(--duo-ink)]" aria-hidden="true" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-black text-[var(--duo-ink)]">المدرس الذكي</h3>
              <span className="inline-flex items-center gap-1 rounded-full bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] px-2 py-1 text-[10px] font-bold text-[var(--duo-green)]"><Sparkles className="h-3 w-3" />AI</span>
            </div>
            <p className="text-xs font-semibold text-[var(--duo-muted)]">متصل الآن · تدريب محادثة</p>
          </div>
        </div>

        <select
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-none outline-none transition focus:border-[var(--duo-green)] focus:ring-2 focus:ring-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] w-auto min-w-[125px] px-3 py-2 text-sm font-bold outline-none"
          aria-label="لغة المحادثة"
        >
          <option value="العربية">العربية</option>
          <option value="الإنجليزية">الإنجليزية</option>
          <option value="الألمانية">الألمانية</option>
          <option value="الفرنسية">الفرنسية</option>
          <option value="الإسبانية">الإسبانية</option>
        </select>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto bg-[var(--duo-bg)] p-4 sm:p-5">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[82%] rounded-[10px] border p-4 shadow-sm ${
                message.role === 'user'
                  ? 'rounded-br-md border-[var(--duo-ink)] bg-[var(--duo-green)] text-white'
                  : 'rounded-bl-md border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)]'
              }`}
            >
              <p className="text-sm font-medium leading-6">{message.content}</p>
              <p
                className={`mt-2 text-[10px] font-bold ${
                  message.role === 'user'
                    ? 'text-white/75'
                    : 'text-[var(--duo-muted)]'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
          </motion.div>
        ))}

        {isLoading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
            <div className="rounded-[10px] rounded-bl-md border border-[var(--duo-line)] bg-[var(--duo-card)] p-4 shadow-sm">
              <div className="flex items-center gap-1.5" aria-label="جاري الرد">
                <span className="h-2 w-2 animate-bounce rounded-full bg-[var(--duo-green)]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[color-mix(in_srgb,var(--duo-yellow)_18%,transparent)] [animation-delay:150ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[var(--duo-ink)] [animation-delay:300ms]" />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      <div className="border-t border-[var(--duo-line)] bg-[var(--duo-card)] p-4 sm:p-5">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="اكتب رسالتك هنا..."
            className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-none outline-none transition focus:border-[var(--duo-green)] focus:ring-2 focus:ring-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] flex-1 px-3 py-3"
            disabled={isLoading}
          />
          <motion.button
            type="button"
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            aria-label="إرسال الرسالة"
            className="rounded-[10px] bg-[var(--duo-green)] text-white shadow-sm transition hover:bg-[var(--duo-green)] disabled:cursor-not-allowed disabled:opacity-50 min-h-12 min-w-12 px-4"
            whileHover={{ scale: isLoading ? 1 : 1.03 }}
            whileTap={{ scale: isLoading ? 1 : 0.96 }}
          >
            <Send className="h-4 w-4" aria-hidden="true" />
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default AITutorChat;
