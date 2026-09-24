'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  Check,
  Clipboard,
  ExternalLink,
  FilterX,
  LinkIcon,
  Loader2,
  Plus,
  Search,
  ShieldAlert,
  X,
  UserPlus,
} from 'lucide-react'
import { AdminNav } from '@/components/admin/AdminNav'
import { AdminPageHeader } from '@/components/admin/AdminShell'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import { apiFetch } from '@/lib/api'
import {
  DEFAULT_TARGET_LANGUAGE,
  TARGET_LANGUAGE_CATALOG,
  SUPPORTED_TARGET_LANGUAGES,
} from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

interface AdminUserItem {
  id: number
  username: string
  email: string | null
  display_name: string
  role: string
  native_language: string
  is_active: boolean
  subscription_status: string
}

const LANGUAGES = [
  'en',
  'es',
  'fr',
  'pt',
  'de',
  'it',
  'pl',
  'nl',
  'ro',
  'ru',
] as const

const PAGE_SIZE = 10

function statusBadgeClass(status: string) {
  switch (status) {
    case 'active':
      return 'border-green-500/40 text-green-400'
    case 'trialing':
      return 'border-blue-500/40 text-blue-400'
    case 'past_due':
    case 'unpaid':
    case 'paused':
      return 'border-yellow-500/40 text-yellow-400'
    case 'incomplete':
    case 'incomplete_expired':
      return 'border-orange-500/40 text-orange-400'
    case 'canceled':
      return 'border-[var(--juba-border)] text-[var(--juba-muted)]'
    default:
      return 'border-[var(--juba-border)] text-[var(--juba-muted)]'
  }
}

