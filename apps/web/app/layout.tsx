import type { Metadata, Viewport } from 'next'
import { JetBrains_Mono, Space_Grotesk } from 'next/font/google'

import { Nav } from '@/components/nav'

import './globals.css'

const grotesk = Space_Grotesk({ subsets: ['latin'], variable: '--font-grotesk' })
const jetbrains = JetBrains_Mono({ subsets: ['latin'], variable: '--font-jetbrains' })

export const metadata: Metadata = {
  title: 'THEA',
  description: 'Your personal assistant.',
  manifest: '/manifest.webmanifest',
  appleWebApp: { capable: true, title: 'THEA', statusBarStyle: 'black-translucent' },
  icons: { icon: '/icon.svg', apple: '/icon.svg' },
}

export const viewport: Viewport = {
  themeColor: '#0d0f12',
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${grotesk.variable} ${jetbrains.variable}`}>
      <body className="min-h-dvh font-sans antialiased">
        <div className="mx-auto flex min-h-dvh max-w-5xl flex-col px-4 pt-[env(safe-area-inset-top)] pb-[calc(env(safe-area-inset-bottom)+5rem)] sm:px-6 sm:pb-8">
          <Nav />
          <main className="flex flex-1 flex-col">{children}</main>
        </div>
      </body>
    </html>
  )
}
