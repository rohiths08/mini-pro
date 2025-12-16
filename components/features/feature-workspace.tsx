'use client'

import { useMemo, useState, useEffect, useRef } from 'react'
import CodeEditor from '@/components/features/code-editor'
import AIResponseBox from '@/components/features/ai-response-box'
import { apiRequest } from '@/lib/api'
import { streamApiRequest } from '@/lib/streaming-api'
import { getAuthToken } from '@/lib/auth'
import { getDefaultLanguage } from '@/lib/preferences'
import { autoDetectLanguage } from '@/lib/language-detector'

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
  const [language, setLanguage] = useState(getDefaultLanguage())
  const [fileName, setFileName] = useState('code')
  const [response, setResponse] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const manualLanguageChangeRef = useRef(false)
  const codeChangeTimerRef = useRef<NodeJS.Timeout | null>(null)

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

  // Auto-detect language when code changes (debounced)
  useEffect(() => {
    // Clear previous timer
    if (codeChangeTimerRef.current) {
      clearTimeout(codeChangeTimerRef.current)
    }

    // Only auto-detect if:
    // 1. User hasn't manually changed language
    // 2. Code is substantial (> 20 chars)
    if (!manualLanguageChangeRef.current && code.trim().length > 20) {
      // Debounce detection by 1 second to avoid detecting while user is typing
      codeChangeTimerRef.current = setTimeout(() => {
        const detected = autoDetectLanguage(code, fileName)
        if (detected && detected !== language) {
          setLanguage(detected)
        }
      }, 1000)
    }

    // Cleanup on unmount
    return () => {
      if (codeChangeTimerRef.current) {
        clearTimeout(codeChangeTimerRef.current)
      }
    }
  }, [code, fileName, language])

  const handleSubmit = async () => {
    const token = getAuthToken()
    if (!token) {
      setError('Please sign in to run AI features.')
      return
    }

    setIsLoading(true)
    setIsStreaming(true)
    setError(null)
    setResponse('') // Clear previous response

    try {
      // Try streaming first
      console.log('🌊 Starting streaming to:', `${config.endpoint}/stream`)
      await streamApiRequest(`${config.endpoint}/stream`, {
        token,
        body: { code, language, file_name: fileName },
        onStart: () => {
          console.log('✅ Stream started!')
          setIsLoading(false) // Stop loading, start streaming
        },
        onChunk: (chunk) => {
          console.log('📦 Chunk received:', chunk.length, 'chars')
          setResponse(prev => prev + chunk)
          // Auto-scroll to bottom
          setTimeout(() => {
            const element = document.getElementById('ai-response-content')
            if (element) {
              element.scrollTop = element.scrollHeight
            }
          }, 0)
        },
        onComplete: () => {
          console.log('✅ Streaming complete!')
          setIsStreaming(false)
        },
        onError: async (streamError) => {
          console.warn('Streaming failed, falling back to regular request:', streamError)
          setIsStreaming(false)

          // Fallback to non-streaming endpoint
          try {
            const result = await apiRequest(config.endpoint, {
              method: 'POST',
              token,
              body: { code, language, file_name: fileName },
            })
            setResponse(config.formatter(result))
          } catch (fallbackError) {
            setError((fallbackError as Error).message)
            setResponse('')
          }
        }
      })
    } catch (err) {
      setError((err as Error).message)
      setResponse('')
      setIsStreaming(false)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang as any) // CodeEditor passes string, we accept it
    manualLanguageChangeRef.current = true // Mark as manual change
  }

  const handleAutoDetect = () => {
    const detected = autoDetectLanguage(code, fileName)
    if (detected) {
      setLanguage(detected)
      manualLanguageChangeRef.current = false // Reset manual flag
    }
  }

  const handleFileNameChange = (name: string) => {
    setFileName(name)
    // Auto-detect on filename change if not manually set
    if (!manualLanguageChangeRef.current) {
      const detected = autoDetectLanguage(code, name)
      if (detected) {
        setLanguage(detected)
      }
    }
  }

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 h-full p-6">
      <CodeEditor
        code={code}
        language={language}
        fileName={fileName}
        onCodeChange={setCode}
        onLanguageChange={handleLanguageChange}
        onFileNameChange={handleFileNameChange}
        onAutoDetect={handleAutoDetect}
        onSubmit={handleSubmit}
        isSubmitting={isLoading}
      />
      <AIResponseBox title={title} content={response} isLoading={isLoading} isStreaming={isStreaming} error={error} emptyMessage={instructions} />
    </div>
  )
}

