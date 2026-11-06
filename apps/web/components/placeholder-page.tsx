/** Shared shell for dashboard pages that are designed but not built yet. */
export function PlaceholderPage({
  title,
  description,
  source,
}: {
  title: string
  description: string
  source: string
}) {
  return (
    <section className="flex flex-col gap-4 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
      <p className="max-w-prose text-muted">{description}</p>
      <div className="rounded-[var(--radius-card)] border border-dashed border-line bg-panel/50 p-8 text-sm text-muted">
        Coming once the agent API serves <code className="font-mono text-text">{source}</code>.
      </div>
    </section>
  )
}
