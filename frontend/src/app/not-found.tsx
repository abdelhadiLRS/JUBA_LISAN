import Link from 'next/link'
import { getTranslations } from 'next-intl/server'

export default async function NotFound() {
  const t = await getTranslations('notFound')

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--juba-bg)] px-6 py-12 text-[var(--juba-text)]">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(108,69,245,0.16),transparent_42%)]" />
      <div className="relative w-full max-w-lg">
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[var(--juba-violet)] text-lg font-black text-white shadow-lg shadow-[var(--juba-shadow-md)]">
            J
          </div>
          <span className="text-xl font-extrabold tracking-tight">
            JUBA <span className="text-[var(--juba-violet)]">LISAN</span>
          </span>
        </div>

        <section className="juba-card overflow-hidden bg-[var(--juba-surface)]">
          <div className="border-b border-[var(--juba-border)] px-7 py-6  sm:px-9">
            <div className="mb-4 inline-flex items-center rounded-full border border-[var(--juba-border)] bg-[var(--juba-lilac)] px-3 py-1 text-[11px] font-bold uppercase tracking-wider text-[var(--juba-violet)]">
              404
            </div>
            <h1 className="text-2xl font-black tracking-tight text-[var(--juba-text)]">
              {t('title')}
            </h1>
          </div>

          <div className="space-y-6 px-7 py-7 sm:px-9 sm:py-8">
            <p className="text-sm leading-7 text-[var(--juba-muted)]">
              {t('body')}
            </p>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Link
                href="/dashboard"
                className="flex-1 rounded-[18px] bg-[var(--juba-violet)] px-6 py-3.5 text-center text-sm font-bold text-white shadow-md shadow-[var(--juba-shadow-md)] transition hover:bg-[var(--juba-violet-dark)] active:scale-[0.98]"
              >
                {t('dashboard')}
              </Link>
              <Link
                href="/"
                className="flex-1 rounded-[18px] border border-[var(--juba-border)] px-6 py-3.5 text-center text-sm font-bold text-[var(--juba-text)] transition hover:bg-neutral-50   hover:bg-[var(--juba-lilac)]"
              >
                {t('home')}
              </Link>
            </div>
          </div>
        </section>

        <p className="mt-6 text-center text-xs text-neutral-400 dark:text-neutral-600">
          © {new Date().getFullYear()} JUBA LISAN
        </p>
      </div>
    </main>
  )
}
