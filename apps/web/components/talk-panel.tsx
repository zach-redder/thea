'use client'

import { useState } from 'react'

import { Orb, type OrbState } from '@/components/orb'
import { ApiError, theaApi } from '@/lib/api-client'

type Line = { from: 'you' | 'thea'; text: string }

/**
 * Talk screen: push-to-talk + typed chat. Hold-to-talk only drives the orb for
 * now; streaming mic audio over the agent's WebSocket comes with the voice
 * pipeline (docs/voice-pipeline.md).
 */
export function TalkPanel() {
  const [orb, setOrb] = useState<OrbState>('idle')
  const [draft, setDraft] = useState('')
  const [lines, setLines] = useState<Line[]>([])
  const [sessionId, setSessionId] = useState<string | undefined>()

  async function send(event: React.FormEvent) {
    event.preventDefault()
    const message = draft.trim()
    if (!message) return

    setDraft('')
    setLines((prev) => [...prev, { from: 'you', text: message }])
    setOrb('thinking')
    try {
      const response = await theaApi.chat({ message, sessionId })
      setSessionId(response.sessionId)
      setLines((prev) => [...prev, { from: 'thea', text: response.reply }])
      setOrb('speaking')
      setTimeout(() => setOrb('idle'), 1500)
    } catch (err) {
      const text = err instanceof ApiError ? err.message : "I can't reach my agent right now."
      setLines((prev) => [...prev, { from: 'thea', text }])
      setOrb('idle')
    }
  }

  return (
    <section className="flex flex-1 flex-col items-center gap-8 pt-4 sm:pt-10">
      <Orb state={orb} />

      <button
        type="button"
        onPointerDown={() => setOrb('listening')}
        onPointerUp={() => setOrb('idle')}
        onPointerLeave={() => orb === 'listening' && setOrb('idle')}
        className="min-h-14 rounded-full border border-line bg-panel px-8 text-sm font-semibold text-text transition-colors hover:border-tide focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-tide active:bg-tide/15"
      >
        Hold to talk
      </button>

      <ol className="flex w-full max-w-xl flex-col gap-3" aria-label="Conversation">
        {lines.length === 0 && (
          <li className="text-center text-sm text-muted">Say &ldquo;Hey THEA&rdquo;, hold the button, or type below.</li>
        )}
        {lines.map((line, i) => (
          <li
            key={i}
            className={`max-w-[85%] rounded-[var(--radius-card)] px-4 py-3 text-[15px] leading-relaxed ${
              line.from === 'you' ? 'self-end bg-ember/15' : 'self-start border border-line bg-panel'
            }`}
          >
            {line.text}
          </li>
        ))}
      </ol>

      <form onSubmit={send} className="sticky bottom-24 mt-auto flex w-full max-w-xl gap-2 sm:bottom-6">
        <label htmlFor="message" className="sr-only">
          Message THEA
        </label>
        <input
          id="message"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Ask THEA anything"
          autoComplete="off"
          className="min-h-12 flex-1 rounded-full border border-line bg-panel px-5 text-text placeholder:text-muted focus-visible:border-ember focus-visible:outline-none"
        />
        <button
          type="submit"
          disabled={orb === 'thinking'}
          className="min-h-12 rounded-full bg-ember px-6 font-semibold text-ink transition-opacity hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ember disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </section>
  )
}
