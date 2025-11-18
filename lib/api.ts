const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000'

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: unknown
  token?: string | null
  headers?: Record<string, string>
}

type ErrorShape = { detail?: string; error?: string; message?: string }

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, token, headers = {} } = options
  const finalHeaders: Record<string, string> = { ...headers }

  if (body !== undefined && !finalHeaders['Content-Type']) {
    finalHeaders['Content-Type'] = 'application/json'
  }

  if (token) {
    finalHeaders.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: finalHeaders,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  const contentType = response.headers.get('Content-Type') ?? ''
  const isJson = contentType.includes('application/json')

  if (!response.ok) {
    let message = response.statusText
    if (isJson) {
      const data: ErrorShape = await response.json()
      message = data.detail ?? data.error ?? data.message ?? message
    }
    throw new Error(message || 'Request failed')
  }

  return isJson ? ((await response.json()) as T) : (await (response.text() as unknown as T))
}

export function buildQuery(params: Record<string, string | number | undefined | null>) {
  const usp = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      usp.append(key, String(value))
    }
  })
  const query = usp.toString()
  return query ? `?${query}` : ''
}

