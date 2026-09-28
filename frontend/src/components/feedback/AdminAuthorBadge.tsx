export function AdminAuthorBadge({ role }: { role: string }) {
  if (role !== 'admin') return null

  return (
    <span className="border-[color-mix(in_srgb,var(--duo-green)_40%,transparent)] text-[var(--duo-green-dark)] inline-flex border-2 rounded-full px-2 py-0.5 font-mono text-[9px] leading-none font-bold tracking-widest uppercase">
      ADMIN
    </span>
  )
}
