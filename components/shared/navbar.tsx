'use client'

import { useEffect, useState } from 'react'
import { Sun, Moon, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface NavbarProps {
  isDark: boolean
  toggleTheme: () => void
  onLogout: () => void
}

export default function Navbar({ isDark, toggleTheme, onLogout }: NavbarProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <nav className="border-b border-border bg-background px-6 py-4 flex items-center justify-between">
      <h1 className="text-lg font-semibold text-foreground">AI CodeDoc Studio</h1>
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          size="icon"
          onClick={toggleTheme}
          title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
        <Button variant="outline" size="icon" onClick={onLogout} title="Logout">
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </nav>
  )
}
