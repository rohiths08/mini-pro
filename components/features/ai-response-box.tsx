'use client'

import { Copy, Download } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Button } from '@/components/ui/button'

interface AIResponseBoxProps {
  title: string
  content: string
  isLoading?: boolean
  isStreaming?: boolean
  error?: string | null
  emptyMessage?: string
}

export default function AIResponseBox({
  title,
  content,
  isLoading,
  isStreaming,
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
      <div className="flex-1 overflow-auto p-4" id="ai-response-content">
        {isLoading || isStreaming ? (
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
                h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mt-6 mb-4 text-foreground border-b border-border pb-2" {...props} />,
                h2: ({ node, ...props }) => <h2 className="text-xl font-semibold mt-6 mb-3 text-foreground border-b border-border/50 pb-1" {...props} />,
                h3: ({ node, ...props }) => <h3 className="text-lg font-medium mt-5 mb-2 text-foreground" {...props} />,
                h4: ({ node, ...props }) => <h4 className="text-base font-medium mt-4 mb-2 text-foreground/90" {...props} />,
                p: ({ node, ...props }) => <div className="mb-3 leading-relaxed text-foreground/90" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc list-outside ml-6 mb-4 space-y-2" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal list-outside ml-6 mb-4 space-y-2" {...props} />,
                li: ({ node, ...props }) => <li className="text-foreground/90 leading-relaxed" {...props} />,
                a: ({ node, ...props }) => <a className="text-primary hover:underline" {...props} />,
                blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-primary/50 pl-4 italic my-4 text-muted-foreground" {...props} />,
                strong: ({ node, ...props }) => <strong className="font-semibold text-foreground" {...props} />,
                em: ({ node, ...props }) => <em className="italic text-foreground/95" {...props} />,
                hr: ({ node, ...props }) => <hr className="my-6 border-border" {...props} />,
                code: ({ node, inline, className, children, ...props }: any) => {
                  const match = /language-(\w+)/.exec(className || '')
                  const language = match ? match[1] : 'text'
                  const codeString = String(children).replace(/\n$/, '')

                  if (inline) {
                    return (
                      <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono text-primary" {...props}>
                        {children}
                      </code>
                    )
                  }

                  return (
                    <SyntaxHighlighter
                      language={language}
                      style={vscDarkPlus}
                      customStyle={{
                        margin: '1rem 0',
                        borderRadius: '0.5rem',
                        fontSize: '0.875rem',
                        border: '1px solid hsl(var(--border))',
                      }}
                      PreTag="div"
                      {...props}
                    >
                      {codeString}
                    </SyntaxHighlighter>
                  )
                },
                pre: ({ node, children, ...props }) => <>{children}</>,
              }}
            >
              {content}
            </ReactMarkdown>
            {isStreaming && (
              <span className="inline-block w-2 h-4 bg-primary animate-pulse ml-1" />
            )}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">{emptyMessage}</p>
        )}
      </div>
    </div>
  )
}
