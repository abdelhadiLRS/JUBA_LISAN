'use client'

import Image from 'next/image'
import { useState } from 'react'
import type { CSSProperties } from 'react'
import { Mic, Pause, Play, Sparkles, Volume2 } from 'lucide-react'

interface LandingAiTutorShowcaseProps {
  dir?: 'ltr' | 'rtl'
  imageAlt: string
  userMessage: string
  aiMessage: string
  activeLabel: string
  speakingLabel: string
  openLabel: string
  href?: string
}

export function LandingAiTutorShowcase({
  dir = 'ltr',
  imageAlt,
  userMessage,
  aiMessage,
  activeLabel,
  speakingLabel,
  openLabel,
  href = '/conversation',
}: LandingAiTutorShowcaseProps) {
  const [playing, setPlaying] = useState(false)

  return (
    <>
      <style>{`
        .juba-jl-ai-showcase {
          background: var(--juba-learning-green-soft, #efffe6) !important;
          color: var(--juba-learning-ink, #242424) !important;
        }
        .juba-jl-ai-showcase .juba-ai-showcase-art {
          border-color: var(--juba-learning-ink, #242424) !important;
          background: #fff !important;
          box-shadow: 8px 9px 0 var(--juba-learning-ink, #242424) !important;
        }
        .juba-jl-ai-showcase .juba-ai-showcase-copy h2 {
          color: var(--juba-learning-ink, #242424) !important;
        }
        .juba-jl-ai-showcase .juba-ai-chat-user {
          background: #fff !important;
          border-color: var(--juba-learning-ink, #242424) !important;
        }
        .juba-jl-ai-showcase .juba-ai-chat-tutor {
          background: var(--juba-learning-green-soft, #efffe6) !important;
          border-color: var(--juba-learning-green-dark, #46a302) !important;
        }
        .juba-jl-ai-showcase .juba-ai-wave i {
          background: var(--juba-learning-green, #58cc02) !important;
        }
        .juba-jl-ai-showcase .juba-ai-play {
          background: var(--juba-learning-green, #58cc02) !important;
          border-color: var(--juba-learning-green-dark, #46a302) !important;
          box-shadow: 3px 3px 0 var(--juba-learning-green-dark, #46a302) !important;
        }
        .juba-jl-ai-showcase .juba-ai-live-pill {
          color: var(--juba-learning-green-dark, #46a302) !important;
        }
      `}</style>
      <div dir={dir} className="juba-ai-showcase juba-jl-ai-showcase">
        <div className="juba-ai-showcase-art">
          <Image
            src="/landing/juba-ai-tutor.svg"
            alt={imageAlt}
            width={760}
            height={560}
            className="juba-ai-showcase-image"
          />
          <div className="juba-ai-chat-bubble juba-ai-chat-user">{userMessage}</div>
          <div className="juba-ai-chat-bubble juba-ai-chat-tutor">{aiMessage}</div>
          <div className="juba-ai-wave" aria-label={playing ? speakingLabel : activeLabel}>
            {Array.from({ length: 11 }).map((_, index) => (
              <i key={index} className={playing ? 'is-playing' : ''} style={{ '--wave-delay': `${index * 70}ms` } as CSSProperties} />
            ))}
          </div>
          <button
            type="button"
            className="juba-ai-play"
            onClick={() => setPlaying((value) => !value)}
            aria-pressed={playing}
            aria-label={playing ? speakingLabel : activeLabel}
          >
            {playing ? <Pause aria-hidden="true" /> : <Play aria-hidden="true" />}
          </button>
          <span className="juba-ai-live-pill"><Volume2 aria-hidden="true" /> {playing ? speakingLabel : activeLabel}</span>
        </div>
        <div className="juba-ai-showcase-copy">
          <span className="juba-ref-kicker"><Sparkles className="h-4 w-4" /> AI</span>
          <h2>{imageAlt}</h2>
          <p>{aiMessage}</p>
          <a href={href} className="juba-ref-button">
            <Mic className="h-4 w-4" /> {openLabel}
          </a>
        </div>
      </div>
    </>
  )
}
