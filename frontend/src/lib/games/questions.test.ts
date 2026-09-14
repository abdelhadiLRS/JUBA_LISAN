import { describe, expect, it } from 'vitest'
import { QUESTION_BANK, getQuestionBank } from './questions'
import { buildDailyQuestion } from './engine'

describe('question bank', () => {
  it('contains localized vocabulary questions', () => {
    expect(getQuestionBank('words', 'ar').length).toBeGreaterThanOrEqual(10)
    expect(getQuestionBank('words', 'fr').length).toBeGreaterThanOrEqual(10)
    expect(getQuestionBank('words', 'en').length).toBeGreaterThanOrEqual(10)
  })

  it('contains curated math questions', () => {
    expect(getQuestionBank('math', 'ar').length).toBeGreaterThan(0)
    expect(getQuestionBank('math', 'fr').length).toBeGreaterThan(0)
    expect(getQuestionBank('math', 'en').length).toBeGreaterThan(0)
  })

  it('has unique question identifiers', () => {
    const ids = QUESTION_BANK.map((item) => item.id)
    expect(new Set(ids).size).toBe(ids.length)
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
