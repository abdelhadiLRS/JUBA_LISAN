import { describe, expect, it } from 'vitest'
import { getQuestionBank } from './questions'
import { buildDailyQuestion } from './engine'

describe('question bank', () => {
  it('contains localized vocabulary questions', () => {
    expect(getQuestionBank('words', 'ar').length).toBeGreaterThan(0)
    expect(getQuestionBank('words', 'fr').length).toBeGreaterThan(0)
    expect(getQuestionBank('words', 'en').length).toBeGreaterThan(0)
  })

  it('returns metadata needed for learning feedback', () => {
    const question = buildDailyQuestion('words', 'ar', 1, '2026-09-14', 0)
    expect(question.id).toBeTruthy()
    expect(question.topic).toBeTruthy()
    expect(question.explanation).toBeTruthy()
    expect(question.choices).toContain(question.answer)
  })

  it('keeps daily bank questions deterministic', () => {
    const first = buildDailyQuestion('words', 'fr', 1, '2026-09-14', 2)
    const second = buildDailyQuestion('words', 'fr', 1, '2026-09-14', 2)
    expect(second).toEqual(first)
  })
})
