/**
 * User preferences management using localStorage
 */

const STORAGE_KEYS = {
    DEFAULT_LANGUAGE: 'default_language',
    DEFAULT_THEME: 'default_theme',
} as const

export type SupportedLanguage =
    | 'javascript'
    | 'typescript'
    | 'python'
    | 'java'
    | 'cpp'
    | 'c'
    | 'go'
    | 'csharp'

export type Theme = 'dark' | 'light' | 'system'

const DEFAULT_LANGUAGE: SupportedLanguage = 'javascript'
const DEFAULT_THEME: Theme = 'dark'

/**
 * Get the user's default language preference
 */
export function getDefaultLanguage(): SupportedLanguage {
    if (typeof window === 'undefined') return DEFAULT_LANGUAGE

    const stored = localStorage.getItem(STORAGE_KEYS.DEFAULT_LANGUAGE)
    return (stored as SupportedLanguage) || DEFAULT_LANGUAGE
}

/**
 * Set the user's default language preference
 */
export function setDefaultLanguage(language: SupportedLanguage): void {
    if (typeof window === 'undefined') return

    localStorage.setItem(STORAGE_KEYS.DEFAULT_LANGUAGE, language)
}

/**
 * Get the user's theme preference
 */
export function getDefaultTheme(): Theme {
    if (typeof window === 'undefined') return DEFAULT_THEME

    const stored = localStorage.getItem(STORAGE_KEYS.DEFAULT_THEME)
    return (stored as Theme) || DEFAULT_THEME
}

/**
 * Set the user's theme preference
 */
export function setDefaultTheme(theme: Theme): void {
    if (typeof window === 'undefined') return

    localStorage.setItem(STORAGE_KEYS.DEFAULT_THEME, theme)
}

/**
 * Map display names to language identifiers
 */
export const LANGUAGE_MAP: Record<string, SupportedLanguage> = {
    'JavaScript': 'javascript',
    'TypeScript': 'typescript',
    'Python': 'python',
    'Java': 'java',
    'C++': 'cpp',
    'C': 'c',
    'Go': 'go',
    'C#': 'csharp',
}

/**
 * Map language identifiers to display names
 */
export const LANGUAGE_DISPLAY_MAP: Record<SupportedLanguage, string> = {
    javascript: 'JavaScript',
    typescript: 'TypeScript',
    python: 'Python',
    java: 'Java',
    cpp: 'C++',
    c: 'C',
    go: 'Go',
    csharp: 'C#',
}
