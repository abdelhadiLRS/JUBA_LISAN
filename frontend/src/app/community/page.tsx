"use client";

import { motion } from "framer-motion";
import WeeklyChallenge from "@/components/social/WeeklyChallenge";
import CulturalCard from "@/components/cultural/CulturalCard";
import CulturalMap from "@/components/cultural/CulturalMap";

const culturalData = [
  {
    id: "1",
    country: "Saudi Arabia",
    flag: "🇸🇦",
    greeting: "As-salamu alaykum (Peace be upon you)",
    tradition: "Traditional Arabic coffee served with dates as a sign of hospitality",
    funFact: "Saudi Arabia has over 30 UNESCO World Heritage Sites and is the birthplace of Islam",
    language: "Arabic",
  },
  {
    id: "2",
    country: "Japan",
    flag: "🇯🇵",
    greeting: "Konnichiwa (Hello/Good afternoon)",
    tradition: "The ancient tea ceremony (Chanoyu) emphasizing harmony, respect, purity, and tranquility",
    funFact: "Japan has the world's oldest company, Kongo Gumi, which operated for over 1,400 years",
    language: "Japanese",
  },
  {
    id: "3",
    country: "Mexico",
    flag: "🇲🇽",
    greeting: "¡Hola! ¿Qué tal? (Hello! How are you?)",
    tradition: "Día de los Muertos (Day of the Dead) celebration honoring deceased loved ones",
    funFact: "Mexico is home to the smallest volcano in the world, Cuexcomate, standing at just 43 feet tall",
    language: "Spanish",
  },
];

export default function CommunityPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[var(--juba-bg)] text-[var(--juba-text)]">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-[var(--juba-violet)] py-20 text-white">
        <div className="absolute inset-0 juba-hero-glow opacity-30" />
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-3xl mx-auto"
          >
            <span className="juba-eyebrow inline-block mb-4">Community & Culture</span>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
              Learn Together, Grow Together
            </h1>
            <p className="text-xl text-white\/80 mb-8">
              Join weekly challenges, explore cultures, and connect with learners worldwide
            </p>
          </motion.div>
        </div>
      </section>

      {/* Weekly Challenge */}
      <section className="border-y-2 border-[var(--juba-lilac)] bg-white py-16">
        <div className="container mx-auto px-4">
          <WeeklyChallenge />
        </div>
      </section>

      {/* Cultural Exploration */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <h2 className="text-4xl font-bold mb-4 text-[var(--juba-text)]">
              Explore Cultures
            </h2>
            <p className="text-lg text-white\/80 max-w-2xl">
              Language is more than words—it's culture, traditions, and human connection.
            </p>
          </motion.div>

          <CulturalMap />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
            {culturalData.map((culture, index) => (
              <motion.div
                key={culture.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <CulturalCard {...culture} />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Social Learning Features */}
      <section className="py-16 bg-white dark:bg-slate-900">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
              Connect & Learn
            </h2>
            <p className="text-lg text-white\/80 max-w-2xl mx-auto">
              Join study groups, find language partners, and practice together
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Study Groups",
                description: "Join or create groups based on your level and goals",
                icon: "👥",
              },
              {
                title: "Language Exchange",
                description: "Find partners who want to learn your native language",
                icon: "🔄",
              },
              {
                title: "Live Sessions",
                description: "Participate in real-time practice sessions with tutors",
                icon: "🎤",
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="rounded-[28px] border-2 border-[var(--juba-lilac)] bg-white p-8 text-center shadow-[var(--juba-shadow-sm)] transition-transform hover:-translate-y-1"
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-3 text-slate-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-white\/80">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
