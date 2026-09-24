import { useTranslations } from 'next-intl'

export type ConvStatus =
  | 'loading'
  | 'ready'
  | 'warming'
  | 'connecting'
  | 'live'
  | 'ended'
  | 'error'

interface Props { status: ConvStatus; userSpeaking: boolean; assistantSpeaking: boolean }

export default function StatusIndicator({ status, userSpeaking, assistantSpeaking }: Props) {
  const t = useTranslations('conversation')
  let label: string
  let dotClass = 'text-[var(--juba-app-muted)]'
  let pulse = false
  if (status === 'loading') label = t('statusLoading')
  else if (status === 'warming') { label = t('statusWarming'); pulse = true }
  else if (status === 'connecting') { label = t('statusConnecting'); pulse = true }
  else if (status === 'live') {
    if (userSpeaking) { label = t('statusDetecting'); dotClass = 'text-[var(--juba-app-green)]'; pulse = true }
    else if (assistantSpeaking) { label = t('statusSpeaking'); dotClass = 'text-[var(--juba-app-green)]'; pulse = true }
    else label = t('statusListening')
  } else if (status === 'ended') label = t('sessionEnded')
  else if (status === 'error') { label = t('statusError'); dotClass = 'text-[#b33a32]' }
  else label = t('statusReady')
  return <div className="flex items-center gap-2 rounded-full border border-[var(--juba-app-line)] bg-[#f3f7ef] px-3 py-1.5">
    <span className={`text-xs leading-none ${dotClass} ${pulse ? 'animate-pulse' : ''}`} aria-hidden="true">●</span>
    <span className="text-[var(--juba-app-muted)] text-[0.68rem] font-semibold tracking-[0.14em] uppercase">{label}</span>
  </div>
}