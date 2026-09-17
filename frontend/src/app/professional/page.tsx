"use client";

import { motion } from "framer-motion";

const professionalPaths = [
  {
    title: "Business Communication",
    description: "Master professional emails, meetings, and presentations",
    skills: ["Email Writing", "Meeting Participation", "Presentations", "Negotiations"],
    icon: "💼",
    level: "Intermediate to Advanced",
  },
  {
    title: "Academic Writing",
    description: "Excel in research papers, essays, and academic discourse",
    skills: ["Research Papers", "Essays", "Citations", "Critical Analysis"],
    icon: "🎓",
    level: "All Levels",
  },
  {
    title: "Healthcare Language",
    description: "Communicate effectively in medical and healthcare settings",
    skills: ["Patient Communication", "Medical Terminology", "Documentation", "Emergency Phrases"],
    icon: "🏥",
    level: "Intermediate+",
  },
  {
    title: "Tech & IT",
    description: "Navigate the global tech industry with confidence",
    skills: ["Technical Documentation", "Code Reviews", "Agile Meetings", "Client Communication"],
    icon: "💻",
    level: "All Levels",
  },
];

const certifications = [
  {
    name: "JUBA Business Language Certificate",
    level: "Professional",
    duration: "12 weeks",
    recognition: "Industry recognized",
  },
  {
    name: "Academic Language Proficiency",
    level: "Advanced",
    duration: "8 weeks",
    recognition: "University accepted",
  },
  {
    name: "Healthcare Communication Badge",
    level: "Specialized",
    duration: "6 weeks",
    recognition: "Healthcare institutions",
  },
];

export default function ProfessionalPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20">
        <div className="absolute inset-0 juba-hero-glow opacity-30" />
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-3xl mx-auto"
          >
            <span className="juba-eyebrow inline-block mb-4">Career Advancement</span>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 juba-gradient-text">
              Professional Language Mastery
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              Unlock career opportunities with industry-specific language skills and recognized certifications
            </p>
          </motion.div>
        </div>
      </section>

      {/* Learning Paths */}
      <section className="py-16 bg-white dark:bg-slate-900">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 text-center"
          >
            <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
              Specialized Learning Paths
            </h2>
            <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
              Choose your career focus and master the language of your profession
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {professionalPaths.map((path, index) => (
              <motion.div
                key={path.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="juba-card p-8 hover:juba-card-hover"
              >
                <div className="flex items-start gap-4 mb-4">
                  <span className="text-5xl">{path.icon}</span>
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                      {path.title}
                    </h3>
                    <span className="inline-block px-3 py-1 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 rounded-full text-sm font-medium">
                      {path.level}
                    </span>
                  </div>
                </div>
                <p className="text-slate-600 dark:text-slate-300 mb-4">
                  {path.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {path.skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 text-center"
          >
            <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
              Industry-Recognized Certifications
            </h2>
            <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
              Earn certificates that validate your professional language proficiency
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {certifications.map((cert, index) => (
              <motion.div
                key={cert.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="juba-card p-8 text-center border-2 border-transparent hover:border-amber-500/30"
              >
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">
                  {cert.name}
                </h3>
                <p className="text-slate-600 dark:text-slate-300 mb-4">
                  {cert.duration} • {cert.level}
                </p>
                <p className="text-sm text-amber-600 dark:text-amber-400 font-medium">
                  ✓ {cert.recognition}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Mock Tests */}
      <section className="py-16 bg-white dark:bg-slate-900">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 text-center"
          >
            <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
              Practice with Real-World Simulations
            </h2>
            <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
              Test your skills with realistic scenarios from actual workplace situations
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "Job Interview Simulation", count: "15+ scenarios", icon: "🎯" },
              { title: "Business Meeting Practice", count: "20+ scenarios", icon: "🤝" },
              { title: "Presentation Builder", count: "10+ templates", icon: "📊" },
              { title: "Email Writing Lab", count: "25+ exercises", icon: "✉️" },
            ].map((item, index) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="juba-card p-6 text-center hover:juba-card-hover cursor-pointer"
              >
                <div className="text-4xl mb-3">{item.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-slate-900 dark:text-white">
                  {item.title}
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  {item.count}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="juba-card p-12 text-center bg-gradient-to-r from-amber-500 to-orange-500 text-white"
          >
            <h2 className="text-4xl font-bold mb-4">Start Your Professional Journey</h2>
            <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
              Join thousands of professionals who have advanced their careers with JUBA LISAN
            </p>
            <button className="px-8 py-4 bg-white text-amber-600 rounded-full font-bold text-lg hover:shadow-lg transition-shadow">
              Begin Free Trial →
            </button>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
