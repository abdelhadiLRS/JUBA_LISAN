import { useTranslations } from 'next-intl'
export type ConvStatus = 'loading' | 'ready' | 'warming' | 'connecting' | 'live' | 'ended' | 'error'
interface Props { status: ConvStatus; userSpeaking: boolean; assistantSpeaking: boolean }
export default function StatusIndicator({ status, userSpeaking, assistantSpeaking }: Props) {
  const t = useTranslations('conversation')
  let label: string; let dotClass = 'text-[rgba(32,33,39,.52)]'; let pulse = false
  if (status === 'loading') label = t('statusLoading')
  else if (status === 'warming') { label = t('statusWarming'); pulse = true }
  else if (status === 'connecting') { label = t('statusConnecting'); pulse = true }
  else if (status === 'live') { if (userSpeaking) { label = t('statusDetecting'); dotClass = 'text-[#5862e2]'; pulse = true } else if (assistantSpeaking) { label = t('statusSpeaking'); dotClass = 'text-[#5862e2]'; pulse = true } else label = t('statusListening') }
  else if (status === 'ended') label = t('sessionEnded')
  else if (status === 'error') { label = t('statusError'); dotClass = 'text-[#b33a32]' }
  else label = t('statusReady')
  return <div className="flex items-center gap-2 rounded-full border border-[rgba(7,7,9,.08)] bg-[#ededff] px-3 py-1.5"><span className={`text-xs leading-none ${dotClass} ${pulse ? 'animate-pulse' : ''}`} aria-hidden="true">●</span><span className="text-[rgba(32,33,39,.52)] text-[0.68rem] font-semibold tracking-[0.14em] uppercase">{label}</span></div>
}