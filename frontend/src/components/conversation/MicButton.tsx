import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'
interface Props { status: ConvStatus; sessionActive?: boolean; onStart: () => void; onStop: () => void }
export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')
  if (status === 'loading' || status === 'warming' || status === 'connecting') return <button disabled className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60 shadow-sm" aria-label={t(status === 'loading' ? 'statusLoading' : status === 'warming' ? 'statusWarming' : 'statusConnecting')}><span className="text-[var(--juba-app-green)] animate-pulse text-xl">○</span></button>
  if (status === 'ready') return <button onClick={onStart} className="bg-[var(--juba-app-green)] text-white hover:-translate-y-0.5 rounded-xl border-2 border-[var(--juba-app-ink)] px-8 py-3 text-xs font-bold tracking-widest uppercase shadow-[4px_4px_0_var(--juba-app-ink)] transition-all">{t('start')}</button>
  if (status === 'live') return <button onClick={onStop} className="border-2 border-[#b33a32] bg-[var(--juba-app-surface)] hover:bg-[#fff4f1] group flex h-16 w-16 items-center justify-center rounded-full transition-colors" aria-label={t('stop')} title={t('stop')}><span className="text-[#b33a32] text-lg transition-transform group-hover:scale-110">■</span></button>
  return <button onClick={onStart} className="border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] hover:border-[var(--juba-app-green)] rounded-xl px-8 py-3 text-xs tracking-widest uppercase shadow-sm transition-colors">{t('startNew')}</button>
}