'use client'

import Link from 'next/link'
import { ChevronRight, Code2, FileText, Zap, GitBranch, Sparkles, Workflow, TestTube, Sun, Moon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/components/theme-provider'

export default function HomePage() {
  const { isDark, toggleTheme, mounted } = useTheme()

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary/60 rounded-lg flex items-center justify-center">
              <Code2 className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-lg font-bold">CodeDoc Studio</span>
          </div>
          <div className="flex items-center gap-3">
            {mounted && (
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg border border-border hover:bg-muted transition-colors"
                aria-label="Toggle dark mode"
              >
                {isDark ? (
                  <Sun className="w-5 h-5 text-muted-foreground" />
                ) : (
                  <Moon className="w-5 h-5 text-muted-foreground" />
                )}
              </button>
            )}
            <Link href="/login">
              <Button variant="default" size="sm">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 sm:py-32 max-w-7xl mx-auto">
        <div className="text-center space-y-8">
          <div className="space-y-4">
            <div className="inline-block px-4 py-2 bg-muted rounded-full text-sm text-muted-foreground">
              AI-Powered Code Analysis
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-balance">
              Transform Your Code into Intelligent Documentation
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
              Generate comprehensive documentation, explanations, tests, and flowcharts instantly with AI. Save hours analyzing code.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link href="/login">
              <Button size="lg" className="gap-2">
                Get Started
                <ChevronRight className="w-4 h-4" />
              </Button>
            </Link>
            <Button variant="outline" size="lg">
              View Documentation
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 bg-muted/30 border-y border-border">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold">Powerful Features</h2>
            <p className="text-muted-foreground mt-2">Everything you need to understand and document your code</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-lg border border-border bg-card hover:border-primary/50 transition-colors"
              >
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold">90%</div>
            <p className="text-muted-foreground mt-2">Faster documentation creation</p>
          </div>
          <div>
            <div className="text-4xl font-bold">7+</div>
            <p className="text-muted-foreground mt-2">AI analysis capabilities</p>
          </div>
          <div>
            <div className="text-4xl font-bold">∞</div>
            <p className="text-muted-foreground mt-2">Code complexity support</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 bg-muted/30 border-t border-border">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h2 className="text-3xl sm:text-4xl font-bold">Ready to automate your documentation?</h2>
          <p className="text-lg text-muted-foreground">
            Join developers who are saving hours every week with AI CodeDoc Studio.
          </p>
          <Link href="/login">
            <Button size="lg">
              Start for Free
              <ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border px-4 sm:px-6 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
          <p>&copy; 2025 AI CodeDoc Studio. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="#" className="hover:text-foreground transition-colors">
              Privacy
            </Link>
            <Link href="#" className="hover:text-foreground transition-colors">
              Terms
            </Link>
            <Link href="#" className="hover:text-foreground transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}

const features = [
  {
    icon: FileText,
    title: 'Documentation Generation',
    description: 'Auto-generate comprehensive documentation from your source code with AI analysis.',
  },
  {
    icon: Sparkles,
    title: 'Code Explanation',
    description: 'Get line-by-line explanations of complex code in plain English.',
  },
  {
    icon: TestTube,
    title: 'Unit Test Generation',
    description: 'Automatically generate unit tests for your code with full coverage.',
  },
  {
    icon: Zap,
    title: 'Code Optimization',
    description: 'Receive AI-powered suggestions to optimize performance and readability.',
  },
  {
    icon: Workflow,
    title: 'Flowchart Visualization',
    description: 'Visualize your code logic with automatic flowchart generation.',
  },
  {
    icon: GitBranch,
    title: 'GitHub Integration',
    description: 'Analyze entire repositories and generate documentation for multiple files.',
  },
]
