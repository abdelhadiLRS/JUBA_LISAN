import Link from 'next/link'
import { getTranslations } from 'next-intl/server'

export default async function NotFound() {
  const t = await getTranslations('notFound')

  return (
    <main className="juba-jl-not-found relative flex min-h-screen items-center justify-center overflow-hidden bg-[#f7f7f7] px-6 py-12 text-[#242424]">
      <style>{`.juba-jl-not-found{font-family:Nunito Sans,Noto Sans Arabic,system-ui,sans-serif}.juba-jl-not-found .juba-card{border:2px solid #e5e5e5;border-radius:22px;box-shadow:0 4px 0 rgba(0,0,0,.06)}.juba-jl-not-found .juba-404-mark{background:#58cc02;color:#fff;border:2px solid #46a302;box-shadow:0 3px 0 #46a302}.juba-jl-not-found .juba-404-pill{background:#efffe6;color:#46a302;border-color:#b9e9a0}.juba-jl-not-found .juba-404-primary{background:#58cc02;color:#fff;border:2px solid #46a302;box-shadow:0 3px 0 #46a302}.juba-jl-not-found .juba-404-secondary{border:2px solid #e5e5e5;background:#fff;color:#242424}.juba-jl-not-found .juba-404-secondary:hover{background:#efffe6;border-color:#58cc02}@media(max-width:640px){.juba-jl-not-found .juba-card{border-radius:18px}}`}</style>
      <div className="relative w-full max-w-lg">
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="juba-404-mark flex h-11 w-11 items-center justify-center rounded-2xl text-lg font-black">
            J
          </div>
          <span className="text-xl font-extrabold tracking-tight">
            JUBA <span className="text-[var(--juba-violet)]">LISAN</span>
          </span>
        </div>

        <section className="juba-card overflow-hidden bg-[var(--juba-surface)]">
          <div className="border-b border-[var(--juba-border)] px-7 py-6  sm:px-9">
            <div className="juba-404-pill mb-4 inline-flex items-center rounded-full border px-3 py-1 text-[11px] font-bold uppercase tracking-wider">
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
                className="juba-404-primary flex-1 rounded-[14px] px-6 py-3.5 text-center text-sm font-bold transition active:scale-[0.98]"
              >
                {t('dashboard')}
              </Link>
              <Link
                href="/"
                className="juba-404-secondary flex-1 rounded-[14px] px-6 py-3.5 text-center text-sm font-bold transition"
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
