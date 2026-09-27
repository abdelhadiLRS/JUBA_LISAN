'use client'
import { AlertTriangle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
interface Props { seconds: number }
export default function SessionTimeoutBanner({ seconds }: Props) {
  const t = useTranslations('conversation')
  const [remaining, setRemaining] = useState(seconds)
  useEffect(() => { setRemaining(seconds) }, [seconds])
  useEffect(() => { if (remaining <= 0) return; const id = setInterval(() => setRemaining((r) => Math.max(0, r - 1)), 1000); return () => clearInterval(id) }, [remaining])
  return <div role="alert" aria-live="polite" className="mb-4 flex items-center gap-3 rounded-2xl border border-[#f2c9c5] bg-[#fff5f4] px-4 py-3 font-sans text-sm font-semibold text-[#a8322b] shadow-[0_3px_0_rgba(168,50,43,.06)]"><AlertTriangle size={17} aria-hidden="true" className="shrink-0 animate-pulse" /><span>{t('warningTimeout', { seconds: remaining })}</span></div>
}