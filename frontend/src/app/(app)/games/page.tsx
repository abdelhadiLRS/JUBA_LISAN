'use client'

import { useEffect, useMemo, useState } from 'react'
import { useLocale, usePathname, useRouter } from 'next-intl'
import {
  ACHIEVEMENTS,
  type AchievementId,
} from '@/lib/games/achievements'
import {
  completeGameSession,
  startGameSession,
  gameLanguageForTargetLanguage,
  type GameSessionQuestion,
  type GameId,
} from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'
import './games.css'

type Lang = 'ar' | 'fr' | 'en' | 'es' | 'de' | 'it' | 'pt' | 'pl' | 'nl' | 'ro' | 'ru'
function getLocalDateKey() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
const DAILY_GAMES: GameId[] = ['matching', 'quick_choice', 'sentence_builder', 'listen_choose', 'spelling', 'word_scramble', 'fill_blank', 'memory', 'context_quest', 'listening_detective', 'word_categories', 'translation_sprint', 'grammar_duel']
const ROUND_SIZE = 5

const copy = {
  ar: {
    title: 'JUBA LISAN',
    subtitle: 'تعلّم باللعب، وتقدّم كل يوم',
    points: 'النقاط', streak: 'سلسلة', level: 'المستوى', games: 'الألعاب التعليمية',
    daily: 'تحدي اليوم', dailyDesc: 'تحدٍ واحد ثابت يوميًا. أكمله لتحصل على XP وتبني عادتك التعليمية.',
    wordMatch: 'مطابقة الكلمات', quickChoice: 'اختيار سريع', translationSprint: 'سباق الترجمة', grammarDuel: 'مبارزة القواعد', contextQuest: 'مهمة المواقف', sentenceBuilder: 'بناء الجملة',
    listenChoose: 'استمع واختر', listeningDetective: 'محقق الاستماع', wordCategories: 'تصنيف الكلمات', spelling: 'تحدي الإملاء', memory: 'بطاقات الذاكرة',
    wordMatchDesc: 'طابق الكلمة مع ترجمتها الصحيحة.', translationSprintDesc: 'ترجم بسرعة ودقة مع الحفاظ على المعنى والزمن.', grammarDuelDesc: 'اختبر دقة القواعد تحت ضغط الاختيار السريع.', quickChoiceDesc: 'اختر الإجابة قبل انتهاء الوقت.', contextQuestDesc: 'اختر الرد الطبيعي المناسب للموقف.',
    sentenceBuilderDesc: 'رتّب الكلمات لبناء جملة صحيحة.', listenChooseDesc: 'استمع إلى الكلمة ثم اخترها.', listeningDetectiveDesc: 'استمع إلى جملة والتقط المعلومة الأساسية.', wordCategoriesDesc: 'صنّف الكلمة ضمن الفئة الدلالية الصحيحة.',
    spellingDesc: 'اكتب الكلمة المطلوبة من التلميح.', wordScramble: 'ترتيب الحروف', fillBlank: 'أكمل الفراغ', wordScrambleDesc: 'رتّب الحروف لاستعادة الكلمة.', fillBlankDesc: 'اختر الكلمة الصحيحة لإكمال الجملة.', memoryDesc: 'اكشف البطاقات وطابق الأزواج الحقيقية.',
    start: 'ابدأ اللعبة', next: 'السؤال التالي', correct: 'إجابة صحيحة!', wrong: 'ليست صحيحة',
    hint: 'تلميح', back: 'الألعاب', score: 'نتيجة الجولة', done: 'أحسنت! أكملت الجولة.', choose: 'اختر الإجابة الصحيحة',
lang: 'اللغة', xp: 'XP', skills: 'المهارات', stats: 'إحصائياتك', gamesPlayed: 'الألعاب',
    questions: 'الأسئلة', accuracy: 'الدقة', best: 'أفضل نتيجة', badges: 'الإنجازات', unlocked: 'مفتوح', newBadge: 'إنجاز جديد!', answered: 'تم تسجيل إجابتك.',
  },
  fr: {
    title: 'JUBA LISAN', subtitle: 'Apprendre en jouant, progresser chaque jour', points: 'Points', streak: 'Série', level: 'Niveau',
    games: 'Jeux éducatifs', daily: 'Défi du jour', dailyDesc: 'Un défi fixe chaque jour pour gagner de l’XP et construire une habitude.',
    wordMatch: 'Association de mots', translationSprint: 'Sprint de traduction', grammarDuel: 'Duel de grammaire', quickChoice: 'Choix rapide', contextQuest: 'Mission situations', sentenceBuilder: 'Constructeur de phrases',
    listenChoose: 'Écoute et choisis', listeningDetective: 'Détective de l’écoute', wordCategories: 'Catégories de mots', spelling: 'Défi d’orthographe', memory: 'Cartes mémoire',
    wordMatchDesc: 'Associe chaque mot à sa bonne traduction.', translationSprintDesc: 'Traduis rapidement en gardant le sens et le temps.', grammarDuelDesc: 'Teste ta précision grammaticale avec des choix rapides.', quickChoiceDesc: 'Choisis avant la fin du temps.', contextQuestDesc: 'Choisis la réponse naturelle adaptée à la situation.',
    sentenceBuilderDesc: 'Remets les mots dans le bon ordre.', listenChooseDesc: 'Écoute le mot puis choisis-le.', listeningDetectiveDesc: 'Écoute une phrase et repère le détail clé.', wordCategoriesDesc: 'Classe le mot dans la bonne catégorie sémantique.',
    spellingDesc: 'Écris le mot demandé à partir de l’indice.', wordScramble: 'Mots mélangés', fillBlank: 'Texte à trous', wordScrambleDesc: 'Remets les lettres dans le bon ordre.', fillBlankDesc: 'Choisis le mot qui complète la phrase.', memoryDesc: 'Retourne les cartes et forme les vraies paires.', start: 'Commencer', next: 'Question suivante',
    correct: 'Bonne réponse !', wrong: 'Pas encore', hint: 'Indice', back: 'Jeux', score: 'Score de la partie', done: 'Bravo ! Partie terminée.',
    choose: 'Choisis la bonne réponse', lang: 'Langue', xp: 'XP', skills: 'Compétences', stats: 'Tes statistiques',
    gamesPlayed: 'Parties', questions: 'Questions', accuracy: 'Précision', best: 'Meilleur score', badges: 'Succès', unlocked: 'débloqué', newBadge: 'Nouveau succès !', answered: 'Réponse enregistrée.',
  },
  en: {
    title: 'JUBA LISAN', subtitle: 'Learn through play. Improve every day.', points: 'Points', streak: 'Streak', level: 'Level',
    games: 'Educational games', daily: 'Daily Challenge', dailyDesc: 'One consistent challenge each day. Complete it to earn XP and build your habit.',
    wordMatch: 'Word Match', translationSprint: 'Translation Sprint', grammarDuel: 'Grammar Duel', quickChoice: 'Quick Choice', contextQuest: 'Context Quest', sentenceBuilder: 'Sentence Builder',
    listenChoose: 'Listen & Choose', listeningDetective: 'Listening Detective', wordCategories: 'Word Categories', spelling: 'Spelling Challenge', memory: 'Memory Cards',
    wordMatchDesc: 'Match each word with its correct translation.', translationSprintDesc: 'Translate quickly while preserving meaning and tense.', grammarDuelDesc: 'Test grammar accuracy with fast choices.', quickChoiceDesc: 'Choose before the timer runs out.', contextQuestDesc: 'Choose the natural response for the situation.',
    sentenceBuilderDesc: 'Arrange the words to build a correct sentence.', listenChooseDesc: 'Listen to the word and choose it.', listeningDetectiveDesc: 'Listen to a sentence and identify the key detail.', wordCategoriesDesc: 'Place the word in the correct semantic category.',
    spellingDesc: 'Type the word requested by the clue.', wordScramble: 'Word Scramble', fillBlank: 'Fill the Blank', wordScrambleDesc: 'Unscramble the letters to recover the word.', fillBlankDesc: 'Choose the word that completes the sentence.', memoryDesc: 'Reveal cards and match the real pairs.', start: 'Start game', next: 'Next question',
    correct: 'Correct!', wrong: 'Not quite', hint: 'Hint', back: 'Games', score: 'Round score', done: 'Great job! Round complete.',
    choose: 'Choose the correct answer', lang: 'Language', xp: 'XP', skills: 'Skills', stats: 'Your stats',
    gamesPlayed: 'Games', questions: 'Questions', accuracy: 'Accuracy', best: 'Best score', badges: 'Achievements', unlocked: 'unlocked', newBadge: 'New achievement!', answered: 'Answer recorded.',
  },  es: {
    title: 'JUBA LISAN', subtitle: 'Aprende jugando. Mejora cada día.', points: 'Puntos', streak: 'Racha', level: 'Nivel', games: 'Juegos educativos',
    daily: 'Desafío diario', dailyDesc: 'Un desafío cada día para ganar XP y crear tu hábito.', wordMatch: 'Parejas de palabras', quickChoice: 'Elección rápida', contextQuest: 'Misión de contexto', sentenceBuilder: 'Constructor de frases',
    listenChoose: 'Escucha y elige', listeningDetective: 'Detective de escucha', wordCategories: 'Categorías de palabras', spelling: 'Desafío de ortografía', memory: 'Cartas de memoria',
    wordMatchDesc: 'Relaciona cada palabra con su traducción correcta.', quickChoiceDesc: 'Elige antes de que termine el tiempo.', contextQuestDesc: 'Elige la respuesta natural para la situación.', sentenceBuilderDesc: 'Ordena las palabras para formar una frase correcta.', listenChooseDesc: 'Escucha la palabra y elígela.', listeningDetectiveDesc: 'Escucha una frase e identifica el detalle clave.', wordCategoriesDesc: 'Coloca la palabra en la categoría semántica correcta.', spellingDesc: 'Escribe la palabra indicada por la pista.', wordScramble: 'Letras mezcladas', fillBlank: 'Completa el espacio', wordScrambleDesc: 'Ordena las letras para recuperar la palabra.', fillBlankDesc: 'Elige la palabra que completa la frase.', memoryDesc: 'Descubre las cartas y forma parejas.',
    start: 'Empezar', next: 'Siguiente pregunta', correct: '¡Correcto!', wrong: 'No exactamente', hint: 'Pista', back: 'Juegos', score: 'Puntuación de la ronda', done: '¡Muy bien! Ronda completada.', choose: 'Elige la respuesta correcta', lang: 'Idioma', xp: 'XP', skills: 'Habilidades', stats: 'Tus estadísticas', gamesPlayed: 'Partidas', questions: 'Preguntas', accuracy: 'Precisión', best: 'Mejor puntuación', badges: 'Logros', unlocked: 'desbloqueado', newBadge: '¡Nuevo logro!', answered: 'Respuesta registrada.',
  },
  de: {
    title: 'JUBA LISAN', subtitle: 'Lerne spielerisch. Werde jeden Tag besser.', points: 'Punkte', streak: 'Serie', level: 'Level', games: 'Lernspiele',
    daily: 'Tageschallenge', dailyDesc: 'Eine Challenge pro Tag, um XP zu verdienen und deine Lernroutine aufzubauen.', wordMatch: 'Wortpaare', quickChoice: 'Schnellauswahl', contextQuest: 'Kontext-Mission', sentenceBuilder: 'Satzbau',
    listenChoose: 'Hören & Wählen', listeningDetective: 'Hördetektiv', wordCategories: 'Wortkategorien', spelling: 'Rechtschreib-Challenge', memory: 'Memory-Karten',
    wordMatchDesc: 'Ordne jedes Wort seiner richtigen Übersetzung zu.', quickChoiceDesc: 'Wähle, bevor die Zeit abläuft.', contextQuestDesc: 'Wähle die natürliche Antwort für die Situation.', sentenceBuilderDesc: 'Ordne die Wörter zu einem korrekten Satz.', listenChooseDesc: 'Höre das Wort und wähle es aus.', listeningDetectiveDesc: 'Höre einen Satz und finde das wichtige Detail.', wordCategoriesDesc: 'Ordne das Wort der richtigen Bedeutungskategorie zu.', spellingDesc: 'Schreibe das gesuchte Wort anhand des Hinweises.', wordScramble: 'Buchstabensalat', fillBlank: 'Lückentext', wordScrambleDesc: 'Ordne die Buchstaben zum richtigen Wort.', fillBlankDesc: 'Wähle das Wort, das den Satz ergänzt.', memoryDesc: 'Decke Karten auf und finde die Paare.',
    start: 'Spiel starten', next: 'Nächste Frage', correct: 'Richtig!', wrong: 'Noch nicht', hint: 'Hinweis', back: 'Spiele', score: 'Rundenpunktzahl', done: 'Gut gemacht! Runde beendet.', choose: 'Wähle die richtige Antwort', lang: 'Sprache', xp: 'XP', skills: 'Fähigkeiten', stats: 'Deine Statistik', gamesPlayed: 'Spiele', questions: 'Fragen', accuracy: 'Genauigkeit', best: 'Beste Punktzahl', badges: 'Erfolge', unlocked: 'freigeschaltet', newBadge: 'Neuer Erfolg!', answered: 'Antwort gespeichert.',
  },
  it: {
    title: 'JUBA LISAN', subtitle: 'Impara giocando. Migliora ogni giorno.', points: 'Punti', streak: 'Serie', level: 'Livello', games: 'Giochi educativi',
    daily: 'Sfida del giorno', dailyDesc: 'Una sfida ogni giorno per guadagnare XP e creare una buona abitudine.', wordMatch: 'Abbinamento parole', quickChoice: 'Scelta rapida', contextQuest: 'Missione di contesto', sentenceBuilder: 'Costruttore di frasi',
    listenChoose: 'Ascolta e scegli', listeningDetective: 'Detective dell’ascolto', wordCategories: 'Categorie di parole', spelling: 'Sfida di ortografia', memory: 'Carte memoria',
    wordMatchDesc: 'Abbina ogni parola alla traduzione corretta.', quickChoiceDesc: 'Scegli prima che finisca il tempo.', contextQuestDesc: 'Scegli la risposta naturale per la situazione.', sentenceBuilderDesc: 'Metti le parole nell’ordine corretto.', listenChooseDesc: 'Ascolta la parola e sceglila.', listeningDetectiveDesc: 'Ascolta una frase e individua il dettaglio chiave.', wordCategoriesDesc: 'Inserisci la parola nella categoria semantica corretta.', spellingDesc: 'Scrivi la parola richiesta dall’indizio.', wordScramble: 'Lettere mescolate', fillBlank: 'Completa lo spazio', wordScrambleDesc: 'Riordina le lettere per trovare la parola.', fillBlankDesc: 'Scegli la parola che completa la frase.', memoryDesc: 'Scopri le carte e abbina le coppie.',
    start: 'Inizia', next: 'Domanda successiva', correct: 'Corretto!', wrong: 'Non proprio', hint: 'Suggerimento', back: 'Giochi', score: 'Punteggio del round', done: 'Ottimo! Round completato.', choose: 'Scegli la risposta corretta', lang: 'Lingua', xp: 'XP', skills: 'Abilità', stats: 'Le tue statistiche', gamesPlayed: 'Partite', questions: 'Domande', accuracy: 'Precisione', best: 'Miglior punteggio', badges: 'Obiettivi', unlocked: 'sbloccato', newBadge: 'Nuovo obiettivo!', answered: 'Risposta registrata.',
  },
  pt: {
    title: 'JUBA LISAN', subtitle: 'Aprenda jogando. Melhore todos os dias.', points: 'Pontos', streak: 'Sequência', level: 'Nível', games: 'Jogos educativos',
    daily: 'Desafio diário', dailyDesc: 'Um desafio por dia para ganhar XP e criar o seu hábito.', wordMatch: 'Combinação de palavras', quickChoice: 'Escolha rápida', contextQuest: 'Missão de contexto', sentenceBuilder: 'Construtor de frases',
    listenChoose: 'Ouça e escolha', listeningDetective: 'Detetive de escuta', wordCategories: 'Categorias de palavras', spelling: 'Desafio de ortografia', memory: 'Cartas de memória',
    wordMatchDesc: 'Associe cada palavra à tradução correta.', quickChoiceDesc: 'Escolha antes de o tempo acabar.', contextQuestDesc: 'Escolha a resposta natural para a situação.', sentenceBuilderDesc: 'Organize as palavras para formar uma frase correta.', listenChooseDesc: 'Ouça a palavra e escolha-a.', listeningDetectiveDesc: 'Ouça uma frase e identifique o detalhe principal.', wordCategoriesDesc: 'Coloque a palavra na categoria semântica correta.', spellingDesc: 'Escreva a palavra indicada pela pista.', wordScramble: 'Letras embaralhadas', fillBlank: 'Complete o espaço', wordScrambleDesc: 'Organize as letras para recuperar a palavra.', fillBlankDesc: 'Escolha a palavra que completa a frase.', memoryDesc: 'Revele as cartas e encontre os pares.',
    start: 'Começar', next: 'Próxima pergunta', correct: 'Correto!', wrong: 'Ainda não', hint: 'Dica', back: 'Jogos', score: 'Pontuação da rodada', done: 'Muito bem! Rodada concluída.', choose: 'Escolha a resposta correta', lang: 'Idioma', xp: 'XP', skills: 'Competências', stats: 'As suas estatísticas', gamesPlayed: 'Jogos', questions: 'Perguntas', accuracy: 'Precisão', best: 'Melhor pontuação', badges: 'Conquistas', unlocked: 'desbloqueado', newBadge: 'Nova conquista!', answered: 'Resposta registada.',
  },
  pl: {
    title: 'JUBA LISAN', subtitle: 'Ucz się przez zabawę. Rób postępy każdego dnia.', points: 'Punkty', streak: 'Seria', level: 'Poziom', games: 'Gry edukacyjne',
    daily: 'Wyzwanie dnia', dailyDesc: 'Jedno wyzwanie dziennie, aby zdobywać XP i budować nawyk.', wordMatch: 'Dopasowanie słów', quickChoice: 'Szybki wybór', contextQuest: 'Misja kontekstowa', sentenceBuilder: 'Budowanie zdań',
    listenChoose: 'Słuchaj i wybierz', listeningDetective: 'Detektyw słuchania', wordCategories: 'Kategorie słów', spelling: 'Wyzwanie ortograficzne', memory: 'Karty pamięci',
    wordMatchDesc: 'Dopasuj każde słowo do właściwego tłumaczenia.', quickChoiceDesc: 'Wybierz, zanim skończy się czas.', contextQuestDesc: 'Wybierz naturalną odpowiedź do sytuacji.', sentenceBuilderDesc: 'Ułóż słowa w poprawne zdanie.', listenChooseDesc: 'Posłuchaj słowa i wybierz je.', listeningDetectiveDesc: 'Posłuchaj zdania i znajdź kluczową informację.', wordCategoriesDesc: 'Umieść słowo w odpowiedniej kategorii znaczeniowej.', spellingDesc: 'Wpisz słowo na podstawie wskazówki.', wordScramble: 'Pomieszane litery', fillBlank: 'Uzupełnij lukę', wordScrambleDesc: 'Ułóż litery, aby odtworzyć słowo.', fillBlankDesc: 'Wybierz słowo uzupełniające zdanie.', memoryDesc: 'Odkrywaj karty i łącz pary.',
    start: 'Rozpocznij', next: 'Następne pytanie', correct: 'Dobrze!', wrong: 'Jeszcze nie', hint: 'Wskazówka', back: 'Gry', score: 'Wynik rundy', done: 'Świetnie! Runda ukończona.', choose: 'Wybierz poprawną odpowiedź', lang: 'Język', xp: 'XP', skills: 'Umiejętności', stats: 'Twoje statystyki', gamesPlayed: 'Gry', questions: 'Pytania', accuracy: 'Dokładność', best: 'Najlepszy wynik', badges: 'Osiągnięcia', unlocked: 'odblokowane', newBadge: 'Nowe osiągnięcie!', answered: 'Odpowiedź zapisana.',
  },
  nl: {
    title: 'JUBA LISAN', subtitle: 'Leer door te spelen. Word elke dag beter.', points: 'Punten', streak: 'Reeks', level: 'Niveau', games: 'Educatieve spellen',
    daily: 'Dagelijkse uitdaging', dailyDesc: 'Elke dag één uitdaging om XP te verdienen en een leergewoonte op te bouwen.', wordMatch: 'Woordkoppeling', quickChoice: 'Snelle keuze', contextQuest: 'Contextmissie', sentenceBuilder: 'Zinnen bouwen',
    listenChoose: 'Luister & kies', listeningDetective: 'Luisterdetective', wordCategories: 'Woordcategorieën', spelling: 'Spellinguitdaging', memory: 'Geheugenkaarten',
    wordMatchDesc: 'Koppel elk woord aan de juiste vertaling.', quickChoiceDesc: 'Kies voordat de tijd om is.', contextQuestDesc: 'Kies de natuurlijke reactie voor de situatie.', sentenceBuilderDesc: 'Zet de woorden in de juiste volgorde.', listenChooseDesc: 'Luister naar het woord en kies het.', listeningDetectiveDesc: 'Luister naar een zin en vind het belangrijkste detail.', wordCategoriesDesc: 'Plaats het woord in de juiste betekenisvolle categorie.', spellingDesc: 'Typ het gevraagde woord op basis van de hint.', wordScramble: 'Woordpuzzel', fillBlank: 'Vul de lege plek', wordScrambleDesc: 'Zet de letters in de juiste volgorde.', fillBlankDesc: 'Kies het woord dat de zin aanvult.', memoryDesc: 'Draai kaarten om en vind de paren.',
    start: 'Start spel', next: 'Volgende vraag', correct: 'Goed!', wrong: 'Nog niet', hint: 'Hint', back: 'Spellen', score: 'Rondescore', done: 'Goed gedaan! Ronde voltooid.', choose: 'Kies het juiste antwoord', lang: 'Taal', xp: 'XP', skills: 'Vaardigheden', stats: 'Jouw statistieken', gamesPlayed: 'Spellen', questions: 'Vragen', accuracy: 'Nauwkeurigheid', best: 'Beste score', badges: 'Prestaties', unlocked: 'vrijgespeeld', newBadge: 'Nieuwe prestatie!', answered: 'Antwoord opgeslagen.',
  },
  ro: {
    title: 'JUBA LISAN', subtitle: 'Învață prin joc. Progresează în fiecare zi.', points: 'Puncte', streak: 'Serie', level: 'Nivel', games: 'Jocuri educative',
    daily: 'Provocarea zilei', dailyDesc: 'O provocare zilnică pentru XP și pentru a-ți construi rutina.', wordMatch: 'Potrivește cuvintele', quickChoice: 'Alegere rapidă', contextQuest: 'Misiune de context', sentenceBuilder: 'Construiește propoziția',
    listenChoose: 'Ascultă și alege', listeningDetective: 'Detectiv de ascultare', wordCategories: 'Categorii de cuvinte', spelling: 'Provocare de ortografie', memory: 'Cărți de memorie',
    wordMatchDesc: 'Potrivește fiecare cuvânt cu traducerea corectă.', quickChoiceDesc: 'Alege înainte să expire timpul.', contextQuestDesc: 'Alege răspunsul natural pentru situație.', sentenceBuilderDesc: 'Aranjează cuvintele într-o propoziție corectă.', listenChooseDesc: 'Ascultă cuvântul și alege-l.', listeningDetectiveDesc: 'Ascultă o propoziție și identifică detaliul esențial.', wordCategoriesDesc: 'Pune cuvântul în categoria semantică potrivită.', spellingDesc: 'Scrie cuvântul cerut pe baza indiciului.', wordScramble: 'Litere amestecate', fillBlank: 'Completează spațiul', wordScrambleDesc: 'Rearanjează literele pentru a găsi cuvântul.', fillBlankDesc: 'Alege cuvântul care completează propoziția.', memoryDesc: 'Descoperă cărțile și potrivește perechile.',
    start: 'Începe jocul', next: 'Următoarea întrebare', correct: 'Corect!', wrong: 'Nu încă', hint: 'Indiciu', back: 'Jocuri', score: 'Scorul rundei', done: 'Bravo! Runda s-a încheiat.', choose: 'Alege răspunsul corect', lang: 'Limbă', xp: 'XP', skills: 'Abilități', stats: 'Statisticile tale', gamesPlayed: 'Jocuri', questions: 'Întrebări', accuracy: 'Precizie', best: 'Cel mai bun scor', badges: 'Realizări', unlocked: 'deblocat', newBadge: 'Realizare nouă!', answered: 'Răspuns înregistrat.',
  },
  ru: {
    title: 'JUBA LISAN', subtitle: 'Учись играя. Становись лучше каждый день.', points: 'Очки', streak: 'Серия', level: 'Уровень', games: 'Обучающие игры',
    daily: 'Задание дня', dailyDesc: 'Одно задание каждый день, чтобы получать XP и формировать привычку.', wordMatch: 'Сопоставление слов', quickChoice: 'Быстрый выбор', contextQuest: 'Контекстная миссия', sentenceBuilder: 'Составление предложений',
    listenChoose: 'Слушай и выбирай', listeningDetective: 'Детектив на слух', wordCategories: 'Категории слов', spelling: 'Орфографический вызов', memory: 'Карточки памяти',
    wordMatchDesc: 'Сопоставь слово с правильным переводом.', quickChoiceDesc: 'Выбери ответ до окончания времени.', contextQuestDesc: 'Выбери естественный ответ для ситуации.', sentenceBuilderDesc: 'Расставь слова в правильном порядке.', listenChooseDesc: 'Послушай слово и выбери его.', listeningDetectiveDesc: 'Послушай предложение и найди ключевую деталь.', wordCategoriesDesc: 'Помести слово в правильную смысловую категорию.', spellingDesc: 'Введи слово по подсказке.', wordScramble: 'Перемешанные буквы', fillBlank: 'Заполни пропуск', wordScrambleDesc: 'Расставь буквы, чтобы восстановить слово.', fillBlankDesc: 'Выбери слово, которое завершает предложение.', memoryDesc: 'Открывай карточки и находи пары.',
    start: 'Начать игру', next: 'Следующий вопрос', correct: 'Правильно!', wrong: 'Почти', hint: 'Подсказка', back: 'Игры', score: 'Счёт раунда', done: 'Отлично! Раунд завершён.', choose: 'Выбери правильный ответ', lang: 'Язык', xp: 'XP', skills: 'Навыки', stats: 'Твоя статистика', gamesPlayed: 'Игры', questions: 'Вопросы', accuracy: 'Точность', best: 'Лучший результат', badges: 'Достижения', unlocked: 'открыто', newBadge: 'Новое достижение!', answered: 'Ответ сохранён.',
  },

} as const

