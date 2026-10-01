'use client'

import { useEffect, useState } from 'react'
import { apiFetch } from '@/lib/api'

type Challenge = {
  title?: string
  description?: string
  progress?: number
  target?: number
  xp_reward?: number
}

export default function WeeklyChallenge() {
  const [challenge, setChallenge] = useState<Challenge | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    void apiFetch('/api/community/weekly-challenge', { credentials: 'include', cache: 'no-store' })
      .then(async (response) => {
        if (!response.ok) return null
        return (await response.json()) as Challenge
      })
      .catch(() => null)
      .then((data) => {
        if (active) setChallenge(data)
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => { active = false }
  }, [])

  const progress = Math.max(0, Number(challenge?.progress ?? 0))
  const target = Math.max(1, Number(challenge?.target ?? 10))
  const percent = Math.min(100, Math.round((progress / target) * 100))

  return (
    <div className="mx-auto w-full max-w-[1480px] rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <span className="juba-eyebrow">Weekly Challenge</span>
          <h2 className="mt-2 text-2xl font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-[26px]">
            {loading ? 'Loading your challenge…' : challenge?.title ?? 'Keep your learning streak alive'}
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-[var(--duo-muted)]">
            {challenge?.description ?? 'Complete focused learning activities this week and build consistent practice habits.'}
          </p>
        </div>
        <div className="shrink-0 rounded-[10px] bg-[var(--duo-green)] px-3.5 py-2.5 text-center text-white shadow-sm">
          <div className="text-xl font-black">+{challenge?.xp_reward ?? 100}</div>
          <div className="text-xs uppercase tracking-wide">XP</div>
        </div>
      </div>
      <div className="mb-2 flex justify-between text-sm font-semibold text-[var(--duo-ink)]">
        <span>{progress} / {target}</span>
        <span>{percent}%</span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-[var(--duo-line)]">
        <div className="h-full rounded-full bg-[var(--duo-green)] transition-[width] duration-500" style={{ width: percent + '%' }} />
      </div>
    </div>
  )
}
