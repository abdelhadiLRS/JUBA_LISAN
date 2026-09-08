import React, { useCallback, useEffect, useMemo, useState } from 'react'
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native'
import { StatusBar } from 'expo-status-bar'
import {
  apiFetch,
  clearToken,
  getToken,
  login,
  me,
  progress,
  todayPlan,
  type ProgressSummary,
  type User,
} from './api'

const C = {
  bg: '#F7F8FC',
  card: '#FFFFFF',
  ink: '#171820',
  muted: '#777986',
  line: '#E6E7EF',
  primary: '#635BFF',
  primarySoft: '#EEEDFF',
  navy: '#20213A',
  soft: '#F1F2F7',
  danger: '#B42318',
}

type Tab = 'Home' | 'Learn' | 'Speak' | 'Review' | 'Progress'
const TABS: Array<[Tab, string]> = [
  ['Home', '⌂'],
  ['Learn', '◫'],
  ['Speak', '◉'],
  ['Review', '✦'],
  ['Progress', '↗'],
]

type TodayLesson = {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  is_completed?: boolean
}

type Flashcard = {
  id: number
  word: string
  translation?: string
  definition?: string
  example_sentence?: string
  repetitions?: number
}

function percent(value: number | undefined) {
  return Math.round(Math.max(0, Math.min(1, value ?? 0)) * 100)
}

function Bar({ label, value }: { label: string; value: number }) {
  return (
    <View style={s.barWrap}>
      <View style={s.between}>
        <Text style={s.body}>{label}</Text>
        <Text style={s.pct}>{value}%</Text>
      </View>
      <View style={s.track}>
        <View style={[s.fill, { width: `${value}%` }]} />
      </View>
    </View>
  )
}

function Header({ title, sub }: { title: string; sub: string }) {
  return (
    <View style={s.header}>
      <View style={s.logo}>
        <Text style={s.logoText}>J</Text>
      </View>
      <View>
        <Text style={s.eyebrow}>{sub}</Text>
        <Text style={s.headerTitle}>{title}</Text>
      </View>
    </View>
  )
}

function Nav({ tab, setTab }: { tab: Tab; setTab: (tab: Tab) => void }) {
  return (
    <View style={s.nav}>
      {TABS.map(([name, icon]) => (
        <Pressable key={name} onPress={() => setTab(name)} style={s.navItem}>
          <Text style={[s.navIcon, name === tab && s.active]}>{icon}</Text>
          <Text style={[s.navText, name === tab && s.active]}>{name}</Text>
        </Pressable>
      ))}
    </View>
  )
}

function Home({
  user,
  summary,
  lessons,
  setTab,
}: {
  user: User
  summary: ProgressSummary
  lessons: TodayLesson[]
  setTab: (tab: Tab) => void
}) {
  const name = user.displayName?.split(' ')[0] || user.username || 'Learner'
  const accuracy = percent(summary.accuracy)
  const vocabulary = percent(summary.vocabulary_progress)
  const nextLesson = lessons.find((lesson) => lesson.id != null && !lesson.is_completed)

  return (
    <ScrollView contentContainerStyle={s.content}>
      <View style={s.top}>
        <View>
          <Text style={s.eyebrow}>YOUR LEARNING SPACE</Text>
          <Text style={s.title}>Hi, {name} 👋</Text>
        </View>
        <View style={s.avatar}>
          <Text style={s.avatarText}>{name[0]?.toUpperCase() || 'J'}</Text>
        </View>
      </View>

      <View style={s.hero}>
        <Text style={s.pill}>✦ AI COACH</Text>
        <Text style={s.heroTitle}>Your next best step is ready.</Text>
        <Text style={s.heroBody}>
          Practice from your real study plan, with progress shared with the web app.
        </Text>
        <Pressable onPress={() => setTab(nextLesson ? 'Learn' : 'Speak')} style={s.heroBtn}>
          <Text style={s.heroBtnText}>{nextLesson ? 'Continue lesson →' : 'Practice speaking →'}</Text>
        </Pressable>
      </View>

      <View style={s.grid}>
        <View style={s.stat}>
          <Text style={s.statIcon}>🔥</Text>
          <Text style={s.statValue}>{summary.current_streak ?? 0}</Text>
          <Text style={s.statLabel}>day streak</Text>
        </View>
        <View style={s.stat}>
          <Text style={s.statIcon}>⚡</Text>
          <Text style={s.statValue}>{summary.total_xp ?? 0}</Text>
          <Text style={s.statLabel}>XP</Text>
        </View>
        <View style={s.stat}>
          <Text style={s.statIcon}>◈</Text>
          <Text style={s.statValue}>{summary.vocabulary_mastered ?? 0}</Text>
          <Text style={s.statLabel}>words</Text>
        </View>
        <View style={s.stat}>
          <Text style={s.statIcon}>✓</Text>
          <Text style={s.statValue}>{accuracy}%</Text>
          <Text style={s.statLabel}>accuracy</Text>
        </View>
      </View>

      {nextLesson && (
        <>
          <Text style={s.section}>Continue learning</Text>
          <View style={s.card}>
            <Text style={s.pillText}>
              WEEK {nextLesson.week} · DAY {nextLesson.day} · {nextLesson.lesson_type.toUpperCase()}
            </Text>
            <Text style={s.cardTitle}>{nextLesson.title}</Text>
            <Text style={s.body}>This lesson comes directly from your current study plan.</Text>
            <Pressable onPress={() => setTab('Learn')} style={s.linkButton}>
              <Text style={s.link}>Open lesson →</Text>
            </Pressable>
          </View>
        </>
      )}

      <Text style={s.section}>Your progress</Text>
      <View style={s.card}>
        <Bar label="Vocabulary" value={vocabulary} />
        <Bar label="Accuracy" value={accuracy} />
        <Bar label="Overall" value={Math.max(vocabulary, accuracy)} />
      </View>
    </ScrollView>
  )
}

