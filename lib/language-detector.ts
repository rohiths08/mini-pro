/**
 * Language Auto-Detection Utility
 * Detects programming language from file extensions and code syntax patterns
 */

type SupportedLanguage = 'javascript' | 'typescript' | 'python' | 'java' | 'go' | 'csharp' | 'cpp' | 'c'

// File extension to language mapping
const extensionMap: Record<string, SupportedLanguage> = {
    // JavaScript/TypeScript
    'js': 'javascript',
    'jsx': 'javascript',
    'mjs': 'javascript',
    'cjs': 'javascript',
    'ts': 'typescript',
    'tsx': 'typescript',

    // Python
    'py': 'python',
    'pyw': 'python',

    // Java
    'java': 'java',

    // Go
    'go': 'go',

    // C#
    'cs': 'csharp',

    // C/C++
    'cpp': 'cpp',
    'cc': 'cpp',
    'cxx': 'cpp',
    'c++': 'cpp',
    'hpp': 'cpp',
    'hh': 'cpp',
    'hxx': 'cpp',
    'c': 'c',
    'h': 'c',
}

// Syntax patterns for each language (ordered by specificity)
const syntaxPatterns: Record<SupportedLanguage, RegExp[]> = {
    python: [
        /^\s*def\s+\w+\s*\(/m,
        /^\s*class\s+\w+/m,
        /^\s*import\s+\w+/m,
        /^\s*from\s+\w+\s+import/m,
        /^\s*@\w+/m, // decorators
        /:\s*$/m, // colon at end of line (common in Python)
    ],

    javascript: [
        /\bconst\s+\w+\s*=/,
        /\blet\s+\w+\s*=/,
        /\bvar\s+\w+\s*=/,
        /=>\s*{?/,
        /\bfunction\s+\w+\s*\(/,
        /\bconsole\.log\(/,
        /\brequire\s*\(/,
        /\bexport\s+(default|const|function)/,
    ],

    typescript: [
        /:\s*(string|number|boolean|any|void)\s*[=;)]/,
        /\binterface\s+\w+/,
        /\btype\s+\w+\s*=/,
        /\benum\s+\w+/,
        /<\w+>/,
        /\bas\s+\w+/,
    ],

    java: [
        /\bpublic\s+class\s+\w+/,
        /\bpublic\s+static\s+void\s+main/,
        /\bprivate\s+\w+\s+\w+/,
        /\bSystem\.out\.print/,
        /\bpackage\s+[\w.]+;/,
        /\bimport\s+[\w.]+;/,
    ],

    go: [
        /\bpackage\s+\w+/,
        /\bfunc\s+\w+\s*\(/,
        /\bfunc\s+\(\w+\s+\*?\w+\)/,
        /\bimport\s+\(/,
        /\bfmt\.Print/,
        /:=\s*/,
    ],

    csharp: [
        /\busing\s+\w+;/,
        /\bnamespace\s+\w+/,
        /\bpublic\s+class\s+\w+/,
        /\bConsole\.Write/,
        /\bprivate\s+\w+\s+\w+/,
        /\bpublic\s+static\s+void\s+Main/,
    ],

    cpp: [
        /#include\s+<\w+>/,
        /\bstd::/,
        /\bcout\s*<</,
        /\bcin\s*>>/,
        /\bnamespace\s+\w+/,
        /\btemplate\s*</,
        /\bclass\s+\w+\s*{/,
    ],

    c: [
        /#include\s+<\w+\.h>/,
        /\bint\s+main\s*\(/,
        /\bprintf\s*\(/,
        /\bscanf\s*\(/,
        /\bmalloc\s*\(/,
        /\bstruct\s+\w+/,
    ],
}

/**
 * Detect language from filename extension
 */
export function detectLanguageFromFilename(filename: string): SupportedLanguage | null {
    if (!filename) return null

    const parts = filename.split('.')
    if (parts.length < 2) return null

    const extension = parts[parts.length - 1].toLowerCase()
    return extensionMap[extension] || null
}

/**
 * Detect language from code syntax patterns
 */
export function detectLanguageFromCode(code: string): SupportedLanguage | null {
    if (!code || code.trim().length < 10) return null

    const scores: Record<SupportedLanguage, number> = {
        javascript: 0,
        typescript: 0,
        python: 0,
        java: 0,
        go: 0,
        csharp: 0,
        cpp: 0,
        c: 0,
    }

    // Count pattern matches for each language
    for (const [lang, patterns] of Object.entries(syntaxPatterns)) {
        for (const pattern of patterns) {
            if (pattern.test(code)) {
                scores[lang as SupportedLanguage]++
            }
        }
    }

    // Find language with highest score
    let maxScore = 0
    let detectedLang: SupportedLanguage | null = null

    for (const [lang, score] of Object.entries(scores)) {
        if (score > maxScore) {
            maxScore = score
            detectedLang = lang as SupportedLanguage
        }
    }

    // Only return if we have at least 2 pattern matches (confidence threshold)
    return maxScore >= 2 ? detectedLang : null
}

/**
 * Auto-detect language from both filename and code
 * Filename takes priority over code analysis
 */
export function autoDetectLanguage(code: string, filename: string): SupportedLanguage | null {
    // First try filename extension (most reliable)
    const langFromFilename = detectLanguageFromFilename(filename)
    if (langFromFilename) return langFromFilename

    // Fallback to code syntax analysis
    return detectLanguageFromCode(code)
}
