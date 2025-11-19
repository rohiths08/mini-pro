'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import ClientDashboard from '@/components/dashboard/client-dashboard'
import { getAuthToken } from '@/lib/auth'
import { apiRequest } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { User, Mail, Calendar, Key } from 'lucide-react'

interface UserProfile {
  id: string
  email: string
  name?: string
  picture?: string
  created_at?: string
}

export default function SettingsPage() {
  const router = useRouter()
  const [isReady, setIsReady] = useState(false)
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const token = getAuthToken()
    if (!token) {
      router.replace('/login')
      return
    }
    setIsReady(true)
    loadProfile(token)
  }, [router])

  const loadProfile = async (token: string) => {
    try {
      const data = await apiRequest<UserProfile>('/auth/profile', {
        method: 'GET',
        token,
      })
      setProfile(data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isReady) {
    return null
  }

  return (
    <ClientDashboard>
      <div className="p-6 h-full overflow-auto">
        <div className="max-w-3xl mx-auto space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Settings</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Manage your account settings and preferences
            </p>
          </div>

          {isLoading ? (
            <div className="animate-pulse space-y-4">
              <div className="h-24 bg-muted rounded-lg" />
              <div className="h-48 bg-muted rounded-lg" />
            </div>
          ) : error ? (
            <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
              {error}
            </div>
          ) : (
            <>
              {/* Account Information */}
              <div className="rounded-lg border border-border bg-card p-6 space-y-4">
                <div className="flex items-center gap-3 pb-4 border-b border-border">
                  <User className="h-5 w-5 text-primary" />
                  <h2 className="text-lg font-semibold text-foreground">Account Information</h2>
                </div>

                <div className="space-y-4">
                  {profile?.picture && (
                    <div className="flex items-center gap-4">
                      <img
                        src={profile.picture}
                        alt="Profile"
                        className="w-16 h-16 rounded-full border-2 border-border"
                      />
                      <div>
                        <p className="text-sm font-medium text-foreground">Profile Picture</p>
                        <p className="text-xs text-muted-foreground">
                          Synced from your OAuth provider
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="grid gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <User className="h-4 w-4" />
                        Name
                      </label>
                      <Input
                        value={profile?.name || 'Not provided'}
                        disabled
                        className="bg-muted"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <Mail className="h-4 w-4" />
                        Email
                      </label>
                      <Input
                        value={profile?.email || 'Not provided'}
                        disabled
                        className="bg-muted"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-sm font-medium text-foreground flex items-center gap-2">
                        <Key className="h-4 w-4" />
                        User ID
                      </label>
                      <Input
                        value={profile?.id || 'Not provided'}
                        disabled
                        className="bg-muted font-mono text-xs"
                      />
                    </div>

                    {profile?.created_at && (
                      <div className="space-y-2">
                        <label className="text-sm font-medium text-foreground flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          Member Since
                        </label>
                        <Input
                          value={new Date(profile.created_at).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          })}
                          disabled
                          className="bg-muted"
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Preferences */}
              <div className="rounded-lg border border-border bg-card p-6 space-y-4">
                <h2 className="text-lg font-semibold text-foreground border-b border-border pb-4">
                  Preferences
                </h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-foreground">Default Language</p>
                      <p className="text-xs text-muted-foreground">
                        Set the default programming language for code editor
                      </p>
                    </div>
                    <select className="h-9 rounded-md border border-border bg-background px-3 text-foreground text-sm">
                      <option>JavaScript</option>
                      <option>TypeScript</option>
                      <option>Python</option>
                      <option>Java</option>
                      <option>C++</option>
                      <option>C</option>
                      <option>Go</option>
                      <option>C#</option>
                    </select>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-foreground">Theme</p>
                      <p className="text-xs text-muted-foreground">
                        Choose your preferred color theme
                      </p>
                    </div>
                    <select className="h-9 rounded-md border border-border bg-background px-3 text-foreground text-sm">
                      <option>Dark</option>
                      <option>Light</option>
                      <option>System</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Danger Zone */}
              <div className="rounded-lg border border-destructive/30 bg-card p-6 space-y-4">
                <h2 className="text-lg font-semibold text-destructive">Danger Zone</h2>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-foreground">Sign Out</p>
                    <p className="text-xs text-muted-foreground">
                      Sign out from your current session
                    </p>
                  </div>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => {
                      localStorage.removeItem('auth_token')
                      router.push('/login')
                    }}
                  >
                    Sign Out
                  </Button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </ClientDashboard>
  )
}
