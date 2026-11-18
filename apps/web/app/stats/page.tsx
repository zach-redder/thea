import { PlaceholderPage } from '@/components/placeholder-page'

export default function StatsPage() {
  return (
    <PlaceholderPage
      title="Stats"
      description="Your numbers across sleep, focus, creator work, money and home, over any range."
      source="GET /api/v1/stats/summary"
    />
  )
}
