import re
from textwrap import dedent


def clean_code(code: str) -> str:
    """Normalize code before sending it to the LLM."""

    if not code:
        return ""

    # Remove common prompt artifacts
    cleaned = dedent(code)
    cleaned = cleaned.replace("\r\n", "\n")

    # Trim repeated blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()

