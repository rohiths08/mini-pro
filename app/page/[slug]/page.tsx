'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import ClientDashboard from '@/components/dashboard/client-dashboard'
import FeatureWorkspace from '@/components/features/feature-workspace'
import FlowchartWorkspace from '@/components/features/flowchart-workspace'
import GithubPanel from '@/components/features/github-panel'
import { getAuthToken } from '@/lib/auth'

const defaultSlug = 'documentation'

export default function FeaturePage() {
  const params = useParams()
  const router = useRouter()
  const slug = (params.slug as string) || defaultSlug
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    const token = getAuthToken()
    if (!token) {
      router.replace('/login')
      return
    }
    setIsReady(true)
  }, [router])

  if (!isReady) {
    return null
  }

  const content = (() => {
    switch (slug) {
      case 'documentation':
        return <FeatureWorkspace feature="documentation" title="Generated Documentation" />
      case 'explain':
        return <FeatureWorkspace feature="explain" title="Code Explanation" />
      case 'tests':
        return <FeatureWorkspace feature="tests" title="Generated Unit Tests" />
      case 'optimize':
        return <FeatureWorkspace feature="optimize" title="Optimization Suggestions" />
      case 'flowchart':
        return <FlowchartWorkspace />
      case 'github':
        return (
          <div className="p-6 h-full">
            <GithubPanel />
          </div>
        )
      default:
        return <div className="p-6 text-sm text-muted-foreground">Select a feature from the sidebar.</div>
    }
  })()

  return <ClientDashboard>{content}</ClientDashboard>
}
