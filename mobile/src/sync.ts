import { apiFetch } from './api'
import { getPendingActions, removePendingAction, type PendingAction } from './offline'

export async function syncPendingActions(): Promise<{ synced: number; remaining: number }> {
  const actions = await getPendingActions()
  let synced = 0

  for (const action of actions) {
    try {
      const response = await apiFetch(action.path, {
        method: action.method,
        body: action.body ? JSON.stringify(action.body) : undefined,
      })
      if (response.ok) {
        await removePendingAction(action.id)
        synced += 1
      } else if (response.status === 401 || response.status === 403) {
        break
      }
    } catch {
      break
    }
  }

  const remaining = (await getPendingActions()).length
  return { synced, remaining }
}

export async function queueReview(cardId: number, quality: number) {
  const action: PendingAction = {
    id: `review-${cardId}-${Date.now()}`,
    method: 'POST',
    path: `/api/flashcards/${cardId}/review`,
    body: { quality },
    createdAt: Date.now(),
  }
  const { queuePendingAction } = await import('./offline')
  await queuePendingAction(action)
}
