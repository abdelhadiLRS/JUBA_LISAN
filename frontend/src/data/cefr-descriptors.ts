export const CEFR_SKILLS = ['listening', 'reading', 'interaction', 'speaking', 'writing'] as const

export type CEFRSkill = (typeof CEFR_SKILLS)[number]

export const CEFR_DESCRIPTORS = {
  A1: {
    listening: 'Understand familiar words and very simple everyday phrases when speech is clear and slow.',
    reading: 'Recognize familiar names, words and short phrases in signs, labels and simple notices.',
    interaction: 'Introduce yourself and exchange basic personal information in short, supported conversations.',
    speaking: 'Use simple sentences to describe yourself, people you know and familiar places.',
    writing: 'Complete simple personal-information forms and write short messages or greetings.',
  },
  A2: {
    listening: 'Understand common expressions about personal information, shopping, work and the local environment.',
    reading: 'Understand short practical texts such as menus, schedules, notices and brief personal messages.',
    interaction: 'Exchange straightforward information about familiar activities and everyday topics.',
    speaking: 'Connect simple phrases to describe family, education, work, living conditions and routines.',
    writing: 'Write short notes and simple messages about familiar needs, experiences and plans.',
  },
  B1: {
    listening: 'Follow the main points of clearly spoken conversations about familiar work, study, social and current topics.',
    reading: 'Understand everyday and work-related texts, including descriptions of events, feelings and experiences.',
    interaction: 'Join conversations on familiar subjects, express preferences and manage common situations while travelling.',
    speaking: 'Link ideas to describe experiences, events, plans and ambitions, and give reasons for opinions.',
    writing: 'Write connected texts about familiar subjects and describe experiences, impressions and viewpoints.',
  },
  B2: {
    listening: 'Follow extended speech and lectures on familiar topics and understand most standard media content.',
    reading: 'Understand detailed articles and reports where writers present arguments, opinions and perspectives.',
    interaction: 'Interact with natural fluency and participate actively in discussions, developing and supporting ideas.',
    speaking: 'Give clear, detailed descriptions and explain viewpoints while weighing different options.',
    writing: 'Produce clear, detailed texts that develop an argument, explain information and emphasize important experiences.',
  },
  C1: {
    listening: 'Understand extended speech, including implicit connections, and follow demanding broadcasts and films with ease.',
    reading: 'Understand long, complex factual and literary texts, including specialized articles and technical instructions.',
    interaction: 'Communicate fluently and flexibly in social and professional situations, expressing ideas precisely.',
    speaking: 'Present complex subjects clearly, develop supporting points and build toward a coherent conclusion.',
    writing: 'Write well-structured, detailed texts on complex subjects while adapting style to the intended reader.',
  },
  C2: {
    listening: 'Understand virtually all spoken language, including rapid speech, subtle meaning and unfamiliar accents.',
    reading: 'Read almost all forms of written language with ease and recognize fine differences in style and meaning.',
    interaction: 'Take part effortlessly in demanding discussions, managing nuance, implication, humour and register.',
    speaking: 'Present and argue complex ideas with precision, coherence and natural flexibility.',
    writing: 'Write clear, sophisticated texts with precise structure, tone and style for demanding audiences.',
  },
} as const
