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
  country, flag, greeting, tradition, funFact, language
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      className="cursor-pointer overflow-hidden rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-sm transition-shadow hover:shadow-md"
      whileHover={{ y: -2 }}
      onClick={() => setIsExpanded(!isExpanded)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="p-5 sm:p-6">
        <div className="mb-4 flex items-center gap-3">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-2xl">{flag}</span>
          <div className="min-w-0">
            <h3 className="truncate text-lg font-bold text-[var(--duo-ink)]">{country}</h3>
            <p className="text-xs text-[var(--duo-muted)]">{language}</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start gap-2.5">
            <span className="mt-0.5 text-[var(--duo-green-dark)]">💬</span>
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wide text-[var(--duo-muted)]">التحية الشائعة</p>
              <p className="font-medium text-[var(--duo-ink)]">{greeting}</p>
            </div>
          </div>
          <div className="flex items-start gap-2.5">
            <span className="mt-0.5 text-[var(--duo-green-dark)]">🎭</span>
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wide text-[var(--duo-muted)]">تقليد ثقافي</p>
              <p className="text-sm text-[var(--duo-ink)]">{tradition}</p>
            </div>
          </div>
          {isExpanded && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="flex items-start gap-2.5">
              <span className="mt-0.5 text-[var(--duo-green-dark)]">💡</span>
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-[var(--duo-muted)]">هل تعلم؟</p>
                <p className="text-sm text-[var(--duo-ink)]">{funFact}</p>
              </div>
            </motion.div>
          )}
        </div>

        <div className="mt-4 border-t border-[var(--duo-line)] pt-3">
          <p className="text-center text-[10px] font-semibold text-[var(--duo-muted)]">انقر للمزيد من المعلومات</p>
        </div>
      </div>
    </motion.div>
  );
};

export default CulturalCard;
