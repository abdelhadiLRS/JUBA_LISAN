export const CEFR_SKILLS = ['listening', 'reading', 'interaction', 'speaking', 'writing'] as const

export type CEFRSkill = (typeof CEFR_SKILLS)[number]

export const CEFR_DESCRIPTORS = {
  en: {
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
  },
  ar: {
    A1: {
      listening: 'فهم الكلمات المألوفة والعبارات اليومية شديدة البساطة عندما يكون الكلام واضحًا وبطيئًا.',
      reading: 'التعرف على الأسماء والكلمات والعبارات القصيرة المألوفة في اللافتات والملصقات والإعلانات البسيطة.',
      interaction: 'التعريف بالنفس وتبادل المعلومات الشخصية الأساسية في محادثات قصيرة ومدعومة.',
      speaking: 'استخدام جمل بسيطة لوصف النفس والأشخاص المعروفين والأماكن المألوفة.',
      writing: 'ملء بيانات شخصية أساسية وكتابة رسائل قصيرة أو عبارات تحية.',
    },
    A2: {
      listening: 'فهم العبارات الشائعة المتعلقة بالمعلومات الشخصية والتسوق والعمل والبيئة المحلية.',
      reading: 'فهم نصوص عملية قصيرة مثل قوائم الطعام والجداول والإعلانات والرسائل الشخصية الموجزة.',
      interaction: 'تبادل معلومات مباشرة حول الأنشطة المألوفة والموضوعات اليومية.',
      speaking: 'ربط عبارات بسيطة لوصف العائلة والتعليم والعمل وظروف المعيشة والروتين اليومي.',
      writing: 'كتابة ملاحظات ورسائل قصيرة وبسيطة حول الاحتياجات والتجارب والخطط المألوفة.',
    },
    B1: {
      listening: 'متابعة الأفكار الرئيسية في محادثات واضحة حول العمل والدراسة والمجتمع والموضوعات الجارية المألوفة.',
      reading: 'فهم النصوص اليومية والمتعلقة بالعمل، بما فيها أوصاف الأحداث والمشاعر والتجارب.',
      interaction: 'المشاركة في محادثات حول موضوعات مألوفة والتعبير عن التفضيلات والتعامل مع مواقف السفر المعتادة.',
      speaking: 'ربط الأفكار لوصف التجارب والأحداث والخطط والطموحات وشرح أسباب الآراء.',
      writing: 'كتابة نصوص مترابطة حول موضوعات مألوفة ووصف التجارب والانطباعات ووجهات النظر.',
    },
    B2: {
      listening: 'متابعة الكلام المطول والمحاضرات حول موضوعات مألوفة وفهم معظم المحتوى الإعلامي باللغة المعيارية.',
      reading: 'فهم المقالات والتقارير التفصيلية التي تعرض حججًا وآراء ووجهات نظر.',
      interaction: 'التفاعل بطلاقة طبيعية والمشاركة الفعالة في النقاشات مع تطوير الأفكار ودعمها.',
      speaking: 'تقديم أوصاف واضحة ومفصلة وشرح وجهات النظر مع موازنة الخيارات المختلفة.',
      writing: 'إنتاج نصوص واضحة ومفصلة تعرض حجة أو معلومات وتبرز التجارب والأفكار المهمة.',
    },
    C1: {
      listening: 'فهم الكلام المطول والروابط الضمنية ومتابعة البرامج والأفلام الصعبة بسهولة.',
      reading: 'فهم النصوص الواقعية والأدبية الطويلة والمعقدة، بما فيها المقالات التخصصية والتعليمات التقنية.',
      interaction: 'التواصل بطلاقة ومرونة في المواقف الاجتماعية والمهنية وصياغة الأفكار بدقة.',
      speaking: 'عرض موضوعات معقدة بوضوح وتطوير النقاط الداعمة والوصول إلى نتيجة مترابطة.',
      writing: 'كتابة نصوص واضحة ومنظمة ومفصلة حول موضوعات معقدة مع تكييف الأسلوب للقارئ.',
    },
    C2: {
      listening: 'فهم اللغة المنطوقة تقريبًا بكل أشكالها، بما فيها الكلام السريع والمعاني الدقيقة واللهجات غير المألوفة.',
      reading: 'قراءة معظم أشكال النصوص بسهولة والتمييز بين الفروق الدقيقة في الأسلوب والمعنى.',
      interaction: 'المشاركة بسلاسة في النقاشات المتقدمة وفهم الدلالات والإيحاءات والفكاهة ومستويات اللغة.',
      speaking: 'عرض الأفكار المعقدة ومناقشتها بدقة وترابط ومرونة طبيعية.',
      writing: 'كتابة نصوص متقدمة واضحة ودقيقة في بنيتها ونبرتها وأسلوبها بما يلائم القراء المتخصصين.',
    },
  },
} as const
