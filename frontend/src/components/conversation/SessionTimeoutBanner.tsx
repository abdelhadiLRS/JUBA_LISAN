'use client'
import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
interface Props { seconds: number }
export default function SessionTimeoutBanner({ seconds }: Props) {
  const t = useTranslations('conversation')
  const [remaining, setRemaining] = useState(seconds)
  useEffect(() => { setRemaining(seconds) }, [seconds])
  useEffect(() => { if (remaining <= 0) return; const id = setInterval(() => setRemaining((r) => Math.max(0, r - 1)), 1000); return () => clearInterval(id) }, [remaining])
  return <div className="border-2 border-[#d7b2ad] bg-[#fff7f5] text-[#9a4138] mb-4 flex items-center gap-3 rounded-xl px-4 py-3 text-xs"><span className="animate-pulse">▲</span><span>{t('warningTimeout', { seconds: remaining })}</span></div>
}