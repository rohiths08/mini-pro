'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import HomePage from '@/components/home/home-page'
import { getAuthToken } from '@/lib/auth'

export default function Page() {
  const router = useRouter()
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    const token = getAuthToken()
    if (token) {
      router.replace('/page/documentation')
    } else {
      setIsChecking(false)
    }
  }, [router])

  if (isChecking) {
    return null
  }

  return <HomePage />
}
