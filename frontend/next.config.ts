import createNextIntlPlugin from 'next-intl/plugin'
import type { NextConfig } from 'next'

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts')

const withBackend = (path: string) =>
  `${process.env.BACKEND_URL || 'http://localhost:8000'}${path}`

const isDesktopBuild = process.env.BUILD_TARGET === 'desktop'

const nextConfig: NextConfig = {
  poweredByHeader: false,
  // Desktop keeps the full Next.js server because the App Router uses
  // request-time cookies/headers and middleware for auth + locale handling.
  ...(isDesktopBuild ? { output: 'standalone' as const } : {}),
  // Keep Next.js/Turbopack anchored to the frontend project. The repository also
  // contains a root package-lock.json, and automatic workspace detection can
  // otherwise place the standalone output under the repository root.
  turbopack: {
    root: __dirname,
  },
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: 'backend' },
    ],
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  webpack(config, { isServer }) {
    if (isServer) {
      const externals = Array.isArray(config.externals) ? config.externals : []
      config.externals = [
        ...externals,
        '@ricky0123/vad-react',
        '@ricky0123/vad-web',
        'onnxruntime-web',
      ]
    }
    return config
  },
  async headers() {
    const headers: Array<{ key: string; value: string }> = [
      ...(isDesktopBuild ? [] : [{ key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' }]),
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(self), geolocation=()' },
      { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
      { key: 'Cross-Origin-Embedder-Policy', value: 'credentialless' },
    ]

    if (process.env.NODE_ENV === 'production') {
      headers.push({
        key: 'Content-Security-Policy',
        value: [
          "default-src 'self'",
          "script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'",
          "style-src 'self' 'unsafe-inline'",
          isDesktopBuild
            ? "connect-src 'self' http://127.0.0.1:* http://localhost:* ws: wss:"
            : "connect-src 'self' ws: wss:",
          isDesktopBuild
            ? "img-src 'self' http://127.0.0.1:* http://localhost:* data: blob:"
            : "img-src 'self' data: blob:",
          isDesktopBuild
            ? "media-src 'self' http://127.0.0.1:* http://localhost:* blob:"
            : "media-src 'self' blob:",
          "worker-src 'self' blob:",
          "font-src 'self'",
          "object-src 'none'",
          "base-uri 'self'",
        ].join('; '),
      })
    }

    return [
      {
        source: '/(.*)',
        headers,
      },
    ]
  },
  async rewrites() {
    // Desktop builds call the dynamically allocated FastAPI port directly.
    // Rewrites are only needed by the server/Docker build.
    if (isDesktopBuild) return []

    return [
      {
        source: '/api/health',
        destination: withBackend('/health'),
      },
      {
        source: '/api/:path*',
        destination: withBackend('/api/:path*'),
      },
    ]
  },
}

export default withNextIntl(nextConfig)
