'use client'
import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
interface Props { seconds: number }
export default function SessionTimeoutBanner({ seconds }: Props) {
  const t = useTranslations('conversation')
  const [remaining, setRemaining] = useState(seconds)
  useEffect(() => { setRemaining(seconds) }, [seconds])
  useEffect(() => { if (remaining <= 0) return; const id = setInterval(() => setRemaining((r) => Math.max(0, r - 1)), 1000); return () => clearInterval(id) }, [remaining])
  return <div className="mb-4 flex items-center gap-3 rounded-[14px] border border-[#b33a32]/20 bg-[#fff4f1] px-4 py-3 text-xs text-[#9a4138]"><span className="animate-pulse">▲</span><span>{t('warningTimeout', { seconds: remaining })}</span></div>
}