import { useTranslations } from 'next-intl'

export default function AppLoading() {
  const t = useTranslations('common')

  return (
    <div className="juba-duo-shell min-h-screen bg-[#f8faf7] text-[#30343b]">
      <aside className="juba-duo-sidebar hidden lg:flex">
        <div className="juba-duo-logo-mark" aria-hidden="true">JL</div>
        <div className="mt-6 w-full space-y-2">
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-11 w-full rounded-xl" />
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-11 w-full rounded-xl" />
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-11 w-full rounded-xl" />
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-11 w-full rounded-xl" />
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-11 w-full rounded-xl" />
        </div>
        <div className="mt-auto w-full space-y-2">
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-10 w-full rounded-xl" />
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse block h-10 w-full rounded-xl" />
        </div>
      </aside>

      <div className="juba-duo-main min-h-screen">
        <header className="flex items-center justify-between border-b border-[#e1e5e2] bg-white px-4 py-3 lg:hidden">
          <div className="juba-duo-mobile-brand">JUBA LISAN</div>
          <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-10 w-10 rounded-xl" />
        </header>

        <main className="min-h-screen bg-[#f8faf7] px-3 py-5 sm:px-6 sm:py-8">
          <div className="mx-auto max-w-6xl space-y-5">
            <section className="rounded-2xl border border-[#e1e5e2] bg-white p-5 sm:p-7">
              <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-4 w-28 rounded-lg" />
              <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-3 h-8 w-2/3 max-w-md rounded-lg" />
              <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-3 h-4 w-full max-w-xl rounded-lg" />
              <div className="mt-6 flex flex-wrap gap-3">
                <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-10 w-24 rounded-xl" />
                <span className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-10 w-24 rounded-xl" />
              </div>
            </section>

            <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
              <section className="rounded-2xl border border-[#e1e5e2] bg-white p-5 sm:p-7">
                <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-5 w-32 rounded-lg" />
                <div className="mt-5 space-y-4">
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-20 w-full rounded-2xl" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-20 w-full rounded-2xl" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-20 w-full rounded-2xl" />
                </div>
              </section>

              <aside className="space-y-4">
                <div className="rounded-2xl border border-[#e1e5e2] bg-white p-5">
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-5 w-28 rounded-lg" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-4 h-3 w-full rounded-lg" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-2 h-3 w-4/5 rounded-lg" />
                </div>
                <div className="rounded-2xl border border-[#e1e5e2] bg-white p-5">
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse h-5 w-36 rounded-lg" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-4 h-3 w-full rounded-lg" />
                  <div className="juba-loading-pill bg-[#f1f7ed] animate-pulse mt-2 h-3 w-3/5 rounded-lg" />
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
