import google.generativeai as genai
import logging
import re
from app.config import settings
from app.utils.prompt_builder import build_flowchart_prompt

logger = logging.getLogger(__name__)
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def sanitize_mermaid_node_ids(mermaid_code: str) -> str:
    """
    Sanitize Mermaid node IDs to remove underscores and hyphens.
    Converts snake_case and kebab-case to camelCase.
    """
    def to_camel_case(text):
        """Convert snake_case or kebab-case to camelCase"""
        parts = re.split(r'[_\-]+', text)
        if len(parts) <= 1:
            return text
        # First part stays lowercase, rest are capitalized
        return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:] if word)
    
    # Replace node IDs that contain underscores or hyphens
    # Match word boundaries followed by alphanumeric with underscores/hyphens
    def replace_node_id(match):
        node_id = match.group(0)
        return to_camel_case(node_id)
    
    # Pattern to match node IDs (alphanumeric with underscores/hyphens)
    # Only replace if it contains underscore or hyphen
    lines = []
    for line in mermaid_code.split('\n'):
        if line.strip().startswith(('flowchart', 'graph')):
            lines.append(line)
            continue
        
        # Replace identifiers containing underscores or hyphens
        line = re.sub(r'\b[A-Za-z][A-Za-z0-9]*(?:[_\-][A-Za-z0-9]+)+\b', replace_node_id, line)
        lines.append(line)
    
    return '\n'.join(lines)

async def generate_flowchart(code_content: str, language: str) -> dict:
    """Generate Mermaid flowchart from code"""
    
    prompt = build_flowchart_prompt(code=code_content, language=language)
    
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Log the raw response for debugging
        logger.info(f"Raw AI response (first 200 chars): {raw_text[:200]}")
        
        # Aggressive cleaning of markdown code blocks
        mermaid_code = raw_text
        
        # Remove ```mermaid and ``` patterns
        import re
        # Remove opening ```mermaid (case insensitive)
        mermaid_code = re.sub(r'^```\s*mermaid\s*\n?', '', mermaid_code, flags=re.IGNORECASE | re.MULTILINE)
        # Remove closing ```
        mermaid_code = re.sub(r'\n?```\s*$', '', mermaid_code, flags=re.MULTILINE)
        # Remove any standalone ``` lines
        mermaid_code = re.sub(r'^```\s*$', '', mermaid_code, flags=re.MULTILINE)
        # Remove inline backticks at start/end of lines
        mermaid_code = re.sub(r'^`+|`+$', '', mermaid_code, flags=re.MULTILINE)
        
        # Clean up whitespace
        mermaid_code = mermaid_code.strip()
        
        logger.info(f"Cleaned mermaid code (first 200 chars): {mermaid_code[:200]}")
        
        # Ensure it starts with a valid mermaid diagram type
        valid_types = ["flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram", "erDiagram", "gantt", "pie", "journey", "gitGraph", "C4Context"]
        
        def starts_with_valid_type(code):
            return any(code.startswith(t) for t in valid_types)

        if not starts_with_valid_type(mermaid_code):
            # Try to extract diagram definition from the response
            lines = mermaid_code.split("\n")
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if any(line_stripped.startswith(t) for t in valid_types):
                    mermaid_code = "\n".join(lines[i:])
                    break
        
        # Final validation
        if not starts_with_valid_type(mermaid_code):
            return {
                "error": "Invalid flowchart format generated",
                "mermaid": "flowchart TD\n    A[Error] --> B[Invalid flowchart format]"
            }
        
        # Sanitize node IDs to remove underscores and hyphens
        mermaid_code = sanitize_mermaid_node_ids(mermaid_code)
        logger.info(f"Sanitized mermaid code (first 200 chars): {mermaid_code[:200]}")
        
        return {
            "mermaid": mermaid_code,
            "language": language
        }
    except Exception as e:
        return {
            "error": str(e),
            "mermaid": "flowchart TD\n    A[Error] --> B[Failed to generate flowchart]"
        }