function Learn({ lessons, loading, error }: { lessons: TodayLesson[]; loading: boolean; error: string }) {
  return (
    <ScrollView contentContainerStyle={s.content}>
      <Header title="Learning path" sub="YOUR CURRICULUM" />
      <View style={s.card}>
        <Text style={s.pillText}>TODAY</Text>
        <Text style={s.cardTitle}>Your real study plan</Text>
        <Text style={s.body}>
          Lessons below are loaded from the JUBA LISAN backend instead of demo content.
        </Text>
      </View>
      {loading && <ActivityIndicator color={C.primary} style={{ marginTop: 30 }} />}
      {!!error && <Text style={s.error}>{error}</Text>}
      {!loading && !lessons.length && (
        <View style={s.card}>
          <Text style={s.cardTitle}>No lessons scheduled</Text>
          <Text style={s.body}>Open the web app to create or update your study plan.</Text>
        </View>
      )}
      {lessons.map((lesson) => (
        <View key={`${lesson.id ?? 'x'}-${lesson.week}-${lesson.day}`} style={s.row}>
          <View style={[s.iconBox, lesson.is_completed && s.iconDone]}>
            <Text style={s.icon}>{lesson.is_completed ? '✓' : '◉'}</Text>
          </View>
          <View style={s.rowBody}>
            <Text style={s.cardTitle}>{lesson.title}</Text>
            <Text style={s.body}>
              W{lesson.week} · D{lesson.day} · {lesson.lesson_type}
            </Text>
          </View>
          <Text style={lesson.is_completed ? s.doneText : s.chev}>
            {lesson.is_completed ? 'Done' : '›'}
          </Text>
        </View>
      ))}
    </ScrollView>
  )
}

