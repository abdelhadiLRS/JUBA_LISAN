import React, { useEffect, useState } from 'react'
import { ActivityIndicator, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native'
import { StatusBar } from 'expo-status-bar'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { Audio } from 'expo-av'
import { apiFetch, clearToken, getToken, login, me, progress, todayPlan, type ProgressSummary, type User } from './src/api'

type RootStackParamList = {
  Login: undefined
  Home: undefined
  Coach: undefined
  Conversation: undefined
  Review: undefined
  Profile: undefined
}

const Stack = createNativeStackNavigator<RootStackParamList>()

const colors = { bg: '#F7F7FB', card: '#FFFFFF', ink: '#16151D', muted: '#73717D', accent: '#6C4CF1', accentSoft: '#EEEAFE', border: '#E9E7F0', success: '#168A68' }

function Button({ title, onPress, secondary = false }: { title: string; onPress: () => void; secondary?: boolean }) {
  return <Pressable onPress={onPress} style={[styles.button, secondary && styles.buttonSecondary]}><Text style={[styles.buttonText, secondary && styles.buttonTextSecondary]}>{title}</Text></Pressable>
}

function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit() {
    if (!email.trim() || !password) return setError('Enter your email and password.')
    setBusy(true); setError('')
    try { await login(email.trim(), password); navigation.replace('Home') }
    catch (e) { setError(e instanceof Error ? e.message : 'Sign in failed') }
    finally { setBusy(false) }
  }

  return <SafeAreaView style={styles.safe}><StatusBar style="dark" /><View style={styles.authWrap}>
    <View style={styles.brandMark}><Text style={styles.brandMarkText}>J</Text></View>
    <Text style={styles.brand}>JUBA LISAN</Text><Text style={styles.tagline}>Your intelligent language journey</Text>
    <View style={styles.card}><Text style={styles.title}>Welcome back</Text><Text style={styles.sub}>Continue your learning journey.</Text>
      <Text style={styles.label}>EMAIL</Text><TextInput value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" style={styles.input} placeholder="you@example.com" placeholderTextColor="#AAA8B3" />
      <Text style={styles.label}>PASSWORD</Text><TextInput value={password} onChangeText={setPassword} secureTextEntry style={styles.input} placeholder="••••••••" placeholderTextColor="#AAA8B3" />
      {!!error && <Text style={styles.error}>{error}</Text>}
      <Button title={busy ? 'Signing in…' : 'Sign in'} onPress={submit} />
    </View>
  </View></SafeAreaView>
}

function HomeScreen({ navigation }: any) {
  const [user, setUser] = useState<User | null>(null)
  const [stats, setStats] = useState<ProgressSummary>({})
  const [plan, setPlan] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { (async () => { try { const [u, p, t] = await Promise.all([me(), progress().catch(() => ({})), todayPlan()]); setUser(u); setStats(p); setPlan(t) } catch { await clearToken(); navigation.replace('Login') } finally { setLoading(false) } })() }, [])
  if (loading) return <SafeAreaView style={styles.safe}><ActivityIndicator style={{ marginTop: 100 }} size="large" color={colors.accent} /></SafeAreaView>
  const firstName = user?.displayName?.split(' ')[0] || user?.username || 'Learner'
  const accuracy = Math.round((stats.accuracy || 0) * 100)
  return <SafeAreaView style={styles.safe}><StatusBar style="dark" /><ScrollView contentContainerStyle={styles.content}>
    <View style={styles.topbar}><View><Text style={styles.eyebrow}>WELCOME BACK</Text><Text style={styles.heading}>Hi, {firstName} 👋</Text></View><Pressable onPress={() => navigation.navigate('Profile')} style={styles.avatar}><Text style={styles.avatarText}>{firstName[0]}</Text></Pressable></View>
    <View style={styles.hero}><View><Text style={styles.heroEyebrow}>TODAY'S MISSION</Text><Text style={styles.heroTitle}>{plan?.lessons?.[0]?.title || 'Build your language habit'}</Text><Text style={styles.heroSub}>A focused session designed around your level.</Text></View><Text style={styles.heroIcon}>✦</Text></View>
    <View style={styles.statsGrid}><Stat label="STREAK" value={`${stats.current_streak || 0}d`} /><Stat label="XP" value={`${stats.total_xp || 0}`} /><Stat label="VOCAB" value={`${stats.vocabulary_mastered || 0}`} /><Stat label="ACCURACY" value={`${accuracy}%`} /></View>
    <Text style={styles.sectionTitle}>Continue learning</Text>
    <View style={styles.card}><Text style={styles.cardKicker}>AI TUTOR</Text><Text style={styles.cardTitle}>Practice a real conversation</Text><Text style={styles.cardText}>Speak naturally. JUBA LISAN listens, corrects and adapts to you.</Text><Button title="Start conversation" onPress={() => navigation.navigate('Conversation')} /></View>
    <View style={styles.row}><View style={[styles.miniCard, { flex: 1, marginRight: 6 }]}><Text style={styles.miniIcon}>🧠</Text><Text style={styles.cardTitleSmall}>Smart review</Text><Text style={styles.cardText}>Words due today</Text><Pressable onPress={() => navigation.navigate('Review')}><Text style={styles.link}>Review →</Text></Pressable></View><View style={[styles.miniCard, { flex: 1, marginLeft: 6 }]}><Text style={styles.miniIcon}>🎯</Text><Text style={styles.cardTitleSmall}>Your coach</Text><Text style={styles.cardText}>Personal next step</Text><Pressable onPress={() => navigation.navigate('Coach')}><Text style={styles.link}>Open coach →</Text></Pressable></View></View>
    <Text style={styles.sectionTitle}>Your progress</Text><View style={styles.card}><ProgressRow label="Overall learning" value={Math.min(100, Math.round((stats.vocabulary_progress || 0) * 100))} /><ProgressRow label="Vocabulary" value={Math.min(100, Math.round((stats.vocabulary_progress || 0) * 100))} /><ProgressRow label="Accuracy" value={accuracy} /></View>
  </ScrollView></SafeAreaView>
}

