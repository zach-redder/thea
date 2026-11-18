import { PlaceholderPage } from '@/components/placeholder-page'

export default function LogsPage() {
  return (
    <PlaceholderPage
      title="Logs"
      description="Recent conversations, tool calls and proactive actions, newest first."
      source="POST /api/v1/sessions/list"
    />
  )
}
