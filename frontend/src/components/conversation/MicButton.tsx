import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'
interface Props { status: ConvStatus; sessionActive?: boolean; onStart: () => void; onStop: () => void }
export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')
  if (status === 'loading' || status === 'warming' || status === 'connecting') return <button disabled className="flex h-16 w-16 items-center justify-center rounded-full border border-[rgba(7,7,9,.08)] bg-white opacity-60 shadow-[0_8px_20px_rgba(43,45,90,.055)]" aria-label={t(status === 'loading' ? 'statusLoading' : status === 'warming' ? 'statusWarming' : 'statusConnecting')}><span className="animate-pulse text-xl text-[#5862e2]">○</span></button>
  if (status === 'ready') return <button onClick={onStart} className="rounded-[14px] border border-[#5862e2] bg-[#5862e2] px-8 py-3 text-xs font-bold tracking-widest text-white uppercase shadow-[0_8px_18px_rgba(88,98,226,.18)] transition-transform hover:-translate-y-px"> {t('start')}</button>
  if (status === 'live') return <button onClick={onStop} className="group flex h-16 w-16 items-center justify-center rounded-full border border-[#b33a32]/30 bg-white transition-colors hover:bg-[#fff4f1]" aria-label={t('stop')} title={t('stop')}><span className="text-lg text-[#b33a32] transition-transform group-hover:scale-110">■</span></button>
  return <button onClick={onStart} className="rounded-[14px] border border-[rgba(7,7,9,.08)] bg-white px-8 py-3 text-xs tracking-widest text-[rgba(32,33,39,.52)] shadow-[0_4px_12px_rgba(43,45,90,.055)] transition-colors hover:border-[#5862e2] hover:text-[#202127] uppercase">{t('startNew')}</button>
}