function Stat({ label, value }: { label: string; value: string }) { return <View style={styles.stat}><Text style={styles.statLabel}>{label}</Text><Text style={styles.statValue}>{value}</Text></View> }
function ProgressRow({ label, value }: { label: string; value: number }) { return <View style={{ marginBottom: 16 }}><View style={styles.progressHeader}><Text style={styles.cardText}>{label}</Text><Text style={styles.progressValue}>{value}%</Text></View><View style={styles.track}><View style={[styles.fill, { width: `${value}%` }]} /></View></View> }

function CoachScreen({ navigation }: any) { return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.content}><Text style={styles.eyebrow}>AI LEARNING COACH</Text><Text style={styles.heading}>Your next best step</Text><View style={styles.coachCard}><Text style={styles.coachEmoji}>🧠</Text><Text style={styles.cardTitle}>Personalized practice</Text><Text style={styles.cardText}>JUBA LISAN can use your progress, accuracy and learning history to guide what you should practice next.</Text><Button title="Practice speaking" onPress={() => navigation.navigate('Conversation')} /><Button title="Review vocabulary" secondary onPress={() => navigation.navigate('Review')} /></View><View style={styles.tip}><Text style={styles.tipTitle}>Coach insight</Text><Text style={styles.cardText}>Keep sessions short and consistent. A 10–15 minute conversation today is better than waiting for a perfect hour.</Text></View></ScrollView></SafeAreaView> }

function ConversationScreen() { const [recording, setRecording] = useState<Audio.Recording | null>(null); const [status, setStatus] = useState('Ready to practice'); async function toggle() { if (recording) { await recording.stopAndUnloadAsync(); setRecording(null); setStatus('Analyzing your speech…'); setTimeout(() => setStatus('Try another sentence'), 1200); return } await Audio.requestPermissionsAsync(); await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true }); const { recording: r } = await Audio.Recording.createAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY); setRecording(r); setStatus('Listening… speak naturally') } return <SafeAreaView style={styles.safe}><View style={styles.conversation}><Text style={styles.eyebrow}>VOICE PRACTICE</Text><Text style={styles.heading}>Talk to your AI tutor</Text><View style={styles.tutor}><View style={styles.tutorAvatar}><Text style={{ fontSize: 36 }}>✦</Text></View><Text style={styles.cardTitle}>Lingu</Text><Text style={styles.cardText}>“Tell me about your day in 2–3 sentences.”</Text><View style={styles.wave}>{[18, 32, 50, 26, 44, 62, 30, 52, 22, 38].map((h, i) => <View key={i} style={[styles.waveBar, { height: h }]} />)}</View></View><Text style={styles.status}>{status}</Text><Pressable onPress={toggle} style={[styles.mic, recording && { backgroundColor: '#E95D67' }]}><Text style={{ fontSize: 30 }}>{recording ? '■' : '🎙️'}</Text></Pressable><Text style={styles.micHint}>{recording ? 'Tap to finish' : 'Tap to speak'}</Text></View></SafeAreaView> }

