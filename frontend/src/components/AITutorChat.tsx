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
    <div className="rounded-[26px] border border-[rgba(7,7,9,.08)] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)] flex h-[600px] flex-col overflow-hidden">
      <div className="flex items-center justify-between border-b border-[rgba(7,7,9,.08)] bg-[#ededff] p-4 sm:p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-[16px] border border-[#202127] bg-[#fff3d1] shadow-[0_8px_20px_rgba(43,45,90,.08)]">
            <Bot className="h-5 w-5 text-[#202127]" aria-hidden="true" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-black text-[#202127]">المدرس الذكي</h3>
              <span className="inline-flex items-center gap-1 rounded-full bg-[#ededff] px-2 py-1 text-[10px] font-bold text-[#373fb8]"><Sparkles className="h-3 w-3" />AI</span>
            </div>
            <p className="text-xs font-semibold text-[rgba(32,33,39,.52)]">متصل الآن · تدريب محادثة</p>
          </div>
        </div>

        <select
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="rounded-[14px] border border-[rgba(7,7,9,.08)] bg-[#fff] text-[#202127] shadow-none outline-none transition focus:border-[#5862e2] focus:ring-2 focus:ring-[#5862e2]/10 w-auto min-w-[125px] px-3 py-2 text-sm font-bold outline-none"
          aria-label="لغة المحادثة"
        >
          <option value="العربية">العربية</option>
          <option value="الإنجليزية">الإنجليزية</option>
          <option value="الألمانية">الألمانية</option>
          <option value="الفرنسية">الفرنسية</option>
          <option value="الإسبانية">الإسبانية</option>
        </select>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto bg-[#f4f4f2] p-4 sm:p-5">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[82%] rounded-[18px] border p-4 shadow-[0_8px_20px_rgba(43,45,90,.06)] ${
                message.role === 'user'
                  ? 'rounded-br-md border-[#202127] bg-[#5862e2] text-white'
                  : 'rounded-bl-md border-[rgba(7,7,9,.08)] bg-[#fff] text-[#202127]'
              }`}
            >
              <p className="text-sm font-medium leading-6">{message.content}</p>
              <p
                className={`mt-2 text-[10px] font-bold ${
                  message.role === 'user'
                    ? 'text-white/75'
                    : 'text-[rgba(32,33,39,.52)]'
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
            <div className="rounded-[18px] rounded-bl-md border border-[rgba(7,7,9,.08)] bg-[#fff] p-4 shadow-[0_8px_20px_rgba(43,45,90,.06)]">
              <div className="flex items-center gap-1.5" aria-label="جاري الرد">
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#5862e2]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#fff3d1] [animation-delay:150ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#202127] [animation-delay:300ms]" />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      <div className="border-t border-[rgba(7,7,9,.08)] bg-[#fff] p-4 sm:p-5">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="اكتب رسالتك هنا..."
            className="rounded-[14px] border border-[rgba(7,7,9,.08)] bg-[#fff] text-[#202127] shadow-none outline-none transition focus:border-[#5862e2] focus:ring-2 focus:ring-[#5862e2]/10 flex-1 px-3 py-3"
            disabled={isLoading}
          />
          <motion.button
            type="button"
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            aria-label="إرسال الرسالة"
            className="rounded-[14px] bg-[#5862e2] text-white shadow-[0_8px_18px_rgba(88,98,226,.18)] transition hover:bg-[#4f59d5] disabled:cursor-not-allowed disabled:opacity-50 min-h-12 min-w-12 px-4"
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
