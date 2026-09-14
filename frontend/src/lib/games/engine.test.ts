import { describe, expect, it } from 'vitest';
import { buildQuestion, getDifficulty, scoreAnswer } from './engine';

describe('game engine', () => {
  it('maps learner level to a bounded difficulty', () => {
    expect(getDifficulty(1)).toBe(1);
    expect(getDifficulty(3)).toBe(2);
    expect(getDifficulty(99)).toBe(3);
  });

  it('builds valid questions for every game', () => {
    for (const game of ['math', 'words', 'sequence'] as const) {
      const question = buildQuestion(game, 'ar', 3);
      expect(question.choices).toHaveLength(game === 'words' ? 8 : 4);
      expect(question.choices).toContain(question.answer);
      expect(question.skill).toBeTruthy();
      expect(question.hint).toBeTruthy();
    }
  });

  it('awards bonus XP for harder correct answers', () => {
    const easy = buildQuestion('math', 'en', 1);
    const hard = buildQuestion('math', 'en', 5);
    expect(scoreAnswer(easy, easy.answer).xp).toBe(10);
    expect(scoreAnswer(hard, hard.answer).xp).toBe(20);
  });

  it('awards no XP for an incorrect answer', () => {
    const question = buildQuestion('sequence', 'fr', 1);
    const wrong = question.choices.find((choice) => choice !== question.answer);
    expect(wrong).toBeDefined();
    expect(scoreAnswer(question, wrong ?? '').correct).toBe(false);
    expect(scoreAnswer(question, wrong ?? '').xp).toBe(0);
  });
});
