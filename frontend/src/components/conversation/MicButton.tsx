import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'
interface Props { status: ConvStatus; sessionActive?: boolean; onStart: () => void; onStop: () => void }
export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')
  if (status === 'loading' || status === 'warming' || status === 'connecting') return <button disabled className="flex h-16 w-16 items-center justify-center rounded-full border border-[var(--duo-line)] bg-[var(--duo-card)] opacity-60 shadow-sm" aria-label={t(status === 'loading' ? 'statusLoading' : status === 'warming' ? 'statusWarming' : 'statusConnecting')}><span className="animate-pulse text-xl text-[var(--duo-green)]">○</span></button>
  if (status === 'ready') return <button onClick={onStart} className="rounded-[10px] border border-[var(--duo-green)] bg-[var(--duo-green)] px-8 py-3 text-xs font-bold tracking-wide text-white uppercase shadow-sm transition-colors hover:bg-[var(--duo-green-dark)]"> {t('start')}</button>
  if (status === 'live') return <button onClick={onStop} className="group flex h-16 w-16 items-center justify-center rounded-full border border-[var(--duo-red)]/30 bg-[var(--duo-card)] transition-colors hover:bg-[color-mix(in_srgb,var(--duo-red)_8%,transparent)]" aria-label={t('stop')} title={t('stop')}><span className="text-lg text-[var(--duo-red)] transition-transform group-hover:scale-110">■</span></button>
  return <button onClick={onStart} className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-8 py-3 text-xs tracking-wide text-[var(--duo-muted)] shadow-sm transition-colors hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] uppercase">{t('startNew')}</button>
}