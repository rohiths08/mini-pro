'use client'

import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { setAuthToken } from '@/lib/auth'

export default function LoginSuccessPage() {
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      setAuthToken(token)
      router.replace('/page/documentation')
    } else {
      router.replace('/login')
    }
  }, [router, searchParams])

  return (
    <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
      <div className="space-y-4 text-center">
        <p className="text-lg font-semibold">Completing login…</p>
        <p className="text-sm text-muted-foreground">You will be redirected shortly.</p>
      </div>
    </div>
  )
}

