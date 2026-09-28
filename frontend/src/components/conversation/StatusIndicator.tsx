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
  return <div role="status" aria-live="polite" aria-atomic="true" className="flex items-center gap-2 rounded-full border border-[var(--duo-line)] bg-[rgba(88,204,2,.12)] px-3 py-1.5"><span className={`text-xs leading-none ${dotClass} ${pulse ? 'animate-pulse' : ''}`} aria-hidden="true">●</span><span className="text-[var(--duo-muted)] text-[0.68rem] font-semibold tracking-wide uppercase">{label}</span></div>
}