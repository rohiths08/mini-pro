import os

LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
}

def detect_language(filename: str, content: str = "") -> str:
    """Detect programming language from filename or content"""
    _, ext = os.path.splitext(filename)
    return LANGUAGE_EXTENSIONS.get(ext.lower(), "plaintext")

def is_valid_code_file(filename: str) -> bool:
    """Check if file is a valid code file"""
    _, ext = os.path.splitext(filename)
    return ext.lower() in LANGUAGE_EXTENSIONS
