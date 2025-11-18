'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { FileText, MessageSquare, Code2, Zap, Network as GitNetwork, LineChart, Settings } from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { icon: FileText, label: 'Documentation', href: '/page/documentation' },
  { icon: MessageSquare, label: 'Explain Code', href: '/page/explain' },
  { icon: Code2, label: 'Unit Tests', href: '/page/tests' },
  { icon: Zap, label: 'Optimize', href: '/page/optimize' },
  { icon: LineChart, label: 'Flowchart', href: '/page/flowchart' },
  { icon: GitNetwork, label: 'GitHub Repo', href: '/page/github' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 border-r border-border bg-background flex flex-col">
      <div className="p-6 border-b border-border">
        <h2 className="text-xl font-bold text-primary">CodeDoc</h2>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-4 py-2 rounded-lg transition-colors',
                isActive ? 'bg-primary text-primary-foreground' : 'text-foreground hover:bg-muted'
              )}
            >
              <Icon className="h-5 w-5" />
              <span className="text-sm font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>
      <div className="border-t border-border p-4">
        <Link
          href="/settings"
          className="flex items-center gap-3 px-4 py-2 rounded-lg text-foreground hover:bg-muted transition-colors"
        >
          <Settings className="h-5 w-5" />
          <span className="text-sm font-medium">Settings</span>
        </Link>
      </div>
    </aside>
  )
}
