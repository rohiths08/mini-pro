'use client'

import { useState } from 'react'
import CodeEditor from '@/components/features/code-editor'
import FlowchartRenderer from '@/components/features/flowchart-renderer'
import { apiRequest } from '@/lib/api'
import { getAuthToken } from '@/lib/auth'

export default function FlowchartWorkspace() {
  const [code, setCode] = useState('function handleRequest(req) {\n  if (!req.user) {\n    return redirect("/login")\n  }\n  return renderDashboard(req.user)\n}')
  const [language, setLanguage] = useState('javascript')
  const [fileName, setFileName] = useState('flow.js')
  const [diagram, setDiagram] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async () => {
    const token = getAuthToken()
    if (!token) {
      setError('Please sign in to generate flowcharts.')
      return
    }
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiRequest<{ mermaid: string; error?: string }>('/ai/flowchart', {
        method: 'POST',
        token,
        body: { code, language, file_name: fileName },
      })
      
      if (result.error) {
        setError(result.error)
        setDiagram(result.mermaid ?? '')
      } else {
        setDiagram(result.mermaid ?? '')
        console.log('Received mermaid code:', result.mermaid?.substring(0, 100))
      }
    } catch (err) {
      setError((err as Error).message)
      setDiagram('')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 h-full p-6">
      <CodeEditor
        code={code}
        language={language}
        fileName={fileName}
        onCodeChange={setCode}
        onLanguageChange={setLanguage}
        onFileNameChange={setFileName}
        onSubmit={handleSubmit}
        isSubmitting={isLoading}
      />
      <FlowchartRenderer mermaidSource={diagram} isLoading={isLoading} error={error} />
    </div>
  )
}

