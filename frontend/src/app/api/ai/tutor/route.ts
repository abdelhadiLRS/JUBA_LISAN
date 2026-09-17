import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const SYSTEM_PROMPTS: Record<string, string> = {
  ar: "أنت مدرس لغوي ودود ومتخصص في تعليم اللغة العربية للناطقين بغيرها. تحدث باللغة العربية الفصحى بشكل واضح وبسيط. قدم تصحيحات لطيفة للأخطاء واقترح بدائل أفضل. شجع المستخدم على الاستمرار في المحادثة.",
  en: "You are a friendly language tutor specializing in teaching English as a foreign language. Speak in clear, simple English. Gently correct mistakes and suggest better alternatives. Encourage the user to continue the conversation.",
  de: "Sie sind ein freundlicher Sprachlehrer, der darauf spezialisiert ist, Deutsch als Fremdsprache zu unterrichten. Sprechen Sie in klarem, einfachem Deutsch. Korrigieren Sie Fehler sanft und schlagen Sie bessere Alternativen vor. Ermutigen Sie den Benutzer, das Gespräch fortzusetzen.",
  fr: "Vous êtes un tuteur de langue amical spécialisé dans l'enseignement du français langue étrangère. Parlez en français clair et simple. Corrigez gentiment les erreurs et suggérez de meilleures alternatives. Encouragez l'utilisateur à poursuivre la conversation.",
  es: "Eres un tutor de idiomas amigable especializado en enseñar español como lengua extranjera. Habla en español claro y sencillo. Corrige suavemente los errores y sugiere mejores alternativas. Anima al usuario a continuar la conversación.",
  it: "Sei un tutor linguistico amichevole specializzato nell'insegnamento dell'italiano come lingua straniera. Parla in italiano chiaro e semplice. Correggi delicatamente gli errori e suggerisci alternative migliori. Incoraggia l'utente a continuare la conversazione.",
  nl: "Je bent een vriendelijke taalleraar gespecialiseerd in het onderwijzen van Nederlands als vreemde taal. Spreek in duidelijk, eenvoudig Nederlands. Corrigeer fouten zachtjes en stel betere alternatieven voor. Moedig de gebruiker aan om het gesprek voort te zetten.",
  pl: "Jesteś przyjaznym nauczycielem języka specjalizującym się w nauczaniu polskiego jako języka obcego. Mów po polsku w sposób jasny i prosty. Delikatnie poprawiaj błędy i sugeruj lepsze alternatywy. Zachęcaj użytkownika do kontynuowania rozmowy.",
  pt: "Você é um tutor de idiomas amigável especializado em ensinar português como língua estrangeira. Fale em português claro e simples. Corrija gentilmente os erros e sugira melhores alternativas. Incentive o usuário a continuar a conversa.",
  ro: "Ești un tutore de limbă prietenos, specializat în predarea limbii române ca limbă străină. Vorbește în română clară și simplă. Corectează delicat greșelile și sugerează alternative mai bune. Încurajează utilizatorul să continue conversația.",
  ru: "Вы дружелюбный репетитор языка, специализирующийся на преподавании русского как иностранного. Говорите на простом и понятном русском языке. Мягко исправляйте ошибки и предлагайте лучшие альтернативы. Поощряйте пользователя продолжать разговор.",
};

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, language = "en", level = "intermediate", conversationHistory = [], userId } = body;

    if (!message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    // Check if API key is configured
    if (!process.env.OPENAI_API_KEY) {
      // Return mock response for development
      return NextResponse.json({
        response: `[وضع تجريبي] مرحباً! أنا مدربك اللغوي. قلت: "${message}". دعنا نواصل المحادثة باللغة ${language}.`,
        correction: null,
        suggestion: "Try to use more complex sentences.",
        translation: null,
        sessionId: `mock-session-${Date.now()}`,
      });
    }

    const systemPrompt = SYSTEM_PROMPTS[language] || SYSTEM_PROMPTS.en;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: systemPrompt },
        ...conversationHistory.slice(-10), // Last 10 messages
        { role: "user", content: message },
      ],
      temperature: 0.7,
      max_tokens: 300,
    });

    const aiResponse = completion.choices[0].message.content || "";

    // Generate correction and suggestion
    const analysisCompletion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `Analyze this language learning exchange. User said: "${message}". AI responded: "${aiResponse}". Provide:
1. Any corrections needed (null if none)
2. A suggestion for improvement
3. Translation to English if not already in English
Return as JSON: {"correction": string|null, "suggestion": string, "translation": string|null}`,
        },
      ],
      response_format: { type: "json_object" },
    });

    const analysis = JSON.parse(analysisCompletion.choices[0].message.content || "{}");

    // Save session to database if userId provided
    let savedSessionId = null;
    if (userId && process.env.DATABASE_URL) {
      try {
        const res = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/api/ai-sessions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId,
            languageCode: language,
            sessionType: 'conversation',
            messages: [...conversationHistory.slice(-10), { role: 'user', content: message }, { role: 'assistant', content: aiResponse }],
            feedback: analysis.suggestion,
          }),
        });
        const data = await res.json();
        savedSessionId = data.id;
      } catch (dbError) {
        console.error('Failed to save session:', dbError);
      }
    }

    return NextResponse.json({
      response: aiResponse,
      correction: analysis.correction,
      suggestion: analysis.suggestion,
      translation: analysis.translation,
      sessionId: savedSessionId || `session-${Date.now()}`,
    });
  } catch (error) {
    console.error("AI Tutor Error:", error);
    return NextResponse.json(
      { error: "Failed to process request", details: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 }
    );
  }
}
