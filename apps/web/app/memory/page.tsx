import { PlaceholderPage } from '@/components/placeholder-page'

export default function MemoryPage() {
  return (
    <PlaceholderPage
      title="Memory"
      description="Everything THEA remembers: episodic memories, plus what she knows about your identity, wardrobe and home."
      source="POST /api/v1/memories/list"
    />
  )
}
