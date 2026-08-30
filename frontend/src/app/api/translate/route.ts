import { NextRequest, NextResponse } from 'next/server'

const MAX_TEXT_LENGTH = 2000

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const text = typeof body?.text === 'string' ? body.text.trim() : ''
    const target = typeof body?.target === 'string' ? body.target.trim().toLowerCase() : ''
    const source = typeof body?.source === 'string' ? body.source.trim().toLowerCase() : 'auto'

    if (!text || !target) {
      return NextResponse.json({ error: 'Text and target language are required.' }, { status: 400 })
    }

    if (text.length > MAX_TEXT_LENGTH) {
      return NextResponse.json({ error: `Text must be ${MAX_TEXT_LENGTH} characters or fewer.` }, { status: 400 })
    }

    if (!/^[a-z]{2,5}$/.test(target) || (source !== 'auto' && !/^[a-z]{2,5}$/.test(source))) {
      return NextResponse.json({ error: 'Unsupported language code.' }, { status: 400 })
    }

    const baseUrl = process.env.TRANSLATION_API_URL || 'https://api.mymemory.translated.net/get'
    const email = process.env.TRANSLATION_CONTACT_EMAIL
    const url = new URL(baseUrl)
    url.searchParams.set('q', text)
    url.searchParams.set('langpair', `${source}|${target}`)
    if (email) url.searchParams.set('de', email)

    const response = await fetch(url, {
      headers: { Accept: 'application/json' },
      next: { revalidate: 0 },
    })

    if (!response.ok) {
      return NextResponse.json({ error: 'Translation service is temporarily unavailable.' }, { status: 502 })
    }

    const data = await response.json()
    const translatedText = data?.responseData?.translatedText

    if (typeof translatedText !== 'string' || !translatedText.trim()) {
      return NextResponse.json({ error: 'No translation was returned.' }, { status: 502 })
    }

    return NextResponse.json({
      translation: translatedText.trim(),
      source,
      target,
      provider: 'configured-translation-service',
    })
  } catch {
    return NextResponse.json({ error: 'Unable to translate right now.' }, { status: 500 })
  }
}
