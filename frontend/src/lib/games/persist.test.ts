import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '@/lib/api'
import { persistGameEvent } from './persist'

vi.mock('@/lib/api', () => ({
  apiFetch: vi.fn(),
}))

const mockedApiFetch = vi.mocked(apiFetch)

const serverStats = {
  total_xp: 160,
  games_played: 1,
  questions_answered: 5,
  correct_answers: 5,
  best_round_score: 25,
  daily_challenges_completed: 0,
  last_daily_challenge_date: '',
  current_correct_streak: 5,
  best_correct_streak: 5,
  achievements: ['first_game'],
}

describe('persistGameEvent', () => {
  beforeEach(() => {
    mockedApiFetch.mockReset()
    vi.spyOn(globalThis.crypto, 'randomUUID').mockReturnValue('event-1234')
  })

  it('reuses one generated event id when a network response is lost', async () => {
    mockedApiFetch
      .mockRejectedValueOnce(new Error('network timeout'))
      .mockResolvedValueOnce(
        new Response(JSON.stringify(serverStats), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    await expect(
      persistGameEvent({
        gameId: 'math',
        questionsAnswered: 5,
        correctAnswers: 5,
        roundScore: 25,
      }),
    ).resolves.toEqual(serverStats)

    expect(mockedApiFetch).toHaveBeenCalledTimes(2)
    const firstBody = JSON.parse(String(mockedApiFetch.mock.calls[0][1]?.body))
    const secondBody = JSON.parse(String(mockedApiFetch.mock.calls[1][1]?.body))
    expect(firstBody.event_id).toBe('event-1234')
    expect(secondBody.event_id).toBe('event-1234')
  })

  it('keeps a caller supplied event id across retries', async () => {
    mockedApiFetch
      .mockRejectedValueOnce(new Error('network timeout'))
      .mockResolvedValueOnce(
        new Response(JSON.stringify(serverStats), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    await persistGameEvent({
      eventId: 'stable-event',
      gameId: 'memory',
      questionsAnswered: 6,
      correctAnswers: 4,
      roundScore: 25,
    })

    const firstBody = JSON.parse(String(mockedApiFetch.mock.calls[0][1]?.body))
    const secondBody = JSON.parse(String(mockedApiFetch.mock.calls[1][1]?.body))
    expect(firstBody.event_id).toBe('stable-event')
    expect(secondBody.event_id).toBe('stable-event')
  })

  it('does not retry non-success HTTP responses', async () => {
    mockedApiFetch.mockResolvedValue(
      new Response(JSON.stringify({ detail: 'bad request' }), { status: 422 }),
    )

    await expect(
      persistGameEvent({
        gameId: 'ordering',
        questionsAnswered: 1,
        correctAnswers: 0,
        roundScore: 0,
      }),
    ).rejects.toThrow('Game event failed: 422')

    expect(mockedApiFetch).toHaveBeenCalledTimes(1)
  })
})
