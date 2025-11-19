'use client'

import { Copy, Download } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Button } from '@/components/ui/button'

interface AIResponseBoxProps {
  title: string
  content: string
  isLoading?: boolean
  error?: string | null
  emptyMessage?: string
}

export default function AIResponseBox({
  title,
  content,
  isLoading,
  error,
  emptyMessage = 'Run the analysis to view AI output.',
}: AIResponseBoxProps) {
  const handleCopy = () => {
    if (!content) return
    navigator.clipboard.writeText(content)
  }

  const handleDownload = () => {
    if (!content) return
    const element = document.createElement('a')
    element.setAttribute('href', `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`)
    element.setAttribute('download', `${title.toLowerCase().replace(/\s+/g, '-')}.md`)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="flex flex-col h-full rounded-lg border border-border bg-muted overflow-hidden">
      <div className="bg-background border-b border-border px-4 py-3 flex items-center justify-between">
        <h3 className="font-semibold text-foreground">{title}</h3>
        <div className="flex gap-2">
          <Button size="sm" variant="outline" onClick={handleCopy} title="Copy" disabled={!content}>
            <Copy className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="outline" onClick={handleDownload} title="Download" disabled={!content}>
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <div className="flex-1 overflow-auto p-4">
        {isLoading ? (
          <div className="animate-pulse space-y-2">
            <div className="h-4 bg-muted-foreground/20 rounded w-3/4" />
            <div className="h-4 bg-muted-foreground/20 rounded w-full" />
            <div className="h-4 bg-muted-foreground/20 rounded w-5/6" />
          </div>
        ) : error ? (
          <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
            {error}
          </div>
        ) : content ? (
          <div className="prose prose-invert prose-sm max-w-none text-foreground prose-headings:text-foreground prose-code:text-primary prose-pre:bg-background prose-pre:border prose-pre:border-border">
            <ReactMarkdown
              components={{
                code: ({ node, inline, className, children, ...props }) => {
                  if (inline) {
                    return (
                      <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                        {children}
                      </code>
                    )
                  }
                  return (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">{emptyMessage}</p>
        )}
      </div>
    </div>
  )
}
