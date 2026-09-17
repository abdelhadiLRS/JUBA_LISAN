'use client';

import React from 'react';
import { motion } from 'framer-motion';

const CulturalMap: React.FC = () => {
  const regions = [
    {
      name: 'الشرق الأوسط',
      countries: ['السعودية', 'الإمارات', 'مصر', 'الأردن'],
      languages: ['العربية الفصحى', 'اللهجات المحلية'],
      color: 'from-amber-400 to-orange-500'
    },
    {
      name: 'أوروبا الغربية',
      countries: ['فرنسا', 'ألمانيا', 'إسبانيا', 'إيطاليا'],
      languages: ['الفرنسية', 'الألمانية', 'الإسبانية', 'الإيطالية'],
      color: 'from-blue-400 to-indigo-500'
    },
    {
      name: 'آسيا الشرقية',
      countries: ['الصين', 'اليابان', 'كوريا الجنوبية'],
      languages: ['الصينية', 'اليابانية', 'الكورية'],
      color: 'from-red-400 to-pink-500'
    },
    {
      name: 'أمريكا اللاتينية',
      countries: ['المكسيك', 'البرازيل', 'الأرجنتين'],
      languages: ['الإسبانية', 'البرتغالية'],
      color: 'from-green-400 to-emerald-500'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          خريطة الثقافات واللغات
        </h2>
        <p className="text-slate-600 dark:text-slate-400">
          استكشف التنوع الثقافي حول العالم
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {regions.map((region, index) => (
          <motion.div
            key={region.name}
            className={`juba-card bg-gradient-to-br ${region.color} p-6 text-white`}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1, duration: 0.4 }}
            whileHover={{ scale: 1.03, rotate: -1 }}
          >
            <h3 className="text-xl font-bold mb-4">{region.name}</h3>
            
            <div className="space-y-3">
              <div>
                <p className="text-sm opacity-80 mb-2">الدول:</p>
                <div className="flex flex-wrap gap-2">
                  {region.countries.map(country => (
                    <span
                      key={country}
                      className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm"
                    >
                      {country}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm opacity-80 mb-2">اللغات:</p>
                <div className="flex flex-wrap gap-2">
                  {region.languages.map(language => (
                    <span
                      key={language}
                      className="px-3 py-1 bg-white/30 backdrop-blur-sm rounded-full text-sm font-medium"
                    >
                      {language}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <motion.button
              className="mt-6 w-full py-3 bg-white/20 backdrop-blur-sm rounded-xl hover:bg-white/30 transition-all font-semibold"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              استكشف الثقافة 🗺️
            </motion.button>
          </motion.div>
        ))}
      </div>

      <motion.div
        className="mt-8 p-6 bg-slate-100 dark:bg-slate-800 rounded-2xl"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="flex items-start gap-4">
          <span className="text-3xl">💡</span>
          <div>
            <h4 className="font-bold text-slate-900 dark:text-white mb-2">
              هل تعلم؟
            </h4>
            <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
              هناك أكثر من 7000 لغة حية في العالم اليوم، لكن نصفها قد يختفي بحلول نهاية هذا القرن. 
              تعلم اللغات يساعد في الحفاظ على هذا التراث الإنساني الغني!
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default CulturalMap;