function ReviewScreen() { return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.content}><Text style={styles.eyebrow}>SMART REVIEW</Text><Text style={styles.heading}>Words due today</Text>{['appointment', 'nevertheless', 'probably', 'although'].map((word, i) => <View style={styles.reviewCard} key={word}><View><Text style={styles.reviewWord}>{word}</Text><Text style={styles.cardText}>{['a scheduled meeting', 'despite that', 'very likely', 'in spite of'][i]}</Text></View><Text style={styles.reviewBadge}>DUE</Text></View>)}<Button title="Start review" onPress={() => {}} /></ScrollView></SafeAreaView> }

function ProfileScreen({ navigation }: any) { return <SafeAreaView style={styles.safe}><View style={styles.content}><Text style={styles.eyebrow}>ACCOUNT</Text><Text style={styles.heading}>Profile</Text><View style={styles.card}><Text style={styles.cardTitle}>JUBA LISAN</Text><Text style={styles.cardText}>One account across web and mobile.</Text><Text style={styles.sync}>✓ Progress sync enabled</Text><Text style={styles.sync}>✓ XP and streak sync</Text><Text style={styles.sync}>✓ Vocabulary sync</Text><Text style={styles.sync}>✓ Conversations sync</Text></View><Button title="Sign out" secondary onPress={async () => { await clearToken(); navigation.replace('Login') }} /></View></SafeAreaView> }

