import type { User } from '@/store/auth'
import type { UserLanguageInfo } from '@/store/language'

function stringOrFallback(value: unknown, fallback = ''): string {
  return typeof value === 'string' ? value : fallback
}

function nullableString(
  value: unknown,
  fallback: string | null | undefined = null
): string | null | undefined {
  if (value === null) return null
  return typeof value === 'string' ? value : fallback
}

function finiteNumber(value: unknown, fallback = 0): number {
  return typeof value === 'number' && Number.isFinite(value) ? value : fallback
}

function booleanOrFallback(value: unknown, fallback = false): boolean {
  return typeof value === 'boolean' ? value : fallback
}

function subscriptionStatus(
  value: unknown,
  fallback: User['subscription_status'] = 'none'
): User['subscription_status'] {
  const supported: User['subscription_status'][] = [
    'none',
    'incomplete',
    'incomplete_expired',
    'trialing',
    'active',
    'past_due',
    'canceled',
    'unpaid',
    'paused',
  ]
  return typeof value === 'string' && supported.includes(value as User['subscription_status'])
    ? (value as User['subscription_status'])
    : fallback
}

/**
 * Map a raw API response (snake_case) to the front-end User shape.
 * Runtime validation is intentionally conservative: malformed optional fields
 * are replaced with safe defaults instead of reaching React/Zustand consumers.
 */
export function mapUser(
  data: Record<string, any>,
  current?: User | null
): User {
  const currentUser = current ?? null
  const currentRole = currentUser?.role ?? 'user'
  const role = data.role === 'admin' || data.role === 'user' ? data.role : currentRole

  return {
    id: finiteNumber(data.id, currentUser?.id ?? 0),
    username: stringOrFallback(data.username, currentUser?.username ?? ''),
    displayName: stringOrFallback(data.display_name, currentUser?.displayName ?? ''),
    email: nullableString(data.email, currentUser?.email),
    native_language: nullableString(data.native_language, currentUser?.native_language),
    target_language: nullableString(data.target_language, currentUser?.target_language),
    ui_locale: nullableString(data.ui_locale, currentUser?.ui_locale ?? null) ?? null,
    role,
    conversation_max_duration: finiteNumber(
      data.conversation_max_duration,
      currentUser?.conversation_max_duration ?? 0
    ),
    conversation_inactivity_timeout: finiteNumber(
      data.conversation_inactivity_timeout,
      currentUser?.conversation_inactivity_timeout ?? 0
    ),
    avatar:
      'avatar' in data
        ? nullableString(data.avatar) ?? null
        : (currentUser?.avatar ?? null),
    is_verified: booleanOrFallback(
      data.is_verified,
      currentUser?.is_verified ?? true
    ),
    bio: nullableString(data.bio, currentUser?.bio ?? null) ?? null,
    learning_goals: Array.isArray(data.learning_goals)
      ? data.learning_goals.filter((goal: unknown): goal is string => typeof goal === 'string')
      : (currentUser?.learning_goals ?? null),
    subscription_status: subscriptionStatus(
      data.subscription_status,
      currentUser?.subscription_status ?? 'none'
    ),
    subscription_ends_at:
      nullableString(data.subscription_ends_at, currentUser?.subscription_ends_at ?? null) ?? null,
    cancel_at_period_end: booleanOrFallback(
      data.cancel_at_period_end,
      currentUser?.cancel_at_period_end ?? false
    ),
    trial_used: booleanOrFallback(data.trial_used, currentUser?.trial_used ?? false),
    assessment_voice_trial_used: booleanOrFallback(
      data.assessment_voice_trial_used,
      currentUser?.assessment_voice_trial_used ?? false
    ),
    freemium_trial_ends_at:
      nullableString(data.freemium_trial_ends_at, currentUser?.freemium_trial_ends_at ?? null) ?? null,
    freemium_trial_used: booleanOrFallback(
      data.freemium_trial_used,
      currentUser?.freemium_trial_used ?? false
    ),
    dismissed_dashboard_banner_revision:
      typeof data.dismissed_dashboard_banner_revision === 'number' &&
      Number.isFinite(data.dismissed_dashboard_banner_revision)
        ? data.dismissed_dashboard_banner_revision
        : (currentUser?.dismissed_dashboard_banner_revision ?? null),
  }
}

export function mapUserLanguageInfo(
  data: Record<string, any>
): UserLanguageInfo {
  const plan = data.plan && typeof data.plan === 'object' && !Array.isArray(data.plan)
    ? data.plan
    : null
  const progress =
    data.progress && typeof data.progress === 'object' && !Array.isArray(data.progress)
      ? data.progress
      : null

  return {
    target_language: stringOrFallback(data.target_language),
    is_active: booleanOrFallback(data.is_active),
    plan: plan
      ? {
          id: finiteNumber(plan.id),
          cefr_level: nullableString(plan.cefr_level) ?? null,
          progress_day: finiteNumber(plan.progress_day),
          total_days: finiteNumber(plan.total_days),
          completion_pct: finiteNumber(plan.completion_pct),
        }
      : null,
    progress: progress
      ? {
          total_xp: finiteNumber(progress.total_xp),
          current_streak: finiteNumber(progress.current_streak),
          lessons_completed: finiteNumber(progress.lessons_completed),
        }
      : null,
  }
}
