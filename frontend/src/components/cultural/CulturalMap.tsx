'use client';

import React from 'react';
import { motion } from 'framer-motion';

const CulturalMap: React.FC = () => {
  const regions = [
    { name: 'الشرق الأوسط', countries: ['السعودية', 'الإمارات', 'مصر', 'الأردن'], languages: ['العربية الفصحى', 'اللهجات المحلية'] },
    { name: 'أوروبا الغربية', countries: ['فرنسا', 'ألمانيا', 'إسبانيا', 'إيطاليا'], languages: ['الفرنسية', 'الألمانية', 'الإسبانية', 'الإيطالية'] },
    { name: 'آسيا الشرقية', countries: ['الصين', 'اليابان', 'كوريا الجنوبية'], languages: ['الصينية', 'اليابانية', 'الكورية'] },
    { name: 'أمريكا اللاتينية', countries: ['المكسيك', 'البرازيل', 'الأرجنتين'], languages: ['الإسبانية', 'البرتغالية'] },
  ];

  return (
    <div className="space-y-5">
      <div className="mb-6">
        <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--duo-green-dark)]">CULTURE</p>
        <h2 className="text-2xl font-extrabold tracking-tight text-[var(--duo-ink)]">خريطة الثقافات واللغات</h2>
        <p className="mt-1 text-sm text-[var(--duo-muted)]">استكشف التنوع الثقافي حول العالم</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {regions.map((region, index) => (
          <motion.div
            key={region.name}
            className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-5 text-[var(--duo-ink)] shadow-sm transition-shadow hover:shadow-md"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.08, duration: 0.3 }}
          >
            <div className="mb-4 flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-sm font-black text-[var(--duo-green-dark)]">{String(index + 1).padStart(2, '0')}</span>
              <h3 className="text-base font-bold">{region.name}</h3>
            </div>
            <div className="space-y-3">
              <div>
                <p className="mb-1.5 text-[10px] font-bold uppercase tracking-wide text-[var(--duo-muted)]">الدول</p>
                <div className="flex flex-wrap gap-1.5">
                  {region.countries.map(country => <span key={country} className="rounded-full bg-[var(--duo-bg)] px-2.5 py-1 text-xs font-medium text-[var(--duo-ink)]">{country}</span>)}
                </div>
              </div>
              <div>
                <p className="mb-1.5 text-[10px] font-bold uppercase tracking-wide text-[var(--duo-muted)]">اللغات</p>
                <div className="flex flex-wrap gap-1.5">
                  {region.languages.map(language => <span key={language} className="rounded-full bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] px-2.5 py-1 text-xs font-semibold text-[var(--duo-green-dark)]">{language}</span>)}
                </div>
              </div>
            </div>
            <button type="button" className="mt-5 h-9 w-full rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] text-xs font-bold text-[var(--duo-ink)] transition-colors hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_6%,transparent)]">
              استكشف الثقافة 🗺️
            </button>
          </motion.div>
        ))}
      </div>

      <motion.div className="mt-6 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-5 shadow-sm" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <div className="flex items-start gap-3">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-yellow)_24%,transparent)] text-lg">💡</span>
          <div>
            <h4 className="mb-1 font-bold text-[var(--duo-ink)]">هل تعلم؟</h4>
            <p className="text-sm leading-relaxed text-[var(--duo-muted)]">هناك أكثر من 7000 لغة حية في العالم اليوم، لكن نصفها قد يختفي بحلول نهاية هذا القرن. تعلم اللغات يساعد في الحفاظ على هذا التراث الإنساني الغني!</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default CulturalMap;
