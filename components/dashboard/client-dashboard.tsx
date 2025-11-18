'use client'

import { ReactNode, useEffect, useState } from 'react'

import { useRouter } from 'next/navigation'
import Navbar from '@/components/shared/navbar'
import Sidebar from '@/components/shared/sidebar'
import { apiRequest } from '@/lib/api'
import { clearAuthToken, getAuthToken } from '@/lib/auth'

interface ClientDashboardProps {
  children: ReactNode
}

export default function ClientDashboard({ children }: ClientDashboardProps) {
  const router = useRouter()
  const [isDark, setIsDark] = useState(true)
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  useEffect(() => {
    const saved = localStorage.getItem('theme')
    if (saved) {
      setIsDark(saved === 'dark')
    }
  }, [])

  useEffect(() => {
    const root = document.documentElement
    if (isDark) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
  }, [isDark])

  const toggleTheme = () => setIsDark((prev) => !prev)

  const handleLogout = async () => {
    if (isLoggingOut) return
    setIsLoggingOut(true)
    const token = getAuthToken()
    try {
      if (token) {
        await apiRequest('/auth/logout', { method: 'POST', token })
      }
    } catch {
      // Ignore network errors during logout
    } finally {
      clearAuthToken()
      router.push('/login')
    }
  }

  return (
    <div className="flex h-screen bg-background text-foreground">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar isDark={isDark} toggleTheme={toggleTheme} onLogout={handleLogout} />
        <main className="flex-1 overflow-auto bg-background">{children}</main>
      </div>
    </div>
  )
}
