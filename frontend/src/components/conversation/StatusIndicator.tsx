import { useTranslations } from 'next-intl'
export type ConvStatus = 'loading' | 'ready' | 'warming' | 'connecting' | 'live' | 'ended' | 'error'
interface Props { status: ConvStatus; userSpeaking: boolean; assistantSpeaking: boolean }
export default function StatusIndicator({ status, userSpeaking, assistantSpeaking }: Props) {
  const t = useTranslations('conversation')
  let label: string; let dotClass = 'text-[var(--duo-muted)]'; let pulse = false
  if (status === 'loading') label = t('statusLoading')
  else if (status === 'warming') { label = t('statusWarming'); pulse = true }
  else if (status === 'connecting') { label = t('statusConnecting'); pulse = true }
  else if (status === 'live') { if (userSpeaking) { label = t('statusDetecting'); dotClass = 'text-[var(--duo-green)]'; pulse = true } else if (assistantSpeaking) { label = t('statusSpeaking'); dotClass = 'text-[var(--duo-green)]'; pulse = true } else label = t('statusListening') }
  else if (status === 'ended') label = t('sessionEnded')
  else if (status === 'error') { label = t('statusError'); dotClass = 'text-[var(--duo-red)]' }
  else label = t('statusReady')
  const isPositive = status === 'ready' || status === 'live'
  const isError = status === 'error'
  const surfaceClass = isError ? 'border-[var(--duo-red)]/20 bg-[color-mix(in_srgb,var(--duo-red)_7%,transparent)]' : isPositive ? 'border-[var(--duo-green)]/20 bg-[color-mix(in_srgb,var(--duo-green)_9%,transparent)]' : 'border-[var(--duo-line)] bg-[var(--duo-card)]'
  return <div role="status" aria-live="polite" aria-atomic="true" className={'flex min-h-8 items-center gap-1.5 rounded-full border px-2.5 py-1 ' + surfaceClass}><span className={'text-[0.62rem] leading-none ' + dotClass + (pulse ? ' animate-pulse' : '')} aria-hidden="true">●</span><span className="text-[0.64rem] font-semibold tracking-[0.04em] text-[var(--duo-muted)] uppercase">{label}</span></div>
}