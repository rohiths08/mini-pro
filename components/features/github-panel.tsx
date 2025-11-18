'use client'

import { useEffect, useState } from 'react'
import { RefreshCcw, Folder, FileCode2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { apiRequest, buildQuery } from '@/lib/api'
import { getAuthToken } from '@/lib/auth'

interface Repo {
  name: string
  url: string
  description: string | null
  owner: string
  is_fork: boolean
}

interface RepoContent {
  name: string
  type: 'file' | 'dir'
  path: string
  url: string
}

export default function GithubPanel() {
  const [repos, setRepos] = useState<Repo[]>([])
  const [contents, setContents] = useState<RepoContent[]>([])
  const [selectedRepo, setSelectedRepo] = useState<Repo | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isContentLoading, setContentLoading] = useState(false)

  const loadRepos = async () => {
    const token = getAuthToken()
    if (!token) {
      setError('Connect your account to GitHub first.')
      return
    }
    setIsLoading(true)
    setError(null)
    try {
      const data = await apiRequest<{ repos: Repo[]; error?: string }>('/github/repos', { token })
      if (data.error) {
        setError(data.error)
        setRepos([])
        return
      }
      setRepos(data.repos ?? [])
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setIsLoading(false)
    }
  }

  const loadContents = async (repo: Repo) => {
    const token = getAuthToken()
    if (!token) return
    setSelectedRepo(repo)
    setContentLoading(true)
    setError(null)
    try {
      const query = buildQuery({ owner: repo.owner, repo: repo.name, path: '' })
      const data = await apiRequest<{ contents: RepoContent[]; error?: string }>(`/github/contents${query}`, {
        token,
      })
      if (data.error) {
        setError(data.error)
        setContents([])
        return
      }
      setContents(data.contents ?? [])
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setContentLoading(false)
    }
  }

  useEffect(() => {
    loadRepos()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="flex flex-col h-full rounded-lg border border-border bg-muted overflow-hidden">
      <div className="bg-background border-b border-border px-4 py-3 flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-foreground">GitHub Repositories</h3>
          <p className="text-xs text-muted-foreground">Fetch metadata through the backend GitHub proxy.</p>
        </div>
        <Button size="sm" variant="outline" onClick={loadRepos} disabled={isLoading}>
          <RefreshCcw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-px flex-1 bg-border">
        <div className="bg-muted p-4 space-y-3 overflow-auto">
          {isLoading ? (
            <p className="text-sm text-muted-foreground">Loading repositories…</p>
          ) : error ? (
            <p className="text-sm text-destructive">{error}</p>
          ) : repos.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No repositories fetched yet. Ensure your backend has a GitHub token stored for this user.
            </p>
          ) : (
            <ul className="space-y-3">
              {repos.map((repo) => (
                <li
                  key={`${repo.owner}/${repo.name}`}
                  className="rounded-lg border border-border bg-background p-3"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="font-semibold text-sm text-foreground">{repo.name}</p>
                      <p className="text-xs text-muted-foreground">{repo.description ?? 'No description'}</p>
                    </div>
                    <Button size="sm" variant="secondary" onClick={() => loadContents(repo)}>
                      Browse
                    </Button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="bg-muted p-4 overflow-auto">
          {isContentLoading ? (
            <p className="text-sm text-muted-foreground">Loading repository contents…</p>
          ) : selectedRepo ? (
            <div>
              <div className="mb-4">
                <p className="font-semibold text-sm text-foreground">{selectedRepo.name}</p>
                <a
                  href={selectedRepo.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-primary hover:underline"
                >
                  Open on GitHub
                </a>
              </div>
              {contents.length > 0 ? (
                <ul className="space-y-2">
                  {contents.map((item) => (
                    <li
                      key={item.path}
                      className="flex items-center gap-3 rounded-lg border border-border bg-background px-3 py-2"
                    >
                      {item.type === 'dir' ? (
                        <Folder className="h-4 w-4 text-primary" />
                      ) : (
                        <FileCode2 className="h-4 w-4 text-primary" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm text-foreground">{item.name}</p>
                        <p className="text-xs text-muted-foreground">{item.type === 'dir' ? 'Directory' : 'File'}</p>
                      </div>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-primary hover:underline"
                      >
                        View
                      </a>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">Select a repository to browse its files.</p>
              )}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">Choose a repository from the list to view its contents.</p>
          )}
        </div>
      </div>
    </div>
  )
}

