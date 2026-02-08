'use client'

import Editor from '@monaco-editor/react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Sparkles } from 'lucide-react'

const languages = ['javascript', 'typescript', 'python', 'java', 'go', 'csharp', 'cpp', 'c']

interface CodeEditorProps {
  code: string
  language: string
  fileName: string
  onCodeChange: (value: string) => void
  onSubmit: () => void
  isSubmitting?: boolean
  onLanguageChange?: (lang: string) => void
  onFileNameChange?: (name: string) => void
  onAutoDetect?: () => void
}

export default function CodeEditor({
  code,
  language,
  fileName,
  onCodeChange,
  onSubmit,
  isSubmitting,
  onLanguageChange,
  onFileNameChange,
  onAutoDetect,
}: CodeEditorProps) {
  return (
    <div className="flex flex-col h-full rounded-lg border border-border bg-muted overflow-hidden">
      <div className="bg-background border-b border-border px-4 py-3 flex flex-wrap items-center gap-3 justify-between">
        <h3 className="font-semibold text-foreground">Code Editor</h3>
        <div className="flex items-center gap-3 flex-wrap">
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            File
            <Input
              value={fileName}
              onChange={(event) => onFileNameChange?.(event.target.value)}
              className="h-8 w-32"
              placeholder="file name"
            />
          </label>
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            Language
            <div className="flex items-center gap-1">
              <select
                value={language}
                onChange={(event) => onLanguageChange?.(event.target.value)}
                className="h-8 rounded-md border border-border bg-background px-2 text-foreground text-sm"
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
              <Button
                size="sm"
                variant="ghost"
                onClick={onAutoDetect}
                title="Auto-detect language"
                className="h-8 px-2"
              >
                <Sparkles className="h-4 w-4" />
              </Button>
            </div>
          </label>
          <Button size="sm" variant="outline" onClick={onSubmit} disabled={isSubmitting}>
            {isSubmitting ? 'Running...' : 'Submit'}
          </Button>
        </div>
      </div>
      <div className="flex-1 overflow-hidden">
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={(value) => onCodeChange(value || '')}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            wordWrap: 'on',
            automaticLayout: true,
          }}
        />
      </div>
    </div>
  )
}
