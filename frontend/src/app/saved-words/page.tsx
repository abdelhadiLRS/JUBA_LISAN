'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, BookOpenCheck, RotateCcw, Trash2, Volume2 } from 'lucide-react'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { getGuestMemory, getGuestReviewState, type TranslatorSavedWord } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useLocale } from 'next-intl'

const REVIEW_KEY = 'juba_lisan_review_state'
type ReviewState = Record<string, { repetitions: number; interval: number; ease: number; due: number }>

function storeReview(value: ReviewState) {
  try { localStorage.setItem(REVIEW_KEY, JSON.stringify(value)) } catch {}
}

export default function SavedWordsPage() {
  const locale = useLocale()
  const isArabic = locale === 'ar'
  const user = useAuthStore((state) => state.user)
  const [words, setWords] = useState<TranslatorSavedWord[]>([])
  const [review, setReview] = useState<ReviewState>({})
  const [index, setIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)

  useEffect(() => {
    setWords(getGuestMemory())
    setReview(getGuestReviewState() as ReviewState)
  }, [])

  const dueWords = useMemo(
    () => words.filter((word) => !review[`${word.source}:${word.target}:${word.word}`] || review[`${word.source}:${word.target}:${word.word}`].due <= Date.now()),
    [words, review],
  )
  const current = dueWords[index]
  const key = current ? `${current.source}:${current.target}:${current.word}` : ''

  function remove(word: TranslatorSavedWord) {
    const next = words.filter((item) => !(item.word === word.word && item.target === word.target && item.source === word.source))
    setWords(next)
    try { localStorage.setItem('juba_lisan_saved_vocabulary', JSON.stringify(next)) } catch {}
    setIndex(0)
  }

  function rate(quality: number) {
    if (!current) return
    const previous = review[key] || { repetitions: 0, interval: 0, ease: 2.5, due: Date.now() }
    const repetitions = quality < 3 ? 0 : previous.repetitions + 1
    const interval = quality < 3
      ? 10 * 60 * 1000
      : Math.max(24 * 60 * 60 * 1000, (previous.interval || 24 * 60 * 60 * 1000) * (quality === 5 ? 3 : quality === 4 ? 2 : 1.3))
    const next = {
      ...review,
      [key]: {
        repetitions,
        interval,
        ease: Math.max(1.3, previous.ease + (quality >= 3 ? 0.1 : -0.2)),
        due: Date.now() + interval,
      },
    }
    setReview(next)
    storeReview(next)
    setRevealed(false)
    setIndex((value) => value + 1)
  }

  const copy = isArabic
    ? {
        visitor: 'وضع الزائر',
        title: 'الكلمات المحفوظة',
        subtitle: 'تبقى مفرداتك في هذا المتصفح حتى تختار مزامنتها مع حسابك.',
        translator: 'المترجم',
        start: 'ابدأ ببناء مفرداتك',
        startText: 'ترجم كلمة، اضغط «تعلّم هذه»، وستظهر هنا بدون الحاجة إلى إنشاء حساب.',
        openTranslator: 'فتح المترجم',
        collection: 'مجموعتك',
        signIn: 'تسجيل الدخول للمزامنة',
        accountVocabulary: 'مفردات الحساب',
        practice: 'تدريب',
        quickReview: 'مراجعة سريعة',
        due: 'مستحقة',
        translation: 'الترجمة',
        word: 'الكلمة',
        reveal: 'اضغط لإظهار الترجمة',
        again: 'مرة أخرى',
        good: 'جيد',
        easy: 'سهل',
        nothing: 'لا توجد كلمات مستحقة الآن.',
        later: 'عد لاحقًا أو أضف كلمات جديدة.',
        remove: 'حذف',
      }
    : {
        visitor: 'Visitor mode',
        title: 'Saved words',
        subtitle: 'Your vocabulary stays in this browser until you choose to sync it.',
        translator: 'Translator',
        start: 'Start building your vocabulary',
        startText: 'Translate a word, tap “Learn this”, and it will appear here without requiring an account.',
        openTranslator: 'Open translator',
        collection: 'Your collection',
        signIn: 'Sign in to sync',
        accountVocabulary: 'Account vocabulary',
        practice: 'Practice',
        quickReview: 'Quick review',
        due: 'due',
        translation: 'Translation',
        word: 'Word',
        reveal: 'Tap to reveal',
        again: 'Again',
        good: 'Good',
        easy: 'Easy',
        nothing: 'Nothing due right now.',
        later: 'Come back later or add more words.',
        remove: 'Remove',
      }

  return (
    <main dir={isArabic ? 'rtl' : 'ltr'} className="min-h-screen bg-[var(--juba-bg)] px-4 py-8 sm:px-6">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs font-black uppercase tracking-[.18em] text-[var(--juba-muted)]">JUBA LISAN · {copy.visitor}</p>
            <h1 className="mt-2 text-4xl font-black tracking-tight text-[var(--juba-text)]">{copy.title}</h1>
            <p className="mt-2 text-sm font-medium text-[var(--juba-muted)]">{copy.subtitle}</p>
          </div>
          <Link href="/" className="inline-flex items-center gap-2 rounded-full border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2.5 text-sm font-black text-[var(--juba-text)]"><ArrowLeft className="h-4 w-4 rtl:rotate-180" />{copy.translator}</Link>
        </header>
        {words.length === 0 ? (
          <section className="rounded-[32px] border-2 border-[var(--juba-border)] bg-[var(--juba-accent)] p-8 text-center shadow-[var(--juba-shadow-md)]">
            <BookOpenCheck className="mx-auto h-10 w-10" />
            <h2 className="mt-4 text-2xl font-black">{copy.start}</h2>
            <p className="mx-auto mt-2 max-w-md text-sm font-semibold text-neutral-800/70">{copy.startText}</p>
            <Link href="/" className="mt-6 inline-flex rounded-full border-2 border-neutral-950 bg-white px-5 py-3 text-sm font-black">{copy.openTranslator}</Link>
          </section>
        ) : (
          <div className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
            <section className="rounded-[32px] border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] p-5 shadow-[var(--juba-shadow-sm)]">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <h2 className="font-black">{copy.collection} <span className="text-[var(--juba-muted)]">({words.length})</span></h2>
                {user ? <Link href="/flashcards/vocabulary" className="rounded-full bg-[var(--juba-accent)] px-4 py-2 text-xs font-black text-neutral-950">{copy.accountVocabulary}</Link> : <Link href="/login" className="rounded-full bg-[var(--juba-text)] px-4 py-2 text-xs font-black text-[var(--juba-surface)]">{copy.signIn}</Link>}
              </div>
              <div className="space-y-2">
                {words.map((word) => (
                  <article key={`${word.source}:${word.target}:${word.word}`} className="flex items-center gap-3 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-2)] p-4">
                    <AudioPlayer text={word.word} size="sm" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-black text-[var(--juba-text)]">{word.word}</p>
                      <p className="truncate text-sm font-semibold text-[var(--juba-muted)]">{word.translation}</p>
                      <p className="mt-1 text-[10px] font-bold uppercase tracking-wider text-[var(--juba-muted)]">{word.source} → {word.target}</p>
                    </div>
                    <button type="button" onClick={() => remove(word)} aria-label={`${copy.remove} ${word.word}`} className="rounded-full p-2 text-[var(--juba-muted)] hover:bg-red-100 hover:text-red-700"><Trash2 className="h-4 w-4" /></button>
                  </article>
                ))}
              </div>
            </section>
            <section className="rounded-[32px] border-2 border-neutral-950 bg-[var(--juba-accent)] p-5 shadow-[5px_5px_0_rgba(17,17,17,.85)]">
              <div className="flex items-center justify-between"><div><p className="text-[10px] font-black uppercase tracking-[.18em] text-neutral-950/55">{copy.practice}</p><h2 className="mt-1 text-2xl font-black">{copy.quickReview}</h2></div><span className="rounded-full bg-neutral-950 px-3 py-1 text-xs font-black text-white">{dueWords.length} {copy.due}</span></div>
              {current ? (
                <>
                  <button type="button" onClick={() => setRevealed((value) => !value)} className="mt-5 min-h-56 w-full rounded-[26px] border-2 border-neutral-950 bg-white p-7 text-center">
                    <p className="text-xs font-black uppercase tracking-widest text-neutral-500">{revealed ? copy.translation : copy.word}</p>
                    <p className="mt-5 text-4xl font-black text-neutral-950">{revealed ? current.translation : current.word}</p>
                    <div className="mt-4 flex items-center justify-center gap-2 text-xs font-bold text-neutral-500"><Volume2 className="h-4 w-4" />{copy.reveal}</div>
                  </button>
                  {revealed && <div className="mt-3 grid grid-cols-3 gap-2"><button type="button" onClick={() => rate(0)} className="rounded-2xl border-2 border-neutral-950 bg-white px-3 py-3 text-xs font-black">{copy.again}</button><button type="button" onClick={() => rate(4)} className="rounded-2xl border-2 border-neutral-950 bg-white px-3 py-3 text-xs font-black">{copy.good}</button><button type="button" onClick={() => rate(5)} className="rounded-2xl border-2 border-neutral-950 bg-neutral-950 px-3 py-3 text-xs font-black text-white">{copy.easy}</button></div>}
                </>
              ) : (
                <div className="mt-5 rounded-[26px] border-2 border-neutral-950 bg-white/75 p-8 text-center"><RotateCcw className="mx-auto h-8 w-8" /><p className="mt-3 font-black">{copy.nothing}</p><p className="mt-1 text-sm font-semibold text-neutral-700">{copy.later}</p></div>
              )}
            </section>
          </div>
        )}
      </div>
    </main>
  )
}
