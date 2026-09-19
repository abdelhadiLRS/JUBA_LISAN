import { create } from 'zustand'
import type { AchievementId, GameStats } from '@/lib/games/achievements'

interface TodayLesson {
  id: number | null
  title: string
  lessonType: string
  week: number
  day: number
  objectives: string[]
  estimatedMinutes: number
  unitId?: string
  isCompleted?: boolean
}

interface UnitProgress {
  unitId: string
  completedLessons: number
  totalLessons: number
  competencies: Record<string, number>
}

export type LevelTestRecommendation = 'advance' | 'extend' | 'repeat'

interface LevelTestResult {
  score: number
  recommendation: LevelTestRecommendation
  nextLevel: string | null
}

interface ProgressStore {
  streak: number
  xp: number
  skills: Record<string, number>
  gameStats: GameStats
  achievements: AchievementId[]
  todayLessons: TodayLesson[]
  completedToday: number[]
  currentUnitId: string
  currentPlanDurationWeeks: number
  unitProgress: Record<string, UnitProgress>
  levelTestUnlocked: boolean
  levelTestResult: LevelTestResult | null
  setProgress: (data: { streak: number; xp: number; skills: Record<string, number>; gameStats?: GameStats; achievements?: AchievementId[] }) => void
  addGameXP: (xp: number, skill: string, correct: boolean) => void
  recordGameAttempt: (correct: boolean) => void
  completeGame: (roundScore: number, daily: boolean, dailyDate?: string) => void
  unlockAchievements: (ids: AchievementId[]) => void
  resetGameProgress: () => void
  setTodayLessons: (lessons: TodayLesson[]) => void
  completeLesson: (id: number) => void
  setCurrentUnit: (unitId: string) => void
  setPlanDuration: (weeks: number) => void
  updateUnitProgress: (unitId: string, progress: Partial<UnitProgress>) => void
  unlockLevelTest: () => void
  setLevelTestResult: (result: LevelTestResult) => void
}

const initialGameStats: GameStats = {
  gamesPlayed: 0,
  questionsAnswered: 0,
  correctAnswers: 0,
  bestRoundScore: 0,
  dailyChallengesCompleted: 0,
  lastDailyChallengeDate: '',
  currentCorrectStreak: 0,
  bestCorrectStreak: 0,
}

const SUPPORTED_LESSON_TYPES = new Set([
  'grammar',
  'vocabulary',
  'reading',
  'writing',
  'listening',
  'conversation',
  'review',
  'level_test',
])

const SUPPORTED_GAME_SKILLS = new Set([
  'math',
  'logic',
  'memory',
  'ordering',
])

const SUPPORTED_SKILLS = new Set([
  ...SUPPORTED_LESSON_TYPES,
  ...SUPPORTED_GAME_SKILLS,
])

function normalizeLessonType(value: unknown): string {
  if (typeof value !== 'string') return 'review'
  const normalized = value.trim().toLowerCase()
  return SUPPORTED_LESSON_TYPES.has(normalized) ? normalized : 'review'
}

function normalizeSkills(value: unknown): Record<string, number> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {}

  return Object.fromEntries(
    Object.entries(value).flatMap(([skill, score]) => {
      if (
        !SUPPORTED_SKILLS.has(skill) ||
        typeof score !== 'number' ||
        !Number.isFinite(score)
      ) {
        return []
      }

      return [[skill, Math.max(0, Math.min(1, score))]]
    })
  )
}

function normalizeTodayLessons(lessons: unknown): TodayLesson[] {
  if (!Array.isArray(lessons)) return []

  return lessons
    .filter((lesson): lesson is TodayLesson => Boolean(lesson && typeof lesson === 'object'))
    .map((lesson) => ({
      ...lesson,
      lessonType: normalizeLessonType(lesson.lessonType),
      objectives: Array.isArray(lesson.objectives)
        ? lesson.objectives.filter((objective) => typeof objective === 'string')
        : [],
      estimatedMinutes:
        typeof lesson.estimatedMinutes === 'number' &&
        Number.isFinite(lesson.estimatedMinutes) &&
        lesson.estimatedMinutes > 0
          ? lesson.estimatedMinutes
          : 25,
      isCompleted: Boolean(lesson.isCompleted),
    }))
}

