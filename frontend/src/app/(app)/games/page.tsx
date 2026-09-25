'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

import { apiFetch } from '@/lib/api'
import type { GameId } from '@/lib/games/persist'

// FIX: the previous commit accidentally stored the two-line separator as the
// literal characters "\\n", which made the TSX parser report "Expected unicode escape".
// The file is intentionally repaired by replacing that literal escape with a real newline.

