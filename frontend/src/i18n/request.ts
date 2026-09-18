import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { getRequestConfig } from 'next-intl/server'
import { cookies, headers } from 'next/headers'
import { SUPPORTED_LOCALES, type Locale } from '@/lib/locales'

function resolveLocale(raw: string | undefined): Locale {
  if (raw && (SUPPORTED_LOCALES as readonly string[]).includes(raw)) {
    return raw as Locale
  }
  return 'en'
}

export default getRequestConfig(async () => {
  const headerStore = await headers()
  const cookieStore = await cookies()

  // x-next-locale is injected by the middleware on every request (including the
  // very first one, before the NEXT_LOCALE cookie has been written to the client)
  const locale = resolveLocale(
    headerStore.get('x-next-locale') ?? cookieStore.get('NEXT_LOCALE')?.value
  )

  const messagesDirCandidates = [
    path.join(process.cwd(), 'messages'),
    path.join(process.cwd(), '..', 'messages'),
    path.join(process.cwd(), '..', '..', 'messages'),
    path.join(process.cwd(), '..', '..', '..', 'messages'),
  ]

  async function loadMessages(requestedLocale: string) {
    for (const messagesDir of messagesDirCandidates) {
      try {
        const file = await readFile(path.join(messagesDir, `${requestedLocale}.json`), 'utf8')
        return JSON.parse(file)
      } catch {
        // Try the next known runtime location.
      }
    }
    return null
  }

  let messages = await loadMessages(locale)
  if (!messages && locale !== 'en') {
    messages = await loadMessages('en')
  }
  if (!messages) {
    throw new Error('No locale messages were found in the application runtime.')
  }

  return {
    locale,
    messages,
  }
})
