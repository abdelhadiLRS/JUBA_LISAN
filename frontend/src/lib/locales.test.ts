import { describe, expect, it } from 'vitest'
import { normalizeLocale } from './locales'

describe('normalizeLocale', () => {
  it.each([
    ['en-GB', 'en'],
    ['en_US', 'en'],
    ['AR-dz', 'ar'],
    ['fr-CA', 'fr'],
    ['de-AT', 'de'],
    ['pt-BR', 'pt'],
    ['uk-UA', 'ru'],
    ['xx-ZZ', 'en'],
    ['', 'en'],
  ])('normalizes %s to %s', (input, expected) => {
    expect(normalizeLocale(input)).toBe(expected)
  })
})