export default function GamesPage() {
  const locale = useLocale() as Lang
  const pathname = usePathname()
  const router = useRouter()
  const [lang, setLang] = useState<Lang>(locale)
  useEffect(() => setLang(locale), [locale])

  function changeInterfaceLanguage(value: Lang) {
    setLang(value)
    router.replace(pathname, { locale: value })
  }
  const [game, setGame] = useState<GameId | null>(null)
  const [dailyMode, setDailyMode] = useState(false)
  const [dailyChallengeDate, setDailyChallengeDate] = useState('')
  const [question, setQuestion] = useState<GameSessionQuestion | null>(null)
  const [sessionQuestions, setSessionQuestions] = useState<GameSessionQuestion[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [answers, setAnswers] = useState<Array<{ question_id: string; choice: string }>>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [roundScore, setRoundScore] = useState(0)
  const [round, setRound] = useState(0)
  const [newAchievements, setNewAchievements] = useState<AchievementId[]>([])
  const [inputValue, setInputValue] = useState('')
  const [timeLeft, setTimeLeft] = useState(8)
  const [roundResult, setRoundResult] = useState<{ score: number; correct: number; questions: number; xp: number } | null>(null)
  const [finishing, setFinishing] = useState(false)

  const {
    xp, streak, skills, gameStats, achievements, setProgress,
  } = useProgressStore()

  const level = Math.floor(xp / 100) + 1
  const t = copy[lang as keyof typeof copy] ?? copy.en
  const translationSprint = 'translationSprint' in t ? t.translationSprint : copy.en.translationSprint
  const translationSprintDesc = 'translationSprintDesc' in t ? t.translationSprintDesc : copy.en.translationSprintDesc
  const grammarDuel = 'grammarDuel' in t ? t.grammarDuel : copy.en.grammarDuel
  const grammarDuelDesc = 'grammarDuelDesc' in t ? t.grammarDuelDesc : copy.en.grammarDuelDesc
  const today = getLocalDateKey()
  const dailyCompletedToday = gameStats.lastDailyChallengeDate === today
  // The client mirrors only the deterministic display rotation; it never grants rewards.
  // Sunday=0..Saturday=6, and the server normalizes Python's weekday() to
  // the same numbering before applying the deterministic game rotation.
  const dayIndex = new Date(`${today}T00:00:00`).getDay()
  const dailyGame = DAILY_GAMES[dayIndex % DAILY_GAMES.length]
  const accuracy = gameStats.questionsAnswered
    ? Math.round((gameStats.correctAnswers / gameStats.questionsAnswered) * 100)
    : 0

  const direction = lang === 'ar' ? 'rtl' : 'ltr'

  function difficultyForGame(id: GameId) {
    const skill = id === 'matching' || id === 'quick_choice' || id === 'word_scramble' || id === 'word_categories' ? 'vocabulary'
      : id === 'context_quest' ? 'speaking'
      : id === 'word_categories' ? 'vocabulary'
      : id === 'listen_choose' || id === 'listening_detective' ? 'listening'
      : id === 'spelling' || id === 'translation_sprint' ? 'writing'
      : id === 'sentence_builder' || id === 'fill_blank' ? 'grammar'
      : 'memory'
    const mastery = skills[skill] ?? 0
    if (mastery < 0.4) return 1
    if (mastery < 0.75) return 2
    return 3
  }
  const gameCards = useMemo(
    () => [
      { id: 'matching' as const, title: t.wordMatch, desc: t.wordMatchDesc, icon: '🔗' },
      { id: 'quick_choice' as const, title: t.quickChoice, desc: t.quickChoiceDesc, icon: '⚡' },
      { id: 'context_quest' as const, title: t.contextQuest, desc: t.contextQuestDesc, icon: '🗣️' },
      { id: 'translation_sprint' as const, title: translationSprint, desc: translationSprintDesc, icon: '🌍' },
      { id: 'grammar_duel' as const, title: grammarDuel, desc: grammarDuelDesc, icon: '⚔️' },
      { id: 'sentence_builder' as const, title: t.sentenceBuilder, desc: t.sentenceBuilderDesc, icon: '🧩' },
      { id: 'listen_choose' as const, title: t.listenChoose, desc: t.listenChooseDesc, icon: '🎧' },
      { id: 'listening_detective' as const, title: t.listeningDetective, desc: t.listeningDetectiveDesc, icon: '🔎' },
      { id: 'word_categories' as const, title: t.wordCategories, desc: t.wordCategoriesDesc, icon: '🗂️' },
      { id: 'spelling' as const, title: t.spelling, desc: t.spellingDesc, icon: '✍️' },
      { id: 'word_scramble' as const, title: t.wordScramble, desc: t.wordScrambleDesc, icon: '🔤' },
      { id: 'fill_blank' as const, title: t.fillBlank, desc: t.fillBlankDesc, icon: '📝' },
      { id: 'memory' as const, title: t.memory, desc: t.memoryDesc, icon: '🧠' },
    ],
    [t]
  )

  const [gameError, setGameError] = useState<string | null>(null)

  async function startGame(id: GameId, daily = false) {
    if (daily && dailyCompletedToday) return
    setGameError(null)

    try {
      // Resolve the active target language before routing any game. The UI
      // locale is presentation-only and must never silently change the
      // language being learned.
      // A game session is persisted against the active study plan. Avoid
      // sending a request that can only return 404 when a learner has not
      // created a plan yet; send them to plan setup instead.
      const planResponse = await fetch('/api/study-plan/current', {
        credentials: 'include',
        cache: 'no-store',
      })
      if (!planResponse.ok) {
        window.location.assign('/plan')
        return
      }
      const plan = await planResponse.json().catch(() => null)
      if (!plan || typeof plan !== 'object' || !('id' in plan)) {
        window.location.assign('/plan')
        return
      }

      // Game content follows the active study plan's target language.
      // The interface locale remains independent, so changing UI language
      // does not unexpectedly switch what the learner is studying.
      const planRecord = plan as { target_language?: string; language?: string }
      const targetLanguage = planRecord.target_language ?? planRecord.language
      const contentLanguage = gameLanguageForTargetLanguage(targetLanguage)

      // Interactive games have their own board and completion flow. Pass the
      // study-plan language into those routes rather than the interface locale.
      if (id === 'memory' || id === 'matching' || id === 'sentence_builder') {
        const route = id === 'sentence_builder' ? 'sentence-builder' : id
        const difficulty = difficultyForGame(id)
        window.location.assign(`/games/${route}?lang=${contentLanguage}&difficulty=${difficulty}`)
        return
      }

      const session = await startGameSession(id, contentLanguage, difficultyForGame(id))
      setGame(id)
      setDailyMode(session.daily_challenge)
      setDailyChallengeDate(session.daily_challenge_date)
      setRound(0)
      setRoundScore(0)
      setSelected(null)
      setInputValue('')
      setTimeLeft(id === 'quick_choice' ? 8 : 0)
      setAnswers([])
      setSessionId(session.session_id)
      setSessionQuestions(session.questions)
      setNewAchievements([])
      setRoundResult(null)
      setFinishing(false)
      setQuestion(session.questions[0] ?? null)
    } catch (error) {
      console.error('[JUBA LISAN] Game session start failed:', error)
      setGame(null)
      setQuestion(null)
      setSessionId(null)
      setGameError(error instanceof Error ? error.message : 'Unable to load the challenge')
    }
  }

  function answer(choice: string) {
    if (!question || selected) return
    setSelected(choice)
    setAnswers((current) => [...current, { question_id: question.id, choice }])
  }

  function submitTextAnswer() {
    if (!question || selected || !inputValue.trim()) return
    setSelected(inputValue.trim())
    setAnswers((current) => [...current, { question_id: question.id, choice: inputValue.trim() }])
  }

  useEffect(() => {
    if (!game || !question || selected || game !== 'quick_choice') return
    setTimeLeft(8)
    const timer = window.setInterval(() => {
      setTimeLeft((value) => {
        if (value <= 1) {
          window.clearInterval(timer)
          setSelected('__timeout__')
          setAnswers((current) => [...current, { question_id: question.id, choice: '__timeout__' }])
          return 0
        }
        return value - 1
      })
    }, 1000)
    return () => window.clearInterval(timer)
  }, [game, question, selected])

  function playAudio() {
    if (!question?.audio_text || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(question.audio_text)
    utterance.lang = question.audio_language || 'en-GB'
    utterance.rate = 0.9
    window.speechSynthesis.speak(utterance)
  }

  async function finishRound() {
    if (!sessionId || finishing) return
    setFinishing(true)
    const previousAchievements = new Set(achievements)
    try {
      const server = await completeGameSession(
        sessionId,
        answers,
        dailyMode,
        dailyMode ? dailyChallengeDate : '',
      )
      const fresh = (server.new_achievements as AchievementId[]).filter(
        (id) => !previousAchievements.has(id)
      )
      if (fresh.length) setNewAchievements(fresh)
      setRoundScore(server.round_score)
      setRoundResult({ score: server.round_score, correct: server.round_correct, questions: server.round_questions, xp: server.xp_earned })
      setProgress({
        streak,
        xp: server.total_xp,
        skills: server.skills,
        gameStats: {
          gamesPlayed: server.games_played,
          questionsAnswered: server.questions_answered,
          correctAnswers: server.correct_answers,
          bestRoundScore: server.best_round_score,
          dailyChallengesCompleted: server.daily_challenges_completed,
          lastDailyChallengeDate: server.last_daily_challenge_date,
          currentCorrectStreak: server.current_correct_streak,
          bestCorrectStreak: server.best_correct_streak,
        },
        achievements: server.achievements as AchievementId[],
      })
    } catch (error) {
      setGameError(error instanceof Error ? error.message : 'Unable to save the round')
    } finally {
      setFinishing(false)
    }
  }

  function next() {
    if (!game || !question) return
    if (round >= ROUND_SIZE - 1) {
      void finishRound()
      return
    }
    const nextRound = round + 1
    setRound(nextRound)
    setSelected(null)
    setInputValue('')
    setQuestion(sessionQuestions[nextRound] ?? null)
  }

  return (
    <main className="juba-games" dir={direction}>
      <section className="games-shell">
        <header className="games-header">
          <div>
            <div className="games-brand">{t.title}</div>
            <h1>{t.subtitle}</h1>
          </div>
          <div className="language-control">
            <span>{t.lang}</span>
            {(['ar', 'fr', 'en', 'es', 'de', 'it', 'pt', 'pl', 'nl', 'ro', 'ru'] as Lang[]).map((value) => (
              <button type="button" key={value} className={lang === value ? 'active' : ''} onClick={() => changeInterfaceLanguage(value)}>
                {value.toUpperCase()}
              </button>
            ))}
          </div>
        </header>

        <section className="stats-grid" aria-label={t.stats}>
          <div><span>⭐</span><strong>{xp}</strong><small>{t.points}</small></div>
          <div><span>🔥</span><strong>{streak}</strong><small>{t.streak}</small></div>
          <div><span>🏆</span><strong>{level}</strong><small>{t.level}</small></div>
        </section>

        {!game ? (
          <>
            {gameError && (
              <div className="feedback" role="alert">
                <strong>{lang === 'ar' ? 'تعذر تحميل اللعبة' : lang === 'fr' ? 'Impossible de charger le jeu' : 'Unable to load the game'}</strong>
                <span>{gameError}</span>
              </div>
            )}
            <div className="achievement-toast" style={{ display: newAchievements.length ? 'block' : 'none' }}>
              🏅 <strong>{t.newBadge}</strong> {newAchievements.map((id) => ACHIEVEMENTS[id].title).join(' · ')}
            </div>
            <button type="button" className={`daily-challenge${dailyCompletedToday ? ' completed' : ''}`} onClick={() => startGame(dailyGame, true)} disabled={dailyCompletedToday} aria-disabled={dailyCompletedToday}>
              <span className="daily-icon">📅</span>
              <span><strong>{t.daily}</strong><small>{t.dailyDesc}</small></span>
              <span className="start">{dailyCompletedToday ? '✓' : t.start} {dailyCompletedToday ? '' : '→'}</span>
            </button>

            <div className="section-heading">
              <h2>{t.games}</h2>
            </div>

            <section className="game-grid">
              {gameCards.map((card) => (
                <button type="button" key={card.id} className="game-card" onClick={() => startGame(card.id)}>
                  <span className="game-icon">{card.icon}</span>
                  <span className="game-title">{card.title}</span>
                  <span className="game-desc">{card.desc}</span>
                  <span className="start">{t.start} →</span>
                </button>
              ))}
            </section>

            <section className="games-dashboard">
              <div className="games-panel">
                <h3>{t.stats}</h3>
                <div className="mini-stats">
                  <span><b>{gameStats.gamesPlayed}</b>{t.gamesPlayed}</span>
                  <span><b>{gameStats.questionsAnswered}</b>{t.questions}</span>
                  <span><b>{accuracy}%</b>{t.accuracy}</span>
                  <span><b>{gameStats.bestRoundScore}</b>{t.best}</span>
                </div>
              </div>
              <div className="games-panel">
                <h3>{t.badges}</h3>
                <div className="badges">
                  {Object.entries(ACHIEVEMENTS).map(([id, badge]) => (
                    <span
                      key={id}
                      className={achievements.includes(id as AchievementId) ? 'badge unlocked' : 'badge'}
                      title={badge.description}
                    >
                      🏅 {badge.title}{achievements.includes(id as AchievementId) ? ` · ${t.unlocked}` : ''}
                    </span>
                  ))}
                </div>
              </div>
            </section>

            <div className="games-skill-summary">
              <strong>{t.skills}</strong>
              {Object.entries(skills).map(([skill, value]) => (
                <span key={skill}>{skill}: {Math.round(value * 100)}%</span>
              ))}
            </div>
          </>
        ) : (
          <section className="play-card">
            <button type="button" className="back" onClick={() => { setGame(null); setDailyMode(false); setQuestion(null); setSessionId(null); setInputValue(''); setRoundResult(null) }}>← {t.back}</button>
            <div className="round-meta">{dailyMode ? `📅 ${t.daily} · ` : ''}{round + 1} / {ROUND_SIZE} · +XP</div>
            {question && (
              <>
                <h2 style={{ whiteSpace: 'pre-line' }}>{question.prompt}</h2>
                {game === 'quick_choice' && !selected && <div className="quick-timer" aria-live="polite">⏱ {timeLeft}s</div>}
                {(game === 'listen_choose' || game === 'listening_detective') && (
                  <button type="button" className="audio-play" onClick={playAudio}>🎧 {lang === 'ar' ? 'تشغيل الصوت' : lang === 'fr' ? 'Écouter' : 'Play audio'}</button>
                )}
                {question.input_mode === 'text' ? (
                  <form className="spelling-form" onSubmit={(event) => { event.preventDefault(); submitTextAnswer() }}>
                    <input value={inputValue} onChange={(event) => setInputValue(event.target.value)} placeholder={lang === 'ar' ? 'اكتب الإجابة' : lang === 'fr' ? 'Écris ta réponse' : 'Type your answer'} autoComplete="off" disabled={Boolean(selected)} />
                    <button type="submit" className="next" disabled={Boolean(selected) || !inputValue.trim()}>{lang === 'ar' ? 'تحقق' : lang === 'fr' ? 'Vérifier' : 'Check'}</button>
                  </form>
                ) : (
                  <>
                    <p className="choose">{t.choose}</p>
                    <div className="choices">
                      {question.choices.map((choice) => {
                        const state = selected === choice ? 'selected' : ''
                        return (
                          <button type="button" key={choice} className={`choice ${state}`} onClick={() => answer(choice)} disabled={Boolean(selected)}>
                            {choice}
                          </button>
                        )
                      })}
                    </div>
                  </>
                )}
                {selected && (
                  <div className="feedback good">
                    <strong>{selected === '__timeout__' ? '⏱ Time!' : t.answered}</strong>
                    <span>{question.hint}</span>
                  </div>
                )}
                {selected && <button type="button" className="next" onClick={next} disabled={finishing}>{round >= ROUND_SIZE - 1 ? (finishing ? '…' : t.done) : t.next} →</button>}
              </>
            )}
            <div className="round-score">{t.score}: <strong>{roundScore}</strong></div>
            {roundResult && (
              <div className="feedback good" role="status">
                <strong>{lang === 'ar' ? '🎉 نتيجة الجولة' : lang === 'fr' ? '🎉 Résultat de la partie' : '🎉 Round result'}</strong>
                <span>
                  {roundResult.correct}/{roundResult.questions} · {roundResult.score} pts · +{roundResult.xp} XP
                </span>
                <button
                  type="button"
                  className="next"
                  onClick={() => {
                    setGame(null)
                    setDailyMode(false)
                    setDailyChallengeDate('')
                    setQuestion(null)
                    setSessionId(null)
                    setRoundResult(null)
                    setAnswers([])
                  }}
                >
                  {t.back} →
                </button>
              </div>
            )}
          </section>
        )}
      </section>
    </main>
  )
}
