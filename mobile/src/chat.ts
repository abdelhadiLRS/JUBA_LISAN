import { apiFetch } from './api'

export type ChatEvent =
  | { type: 'conversation'; conversationId: number }
  | { type: 'token'; token: string }
  | { type: 'memory_updated' }
  | { type: 'response_reset' }
  | { type: 'done' }
  | { type: 'error'; message: string }

export type ChatResult = {
  conversationId: number | null
  response: string
  memoryUpdated: boolean
}

export type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

function parseEventLine(line: string): Record<string, unknown> | null {
  if (!line.startsWith('data:')) return null
  const payload = line.slice(5).trim()
  if (!payload) return null
  try {
    return JSON.parse(payload) as Record<string, unknown>
  } catch {
    return null
  }
}

export async function getLatestChatConversation(): Promise<{ id: number; title: string } | null> {
  const response = await apiFetch('/api/chat/conversations')
  if (!response.ok) return null
  const data = (await response.json()) as Array<{ id?: unknown; title?: unknown }>
  const first = data[0]
  if (!first || typeof first.id !== 'number') return null
  return { id: first.id, title: typeof first.title === 'string' ? first.title : 'Conversation' }
}

export async function createChatConversation(title = 'New conversation'): Promise<{ id: number; title: string }> {
  const response = await apiFetch('/api/chat/conversations', {
    method: 'POST',
    body: JSON.stringify({ title }),
  })
  const body = await response.text()
  if (!response.ok) {
    let detail = 'Unable to create a new conversation.'
    try {
      const parsed = JSON.parse(body) as { detail?: unknown }
      if (typeof parsed.detail === 'string') detail = parsed.detail
    } catch {
      // Keep the generic message for non-JSON error bodies.
    }
    throw new Error(detail)
  }
  const data = JSON.parse(body) as { id?: unknown; title?: unknown }
  if (typeof data.id !== 'number') throw new Error('The conversation service returned an invalid conversation.')
  return { id: data.id, title: typeof data.title === 'string' ? data.title : title }
}

export async function getChatMessages(conversationId: number): Promise<ChatMessage[]> {
  const response = await apiFetch(`/api/chat/conversations/${conversationId}/messages`)
  if (!response.ok) return []
  const data = (await response.json()) as { messages?: unknown }
  if (!Array.isArray(data.messages)) return []
  return data.messages.filter((message): message is ChatMessage => {
    if (!message || typeof message !== 'object') return false
    const item = message as { role?: unknown; content?: unknown }
    return (item.role === 'user' || item.role === 'assistant') && typeof item.content === 'string'
  })
}

/**
 * Sends a message to the real backend tutor endpoint.
 *
 * The backend uses Server-Sent Events. We intentionally collect the response
 * here instead of depending on ReadableStream support, so the helper also
 * works in React Native environments where streaming fetch bodies vary.
 */
export async function sendChatMessage(
  message: string,
  conversationId?: number,
): Promise<ChatResult> {
  const trimmed = message.trim()
  if (!trimmed) throw new Error('Message cannot be empty.')

  const response = await apiFetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      message: trimmed,
      ...(conversationId ? { conversation_id: conversationId } : {}),
    }),
  })

  const body = await response.text()
  if (!response.ok) {
    let detail = 'Unable to contact the language tutor.'
    try {
      const parsed = JSON.parse(body) as { detail?: unknown }
      if (typeof parsed.detail === 'string') detail = parsed.detail
    } catch {
      // Keep the generic message for non-JSON error bodies.
    }
    throw new Error(detail)
  }

  let currentConversationId = conversationId ?? null
  let answer = ''
  let memoryUpdated = false
  let responseWasReset = false
  let backendError: string | null = null

  for (const line of body.split(/\r?\n/)) {
    const event = parseEventLine(line)
    if (!event) continue

    if (typeof event.conversation_id === 'number') currentConversationId = event.conversation_id
    if (typeof event.token === 'string') {
      if (responseWasReset) {
        answer = ''
        responseWasReset = false
      }
      answer += event.token
    }
    if (event.memory_updated === true) memoryUpdated = true
    if (event.response_reset === true) responseWasReset = true
    if (typeof event.error === 'string') backendError = event.error
  }

  if (backendError) throw new Error(backendError)
  if (!answer.trim()) throw new Error('The language tutor returned an empty response.')

  return { conversationId: currentConversationId, response: answer, memoryUpdated }
}