function Speak() {
  return (
    <ScrollView contentContainerStyle={s.content}>
      <Header title="AI Conversation" sub="VOICE-FIRST LEARNING" />
      <View style={s.speak}>
        <View style={s.tutor}><Text style={s.tutorMark}>✦</Text></View>
        <Text style={s.cardTitle}>Lingu</Text>
        <Text style={s.body}>Your AI language tutor</Text>
        <View style={s.prompt}>
          <Text style={s.pillText}>YOUR TURN</Text>
          <Text style={s.promptText}>Tell me about your day in 2–3 sentences.</Text>
        </View>
        <View style={s.wave}>
          {[18, 30, 44, 25, 52, 35, 62, 28, 46, 34, 58, 24].map((height, i) => (
            <View key={i} style={[s.waveBar, { height }]} />
          ))}
        </View>
      </View>
      <Text style={s.status}>Microphone-ready UI</Text>
      <Pressable style={s.mic} accessibilityLabel="Start speaking">
        <Text style={{ fontSize: 28 }}>🎙️</Text>
      </Pressable>
      <Text style={s.bodyCenter}>Voice capture will be wired to the conversation endpoint next.</Text>
      <View style={s.scores}>
        {['Pronunciation', 'Grammar', 'Fluency'].map((label) => (
          <View key={label} style={s.scoreCard}>
            <Text style={s.scoreValue}>—</Text>
            <Text style={s.scoreLabel}>{label}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  )
}

function Review({ loading, cards, error, refresh }: { loading: boolean; cards: Flashcard[]; error: string; refresh: () => void }) {
  const [index, setIndex] = useState(0)
  const card = cards[index]

  useEffect(() => setIndex(0), [cards.length])

  const review = async (quality: number) => {
    if (!card) return
    const res = await apiFetch(`/api/flashcards/${card.id}/review`, {
      method: 'POST',
      body: JSON.stringify({ quality }),
    })
    if (!res.ok) return
    if (index + 1 >= cards.length) refresh()
    else setIndex((value) => value + 1)
  }

  return (
    <ScrollView contentContainerStyle={s.content}>
      <Header title="Smart Review" sub="SPACED REPETITION" />
      <Text style={s.pillText}>DUE NOW</Text>
      <Text style={s.title}>{cards.length} cards</Text>
      {loading && <ActivityIndicator color={C.primary} style={{ marginTop: 30 }} />}
      {!!error && <Text style={s.error}>{error}</Text>}
      {!loading && !card && (
        <View style={s.flash}>
          <Text style={s.word}>All caught up 🎉</Text>
          <Text style={s.bodyCenter}>There are no flashcards due right now.</Text>
          <Pressable onPress={refresh} style={s.primaryButton}>
            <Text style={s.primaryButtonText}>Refresh</Text>
          </Pressable>
        </View>
      )}
      {card && (
        <>
          <View style={s.flash}>
            <Text style={s.word}>{card.word}</Text>
            <Text style={s.meaning}>{card.translation || card.definition || '—'}</Text>
            {!!card.example_sentence && <Text style={s.example}>{card.example_sentence}</Text>}
            <Text style={s.cardMeta}>Card {index + 1} of {cards.length}</Text>
          </View>
          <View style={s.two}>
            <Pressable onPress={() => review(0)} style={s.review}><Text>Again</Text></Pressable>
            <Pressable onPress={() => review(3)} style={s.review}><Text>Hard</Text></Pressable>
            <Pressable onPress={() => review(4)} style={[s.review, s.reviewMain]}><Text style={{ color: '#fff', fontWeight: '900' }}>Good</Text></Pressable>
            <Pressable onPress={() => review(5)} style={s.review}><Text>Easy</Text></Pressable>
          </View>
        </>
      )}
    </ScrollView>
  )
}

function ProgressScreen({ summary }: { summary: ProgressSummary }) {
  const accuracy = percent(summary.accuracy)
  const vocabulary = percent(summary.vocabulary_progress)
  return (
    <ScrollView contentContainerStyle={s.content}>
      <Header title="Progress" sub="YOUR JOURNEY" />
      <View style={s.heroLight}>
        <Text style={s.pillText}>CURRENT MOMENTUM</Text>
        <Text style={s.big}>{summary.total_xp ?? 0} XP</Text>
        <Text style={s.body}>🔥 {summary.current_streak ?? 0} day streak</Text>
      </View>
      <Text style={s.section}>Skill growth</Text>
      <View style={s.card}>
        <Bar label="Vocabulary" value={vocabulary} />
        <Bar label="Accuracy" value={accuracy} />
        <Bar label="Speaking" value={Math.round((vocabulary + accuracy) / 2)} />
        <Bar label="Listening" value={Math.round(vocabulary * 0.9)} />
      </View>
    </ScrollView>
  )
}

function Login({ onSuccess }: { onSuccess: () => void }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const submit = async () => {
    if (!email.trim() || !password) {
      setError('Enter your email and password.')
      return
    }
    setBusy(true)
    setError('')
    try {
      await login(email.trim(), password)
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to sign in')
    } finally {
      setBusy(false)
    }
  }

  return (
    <SafeAreaView style={s.safe}>
      <StatusBar style="dark" />
      <KeyboardAvoidingView style={s.login} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View style={s.logoLarge}><Text style={s.logoLargeText}>J</Text></View>
        <Text style={s.loginTitle}>JUBA LISAN</Text>
        <Text style={s.bodyCenter}>Mobile learning, connected to your study plan.</Text>
        <TextInput autoCapitalize="none" keyboardType="email-address" placeholder="Email" placeholderTextColor={C.muted} value={email} onChangeText={setEmail} style={s.input} />
        <TextInput secureTextEntry placeholder="Password" placeholderTextColor={C.muted} value={password} onChangeText={setPassword} style={s.input} />
        {!!error && <Text style={s.error}>{error}</Text>}
        <Pressable disabled={busy} onPress={submit} style={s.primaryButton}>
          {busy ? <ActivityIndicator color="#fff" /> : <Text style={s.primaryButtonText}>Sign in</Text>}
        </Pressable>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

export default function AppShellV2() {
  const [ready, setReady] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [summary, setSummary] = useState<ProgressSummary>({})
  const [lessons, setLessons] = useState<TodayLesson[]>([])
  const [cards, setCards] = useState<Flashcard[]>([])
  const [tab, setTab] = useState<Tab>('Home')
  const [learnLoading, setLearnLoading] = useState(false)
  const [reviewLoading, setReviewLoading] = useState(false)
  const [learnError, setLearnError] = useState('')
  const [reviewError, setReviewError] = useState('')

  const loadSession = useCallback(async () => {
    try {
      if (!(await getToken())) return
      const [currentUser, currentProgress] = await Promise.all([me(), progress().catch(() => ({}))])
      setUser(currentUser)
      setSummary(currentProgress)
    } catch {
      await clearToken()
      setUser(null)
    } finally {
      setReady(true)
    }
  }, [])

  const loadLessons = useCallback(async () => {
    setLearnLoading(true)
    setLearnError('')
    try {
      const data = await todayPlan()
      const value = Array.isArray(data) ? data : data?.lessons
      setLessons(Array.isArray(value) ? value : [])
    } catch {
      setLearnError('Unable to load today’s lessons.')
    } finally {
      setLearnLoading(false)
    }
  }, [])

  const loadCards = useCallback(async () => {
    setReviewLoading(true)
    setReviewError('')
    try {
      const response = await apiFetch('/api/flashcards/due')
      if (!response.ok) throw new Error('Unable to load review cards')
      const data = await response.json()
      const value = Array.isArray(data) ? data : data?.flashcards
      setCards(Array.isArray(value) ? value : [])
    } catch {
      setReviewError('Unable to load review cards.')
    } finally {
      setReviewLoading(false)
    }
  }, [])

  useEffect(() => { void loadSession() }, [loadSession])
  useEffect(() => { if (user) { void loadLessons(); void loadCards() } }, [user, loadLessons, loadCards])

  const refreshAll = useCallback(async () => {
    if (!user) return
    const [, p] = await Promise.all([
      loadCards(),
      progress().catch(() => summary),
    ])
    setSummary(p)
  }, [user, loadCards, summary])

  const content = useMemo(() => {
    if (!user) return null
    if (tab === 'Home') return <Home user={user} summary={summary} lessons={lessons} setTab={setTab} />
    if (tab === 'Learn') return <Learn lessons={lessons} loading={learnLoading} error={learnError} />
    if (tab === 'Speak') return <Speak />
    if (tab === 'Review') return <Review loading={reviewLoading} cards={cards} error={reviewError} refresh={() => void refreshAll()} />
    return <ProgressScreen summary={summary} />
  }, [tab, user, summary, lessons, learnLoading, learnError, reviewLoading, cards, reviewError, refreshAll])

  if (!ready) return <SafeAreaView style={s.safe}><ActivityIndicator style={{ marginTop: 120 }} color={C.primary} /></SafeAreaView>
  if (!user) return <Login onSuccess={() => { setReady(false); void loadSession() }} />

  return (
    <SafeAreaView style={s.safe}>
      <StatusBar style="dark" />
      {content}
      <Nav tab={tab} setTab={setTab} />
      <Pressable onPress={async () => { await clearToken(); setUser(null); setReady(true) }} style={s.signOut} accessibilityLabel="Sign out">
        <Text style={s.signOutText}>↪</Text>
      </Pressable>
    </SafeAreaView>
  )
}

const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: C.bg },
  content: { padding: 20, paddingBottom: 120 },
  top: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  title: { fontSize: 30, color: C.ink, fontWeight: '900', marginTop: 4 },
  header: { flexDirection: 'row', alignItems: 'center', marginBottom: 24 },
  logo: { width: 42, height: 42, borderRadius: 14, backgroundColor: C.primary, alignItems: 'center', justifyContent: 'center', marginRight: 10 },
  logoText: { color: '#fff', fontSize: 22, fontWeight: '900' },
  eyebrow: { fontSize: 9, color: C.primary, fontWeight: '900', letterSpacing: 1.3 },
  headerTitle: { fontSize: 24, color: C.ink, fontWeight: '900', marginTop: 2 },
  avatar: { width: 46, height: 46, borderRadius: 16, backgroundColor: C.primarySoft, alignItems: 'center', justifyContent: 'center' },
  avatarText: { color: C.primary, fontWeight: '900', fontSize: 18 },
  hero: { backgroundColor: C.navy, borderRadius: 28, padding: 22, minHeight: 235, overflow: 'hidden', marginBottom: 14 },
  pill: { alignSelf: 'flex-start', backgroundColor: '#37384F', color: '#C2BEFF', paddingHorizontal: 10, paddingVertical: 6, borderRadius: 99, fontSize: 9, fontWeight: '900' },
  heroTitle: { color: '#fff', fontSize: 24, fontWeight: '900', lineHeight: 29, marginTop: 17 },
  heroBody: { color: '#C4C4D0', lineHeight: 20, marginTop: 8 },
  heroBtn: { alignSelf: 'flex-start', backgroundColor: '#fff', borderRadius: 13, paddingHorizontal: 15, paddingVertical: 11, marginTop: 18 },
  heroBtnText: { color: C.navy, fontWeight: '900' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -4 },
  stat: { width: '50%', backgroundColor: C.card, borderRadius: 19, borderWidth: 1, borderColor: C.line, padding: 14, marginBottom: 8 },
  statIcon: { fontSize: 15 },
  statValue: { color: C.ink, fontSize: 23, fontWeight: '900', marginTop: 7 },
  statLabel: { color: C.muted, fontSize: 9, fontWeight: '800' },
  section: { fontSize: 18, color: C.ink, fontWeight: '900', marginTop: 10, marginBottom: 11 },
  card: { backgroundColor: C.card, borderRadius: 22, padding: 19, borderWidth: 1, borderColor: C.line, marginBottom: 12 },
  cardTitle: { color: C.ink, fontSize: 18, fontWeight: '900', marginTop: 6 },
  body: { color: C.muted, fontSize: 13, lineHeight: 19, marginTop: 5 },
  bodyCenter: { textAlign: 'center', color: C.muted, fontSize: 11, lineHeight: 17, marginTop: 7 },
  pillText: { color: C.primary, fontSize: 9, fontWeight: '900', letterSpacing: 1.1 },
  linkButton: { alignSelf: 'flex-start', marginTop: 12 },
  link: { color: C.primary, fontWeight: '900', fontSize: 11 },
  barWrap: { marginBottom: 14 },
  between: { flexDirection: 'row', justifyContent: 'space-between' },
  pct: { color: C.primary, fontWeight: '900', fontSize: 11 },
  track: { height: 8, backgroundColor: C.soft, borderRadius: 99, overflow: 'hidden', marginTop: 7 },
  fill: { height: '100%', backgroundColor: C.primary, borderRadius: 99 },
  nav: { position: 'absolute', left: 12, right: 12, bottom: 10, height: 70, borderRadius: 23, backgroundColor: '#fff', borderWidth: 1, borderColor: C.line, flexDirection: 'row', justifyContent: 'space-around', alignItems: 'center', elevation: 8 },
  navItem: { alignItems: 'center', minWidth: 55 },
  navIcon: { fontSize: 18, color: C.muted },
  navText: { fontSize: 9, color: C.muted, fontWeight: '800', marginTop: 3 },
  active: { color: C.primary },
  row: { backgroundColor: C.card, borderRadius: 21, borderWidth: 1, borderColor: C.line, padding: 15, flexDirection: 'row', alignItems: 'center', marginBottom: 9 },
  iconBox: { width: 52, height: 52, borderRadius: 17, backgroundColor: C.primarySoft, alignItems: 'center', justifyContent: 'center', marginRight: 13 },
  iconDone: { backgroundColor: '#E9F8EF' },
  icon: { color: C.primary, fontSize: 19, fontWeight: '900' },
  rowBody: { flex: 1 },
  chev: { fontSize: 29, color: '#B0B0BA' },
  doneText: { color: '#21834A', fontSize: 11, fontWeight: '900' },
  speak: { backgroundColor: C.card, borderRadius: 28, borderWidth: 1, borderColor: C.line, padding: 22, alignItems: 'center' },
  tutor: { width: 76, height: 76, borderRadius: 28, backgroundColor: C.primarySoft, alignItems: 'center', justifyContent: 'center' },
  tutorMark: { fontSize: 32, color: C.primary },
  prompt: { alignSelf: 'stretch', backgroundColor: C.soft, borderRadius: 18, padding: 16, marginTop: 20 },
  promptText: { color: C.ink, fontSize: 16, fontWeight: '700', lineHeight: 23, marginTop: 7 },
  wave: { height: 70, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 5, marginTop: 15 },
  waveBar: { width: 5, backgroundColor: C.primary, borderRadius: 5 },
  status: { textAlign: 'center', color: C.muted, marginTop: 18 },
  mic: { width: 76, height: 76, borderRadius: 38, backgroundColor: C.primary, alignItems: 'center', justifyContent: 'center', alignSelf: 'center', marginTop: 17 },
  scores: { flexDirection: 'row', marginTop: 24, marginHorizontal: -4 },
  scoreCard: { flex: 1, backgroundColor: C.card, borderWidth: 1, borderColor: C.line, borderRadius: 17, padding: 13, alignItems: 'center', marginHorizontal: 4 },
  scoreValue: { color: C.primary, fontSize: 18, fontWeight: '900' },
  scoreLabel: { color: C.muted, fontSize: 9, marginTop: 4, textAlign: 'center' },
  flash: { backgroundColor: C.card, minHeight: 330, borderRadius: 29, borderWidth: 1, borderColor: C.line, padding: 22, alignItems: 'center', justifyContent: 'center', marginTop: 15 },
  word: { color: C.ink, fontSize: 35, fontWeight: '900', textAlign: 'center' },
  meaning: { color: C.primary, fontSize: 16, fontWeight: '700', marginTop: 8, textAlign: 'center' },
  example: { backgroundColor: C.soft, borderRadius: 17, padding: 15, marginTop: 30, color: C.ink, lineHeight: 20, textAlign: 'center' },
  cardMeta: { color: C.muted, fontSize: 10, marginTop: 18 },
  two: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -4 },
  review: { flex: 1, minWidth: '44%', height: 52, borderRadius: 15, backgroundColor: C.card, borderWidth: 1, borderColor: C.line, alignItems: 'center', justifyContent: 'center', margin: 4 },
  reviewMain: { backgroundColor: C.primary, borderColor: C.primary },
  heroLight: { backgroundColor: C.primarySoft, borderRadius: 26, padding: 21 },
  big: { fontSize: 36, color: C.ink, fontWeight: '900', marginTop: 7 },
  error: { color: C.danger, backgroundColor: '#FEECEC', padding: 12, borderRadius: 12, marginTop: 12, fontSize: 12, lineHeight: 17 },
  login: { flex: 1, justifyContent: 'center', padding: 24 },
  logoLarge: { width: 70, height: 70, borderRadius: 24, backgroundColor: C.primary, alignItems: 'center', justifyContent: 'center', alignSelf: 'center' },
  logoLargeText: { color: '#fff', fontSize: 36, fontWeight: '900' },
  loginTitle: { color: C.ink, fontSize: 28, fontWeight: '900', textAlign: 'center', marginTop: 14 },
  input: { height: 52, backgroundColor: C.card, borderWidth: 1, borderColor: C.line, borderRadius: 14, paddingHorizontal: 15, marginTop: 12, color: C.ink },
  primaryButton: { height: 52, borderRadius: 15, backgroundColor: C.primary, alignItems: 'center', justifyContent: 'center', marginTop: 14, paddingHorizontal: 20 },
  primaryButtonText: { color: '#fff', fontWeight: '900' },
  signOut: { position: 'absolute', top: 8, right: 14, width: 30, height: 30, borderRadius: 10, backgroundColor: C.card, borderWidth: 1, borderColor: C.line, alignItems: 'center', justifyContent: 'center' },
  signOutText: { color: C.muted, fontSize: 15, fontWeight: '900' },
})