export const useProgressStore = create<ProgressStore>((set) => ({
  streak: 0,
  xp: 0,
  skills: {},
  gameStats: initialGameStats,
  achievements: [],
  todayLessons: [],
  completedToday: [],
  currentUnitId: '',
  currentPlanDurationWeeks: 12,
  unitProgress: {},
  levelTestUnlocked: false,
  levelTestResult: null,
  setProgress: (data) => set({
    streak: data.streak,
    xp: data.xp,
    skills: normalizeSkills(data.skills),
    ...(data.gameStats ? { gameStats: data.gameStats } : {}),
    ...(data.achievements ? { achievements: data.achievements } : {}),
  }),
  addGameXP: (xp, skill, correct) =>
    set((state) => ({
      xp: state.xp + xp,
      skills: correct
        ? {
            ...normalizeSkills(state.skills),
            ...(SUPPORTED_SKILLS.has(skill)
              ? { [skill]: Math.min(1, (state.skills[skill] ?? 0) + 0.05) }
              : {}),
          }
        : normalizeSkills(state.skills),
    })),
  recordGameAttempt: (correct, questionsAnswered = 1, correctAnswers = correct ? 1 : 0) =>
    set((state) => {
      const safeQuestions = Math.max(0, Math.floor(questionsAnswered))
      const safeCorrect = Math.max(0, Math.min(safeQuestions, Math.floor(correctAnswers)))
      const batchIsPerfect = safeQuestions > 0 && safeCorrect === safeQuestions
      const currentCorrectStreak = batchIsPerfect
        ? (state.gameStats.currentCorrectStreak ?? 0) + safeCorrect
        : 0
      return {
        gameStats: {
          ...state.gameStats,
          currentCorrectStreak,
          questionsAnswered: state.gameStats.questionsAnswered + safeQuestions,
          correctAnswers: state.gameStats.correctAnswers + safeCorrect,
          bestCorrectStreak: Math.max(state.gameStats.bestCorrectStreak, currentCorrectStreak),
        },
      }
    }),
  completeGame: (roundScore, daily, dailyDate) =>
    set((state) => {
      const alreadyClaimedToday =
        daily &&
        Boolean(dailyDate) &&
        state.gameStats.lastDailyChallengeDate === dailyDate
      return {
        gameStats: {
          ...state.gameStats,
          gamesPlayed: state.gameStats.gamesPlayed + 1,
          bestRoundScore: Math.max(state.gameStats.bestRoundScore, roundScore),
          dailyChallengesCompleted:
            state.gameStats.dailyChallengesCompleted + (daily && !alreadyClaimedToday ? 1 : 0),
          lastDailyChallengeDate:
            daily && !alreadyClaimedToday
              ? dailyDate
              : state.gameStats.lastDailyChallengeDate,
        },
      }
    }),
  unlockAchievements: (ids) => set((state) => ({ achievements: Array.from(new Set([...state.achievements, ...ids])) })),
  resetGameProgress: () => set({ gameStats: initialGameStats, achievements: [] }),
  setTodayLessons: (lessons) => set({ todayLessons: normalizeTodayLessons(lessons) }),
  completeLesson: (id) => set((state) => ({ completedToday: [...state.completedToday, id] })),
  setCurrentUnit: (unitId) => set({ currentUnitId: unitId }),
  setPlanDuration: (weeks) => set({ currentPlanDurationWeeks: weeks }),
  updateUnitProgress: (unitId, progress) =>
    set((state) => ({
      unitProgress: {
        ...state.unitProgress,
        [unitId]: { ...state.unitProgress[unitId], ...progress, unitId },
      },
    })),
  unlockLevelTest: () => set({ levelTestUnlocked: true }),
  setLevelTestResult: (result) => set({ levelTestResult: result }),
}))
