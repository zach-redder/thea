import { PlaceholderPage } from '@/components/placeholder-page'

export default function TodayPage() {
  return (
    <PlaceholderPage
      title="Today"
      description="The daily glance: your agenda, habits due, what changed overnight, and THEA's one-line read."
      source="GET /api/v1/today"
    />
  )
}