export default function App() { const [ready, setReady] = useState(false); const [initial, setInitial] = useState<'Login' | 'Home'>('Login'); useEffect(() => { getToken().then(t => { setInitial(t ? 'Home' : 'Login'); setReady(true) }) }, []); if (!ready) return <SafeAreaView style={styles.safe}><ActivityIndicator style={{ marginTop: 100 }} color={colors.accent} /></SafeAreaView>; return <NavigationContainer><Stack.Navigator initialRouteName={initial} screenOptions={{ headerShown: false }}>{<Stack.Screen name="Login" component={LoginScreen} />}<Stack.Screen name="Home" component={HomeScreen} /><Stack.Screen name="Coach" component={CoachScreen} /><Stack.Screen name="Conversation" component={ConversationScreen} /><Stack.Screen name="Review" component={ReviewScreen} /><Stack.Screen name="Profile" component={ProfileScreen} /></Stack.Navigator></NavigationContainer> }

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg }, content: { padding: 20, paddingBottom: 40 }, authWrap: { flex: 1, justifyContent: 'center', padding: 24 }, brandMark: { alignSelf: 'center', width: 62, height: 62, borderRadius: 20, backgroundColor: colors.accent, alignItems: 'center', justifyContent: 'center', marginBottom: 14 }, brandMarkText: { color: '#FFF', fontSize: 32, fontWeight: '800' }, brand: { textAlign: 'center', fontSize: 23, fontWeight: '800', color: colors.ink, letterSpacing: 2 }, tagline: { textAlign: 'center', color: colors.muted, marginTop: 6, marginBottom: 30 }, card: { backgroundColor: colors.card, borderRadius: 22, padding: 20, borderWidth: 1, borderColor: colors.border, marginBottom: 14 }, title: { fontSize: 25, fontWeight: '800', color: colors.ink }, sub: { color: colors.muted, marginTop: 6, marginBottom: 24 }, label: { color: colors.muted, fontSize: 11, fontWeight: '800', letterSpacing: 1.2, marginBottom: 7, marginTop: 10 }, input: { height: 52, borderRadius: 14, borderWidth: 1, borderColor: colors.border, paddingHorizontal: 15, color: colors.ink, backgroundColor: '#FBFAFD' }, error: { color: '#C73B4A', marginTop: 12 }, button: { backgroundColor: colors.accent, borderRadius: 14, minHeight: 50, alignItems: 'center', justifyContent: 'center', marginTop: 16, paddingHorizontal: 18 }, buttonSecondary: { backgroundColor: colors.accentSoft }, buttonText: { color: '#FFF', fontWeight: '800', letterSpacing: .4 }, buttonTextSecondary: { color: colors.accent }, topbar: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }, eyebrow: { color: colors.accent, fontSize: 11, fontWeight: '800', letterSpacing: 1.5, marginBottom: 6 }, heading: { color: colors.ink, fontSize: 30, fontWeight: '800', letterSpacing: -.7 }, avatar: { width: 46, height: 46, borderRadius: 15, backgroundColor: colors.accentSoft, alignItems: 'center', justifyContent: 'center' }, avatarText: { color: colors.accent, fontWeight: '800', fontSize: 18 }, hero: { backgroundColor: colors.ink, borderRadius: 24, padding: 22, marginBottom: 14, flexDirection: 'row', alignItems: 'center' }, heroEyebrow: { color: '#BDB8FF', fontSize: 10, fontWeight: '800', letterSpacing: 1.3 }, heroTitle: { color: '#FFF', fontSize: 21, fontWeight: '800', marginTop: 8, maxWidth: 260 }, heroSub: { color: '#B9B6C4', marginTop: 7, lineHeight: 20, maxWidth: 280 }, heroIcon: { color: '#A69BFF', fontSize: 44, marginLeft: 'auto' }, statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 26 }, stat: { backgroundColor: colors.card, borderRadius: 17, borderWidth: 1, borderColor: colors.border, padding: 15, width: '48%' }, statLabel: { color: colors.muted, fontSize: 10, fontWeight: '800', letterSpacing: 1 }, statValue: { color: colors.ink, fontSize: 25, fontWeight: '800', marginTop: 7 }, sectionTitle: { color: colors.ink, fontSize: 19, fontWeight: '800', marginTop: 8, marginBottom: 12 }, cardKicker: { color: colors.accent, fontSize: 10, fontWeight: '800', letterSpacing: 1.4 }, cardTitle: { color: colors.ink, fontSize: 20, fontWeight: '800', marginTop: 7 }, cardTitleSmall: { color: colors.ink, fontSize: 16, fontWeight: '800', marginTop: 5 }, cardText: { color: colors.muted, lineHeight: 20, marginTop: 6 }, row: { flexDirection: 'row', marginBottom: 10 }, miniCard: { backgroundColor: colors.card, borderRadius: 20, borderWidth: 1, borderColor: colors.border, padding: 16 }, miniIcon: { fontSize: 23 }, link: { color: colors.accent, fontWeight: '800', marginTop: 12 }, progressHeader: { flexDirection: 'row', justifyContent: 'space-between' }, progressValue: { color: colors.accent, fontWeight: '800' }, track: { height: 8, backgroundColor: '#EEECF3', borderRadius: 8, overflow: 'hidden', marginTop: 8 }, fill: { height: 8, backgroundColor: colors.accent, borderRadius: 8 }, coachCard: { backgroundColor: colors.card, borderRadius: 24, padding: 22, marginTop: 20, borderWidth: 1, borderColor: colors.border }, coachEmoji: { fontSize: 34 }, tip: { backgroundColor: colors.accentSoft, padding: 18, borderRadius: 20, marginTop: 8 }, tipTitle: { color: colors.accent, fontWeight: '800', marginBottom: 4 }, conversation: { flex: 1, alignItems: 'center', padding: 24, paddingTop: 70 }, tutor: { width: '100%', backgroundColor: colors.card, borderRadius: 26, borderWidth: 1, borderColor: colors.border, padding: 25, alignItems: 'center', marginTop: 25 }, tutorAvatar: { width: 84, height: 84, borderRadius: 30, backgroundColor: colors.accentSoft, alignItems: 'center', justifyContent: 'center', marginBottom: 12 }, wave: { flexDirection: 'row', alignItems: 'center', gap: 5, height: 70, marginTop: 15 }, waveBar: { width: 5, borderRadius: 5, backgroundColor: colors.accent }, status: { color: colors.muted, marginTop: 24 }, mic: { width: 88, height: 88, borderRadius: 44, backgroundColor: colors.accent, alignItems: 'center', justifyContent: 'center', marginTop: 25 }, micHint: { color: colors.muted, marginTop: 10 }, reviewCard: { backgroundColor: colors.card, borderRadius: 19, borderWidth: 1, borderColor: colors.border, padding: 18, marginBottom: 10, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }, reviewWord: { color: colors.ink, fontSize: 19, fontWeight: '800' }, reviewBadge: { color: colors.accent, backgroundColor: colors.accentSoft, paddingHorizontal: 9, paddingVertical: 5, borderRadius: 9, fontSize: 10, fontWeight: '800' }, sync: { color: colors.success, marginTop: 12, fontWeight: '700' }
})
