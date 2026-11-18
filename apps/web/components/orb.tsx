export type OrbState = 'idle' | 'listening' | 'thinking' | 'speaking'

const STATE_STYLES: Record<OrbState, { core: string; label: string }> = {
  idle: { core: 'from-ember/80 to-ember/20 animate-[breathe_5s_ease-in-out_infinite]', label: 'Here' },
  listening: { core: 'from-tide to-tide/20 scale-110', label: 'Listening' },
  thinking: { core: 'from-ember to-tide/40 animate-spin [animation-duration:3s]', label: 'Thinking' },
  speaking: { core: 'from-ember to-ember/30 animate-[breathe_0.8s_ease-in-out_infinite]', label: 'Speaking' },
}

/** THEA's face: one glowing presence that changes with what she's doing. */
export function Orb({ state }: { state: OrbState }) {
  const { core, label } = STATE_STYLES[state]

  return (
    <div className="flex flex-col items-center gap-4" role="status" aria-live="polite">
      <div className="relative size-48 sm:size-60">
        <span className="absolute inset-0 rounded-full bg-ember/10 blur-3xl" />
        {state === 'listening' && (
          <span className="absolute inset-6 rounded-full border border-tide/60 animate-[ripple_1.6s_ease-out_infinite]" />
        )}
        <span
          className={`absolute inset-6 rounded-full bg-radial-[at_35%_30%] transition-all duration-500 ${core}`}
        />
      </div>
      <span className="text-xs font-medium uppercase tracking-[0.25em] text-muted">
        <span className="sr-only">THEA is </span>
        {label}
      </span>
    </div>
  )
}
