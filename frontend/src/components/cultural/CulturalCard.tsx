'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface CulturalCardProps {
  country: string;
  flag: string;
  greeting: string;
  tradition: string;
  funFact: string;
  language: string;
}

const CulturalCard: React.FC<CulturalCardProps> = ({
  country,
  flag,
  greeting,
  tradition,
  funFact,
  language
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      className="overflow-hidden rounded-[20px] border-2 border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-[0_3px_0_var(--duo-line)] cursor-pointer"
      whileHover={{ y: -5 }}
      onClick={() => setIsExpanded(!isExpanded)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="p-6">
        <div className="flex items-center gap-4 mb-4">
          <span className="text-4xl">{flag}</span>
          <div>
            <h3 className="text-xl font-bold text-[var(--duo-ink)]">{country}</h3>
            <p className="text-sm text-[var(--duo-muted)]">{language}</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <span className="text-[var(--duo-yellow)]">💬</span>
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400">التحية الشائعة</p>
              <p className="text-slate-900 dark:text-white font-medium">{greeting}</p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <span className="text-amber-600 dark:text-amber-500">🎭</span>
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400">تقليد ثقافي</p>
              <p className="text-slate-900 dark:text-white">{tradition}</p>
            </div>
          </div>

          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="flex items-start gap-2"
            >
              <span className="text-amber-600 dark:text-amber-500">💡</span>
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400">هل تعلم؟</p>
                <p className="text-slate-900 dark:text-white">{funFact}</p>
              </div>
            </motion.div>
          )}
        </div>

        <div className="mt-4 pt-4 border-t border-[var(--duo-line)]">
          <p className="text-xs text-slate-500 dark:text-slate-400 text-center">
            انقر للمزيد من المعلومات
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default CulturalCard;
