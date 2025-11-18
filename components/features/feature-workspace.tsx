'use client'

import { useMemo, useState } from 'react'
import CodeEditor from '@/components/features/code-editor'
import AIResponseBox from '@/components/features/ai-response-box'
import { apiRequest } from '@/lib/api'
import { getAuthToken } from '@/lib/auth'

type FeatureType = 'documentation' | 'explain' | 'tests' | 'optimize'

const featureConfig: Record<
  FeatureType,
  {
    endpoint: string
    formatter: (payload: any) => string
    placeholder: string
  }
> = {
  documentation: {
    endpoint: '/ai/documentation',
    formatter: (payload) => payload.markdown ?? 'No documentation returned.',
    placeholder: '#include <stdio.h>\n\nint main() {\n  printf("Hello, world!");\n  return 0;\n}',
  },
  explain: {
    endpoint: '/ai/explain',
    formatter: (payload) => payload.full_explanation ?? 'No explanation returned.',
    placeholder: 'function sum(a, b) {\n  return a + b\n}',
  },
  tests: {
    endpoint: '/ai/tests',
    formatter: (payload) => payload.test_source ?? 'No unit tests returned.',
    placeholder: 'const isEven = (value) => value % 2 === 0;\nexport default isEven;',
  },
  optimize: {
    endpoint: '/ai/optimize',
    formatter: (payload) => payload.refactored_code ?? 'No optimization returned.',
    placeholder: 'def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)',
  },
}

interface FeatureWorkspaceProps {
  feature: FeatureType
  title: string
}

export default function FeatureWorkspace({ feature, title }: FeatureWorkspaceProps) {
  const config = featureConfig[feature]
  const [code, setCode] = useState(config.placeholder)
  const [language, setLanguage] = useState('javascript')
  const [fileName, setFileName] = useState('code')
  const [response, setResponse] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const instructions = useMemo(() => {
    switch (feature) {
      case 'documentation':
        return 'Generate Markdown docs with summaries, parameters, and usage examples.'
      case 'explain':
        return 'Explain the code line-by-line so new contributors understand logic quickly.'
      case 'tests':
        return 'Produce tests that cover core logic and edge cases.'
      case 'optimize':
        return 'Suggest performance or readability improvements.'
    }
  }, [feature])

  const handleSubmit = async () => {
    const token = getAuthToken()
    if (!token) {
      setError('Please sign in to run AI features.')
      return
    }
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiRequest(config.endpoint, {
        method: 'POST',
        token,
        body: { code, language, file_name: fileName },
      })
      setResponse(config.formatter(result))
    } catch (err) {
      setError((err as Error).message)
      setResponse('')
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
      <AIResponseBox title={title} content={response} isLoading={isLoading} error={error} emptyMessage={instructions} />
    </div>
  )
}

