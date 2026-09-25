import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params
  const baseUrl = BACKEND_URL.endsWith('/') ? BACKEND_URL.slice(0, -1) : BACKEND_URL
  const backendUrl = `${baseUrl}/api/${path.join('/')}`
  const headers = new Headers(request.headers)

  // The browser talks to Next.js; forward the request context the FastAPI
  // application needs for authentication and CORS-independent local development.
  headers.delete('host')
  headers.delete('content-length')
  headers.delete('connection')

  const init: RequestInit = {
    method: request.method,
    headers,
    redirect: 'manual',
    cache: 'no-store',
  }

  if (request.method !== 'GET' && request.method !== 'HEAD') {
    init.body = await request.arrayBuffer()
  }

  try {
    const response = await fetch(backendUrl, init)
    const responseHeaders = new Headers(response.headers)
    responseHeaders.delete('content-encoding')
    responseHeaders.delete('content-length')

    return new NextResponse(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    })
  } catch (error) {
    console.error('[JUBA LISAN API proxy] Backend unavailable:', error)
    return NextResponse.json(
      { detail: 'Backend API is unavailable' },
      { status: 503 },
    )
  }
}

export const GET = proxy
export const POST = proxy
export const PUT = proxy
export const PATCH = proxy
export const DELETE = proxy
export const HEAD = proxy
export const OPTIONS = proxy
