import { NextRequest, NextResponse } from 'next/server'

const MAX_TEXT_LENGTH = 2000
const SUPPORTED_LANGUAGES = new Set(['ar', 'en', 'fr', 'es', 'it', 'de', 'pt', 'ja', 'ko', 'zh'])

function detectLanguage(text: string) {
  if (/\p{Script=Arabic}/u.test(text)) return 'ar'
  if (/\p{Script=Hiragana}|\p{Script=Katakana}|\p{Script=Han}/u.test(text)) return /\p{Script=Han}/u.test(text) && !/\p{Script=Hiragana}|\p{Script=Katakana}/u.test(text) ? 'zh' : 'ja'
  if (/\p{Script=Hangul}/u.test(text)) return 'ko'
  if (/[àâçéèêëîïôùûüÿœæ]/i.test(text)) return 'fr'
  if (/\b(le|la|les|des|une|un|avec|pour|dans|est|bonjour)\b/i.test(text)) return 'fr'
  if (/\b(el|la|los|las|una|uno|para|con|hola|que)\b/i.test(text)) return 'es'
  if (/\b(il|lo|gli|una|uno|per|con|ciao|che)\b/i.test(text)) return 'it'
  if (/\b(der|die|das|ein|eine|und|für|mit|hallo|ist)\b/i.test(text)) return 'de'
  if (/\b(o|a|os|as|um|uma|para|com|olá|que)\b/i.test(text)) return 'pt'
  return 'en'
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const text = typeof body?.text === 'string' ? body.text.trim() : ''
    const target = typeof body?.target === 'string' ? body.target.trim().toLowerCase() : ''
    const requestedSource = typeof body?.source === 'string' ? body.source.trim().toLowerCase() : 'auto'

    if (!text || !target) {
      return NextResponse.json({ error: 'Text and target language are required.' }, { status: 400 })
    }

    if (text.length > MAX_TEXT_LENGTH) {
      return NextResponse.json({ error: `Text must be ${MAX_TEXT_LENGTH} characters or fewer.` }, { status: 400 })
    }

    if (!SUPPORTED_LANGUAGES.has(target)) {
      return NextResponse.json({ error: 'Unsupported target language.' }, { status: 400 })
    }

    const source = requestedSource === 'auto' ? detectLanguage(text) : requestedSource
    if (!SUPPORTED_LANGUAGES.has(source)) {
      return NextResponse.json({ error: 'Unsupported source language.' }, { status: 400 })
    }

    if (source === target) {
      return NextResponse.json({ translation: text, source, target, provider: 'identity' })
    }

    const baseUrl = process.env.TRANSLATION_API_URL || 'https://api.mymemory.translated.net/get'
    const email = process.env.TRANSLATION_CONTACT_EMAIL
    const url = new URL(baseUrl)
    url.searchParams.set('q', text)
    url.searchParams.set('langpair', `${source}|${target}`)
    if (email) url.searchParams.set('de', email)

    const response = await fetch(url, { headers: { Accept: 'application/json' }, cache: 'no-store' })
    if (!response.ok) return NextResponse.json({ error: 'Translation service is temporarily unavailable.' }, { status: 502 })

    const data = await response.json()
    const translatedText = data?.responseData?.translatedText
    if (typeof translatedText !== 'string' || !translatedText.trim()) return NextResponse.json({ error: 'No translation was returned.' }, { status: 502 })

    return NextResponse.json({ translation: translatedText.trim(), source, target, provider: 'configured-translation-service' })
  } catch {
    return NextResponse.json({ error: 'Unable to translate right now.' }, { status: 500 })
  }
}
