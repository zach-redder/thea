import Link from 'next/link'

const ITEMS = [
  { href: '/stats', title: 'Stats', blurb: 'Your numbers: sleep, focus, creator, money, home.' },
  { href: '/life', title: 'Life log', blurb: 'A timeline of what happened, and what she remembers.' },
  { href: '/memory', title: 'Memory', blurb: 'Browse, search and delete what THEA remembers.' },
  { href: '/logs', title: 'Logs', blurb: 'Conversations, tool calls and approvals.' },
  { href: '/health', title: 'Health', blurb: 'Is everything connected and running?' },
  { href: '/settings', title: 'Settings', blurb: 'Integrations, autonomy, privacy and pairing.' },
] as const

export default function MorePage() {
  return (
    <section className="flex flex-col gap-6 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">More</h1>
      <ul className="grid gap-3 sm:grid-cols-2">
        {ITEMS.map(({ href, title, blurb }) => (
          <li key={href}>
            <Link
              href={href}
              className="flex h-full flex-col gap-1 rounded-[var(--radius-card)] border border-line bg-panel p-5 transition-colors hover:border-ember focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ember"
            >
              <span className="font-semibold">{title}</span>
              <span className="text-sm text-muted">{blurb}</span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
