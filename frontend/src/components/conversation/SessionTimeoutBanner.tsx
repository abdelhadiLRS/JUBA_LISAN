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
  return <div role="alert" aria-live="polite" className="mb-3 flex min-h-9 items-center gap-2 rounded-[10px] border border-[color-mix(in_srgb,var(--duo-red)_22%,transparent)] bg-[color-mix(in_srgb,var(--duo-red)_6%,transparent)] px-3 py-2 font-sans text-[0.68rem] font-semibold leading-5 text-[var(--duo-red)] shadow-sm sm:px-3.5"><AlertTriangle size={14} aria-hidden="true" className="shrink-0 animate-pulse" /><span>{t('warningTimeout', { seconds: remaining })}</span></div>
}