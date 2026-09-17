'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Challenge {
  id: string;
  title: string;
  description: string;
  participants: number;
  reward: string;
  deadline: string;
  difficulty: 'سهل' | 'متوسط' | 'صعب';
}

const WeeklyChallenge: React.FC = () => {
  const [joinedChallenges, setJoinedChallenges] = useState<string[]>([]);

  const challenges: Challenge[] = [
    {
      id: '1',
      title: 'تحدي المحادثة اليومية',
      description: 'تحدث لمدة 5 دقائق يومياً باللغة التي تتعلمها',
      participants: 1247,
      reward: '+50 نقطة خبرة',
      deadline: '7 أيام',
      difficulty: 'سهل'
    },
    {
      id: '2',
      title: 'تحدي المفردات الجديدة',
      description: 'تعلم 20 كلمة جديدة هذا الأسبوع',
      participants: 892,
      reward: '+100 نقطة خبرة',
      deadline: '5 أيام',
      difficulty: 'متوسط'
    },
    {
      id: '3',
      title: 'تحدي الكتابة الإبداعية',
      description: 'اكتب قصة قصيرة (100 كلمة) باللغة المستهدفة',
      participants: 456,
      reward: '+200 نقطة خبرة + شارة',
      deadline: '3 أيام',
      difficulty: 'صعب'
    }
  ];

  const toggleJoin = (challengeId: string) => {
    setJoinedChallenges(prev =>
      prev.includes(challengeId)
        ? prev.filter(id => id !== challengeId)
        : [...prev, challengeId]
    );
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'سهل': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'متوسط': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'صعب': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default: return 'bg-slate-100 text-slate-800 dark:bg-slate-900 dark:text-slate-200';
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          التحديات الأسبوعية
        </h2>
        <p className="text-slate-600 dark:text-slate-400">
          شارك في التحديات وحقق إنجازات رائعة
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {challenges.map((challenge, index) => (
          <motion.div
            key={challenge.id}
            className="juba-card bg-white dark:bg-slate-800 p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.3 }}
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex items-start justify-between mb-4">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(challenge.difficulty)}`}>
                {challenge.difficulty}
              </span>
              <span className="text-xs text-slate-500 dark:text-slate-400">
                {challenge.deadline} متبقي
              </span>
            </div>

            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
              {challenge.title}
            </h3>

            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              {challenge.description}
            </p>

            <div className="flex items-center gap-4 mb-4 text-sm">
              <span className="text-slate-500 dark:text-slate-400">
                👥 {challenge.participants} مشارك
              </span>
              <span className="text-amber-600 dark:text-amber-500 font-medium">
                🏆 {challenge.reward}
              </span>
            </div>

            <motion.button
              className={`w-full py-3 rounded-xl font-semibold transition-all ${
                joinedChallenges.includes(challenge.id)
                  ? 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400'
                  : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:shadow-lg'
              }`}
              onClick={() => toggleJoin(challenge.id)}
              whileTap={{ scale: 0.98 }}
            >
              {joinedChallenges.includes(challenge.id) ? '✅ انضممت' : '🚀 انضم الآن'}
            </motion.button>
          </motion.div>
        ))}
      </div>

      {joinedChallenges.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 p-6 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-2xl border border-amber-200 dark:border-amber-800"
        >
          <div className="flex items-center gap-4">
            <span className="text-3xl">🎯</span>
            <div>
              <h4 className="font-bold text-slate-900 dark:text-white">
                تحدياتك النشطة: {joinedChallenges.length}
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                استمر في التقدم وحقق أهدافك!
              </p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default WeeklyChallenge;
