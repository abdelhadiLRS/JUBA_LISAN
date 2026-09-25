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
    <div className="mx-auto max-w-4xl rounded-[28px] border-2 border-[var(--juba-lilac)] bg-[var(--juba-bg)] p-8 shadow-[var(--juba-shadow-sm)]">
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <span className="juba-eyebrow">Weekly Challenge</span>
          <h2 className="mt-2 text-3xl font-bold text-[var(--juba-text)]">
            {loading ? 'Loading your challenge…' : challenge?.title ?? 'Keep your learning streak alive'}
          </h2>
          <p className="mt-2 text-[var(--juba-text-muted)]">
            {challenge?.description ?? 'Complete focused learning activities this week and build consistent practice habits.'}
          </p>
        </div>
        <div className="rounded-2xl bg-[var(--juba-violet)] px-4 py-3 text-center text-white">
          <div className="text-2xl font-black">+{challenge?.xp_reward ?? 100}</div>
          <div className="text-xs uppercase tracking-wide">XP</div>
        </div>
      </div>
      <div className="mb-2 flex justify-between text-sm font-semibold text-[var(--juba-text)]">
        <span>{progress} / {target}</span>
        <span>{percent}%</span>
      </div>
      <div className="h-4 overflow-hidden rounded-full bg-[var(--juba-line)]">
        <div className="h-full rounded-full bg-[var(--juba-violet)] transition-[width] duration-500" style={{ width: percent + '%' }} />
      </div>
    </div>
  )
}
