'use client'

import { useEffect, useMemo, useState } from 'react'
import mermaid from 'mermaid'

interface FlowchartRendererProps {
  mermaidSource: string
  isLoading?: boolean
  error?: string | null
}

export default function FlowchartRenderer({ mermaidSource, isLoading, error }: FlowchartRendererProps) {
  const [svg, setSvg] = useState<string>('')
  const [renderError, setRenderError] = useState<string | null>(null)

  const chartDefinition = useMemo(() => mermaidSource.trim(), [mermaidSource])

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      securityLevel: 'loose',
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
      }
    })
  }, [])

  useEffect(() => {
    let isMounted = true
    const renderChart = async () => {
      if (!chartDefinition || error) {
        setSvg('')
        setRenderError(error || null)
        return
      }


      // Clean the mermaid code
      const cleanMermaidCode = (code: string) => {
        let cleaned = code.trim()
        // Remove markdown code blocks if present
        cleaned = cleaned.replace(/^```mermaid\s*/i, '').replace(/^```\s*/, '')
        cleaned = cleaned.replace(/```$/, '')
        return cleaned.trim()
      }

      const cleanedDefinition = cleanMermaidCode(chartDefinition)

      // Validate that the chart definition looks correct
      // Relaxed validation to support more diagram types
      const validTypes = ['flowchart', 'graph', 'sequenceDiagram', 'classDiagram', 'stateDiagram', 'erDiagram', 'gantt', 'pie', 'journey', 'gitGraph', 'C4Context']
      const startsWithValidType = validTypes.some(type => cleanedDefinition.startsWith(type))

      if (!startsWithValidType) {
        // Fallback: if it doesn't start with a known type, try to find it in the first few lines
        const lines = cleanedDefinition.split('\n')
        const hasValidType = lines.some(line => validTypes.some(type => line.trim().startsWith(type)))

        if (!hasValidType) {
          if (isMounted) {
            setRenderError('Invalid Mermaid syntax: Could not identify diagram type')
            setSvg('')
            console.error('Invalid mermaid code:', cleanedDefinition.substring(0, 100))
          }
          return
        }
      }

      try {
        const { svg } = await mermaid.render(`flowchart-${Date.now()}`, cleanedDefinition)
        if (isMounted) {
          setSvg(svg)
          setRenderError(null)
        }
      } catch (err) {
        if (isMounted) {
          const errorMsg = (err as Error).message
          console.error('Mermaid render error:', errorMsg)
          console.error('Mermaid code:', chartDefinition)
          setRenderError(`Flowchart render error: ${errorMsg}`)
          setSvg('')
        }
      }
    }
    renderChart()
    return () => {
      isMounted = false
    }
  }, [chartDefinition, error])

  return (
    <div className="flex flex-col h-full rounded-lg border border-border bg-muted overflow-hidden">
      <div className="bg-background border-b border-border px-4 py-3">
        <h3 className="font-semibold text-foreground">Flowchart</h3>
      </div>
      <div className="flex-1 overflow-auto p-4 flex items-center justify-center">
        {isLoading ? (
          <div className="animate-pulse space-y-2 w-full">
            <div className="h-4 bg-muted-foreground/20 rounded w-1/2 mx-auto" />
            <div className="h-4 bg-muted-foreground/20 rounded w-3/4 mx-auto" />
            <div className="h-4 bg-muted-foreground/20 rounded w-2/3 mx-auto" />
          </div>
        ) : renderError ? (
          <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive max-w-md text-center">
            {renderError}
          </div>
        ) : svg ? (
          <div
            className="w-full max-w-3xl"
            dangerouslySetInnerHTML={{ __html: svg }}
            aria-label="Generated flowchart"
          />
        ) : (
          <p className="text-sm text-muted-foreground text-center">Run the flowchart generator to visualize logic.</p>
        )}
      </div>
    </div>
  )
}
