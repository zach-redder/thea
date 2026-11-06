// The agent speaks snake_case JSON; this app is camelCase. Convert at the API boundary only.

type Json = string | number | boolean | null | Json[] | { [key: string]: Json }

const toCamel = (key: string) => key.replace(/_([a-z0-9])/g, (_, c: string) => c.toUpperCase())
const toSnake = (key: string) => key.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`)

function convertKeys(value: unknown, convert: (key: string) => string): Json {
  if (Array.isArray(value)) return value.map((item) => convertKeys(item, convert))
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value)
        .filter(([, v]) => v !== undefined)
        .map(([k, v]) => [convert(k), convertKeys(v, convert)]),
    )
  }
  return value as Json
}

export const keysToCamel = <T>(value: unknown): T => convertKeys(value, toCamel) as T
export const keysToSnake = (value: unknown): Json => convertKeys(value, toSnake)
