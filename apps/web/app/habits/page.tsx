import { PlaceholderPage } from '@/components/placeholder-page'

export default function HabitsPage() {
  return (
    <PlaceholderPage
      title="Habits"
      description="Check things off with one tap. Streaks, history and the times you do best."
      source="POST /api/v1/habits/list"
    />
  )
}
