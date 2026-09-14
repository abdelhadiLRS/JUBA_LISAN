import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'

interface Props {
  status: ConvStatus
  sessionActive?: boolean
  onStart: () => void
  onStop: () => void
}

export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')

  if (status === 'loading') {
    return (
      <button
        disabled
        className="border-[var(--juba-border)] bg-[var(--juba-surface)] flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-40 shadow-sm"
        aria-label={t('statusLoading')}
      >
        <span className="text-[var(--juba-muted)] animate-pulse text-xl">◌</span>
      </button>
    )
  }

  if (status === 'warming') {
    return (
      <button
        disabled
        className="border-[var(--juba-border)] bg-[var(--juba-surface)] flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60 shadow-sm"
        aria-label={t('statusWarming')}
      >
        <span className="text-[var(--juba-primary-dark)] animate-pulse text-xl">○</span>
      </button>
    )
  }

  if (status === 'connecting') {
    return (
      <button
        disabled
        className="border-[var(--juba-border)] bg-[var(--juba-surface)] flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60 shadow-sm"
        aria-label={t('statusConnecting')}
      >
        <span className="text-[var(--juba-primary-dark)] animate-pulse text-xl">○</span>
      </button>
    )
  }

  if (status === 'ready') {
    return (
      <button
        onClick={onStart}
        className="bg-[var(--juba-primary-dark)] text-white hover:brightness-95] rounded-xl px-8 py-3 text-xs font-bold tracking-widest uppercase shadow-[0_8px_20px_rgba(125,109,150,.16)] transition-all"
      >
        {t('start')}
      </button>
    )
  }

  if (status === 'live') {
    return (
      <button
        onClick={onStop}
        className="border-[color-mix(in_srgb,var(--juba-danger)_60%,var(--juba-border))] bg-[var(--juba-surface)] hover:bg-[color-mix(in_srgb,var(--juba-danger)_10%,var(--juba-surface))] group flex h-16 w-16 items-center justify-center rounded-full border-2 transition-colors"
        aria-label={t('stop')}
        title={t('stop')}
      >
        <span className="text-[var(--juba-danger)] text-lg transition-transform group-hover:scale-110">■</span>
      </button>
    )
  }

  return (
    <button
      onClick={onStart}
      className="border-[var(--juba-border)] bg-[var(--juba-surface)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-primary)] rounded-xl border px-8 py-3 text-xs tracking-widest uppercase shadow-sm transition-colors"
    >
      {t('startNew')}
    </button>
  )
}
