export function AdminAuthorBadge({ role }: { role: string }) {
  if (role !== 'admin') return null

  return (
    <span className="border-[var(--juba-app-green)]/40 text-[var(--juba-app-green-dark)] inline-flex border-2 rounded-full px-2 py-0.5 font-mono text-[9px] leading-none font-bold tracking-widest uppercase">
      ADMIN
    </span>
  )
}
