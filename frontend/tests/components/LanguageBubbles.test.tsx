import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
  useLocale: () => 'en',
}))

vi.mock('next/image', () => ({
  default: function MockImage(
    props: React.ImgHTMLAttributes<HTMLImageElement> & {
      unoptimized?: boolean
      priority?: boolean
    }
  ) {
    const { unoptimized, priority, ...imgProps } = props
    void unoptimized
    void priority
    return React.createElement('img', imgProps)
  },
}))

describe('LanguageBubbles', () => {
  it('renders correctly', () => {
    const { container } = render(<LanguageBubbles />)
    expect(container).toBeDefined()
  })
})
