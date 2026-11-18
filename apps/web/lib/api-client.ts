import { keysToCamel, keysToSnake } from '@/lib/case-convert'

// Contract: services/agent/src/thea_agent/api/v1/schemas.py (docs/api.md).

export type Health = { status: 'ok'; service: string; version: string }

export type ChatRequest = {
  message: string
  sessionId?: string
  channel?: 'web' | 'phone' | 'desktop'
  speak?: boolean
}

export type ChatResponse = { sessionId: string; reply: string; createdAt: string }

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message)
  }
}

const BASE_URL = process.env.NEXT_PUBLIC_THEA_API_URL ?? 'http://localhost:8000'
const TOKEN_KEY = 'thea.api_token'

/** The personal API token is pasted once per device (pairing) and kept locally, never baked into the bundle. */
export const apiToken = {
  get: () => (typeof window === 'undefined' ? null : window.localStorage.getItem(TOKEN_KEY)),
  set: (token: string) => window.localStorage.setItem(TOKEN_KEY, token),
}

async function request<T>(method: 'GET' | 'POST', path: string, body?: unknown): Promise<T> {
  const token = apiToken.get()
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(keysToSnake(body)),
  })

  const data: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    // FastAPI errors look like {"detail": "..."}; show THEA's message, not "Request failed with 501".
    const detail = (data as { detail?: unknown } | null)?.detail
    throw new ApiError(typeof detail === 'string' ? detail : 'Something went wrong talking to THEA.', response.status)
  }
  return keysToCamel<T>(data)
}

export const theaApi = {
  health: () => request<Health>('GET', '/health'),
  chat: (body: ChatRequest) => request<ChatResponse>('POST', '/api/v1/chat', { channel: 'web', ...body }),
}