export default function AdminUsersPage() {
  const t = useTranslations('admin')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const tLang = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const searchParams = useSearchParams()
  const [users, setUsers] = useState<AdminUserItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [searchInput, setSearchInput] = useState(
    () => searchParams.get('q') ?? ''
  )
  const [searchTerm, setSearchTerm] = useState(
    () => searchParams.get('q') ?? ''
  )
  const [subscriptionFilter, setSubscriptionFilter] = useState(() => {
    const subscription = searchParams.get('subscription')
    return subscription &&
      [
        'none',
        'trialing',
        'active',
        'past_due',
        'canceled',
        'incomplete',
        'incomplete_expired',
        'unpaid',
        'paused',
      ].includes(subscription)
      ? subscription
      : ''
  })
  const [roleFilter, setRoleFilter] = useState(() => {
    const role = searchParams.get('role')
    return role === 'user' || role === 'admin' ? role : ''
  })
  const [activeFilter, setActiveFilter] = useState(() => {
    const active = searchParams.get('is_active')
    return active === 'true' || active === 'false' ? active : ''
  })
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [inviteUrl, setInviteUrl] = useState('')
  const [inviteCopied, setInviteCopied] = useState(false)
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    display_name: '',
    native_language: 'es',
    target_language: DEFAULT_TARGET_LANGUAGE,
    role: 'user',
  })
  const [error, setError] = useState('')
  const [createSaving, setCreateSaving] = useState(false)
  const [actionBusy, setActionBusy] = useState<string | null>(null)
  const [deletePending, setDeletePending] = useState<AdminUserItem | null>(null)
  const [activePending, setActivePending] = useState<AdminUserItem | null>(null)
  const currentUserId = useAuthStore((s) => s.user?.id)
  const availableLanguageCodes = useLanguageStore(
    (s) => s.availableLanguageCodes
  )

  useEffect(() => {
    if (window.location.search.includes('create=1')) {
      setShowCreate(true)
    }
  }, [])

  useEffect(() => {
    if (!showCreate) return
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') setShowCreate(false)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [showCreate])

  const visibleTargetLanguages = useMemo(() => {
    if (availableLanguageCodes.length === 0) return SUPPORTED_TARGET_LANGUAGES
    return TARGET_LANGUAGE_CATALOG.filter((l) =>
      availableLanguageCodes.includes(l.code)
    )
  }, [availableLanguageCodes])

  const targetLanguageOptions = useMemo(
    () =>
      [...visibleTargetLanguages].sort((a, b) =>
        tTarget(a.code).localeCompare(tTarget(b.code))
      ),
    [tTarget, visibleTargetLanguages]
  )

  const roleOptions = useMemo(
    () =>
      [
        { value: 'user', label: t('roleUser') },
        { value: 'admin', label: t('roleAdmin') },
      ].sort((a, b) => a.label.localeCompare(b.label)),
    [t]
  )

  const statusOptions = useMemo(
    () =>
      [
        { value: 'true', label: t('active') },
        { value: 'false', label: t('inactive') },
      ].sort((a, b) => a.label.localeCompare(b.label)),
    [t]
  )

  const subscriptionOptions = useMemo(
    () =>
      [
        { value: 'none', label: tBilling('statusNone') },
        { value: 'active', label: tBilling('statusActive') },
        { value: 'trialing', label: tBilling('statusTrialing') },
        { value: 'past_due', label: tBilling('statusPastDue') },
        { value: 'unpaid', label: tBilling('statusUnpaid') },
        { value: 'paused', label: tBilling('statusPaused') },
        { value: 'incomplete', label: tBilling('statusIncomplete') },
        {
          value: 'incomplete_expired',
          label: tBilling('statusIncompleteExpired'),
        },
        { value: 'canceled', label: tBilling('statusCanceled') },
      ].sort((a, b) => a.label.localeCompare(b.label)),
    [tBilling]
  )

  const loadUsers = useCallback(
    async (
      pageIndex: number,
      query: string,
      subscription: string,
      role: string,
      active: string
    ) => {
      setLoading(true)
      setError('')
      try {
        const params = new URLSearchParams({
          skip: String(pageIndex * PAGE_SIZE),
          limit: String(PAGE_SIZE),
        })
        if (query.trim()) params.set('q', query.trim())
        if (subscription) params.set('subscription', subscription)
        if (role) params.set('role', role)
        if (active) params.set('is_active', active)
        const res = await apiFetch(`/api/admin/users?${params.toString()}`)
        if (res.ok) {
          const data = await res.json()
          setUsers(data.items)
          setTotal(data.total)
        } else if (res.status === 403) {
          setError(t('adminRequired'))
        } else {
          setError(t('usersLoadError'))
        }
      } catch {
        setError(t('usersLoadError'))
      } finally {
        setLoading(false)
      }
    },
    [t]
  )

  useEffect(() => {
    loadUsers(page, searchTerm, subscriptionFilter, roleFilter, activeFilter)
  }, [loadUsers, page]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (page !== 0) {
      setPage(0)
    } else {
      loadUsers(0, searchTerm, subscriptionFilter, roleFilter, activeFilter)
    }
  }, [subscriptionFilter, roleFilter, activeFilter]) // eslint-disable-line react-hooks/exhaustive-deps

  function handleSearch() {
    const term = searchInput
    setSearchTerm(term)
    if (page !== 0) {
      setPage(0)
    } else {
      loadUsers(0, term, subscriptionFilter, roleFilter, activeFilter)
    }
  }

  function clearFilters() {
    setSearchInput('')
    setSearchTerm('')
    setSubscriptionFilter('')
    setRoleFilter('')
    setActiveFilter('')
    if (page !== 0) {
      setPage(0)
    } else {
      loadUsers(0, '', '', '', '')
    }
  }

  function openCreateUser() {
    setError('')
    setShowCreate(true)
  }

  async function createUser(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (!/^[a-zA-Z0-9._\s-]+$/.test(form.username)) {
      setError(t('invalidUsernameChars'))
      return
    }
    setCreateSaving(true)
    try {
      const sanitizedUsername = form.username.replace(/\s+/g, '_').toLowerCase()
      const res = await apiFetch('/api/admin/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, username: sanitizedUsername }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || t('createUserError'))
      }
      setShowCreate(false)
      setForm({
        username: '',
        email: '',
        password: '',
        display_name: '',
        native_language: 'es',
        target_language: DEFAULT_TARGET_LANGUAGE,
        role: 'user',
      })
      await loadUsers(
        page,
        searchTerm,
        subscriptionFilter,
        roleFilter,
        activeFilter
      )
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('createUserError'))
    } finally {
      setCreateSaving(false)
    }
  }

  async function toggleActive(user: AdminUserItem) {
    setActionBusy(`active-${user.id}`)
    const res = await apiFetch(`/api/admin/users/${user.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: !user.is_active }),
    })
    setActivePending(null)
    setActionBusy(null)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(data.detail || t('updateUserError'))
      return
    }
    await loadUsers(
      page,
      searchTerm,
      subscriptionFilter,
      roleFilter,
      activeFilter
    )
  }

  async function deleteUser(user: AdminUserItem) {
    setActionBusy(`delete-${user.id}`)
    const res = await apiFetch(`/api/admin/users/${user.id}`, {
      method: 'DELETE',
    })
    setDeletePending(null)
    setActionBusy(null)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(data.detail || t('deleteUserError'))
    } else {
      const newTotal = total - 1
      const maxPage = Math.max(0, Math.ceil(newTotal / PAGE_SIZE) - 1)
      const targetPage = Math.min(page, maxPage)
      if (targetPage !== page) {
        setPage(targetPage)
      } else {
        await loadUsers(
          targetPage,
          searchTerm,
          subscriptionFilter,
          roleFilter,
          activeFilter
        )
      }
    }
  }

  async function generateInvite() {
    setActionBusy('invite')
    setError('')
    setInviteCopied(false)
    try {
      const res = await apiFetch('/api/admin/invite', { method: 'POST' })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setInviteUrl(`${window.location.origin}${data.invite_url}`)
    } catch {
      setError(t('inviteError'))
    } finally {
      setActionBusy(null)
    }
  }

  async function copyInvite() {
    if (!inviteUrl) return
    try {
      await navigator.clipboard.writeText(inviteUrl)
      setInviteCopied(true)
      window.setTimeout(() => setInviteCopied(false), 2000)
    } catch {
      setError(t('copyInviteError'))
    }
  }

  const inputCls =
    'w-full bg-[var(--juba-bg)] border border-[var(--juba-border)] px-4 py-3 font-sans text-xs text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:outline-none focus:border-[var(--juba-violet)] transition-colors'

  const hasFilters =
    searchTerm ||
    subscriptionFilter ||
    roleFilter ||
    activeFilter ||
    searchInput

  if (loading && users.length === 0) {
    return <PageLoading label={t('loading')} />
  }

  return (
    <div className="juba-admin-users-shell mx-auto max-w-6xl space-y-4 p-6">
      <AdminPageHeader
        eyebrow={`${t('title')} / ${t('users')}`}
        title={t('users')}
        actions={
          <>
            <button
              onClick={generateInvite}
              disabled={actionBusy === 'invite'}
              className="border-[var(--juba-border)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] inline-flex items-center gap-2 border px-3 py-2 font-semibold tracking-wide transition-colors disabled:opacity-40"
            >
              {actionBusy === 'invite' ? (
                <Loader2 className="size-3.5 animate-spin" aria-hidden="true" />
              ) : (
                <LinkIcon className="size-3.5" aria-hidden="true" />
              )}
              {t('inviteBtn')}
            </button>
            <button
              onClick={openCreateUser}
              className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 inline-flex items-center gap-2 px-3 py-2 font-sans text-xs font-bold tracking-wide transition-colors"
            >
              <Plus className="size-3.5" aria-hidden="true" />
              {t('createUserBtn')}
            </button>
          </>
        }
      />

      <AdminNav />

      {inviteUrl && (
        <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] border px-5 py-4">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
            <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-semibold tracking-wide">
              {t('inviteLink')}
            </p>
            <button
              onClick={copyInvite}
              className="border-[var(--juba-border)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] inline-flex items-center gap-2 border px-3 py-1.5 font-semibold tracking-wide transition-colors"
            >
              {inviteCopied ? (
                <Check className="size-3.5" aria-hidden="true" />
              ) : (
                <Clipboard className="size-3.5" aria-hidden="true" />
              )}
              {inviteCopied ? t('inviteCopied') : t('copyLink')}
            </button>
          </div>
          <p className="text-[var(--juba-muted)] font-sans text-xs break-all">
            {inviteUrl}
          </p>
          <p className="text-[var(--juba-muted)] text-[var(--juba-muted)] mt-2 font-sans">
            {t('inviteExpiry')}
          </p>
        </div>
      )}

      {error && (
        <div className="border-red-200/40 text-red-600 border px-4 py-3 font-sans text-xs border-[var(--juba-border)]">
          {error}
        </div>
      )}

      <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] border">
        <div className="border-[var(--juba-border)] flex flex-wrap items-center gap-2 border-b px-5 py-4">
          <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
          <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-semibold tracking-wide">
            {t('users')}
          </span>
          {loading && (
            <Loader2
              className="text-[var(--juba-muted)] size-3.5 animate-spin"
              aria-hidden="true"
            />
          )}
          <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] ml-auto font-semibold tracking-wide">
            {total} {t('total')}
          </span>
        </div>

        <div className="border-[var(--juba-border)] grid gap-2 border-b px-5 py-3 lg:grid-cols-[minmax(14rem,1fr)_auto_auto_auto_auto]">
          <div className="flex min-w-0">
            <input
              type="search"
              placeholder={t('searchPlaceholder')}
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSearch()
              }}
              autoCorrect="off"
              autoCapitalize="none"
              spellCheck={false}
              className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:border-[var(--juba-violet)] min-w-0 flex-1 border px-4 py-2 font-sans text-xs transition-colors focus:outline-none"
            />
            <button
              type="button"
              onClick={handleSearch}
              className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] -ml-px inline-flex w-10 shrink-0 items-center justify-center border transition-colors"
              aria-label={t('searchAction')}
            >
              <Search className="size-3.5" aria-hidden="true" />
            </button>
          </div>
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] focus:border-[var(--juba-violet)] appearance-none border px-4 py-2 font-sans text-xs transition-colors focus:outline-none"
            aria-label={t('roleFilter')}
          >
            <option value="">{t('allRoles')}</option>
            {roleOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <select
            value={activeFilter}
            onChange={(e) => setActiveFilter(e.target.value)}
            className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] focus:border-[var(--juba-violet)] appearance-none border px-4 py-2 font-sans text-xs transition-colors focus:outline-none"
            aria-label={t('statusFilter')}
          >
            <option value="">{t('allStatuses')}</option>
            {statusOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <select
            value={subscriptionFilter}
            onChange={(e) => setSubscriptionFilter(e.target.value)}
            className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] focus:border-[var(--juba-violet)] appearance-none border px-4 py-2 font-sans text-xs transition-colors focus:outline-none"
            aria-label={t('subscriptionFilter')}
          >
            <option value="">{t('allSubscriptions')}</option>
            {subscriptionOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button
            type="button"
            onClick={clearFilters}
            disabled={!hasFilters}
            className="border-[var(--juba-border)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] inline-flex items-center justify-center gap-2 border px-3 py-2 font-semibold tracking-wide transition-colors disabled:cursor-not-allowed disabled:opacity-30"
          >
            <FilterX className="size-3.5" aria-hidden="true" />
            {t('clearFilters')}
          </button>
        </div>

        {users.length === 0 ? (
          <p className="text-[var(--juba-muted)] px-6 py-10 text-center font-sans text-xs">
            {t('noUsers')}
          </p>
        ) : (
          <>
            <div className="hidden lg:block">
              <table className="w-full table-fixed border-collapse border-[var(--juba-border)]">
                <thead>
                  <tr className="border-[var(--juba-border)] border-b">
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[25%] px-5 py-3 text-left font-semibold tracking-wide">
                      {t('userColumn')}
                    </th>
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[25%] px-5 py-3 text-left font-semibold tracking-wide">
                      {t('fieldEmail')}
                    </th>
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[12.5%] px-5 py-3 text-left font-semibold tracking-wide">
                      {t('role')}
                    </th>
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[12.5%] px-5 py-3 text-left font-semibold tracking-wide">
                      {t('status')}
                    </th>
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[15%] px-5 py-3 text-left font-semibold tracking-wide">
                      {t('fieldSubscription')}
                    </th>
                    <th className="text-[var(--juba-text)] text-[var(--juba-muted)] w-[10%] px-5 py-3 text-right font-semibold tracking-wide">
                      {t('actions')}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr
                      key={u.id}
                      className="border-[var(--juba-border)] hover:bg-[var(--juba-bg)]/60 border-b last:border-0"
                    >
                      <td className="px-5 py-4 align-middle">
                        <p className="text-[var(--juba-text)] truncate font-sans text-sm">
                          {u.display_name}
                        </p>
                        <p className="text-[var(--juba-text)] text-[var(--juba-muted)] truncate font-sans">
                          #{u.id} / @{u.username.toLowerCase()} /{' '}
                          {u.native_language}
                        </p>
                      </td>
                      <td className="text-[var(--juba-muted)] truncate px-5 py-4 align-middle font-sans text-xs">
                        {u.email || '—'}
                      </td>
                      <td className="px-5 py-4 align-middle">
                        <span
                          className={`text-[var(--juba-muted)] border px-2 py-0.5 font-semibold tracking-wide ${
                            u.role === 'admin'
                              ? 'border-fl-fg/40 text-[var(--juba-text)]'
                              : 'border-[var(--juba-border)] text-[var(--juba-muted)]'
                          }`}
                        >
                          {u.role === 'admin' ? t('roleAdmin') : t('roleUser')}
                        </span>
                      </td>
                      <td className="px-5 py-4 align-middle">
                        <span
                          className={`text-[var(--juba-muted)] border px-2 py-0.5 font-semibold tracking-wide ${
                            u.is_active
                              ? 'border-green-500/40 text-green-400'
                              : 'border-red-200/30 text-red-600-fg'
                          }`}
                        >
                          {u.is_active ? t('active') : t('inactive')}
                        </span>
                      </td>
                      <td className="px-5 py-4 align-middle">
                        <span
                          className={`text-[var(--juba-muted)] border px-2 py-0.5 font-semibold tracking-wide ${statusBadgeClass(u.subscription_status)}`}
                        >
                          {subscriptionLabel(u.subscription_status, tBilling)}
                        </span>
                      </td>
                      <td className="px-5 py-4 align-middle">
                        <div className="flex justify-end gap-1">
                          <Link
                            href={`/admin/users/${u.id}`}
                            className="border-[var(--juba-border)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] inline-flex size-8 items-center justify-center border transition-colors"
                            aria-label={t('viewStats')}
                          >
                            <ExternalLink
                              className="size-3.5"
                              aria-hidden="true"
                            />
                          </Link>
                          <button
                            onClick={() => setActivePending(u)}
                            disabled={u.id === currentUserId}
                            className={`inline-flex size-8 items-center justify-center border transition-colors ${
                              u.id === currentUserId
                                ? 'cursor-not-allowed opacity-20'
                                : u.is_active
                                  ? 'border-red-200/30 text-red-600-fg hover:border-red-200'
                                  : 'border-[var(--juba-border)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)]'
                            }`}
                            aria-label={
                              u.is_active ? t('deactivate') : t('activate')
                            }
                            title={
                              u.id === currentUserId
                                ? t('cannotDeactivateSelf')
                                : u.is_active
                                  ? t('deactivate')
                                  : t('activate')
                            }
                          >
                            {actionBusy === `active-${u.id}` ? (
                              <Loader2
                                className="size-3.5 animate-spin"
                                aria-hidden="true"
                              />
                            ) : (
                              <ShieldAlert
                                className="size-3.5"
                                aria-hidden="true"
                              />
                            )}
                          </button>
                          <button
                            onClick={() => setDeletePending(u)}
                            disabled={u.id === currentUserId}
                            className="border-red-200/30 text-red-600-fg hover:border-red-200 hover:text-red-600 inline-flex size-8 items-center justify-center border transition-colors disabled:cursor-not-allowed disabled:opacity-20 border-[var(--juba-border)]"
                            aria-label={t('delete')}
                            title={
                              u.id === currentUserId
                                ? t('cannotDeleteSelf')
                                : t('delete')
                            }
                          >
                            {actionBusy === `delete-${u.id}` ? (
                              <Loader2
                                className="size-3.5 animate-spin"
                                aria-hidden="true"
                              />
                            ) : (
                              <span className="text-xs leading-none">X</span>
                            )}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="lg:hidden">
              {users.map((u, i) => (
                <div
                  key={u.id}
                  className={`space-y-3 px-4 py-4 ${i < users.length - 1 ? 'border-[var(--juba-border)] border-b' : ''}`}
                >
                  <div className="min-w-0 space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[var(--juba-text)] font-sans text-sm">
                        {u.display_name}
                      </span>
                      <span
                        className={`text-[var(--juba-muted)] border px-2 py-0.5 font-semibold tracking-wide ${
                          u.role === 'admin'
                            ? 'border-fl-fg/40 text-[var(--juba-text)]'
                            : 'border-[var(--juba-border)] text-[var(--juba-muted)]'
                        }`}
                      >
                        {u.role === 'admin' ? t('roleAdmin') : t('roleUser')}
                      </span>
                      <span
                        className={`text-[var(--juba-muted)] border px-2 py-0.5 font-semibold tracking-wide ${
                          u.is_active
                            ? 'border-green-500/40 text-green-400'
                            : 'border-red-200/30 text-red-600-fg'
                        }`}
                      >
                        {u.is_active ? t('active') : t('inactive')}
                      </span>
                    </div>
                    <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-sans break-all">
                      <span className="text-[var(--juba-muted)]">#{u.id}</span> /{' '}
                      {u.username.toLowerCase()} {u.email ? `/ ${u.email}` : ''}{' '}
                      / {u.native_language}
                    </p>
                    <span
                      className={`text-[var(--juba-muted)] inline-flex border px-2 py-0.5 font-semibold tracking-wide ${statusBadgeClass(u.subscription_status)}`}
                    >
                      {subscriptionLabel(u.subscription_status, tBilling)}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Link
                      href={`/admin/users/${u.id}`}
                      className="border-[var(--juba-border)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] inline-flex items-center gap-2 border px-3 py-2 font-semibold tracking-wide transition-colors"
                    >
                      <ExternalLink className="size-3.5" aria-hidden="true" />
                      {t('viewStats')}
                    </Link>
                    <button
                      onClick={() => setActivePending(u)}
                      disabled={u.id === currentUserId}
                      className={`text-[var(--juba-text)] inline-flex items-center gap-2 border px-3 py-2 font-semibold tracking-wide transition-colors ${
                        u.id === currentUserId
                          ? 'cursor-not-allowed opacity-20'
                          : u.is_active
                            ? 'border-red-200/30 text-red-600-fg hover:border-red-200'
                            : 'border-[var(--juba-border)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)]'
                      }`}
                    >
                      {actionBusy === `active-${u.id}` && (
                        <Loader2
                          className="size-3.5 animate-spin"
                          aria-hidden="true"
                        />
                      )}
                      {u.is_active ? t('deactivate') : t('activate')}
                    </button>
                    <button
                      onClick={() => setDeletePending(u)}
                      disabled={u.id === currentUserId}
                      className="border-red-200/30 text-[var(--juba-text)] text-red-600-fg hover:border-red-200 hover:text-red-600 inline-flex items-center gap-2 border px-3 py-2 font-semibold tracking-wide transition-colors disabled:cursor-not-allowed disabled:opacity-20 border-[var(--juba-border)]"
                    >
                      {actionBusy === `delete-${u.id}` && (
                        <Loader2
                          className="size-3.5 animate-spin"
                          aria-hidden="true"
                        />
                      )}
                      {t('delete')}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      <Pagination
        page={page}
        totalPages={Math.ceil(total / PAGE_SIZE)}
        loading={loading}
        onPageChange={setPage}
        prevLabel={t('prevPage')}
        nextLabel={t('nextPage')}
      />

      {showCreate && (
        <div
          className="fixed inset-0 z-[200] flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
          onClick={() => setShowCreate(false)}
        >
          <div
            className="border-[var(--juba-border)] bg-[var(--juba-surface)] max-h-[calc(100vh-2rem)] w-full max-w-md overflow-y-auto border shadow-2xl"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-labelledby="admin-create-user-title"
            aria-describedby="admin-create-user-description"
          >
            <div className="border-[var(--juba-border)] flex items-start justify-between gap-4 border-b px-6 py-5">
              <div>
                <div className="flex items-center gap-2">
                  <UserPlus
                    className="text-[var(--juba-muted)] size-4"
                    aria-hidden="true"
                  />
                  <h2
                    id="admin-create-user-title"
                    className="text-[var(--juba-text)] font-sans text-sm tracking-wide"
                  >
                    {t('createUser')}
                  </h2>
                </div>
                <p
                  id="admin-create-user-description"
                  className="text-[var(--juba-muted)] mt-2 font-sans text-xs"
                >
                  {t('createUserSheetDesc')}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowCreate(false)}
                className="text-[var(--juba-muted)] hover:text-[var(--juba-text)] p-1 transition-colors"
                aria-label={tCommon('cancel')}
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>

            <form
              id="admin-create-user-form"
              onSubmit={createUser}
              className="space-y-4 px-6 py-5"
            >
              {error && (
                <div className="border-red-200/40 text-red-600 border px-4 py-3 font-sans text-xs border-[var(--juba-border)]">
                  {error}
                </div>
              )}
              {[
                {
                  key: 'username',
                  label: t('fieldUsername'),
                  required: true,
                  type: 'text',
                },
                {
                  key: 'email',
                  label: t('fieldEmail'),
                  required: true,
                  type: 'email',
                },
                {
                  key: 'password',
                  label: t('fieldPassword'),
                  required: true,
                  type: 'password',
                },
                {
                  key: 'display_name',
                  label: t('fieldDisplayName'),
                  required: true,
                  type: 'text',
                },
              ].map(({ key, label, required, type }) => (
                <label key={key} className="block">
                  <span className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 block font-sans text-xs tracking-wide">
                    {label}
                  </span>
                  <input
                    type={type}
                    required={required}
                    value={form[key as keyof typeof form]}
                    onChange={(e) =>
                      setForm({ ...form, [key]: e.target.value })
                    }
                    autoCorrect={
                      type === 'email' || type === 'password'
                        ? 'off'
                        : undefined
                    }
                    autoCapitalize={
                      type === 'email' || type === 'password'
                        ? 'none'
                        : undefined
                    }
                    spellCheck={
                      type === 'email' || type === 'password'
                        ? false
                        : undefined
                    }
                    className={inputCls}
                  />
                </label>
              ))}
              <label className="block">
                <span className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 block font-sans text-xs tracking-wide">
                  {t('fieldNativeLanguage')}
                </span>
                <select
                  value={form.native_language}
                  onChange={(e) =>
                    setForm({ ...form, native_language: e.target.value })
                  }
                  className={inputCls + ' appearance-none'}
                >
                  {[...LANGUAGES]
                    .sort((a, b) => tLang(a).localeCompare(tLang(b)))
                    .map((code) => (
                      <option key={code} value={code}>
                        {tLang(code)}
                      </option>
                    ))}
                </select>
              </label>
              <label className="block">
                <span className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 block font-sans text-xs tracking-wide">
                  {t('fieldTargetLanguage')}
                </span>
                <select
                  value={form.target_language}
                  onChange={(e) =>
                    setForm({ ...form, target_language: e.target.value })
                  }
                  className={inputCls + ' appearance-none'}
                >
                  {targetLanguageOptions.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {tTarget(lang.code)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 block font-sans text-xs tracking-wide">
                  {t('fieldRole')}
                </span>
                <select
                  value={form.role}
                  onChange={(e) => setForm({ ...form, role: e.target.value })}
                  className={inputCls + ' appearance-none'}
                >
                  {roleOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
            </form>

            <div className="border-[var(--juba-border)] grid grid-cols-2 gap-2 border-t px-6 py-5">
              <button
                type="button"
                onClick={() => setShowCreate(false)}
                className="border-[var(--juba-border)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:border-[var(--juba-violet)] hover:text-[var(--juba-text)] border py-3 font-sans font-bold tracking-wide transition-colors"
              >
                {tCommon('cancel')}
              </button>
              <button
                type="submit"
                form="admin-create-user-form"
                disabled={createSaving}
                className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 inline-flex items-center justify-center gap-2 py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-50"
              >
                {createSaving && (
                  <Loader2
                    className="size-3.5 animate-spin"
                    aria-hidden="true"
                  />
                )}
                {t('submitCreate')}
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmDialog
        open={activePending !== null}
        title={
          activePending?.is_active ? t('deactivateUser') : t('activateUser')
        }
        message={
          activePending?.is_active
            ? t('deactivateUserMessage')
            : t('activateUserMessage')
        }
        confirmLabel={
          activePending?.is_active ? t('deactivate') : t('activate')
        }
        danger={activePending?.is_active}
        onConfirm={() => activePending && toggleActive(activePending)}
        onCancel={() => setActivePending(null)}
      />

      <ConfirmDialog
        open={deletePending !== null}
        title={t('deleteUser')}
        message={t('deleteUserMessage')}
        confirmLabel={t('deleteConfirm')}
        danger
        onConfirm={() => deletePending && deleteUser(deletePending)}
        onCancel={() => setDeletePending(null)}
      />
    </div>
  )
}

function subscriptionLabel(
  status: string,
  tBilling: (
    key:
      | 'statusActive'
      | 'statusTrialing'
      | 'statusPastDue'
      | 'statusUnpaid'
      | 'statusPaused'
      | 'statusIncomplete'
      | 'statusIncompleteExpired'
      | 'statusCanceled'
      | 'statusNone'
  ) => string
) {
  switch (status) {
    case 'active':
      return tBilling('statusActive')
    case 'trialing':
      return tBilling('statusTrialing')
    case 'past_due':
      return tBilling('statusPastDue')
    case 'unpaid':
      return tBilling('statusUnpaid')
    case 'paused':
      return tBilling('statusPaused')
    case 'incomplete':
      return tBilling('statusIncomplete')
    case 'incomplete_expired':
      return tBilling('statusIncompleteExpired')
    case 'canceled':
      return tBilling('statusCanceled')
    default:
      return tBilling('statusNone')
  }
}
