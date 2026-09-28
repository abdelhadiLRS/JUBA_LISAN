import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'
interface Props { status: ConvStatus; sessionActive?: boolean; onStart: () => void; onStop: () => void }
export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')
  if (status === 'loading' || status === 'warming' || status === 'connecting') return <button disabled className="flex h-16 w-16 items-center justify-center rounded-full border border-[var(--duo-line)] bg-white opacity-60 shadow-[0_4px_12px_rgba(31,41,51,.06)]" aria-label={t(status === 'loading' ? 'statusLoading' : status === 'warming' ? 'statusWarming' : 'statusConnecting')}><span className="animate-pulse text-xl text-[var(--duo-green)]">○</span></button>
  if (status === 'ready') return <button onClick={onStart} className="rounded-[14px] border border-[var(--duo-green)] bg-[var(--duo-green)] px-8 py-3 text-xs font-bold tracking-wide text-white uppercase shadow-[0_4px_0_var(--duo-green-dark)] transition-transform hover:-translate-y-px"> {t('start')}</button>
  if (status === 'live') return <button onClick={onStop} className="group flex h-16 w-16 items-center justify-center rounded-full border border-[var(--duo-red)]/30 bg-white transition-colors hover:bg-[rgba(255,75,75,.08)]" aria-label={t('stop')} title={t('stop')}><span className="text-lg text-[var(--duo-red)] transition-transform group-hover:scale-110">■</span></button>
  return <button onClick={onStart} className="rounded-[14px] border border-[var(--duo-line)] bg-white px-8 py-3 text-xs tracking-wide text-[var(--duo-muted)] shadow-[0_4px_12px_rgba(43,45,90,.055)] transition-colors hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] uppercase">{t('startNew')}</button>
}