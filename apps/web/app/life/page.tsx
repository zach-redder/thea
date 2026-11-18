import { PlaceholderPage } from '@/components/placeholder-page'

export default function LifePage() {
  return (
    <PlaceholderPage
      title="Life log"
      description="A searchable timeline of events and memories: the documentation of your life."
      source="POST /api/v1/life/list"
    />
  )
}
