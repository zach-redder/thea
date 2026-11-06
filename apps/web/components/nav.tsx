'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const LINKS = [
  { href: '/', label: 'Talk' },
  { href: '/memory', label: 'Memory' },
  { href: '/logs', label: 'Logs' },
  { href: '/health', label: 'Health' },
] as const

/** Top bar on desktop, bottom tab bar on phones (thumb reach). */
export function Nav() {
  const pathname = usePathname()

  return (
    <nav
      aria-label="Primary"
      className="fixed inset-x-0 bottom-0 z-10 border-t border-line bg-ink/90 pb-[env(safe-area-inset-bottom)] backdrop-blur sm:static sm:border-0 sm:bg-transparent sm:py-6"
    >
      <div className="mx-auto flex max-w-5xl items-center justify-around sm:justify-between sm:px-0">
        <span className="hidden text-lg font-bold tracking-[0.3em] text-ember sm:block">THEA</span>
        <ul className="flex w-full justify-around sm:w-auto sm:gap-2">
          {LINKS.map(({ href, label }) => {
            const active = pathname === href
            return (
              <li key={href}>
                <Link
                  href={href}
                  aria-current={active ? 'page' : undefined}
                  className={`flex min-h-11 min-w-11 items-center justify-center rounded-full px-4 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ember ${
                    active ? 'bg-panel text-text' : 'text-muted hover:text-text'
                  }`}
                >
                  {label}
                </Link>
              </li>
            )
          })}
        </ul>
      </div>
    </nav>
  )
}
