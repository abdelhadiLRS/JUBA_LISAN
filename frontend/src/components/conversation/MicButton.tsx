import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'
interface Props { status: ConvStatus; sessionActive?: boolean; onStart: () => void; onStop: () => void }
export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')
  if (status === 'loading' || status === 'warming' || status === 'connecting') return <button disabled className="border-[rgba(7,7,9,.08)] bg-[#fff] flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60 shadow-sm" aria-label={t(status === 'loading' ? 'statusLoading' : status === 'warming' ? 'statusWarming' : 'statusConnecting')}><span className="text-[#5862e2] animate-pulse text-xl">○</span></button>
  if (status === 'ready') return <button onClick={onStart} className="bg-[#5862e2] text-white hover:-translate-y-0.5 rounded-xl border-2 border-[#202127] px-8 py-3 text-xs font-bold tracking-widest uppercase shadow-[4px_4px_0_#202127] transition-all">{t('start')}</button>
  if (status === 'live') return <button onClick={onStop} className="border-2 border-[#b33a32] bg-[#fff] hover:bg-[#fff4f1] group flex h-16 w-16 items-center justify-center rounded-full transition-colors" aria-label={t('stop')} title={t('stop')}><span className="text-[#b33a32] text-lg transition-transform group-hover:scale-110">■</span></button>
  return <button onClick={onStart} className="border-2 border-[rgba(7,7,9,.08)] bg-[#fff] text-[rgba(32,33,39,.52)] hover:text-[#202127] hover:border-[#5862e2] rounded-xl px-8 py-3 text-xs tracking-widest uppercase shadow-sm transition-colors">{t('startNew')}</button>
}