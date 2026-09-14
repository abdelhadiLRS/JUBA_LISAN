import { describe, expect, it } from 'vitest'
import { buildDailyQuestion, buildQuestion, getDifficulty, scoreAnswer, type GameId } from './engine'

describe('game engine', () => {
  it('maps learner level to a bounded difficulty', () => {
    expect(getDifficulty(1)).toBe(1)
    expect(getDifficulty(3)).toBe(2)
    expect(getDifficulty(99)).toBe(3)
  })

  it('builds valid questions for every game', () => {
    const games: GameId[] = ['math', 'words', 'sequence', 'memory', 'matching', 'ordering']
    for (const game of games) {
      const question = buildQuestion(game, 'ar', 3)
      expect(question.choices.length).toBeGreaterThanOrEqual(4)
      expect(question.choices).toContain(question.answer)
      expect(question.skill).toBeTruthy()
      expect(question.hint).toBeTruthy()
    }
  })

  it('produces repeatable daily questions for the same date and round', () => {
    const first = buildDailyQuestion('math', 'ar', 3, '2026-09-14', 0)
    const second = buildDailyQuestion('math', 'ar', 3, '2026-09-14', 0)
    expect(second).toEqual(first)
  })

  it('changes the daily challenge when the round changes', () => {
    const first = buildDailyQuestion('sequence', 'en', 3, '2026-09-14', 0)
    const second = buildDailyQuestion('sequence', 'en', 3, '2026-09-14', 1)
    expect(second.prompt !== first.prompt || second.choices.join('|') !== first.choices.join('|')).toBe(true)
  })

  it('supports deterministic daily generation for the new game modes', () => {
    const games: GameId[] = ['memory', 'matching', 'ordering']
    for (const game of games) {
      const first = buildDailyQuestion(game, 'fr', 3, '2026-09-14', 2)
      const second = buildDailyQuestion(game, 'fr', 3, '2026-09-14', 2)
      expect(second).toEqual(first)
    }
  })

  it('awards bonus XP for harder correct answers', () => {
    const easy = buildQuestion('math', 'en', 1)
    const hard = buildQuestion('math', 'en', 5)
    expect(scoreAnswer(easy, easy.answer).xp).toBe(10)
    expect(scoreAnswer(hard, hard.answer).xp).toBe(20)
  })

  it('awards no XP for an incorrect answer', () => {
    const question = buildQuestion('sequence', 'fr', 1)
    const wrong = question.choices.find((choice) => choice !== question.answer)
    expect(wrong).toBeDefined()
    expect(scoreAnswer(question, wrong ?? '').correct).toBe(false)
    expect(scoreAnswer(question, wrong ?? '').xp).toBe(0)
  })
})
