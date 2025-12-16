/**
 * Streaming API Client for Server-Sent Events (SSE)
 * Handles real-time streaming responses from the backend
 */

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000'

export interface StreamOptions {
    method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
    body?: unknown
    token?: string | null
    headers?: Record<string, string>
    onChunk: (chunk: string) => void
    onComplete?: () => void
    onError?: (error: Error) => void
    onStart?: () => void
}

interface SSEEvent {
    type: 'start' | 'chunk' | 'done' | 'error'
    content?: string
    message?: string
}

/**
 * Stream API request using Server-Sent Events
 * Processes chunks as they arrive from the server
 */
export async function streamRequest(
    path: string,
    options: StreamOptions
): Promise<void> {
    const {
        method = 'POST',
        body,
        token,
        headers = {},
        onChunk,
        onComplete,
        onError,
        onStart
    } = options

    const finalHeaders: Record<string, string> = { ...headers }

    if (body !== undefined && !finalHeaders['Content-Type']) {
        finalHeaders['Content-Type'] = 'application/json'
    }

    if (token) {
        finalHeaders.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`
    }

    try {
        const response = await fetch(`${API_BASE}${path}`, {
            method,
            headers: finalHeaders,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        })

        if (!response.ok) {
            const contentType = response.headers.get('Content-Type') ?? ''
            const isJson = contentType.includes('application/json')

            let message = response.statusText
            if (isJson) {
                const data = await response.json()
                message = data.detail ?? data.error ?? data.message ?? message
            }

            throw new Error(message || 'Request failed')
        }

        // Check if response is actually a stream
        if (!response.body) {
            throw new Error('Response body is null')
        }

        // Signal streaming has started
        onStart?.()

        // Read the stream
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
            const { done, value } = await reader.read()

            if (done) {
                break
            }

            // Decode the chunk
            buffer += decoder.decode(value, { stream: true })

            // Process complete SSE messages
            const lines = buffer.split('\n')
            buffer = lines.pop() || '' // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6) // Remove 'data: ' prefix

                    try {
                        const event: SSEEvent = JSON.parse(data)

                        switch (event.type) {
                            case 'start':
                                // Stream started
                                break

                            case 'chunk':
                                if (event.content) {
                                    onChunk(event.content)
                                }
                                break

                            case 'done':
                                // Stream completed successfully
                                onComplete?.()
                                return

                            case 'error':
                                throw new Error(event.message || 'Streaming error')
                        }
                    } catch (parseError) {
                        // If JSON parsing fails, treat as raw chunk
                        if (data && data !== '[DONE]') {
                            onChunk(data)
                        }
                    }
                }
            }
        }

        // Stream ended naturally
        onComplete?.()

    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error'
        onError?.(new Error(errorMessage))
        throw error
    }
}

/**
 * Helper function to create a streaming request with common options
 */
export async function streamApiRequest(
    endpoint: string,
    options: {
        body: unknown
        token: string | null
        onChunk: (chunk: string) => void
        onComplete?: () => void
        onError?: (error: Error) => void
        onStart?: () => void
    }
): Promise<void> {
    return streamRequest(endpoint, {
        method: 'POST',
        ...options
    })
}
