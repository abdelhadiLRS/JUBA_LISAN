import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '@/lib/api'
import { completeGameSession, startGameSession } from './persist'

vi.mock('@/lib/api', () => ({
  apiFetch: vi.fn(),
}))

const mockedApiFetch = vi.mocked(apiFetch)

describe('server game sessions', () => {
  beforeEach(() => {
    mockedApiFetch.mockReset()
  })

  it('starts a server-owned session with bounded difficulty', async () => {
    mockedApiFetch.mockResolvedValue(
      new Response(
        JSON.stringify({
          session_id: 'session-123',
          game_id: 'math',
          questions: [
            {
              id: 'q1',
              prompt: '2 + 2 = ?',
              choices: ['3', '4', '5', '6'],
              hint: 'Add two numbers',
              skill: 'math',
              difficulty: 3,
            },
          ],
          expires_at: '2026-09-19T12:15:00Z',
        }),
        { status: 200 },
      ),
    )

    const result = await startGameSession('math', 'en', 99)

    expect(result.session_id).toBe('session-123')
    const body = JSON.parse(String(mockedApiFetch.mock.calls[0][1]?.body))
    expect(body).toEqual({ game_id: 'math', language: 'en', difficulty: 3 })
  })

  it('submits only answers and interaction traces to the completion endpoint', async () => {
    mockedApiFetch.mockResolvedValue(
      new Response(
        JSON.stringify({
          total_xp: 125,
          games_played: 2,
          questions_answered: 5,
          correct_answers: 4,
          best_round_score: 25,
          daily_challenges_completed: 1,
          last_daily_challenge_date: '2026-09-19',
          current_correct_streak: 4,
          best_correct_streak: 7,
          achievements: ['first_game'],
          skills: { vocabulary: 0.8 },
          round_score: 20,
          round_correct: 4,
          round_questions: 5,
          xp_earned: 21,
          new_achievements: [],
        }),
        { status: 200 },
      ),
    )

    const result = await completeGameSession(
      'session-123',
      [{ question_id: 'q1', choice: '4' }],
      true,
      '2026-09-19',
      [{ first: 'a', second: 'b' }],
    )

    expect(result.xp_earned).toBe(21)
    const body = JSON.parse(String(mockedApiFetch.mock.calls[0][1]?.body))
    expect(body).toEqual({
      session_id: 'session-123',
      answers: [{ question_id: 'q1', choice: '4' }],
      interaction_trace: [{ first: 'a', second: 'b' }],
      daily_challenge: true,
      daily_challenge_date: '2026-09-19',
    })
  })

  it('rejects failed HTTP responses without retrying', async () => {
    mockedApiFetch.mockResolvedValue(
      new Response(JSON.stringify({ detail: 'expired' }), { status: 410 }),
    )

    await expect(completeGameSession('session-123', [])).rejects.toThrow(
      'Game session completion failed: 410',
    )
    expect(mockedApiFetch).toHaveBeenCalledTimes(1)
  })
})
