import { beforeEach, describe, expect, it, vi } from 'vitest'

const authState = {
  accessToken: 'test-access-token' as string | null,
  setTokens: vi.fn(),
  logout: vi.fn(),
}

const loadingState = {
  inc: vi.fn(),
  dec: vi.fn(),
}

vi.mock('@/store/auth', () => ({
  useAuthStore: {
    getState: () => authState,
  },
}))

vi.mock('@/store/loading', () => ({
  useLoadingStore: {
    getState: () => loadingState,
  },
}))

describe('syncGuestMemoryAfterLogin', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    authState.accessToken = 'test-access-token'
    document.cookie = 'juba_guest_id=; Max-Age=0; Path=/'
    localStorage.clear()
  })

  it('uses the active language even when an inactive language appears first', async () => {
    localStorage.setItem(
      'juba_lisan_saved_vocabulary',
      JSON.stringify([
        { source: 'ar', target: 'fr', word: 'bonjour', translation: 'مرحبا' },
        { source: 'ar', target: 'en', word: 'book', translation: 'كتاب' },
      ])
    )

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input)
      if (url.endsWith('/api/languages')) {
        return new Response(
          JSON.stringify({
            languages: [
              { target_language: 'fr-FR', is_active: false },
              { target_language: 'en-US', is_active: true },
            ],
          }),
          { status: 200, headers: { 'Content-Type': 'application/json' } }
        )
      }
      if (url.endsWith('/api/flashcards/bulk')) {
        return new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      }
      throw new Error(`Unexpected request: ${url}`)
    })

    const { syncGuestMemoryAfterLogin } = await import('@/lib/api')
    await expect(syncGuestMemoryAfterLogin()).resolves.toBe(true)

    const bulkRequest = fetchMock.mock.calls.find(([input]) => String(input).endsWith('/api/flashcards/bulk'))
    expect(bulkRequest).toBeDefined()
    expect(JSON.parse(String(bulkRequest?.[1]?.body))).toMatchObject({
      flashcards: [
        expect.objectContaining({ word: 'book', definition: 'كتاب' }),
      ],
    })
    expect(localStorage.getItem('juba_lisan_saved_vocabulary')).toContain('bonjour')
    expect(localStorage.getItem('juba_lisan_saved_vocabulary')).not.toContain('book')
    expect(JSON.parse(localStorage.getItem('juba_lisan_sync_notice') || '{}')).toMatchObject({
      status: 'synced',
      count: 1,
    })
  })
})
