import { useTranslations } from 'next-intl'

export default function AppLoading() {
  const t = useTranslations('common')

  return (
    <div className="juba-app-shell min-h-screen bg-[var(--juba-bg,var(--duo-bg))] text-[var(--juba-ink,var(--duo-ink))]">
      <aside className="juba-duo-sidebar hidden lg:flex">
        <div className="juba-duo-logo-mark" aria-hidden="true">JL</div>
        <div className="mt-6 w-full space-y-2">
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-11 w-full rounded-[10px]" />
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-11 w-full rounded-[10px]" />
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-11 w-full rounded-[10px]" />
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-11 w-full rounded-[10px]" />
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-11 w-full rounded-[10px]" />
        </div>
        <div className="mt-auto w-full space-y-2">
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-10 w-full rounded-[10px]" />
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse block h-10 w-full rounded-[10px]" />
        </div>
      </aside>

      <div className="juba-main min-h-screen">
        <header className="flex items-center justify-between border-b border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] px-4 py-3 lg:hidden">
          <div className="juba-duo-mobile-brand">JUBA LISAN</div>
          <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-10 w-10 rounded-[10px]" />
        </header>

        <main aria-busy="true" className="min-h-screen bg-[var(--juba-bg,var(--duo-bg))] px-3 py-5 sm:px-6 sm:py-8">
          <div className="mx-auto max-w-6xl space-y-5">
            <section className="rounded-[10px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-5 sm:p-7">
              <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-4 w-28 rounded-lg" />
              <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-3 h-8 w-2/3 max-w-md rounded-lg" />
              <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-3 h-4 w-full max-w-xl rounded-lg" />
              <div className="mt-6 flex flex-wrap gap-3">
                <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-10 w-24 rounded-[10px]" />
                <span className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-10 w-24 rounded-[10px]" />
              </div>
            </section>

            <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
              <section className="rounded-[10px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-5 sm:p-7">
                <div className="flex items-center justify-between gap-3"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-5 w-32 rounded-lg" /><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-4 w-16 rounded-lg" /></div>
                <div className="mt-5 h-2 overflow-hidden rounded-[10px] bg-[var(--juba-bg,var(--duo-bg))]"><div className="juba-loading-pill bg-[var(--juba-green,var(--duo-green))/20] animate-pulse h-full w-1/3 rounded-[10px]" /></div>
                <div className="mt-5 space-y-4">
                  <div className="flex items-center gap-4 rounded-[10px] border border-[var(--juba-border,var(--duo-line))] p-4"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-14 w-14 shrink-0 rounded-full" /><div className="flex-1 space-y-2"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-4 w-3/5 rounded-lg" /><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-3 w-2/5 rounded-lg" /></div></div>
                  <div className="flex items-center gap-4 rounded-[10px] border border-[var(--juba-border,var(--duo-line))] p-4"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-14 w-14 shrink-0 rounded-full" /><div className="flex-1 space-y-2"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-4 w-2/3 rounded-lg" /><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-3 w-1/2 rounded-lg" /></div></div>
                  <div className="flex items-center gap-4 rounded-[10px] border border-[var(--juba-border,var(--duo-line))] p-4"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-14 w-14 shrink-0 rounded-full" /><div className="flex-1 space-y-2"><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-4 w-1/2 rounded-lg" /><div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-3 w-2/5 rounded-lg" /></div></div>
                </div>
              </section>

              <aside className="space-y-4">
                <div className="rounded-[10px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-5">
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-5 w-28 rounded-lg" />
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-4 h-3 w-full rounded-lg" />
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-2 h-3 w-4/5 rounded-lg" />
                </div>
                <div className="rounded-[10px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-5">
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse h-5 w-36 rounded-lg" />
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-4 h-3 w-full rounded-lg" />
                  <div className="juba-loading-pill bg-[var(--juba-bg,var(--duo-bg))] animate-pulse mt-2 h-3 w-3/5 rounded-lg" />
                </div>
              </aside>
            </div>

            <div className="visually-hidden" role="status" aria-live="polite">
              {t('loading')}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
