'use client'

import { useEffect, useState } from 'react'

import { type Health, theaApi } from '@/lib/api-client'

type Status = { kind: 'loading' } | { kind: 'up'; health: Health } | { kind: 'down' }

export default function HealthPage() {
  const [status, setStatus] = useState<Status>({ kind: 'loading' })

  useEffect(() => {
    theaApi
      .health()
      .then((health) => setStatus({ kind: 'up', health }))
      .catch(() => setStatus({ kind: 'down' }))
  }, [])

  return (
    <section className="flex flex-col gap-6 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">Health</h1>
      <div className="flex items-center gap-4 rounded-[var(--radius-card)] border border-line bg-panel p-6">
        <span
          aria-hidden
          className={`size-3 rounded-full ${
            status.kind === 'up' ? 'bg-tide' : status.kind === 'down' ? 'bg-alert' : 'animate-pulse bg-muted'
          }`}
        />
        <div>
          <p className="font-semibold">Agent</p>
          <p className="text-sm text-muted">
            {status.kind === 'loading' && 'Checking…'}
            {status.kind === 'up' && `Online · v${status.health.version}`}
            {status.kind === 'down' && 'Unreachable. Is the agent running on port 8000?'}
          </p>
        </div>
      </div>
      <p className="text-sm text-muted">Per-integration status (thea.integrations) appears here once the agent serves it.</p>
    </section>
  )
}
