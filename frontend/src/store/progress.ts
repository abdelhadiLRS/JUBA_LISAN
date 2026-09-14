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
  completeGame: (roundScore: number, daily: boolean) => void
  unlockAchievements: (ids: AchievementId[]) => void
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
  currentCorrectStreak: 0,
  bestCorrectStreak: 0,
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
    skills: data.skills,
    ...(data.gameStats ? { gameStats: data.gameStats } : {}),
    ...(data.achievements ? { achievements: data.achievements } : {}),
  }),
  addGameXP: (xp, skill, correct) =>
    set((state) => ({
      xp: state.xp + xp,
      streak: correct ? state.streak + 1 : 0,
      skills: correct
        ? { ...state.skills, [skill]: Math.min(1, (state.skills[skill] ?? 0) + 0.05) }
        : state.skills,
    })),
  recordGameAttempt: (correct) =>
    set((state) => {
      const currentCorrectStreak = correct ? (state.gameStats.currentCorrectStreak ?? 0) + 1 : 0
      return {
        gameStats: {
          ...state.gameStats,
          currentCorrectStreak,
          questionsAnswered: state.gameStats.questionsAnswered + 1,
          correctAnswers: state.gameStats.correctAnswers + (correct ? 1 : 0),
          bestCorrectStreak: Math.max(state.gameStats.bestCorrectStreak, currentCorrectStreak),
        },
      }
    }),
  completeGame: (roundScore, daily) =>
    set((state) => ({
      gameStats: {
        ...state.gameStats,
        gamesPlayed: state.gameStats.gamesPlayed + 1,
        bestRoundScore: Math.max(state.gameStats.bestRoundScore, roundScore),
        dailyChallengesCompleted: state.gameStats.dailyChallengesCompleted + (daily ? 1 : 0),
      },
    })),
  unlockAchievements: (ids) => set((state) => ({ achievements: Array.from(new Set([...state.achievements, ...ids])) })),
  setTodayLessons: (lessons) => set({ todayLessons: lessons }),
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
