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
            <div className="flex-fill min-w-0">
              <div className="d-flex align-items-center gap-2">
                <span className="placeholder col-1" style={{ minWidth: 72, height: 28 }} />
                <span className="placeholder col-1" style={{ minWidth: 84, height: 28 }} />
                <span className="placeholder col-1" style={{ minWidth: 96, height: 28 }} />
              </div>
            </div>
            <span className="placeholder rounded-circle" style={{ width: 36, height: 36 }} />
          </div>
        </header>

        <div className="juba-page-context bg-white border-bottom">
          <div className="container-xl py-3">
            <span className="placeholder col-2 mb-2" style={{ minWidth: 110, height: 12 }} />
            <div className="placeholder col-3" style={{ minWidth: 150, height: 28 }} />
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
