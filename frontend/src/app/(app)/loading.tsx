import { useTranslations } from 'next-intl'

export default function AppLoading() {
  const t = useTranslations('common')

  return (
    <div className="page juba-tabler-app min-h-screen bg-[#f5f7fb]">
      <div className="page-wrapper min-w-0 w-100">
        <header className="navbar navbar-expand-md navbar-light bg-white border-bottom">
          <div className="container-fluid flex-nowrap gap-3">
            <div className="navbar-brand d-flex align-items-center gap-2 me-2">
              <span className="avatar avatar-sm rounded-2 bg-primary text-white fw-bold">JL</span>
              <span className="fw-bold text-dark">JUBA LISAN</span>
            </div>
            <div className="flex-fill overflow-visible min-w-0 juba-top-nav-shell">
              <div className="navbar-nav flex-row flex-nowrap align-items-center gap-1 juba-top-nav">
                <span className="placeholder rounded-2" style={{ width: 72, height: 28 }} />
                <span className="placeholder rounded-2" style={{ width: 84, height: 28 }} />
                <span className="placeholder rounded-2" style={{ width: 96, height: 28 }} />
                <span className="placeholder rounded-2" style={{ width: 88, height: 28 }} />
              </div>
            </div>
            <div className="navbar-nav flex-row align-items-center gap-2 ms-auto">
              <span className="placeholder rounded-circle" style={{ width: 36, height: 36 }} />
              <span className="placeholder rounded-2" style={{ width: 76, height: 28 }} />
              <span className="placeholder rounded-circle" style={{ width: 36, height: 36 }} />
              <span className="placeholder rounded-2" style={{ width: 36, height: 28 }} />
            </div>
          </div>
        </header>

        <div className="juba-page-context bg-white border-bottom">
          <div className="container-xl py-3">
            <div className="d-flex align-items-center gap-3">
              <span className="placeholder rounded-2 flex-shrink-0" style={{ width: 40, height: 40 }} />
              <div className="min-w-0">
                <span className="placeholder d-block mb-2" style={{ width: 110, height: 10 }} />
                <span className="placeholder d-block" style={{ width: 150, height: 24 }} />
              </div>
            </div>
          </div>
        </div>

        <main className="page-body bg-[#f5f7fb]">
          <div className="container-xl py-4">
            <div className="juba-app-page">
              <div className="row g-4">
                <div className="col-12">
                  <div className="card">
                    <div className="card-body p-4">
                      <div className="placeholder col-5 mb-3" style={{ height: 28 }} />
                      <div className="placeholder col-8 mb-2" style={{ height: 14 }} />
                      <div className="placeholder col-6" style={{ height: 14 }} />
                    </div>
                  </div>
                </div>
                <div className="col-12 col-md-6">
                  <div className="card h-100">
                    <div className="card-body p-4">
                      <div className="placeholder col-4 mb-3" style={{ height: 20 }} />
                      <div className="placeholder col-10 mb-2" style={{ height: 12 }} />
                      <div className="placeholder col-7" style={{ height: 12 }} />
                    </div>
                  </div>
                </div>
                <div className="col-12 col-md-6">
                  <div className="card h-100">
                    <div className="card-body p-4">
                      <div className="placeholder col-4 mb-3" style={{ height: 20 }} />
                      <div className="placeholder col-10 mb-2" style={{ height: 12 }} />
                      <div className="placeholder col-7" style={{ height: 12 }} />
                    </div>
                  </div>
                </div>
              </div>
              <div className="visually-hidden" role="status" aria-live="polite">
                {t('loading')}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
