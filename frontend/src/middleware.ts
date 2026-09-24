import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { SUPPORTED_LOCALES, type Locale } from '@/lib/locales'

// Routes that require authentication — anything else passes through so unknown
// URLs reach Next.js's 404 handler instead of being redirected to /login.
const PROTECTED_ROUTES = [
  '/admin',
  '/assessment',
  '/billing',
  '/chat',
  '/conversation',
  '/dashboard',
  '/faq',
  '/feedback',
  '/flashcards',
  '/grammar',
  '/lesson',
  '/listening',
  '/onboarding',
  '/phrasebook',
  '/plan',
  '/progress',
  '/settings',
  '/vocabulary',
]

function detectLocale(req: NextRequest): Locale {
  // 1. Cookie already set — always respect an explicit user choice.
  const cookie = req.cookies.get('NEXT_LOCALE')?.value
  if (cookie && (SUPPORTED_LOCALES as readonly string[]).includes(cookie)) {
    return cookie as Locale
  }

  // 2. Use the visitor's country when the hosting/CDN exposes it.
  // This avoids browser geolocation permission prompts and works before hydration.
  const country = (
    req.headers.get('x-vercel-ip-country') ??
    req.headers.get('cf-ipcountry') ??
    req.headers.get('x-country-code') ??
    ''
  ).trim().toUpperCase()

  const countryLocale: Record<string, Locale> = {
    DZ: 'ar',
    MA: 'fr',
    TN: 'fr',
    EG: 'ar',
    SA: 'ar',
    AE: 'ar',
    QA: 'ar',
    KW: 'ar',
    BH: 'ar',
    OM: 'ar',
    JO: 'ar',
    LB: 'ar',
    IQ: 'ar',
    SY: 'ar',
    YE: 'ar',
    FR: 'fr',
    BE: 'fr',
    LU: 'fr',
    CH: 'fr',
    ES: 'es',
    MX: 'es',
    AR: 'es',
    CL: 'es',
    CO: 'es',
    PE: 'es',
    DE: 'de',
    AT: 'de',
    IT: 'it',
    PT: 'pt',
    BR: 'pt',
    PL: 'pl',
    NL: 'nl',
    RO: 'ro',
    RU: 'ru',
    UA: 'ru',
    GB: 'en',
    US: 'en',
    CA: 'en',
    AU: 'en',
    NZ: 'en',
  }

  const locationLocale = countryLocale[country]
  if (locationLocale) return locationLocale

  // 3. Parse Accept-Language header with q-weight sorting
  const accept = req.headers.get('accept-language') ?? ''
  const parsed = accept
    .split(',')
    .map((part) => {
      const [langTag, ...params] = part.trim().split(';')
      const qParam = params.find((p) => p.trim().startsWith('q='))
      const q = qParam ? parseFloat(qParam.split('=')[1]) : 1.0
      const lang = langTag.trim().split(/[-_]/)[0].toLowerCase()
      return { lang, q: isNaN(q) ? 0 : q }
    })
    .sort((a, b) => b.q - a.q)

  for (const { lang } of parsed) {
    if ((SUPPORTED_LOCALES as readonly string[]).includes(lang)) {
      return lang as Locale
    }
  }

  // 4. Default to English
  return 'en'
}

export function middleware(req: NextRequest) {
  // Detect locale first so we can forward it as a request header.
  // This is needed because request.ts reads incoming request headers/cookies;
  // a cookie set only on the response is not visible on that same request cycle.
  const locale = detectLocale(req)

  const hasRefreshToken = req.cookies.has('refresh_token')
  const isProtected = PROTECTED_ROUTES.some((r) =>
    req.nextUrl.pathname.startsWith(r)
  )

  if (!hasRefreshToken && isProtected) {
    const response = NextResponse.redirect(new URL('/login', req.url))
    if (!req.cookies.has('NEXT_LOCALE')) {
      response.cookies.set('NEXT_LOCALE', locale, {
        path: '/',
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production' && process.env.BUILD_TARGET !== 'desktop',
        maxAge: 60 * 60 * 24 * 365,
      })
    }
    return response
  }

  // Inject locale as a request header so request.ts picks it up immediately
  // (even on the very first visit when no NEXT_LOCALE cookie exists yet)
  const requestHeaders = new Headers(req.headers)
  requestHeaders.set('x-next-locale', locale)

  const response = NextResponse.next({ request: { headers: requestHeaders } })

  // Persist as cookie for subsequent requests
  if (!req.cookies.has('NEXT_LOCALE')) {
    response.cookies.set('NEXT_LOCALE', locale, {
      path: '/',
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production' && process.env.BUILD_TARGET !== 'desktop',
      maxAge: 60 * 60 * 24 * 365,
    })
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next|favicon\.ico|api|.*\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)',
  ],
}
