from huggingface_hub import InferenceClient
import logging
import re
from app.config import settings
from app.utils.prompt_builder import build_flowchart_prompt

logger = logging.getLogger(__name__)

# Initialize Hugging Face client
# Using Qwen2.5-Coder-32B-Instruct which is excellent for code tasks
client = InferenceClient(
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    token=settings.HUGGINGFACE_API_KEY
)

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
    
    try:
        if not settings.HUGGINGFACE_API_KEY:
            logger.warning("HUGGINGFACE_API_KEY not set. Flowchart generation may fail.")
            
        prompt = build_flowchart_prompt(code=code_content, language=language)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Call Hugging Face Inference API
        response = client.chat_completion(messages, max_tokens=2000)
        raw_text = response.choices[0].message.content.strip()
        
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
        
        # Fix unquoted labels containing special characters
        def fix_unquoted_labels(code: str) -> str:
            """Fix labels that contain special characters but aren't quoted."""
            lines = []
            for line in code.split('\n'):
                # Skip flowchart/graph declaration lines
                if line.strip().startswith(('flowchart', 'graph')):
                    lines.append(line)
                    continue
                
                # Pattern to match node definitions with square brackets or curly braces
                # Look for patterns like: nodeId[text with (parens) or /slashes or "quotes"]
                # that aren't already wrapped in quotes
                
                # Fix square bracket labels [text] that contain special chars but no quotes
                def fix_bracket_label(match):
                    full = match.group(0)  # e.g., "nodeId[Call factorial(5)]"
                    node_id = match.group(1)  # e.g., "nodeId"
                    label = match.group(2)  # e.g., "Call factorial(5)"
                    
                    # Check if label contains special characters and isn't already quoted
                    if not (label.startswith('"') and label.endswith('"')):
                        # Check for special characters that need quoting
                        special_chars = ['(', ')', '[', ']', '{', '}', '/', '"', "'", '\\', '<', '>', '=', '*', '-']
                        if any(char in label for char in special_chars):
                            # Escape any existing quotes in the label
                            escaped_label = label.replace('"', '\\"')
                            return f'{node_id}["{escaped_label}"]'
                    return full
                
                # Fix curly brace labels {{text}} that contain special chars but no quotes
                def fix_curly_label(match):
                    full = match.group(0)  # e.g., "nodeId{{n === 0?}}"
                    node_id = match.group(1)  # e.g., "nodeId"
                    label = match.group(2)  # e.g., "n === 0?"
                    
                    # Check if label contains special characters and isn't already quoted
                    if not (label.startswith('"') and label.endswith('"')):
                        special_chars = ['(', ')', '[', ']', '{', '}', '/', '"', "'", '\\', '<', '>', '=', '*']
                        if any(char in label for char in special_chars):
                            escaped_label = label.replace('"', '\\"')
                            return f'{node_id}{{{{{escaped_label}}}}}'
                    return full
                
                # Apply fixes - match node definitions with square brackets
                line = re.sub(r'(\w+)\[([^\]]+)\]', fix_bracket_label, line)
                # Apply fixes - match node definitions with double curly braces
                line = re.sub(r'(\w+)\{\{([^}]+)\}\}', fix_curly_label, line)
                
                lines.append(line)
            
            return '\n'.join(lines)
        
        mermaid_code = fix_unquoted_labels(mermaid_code)
        logger.info(f"Fixed labels (first 200 chars): {mermaid_code[:200]}")
        
        # Sanitize node IDs to remove underscores and hyphens
        mermaid_code = sanitize_mermaid_node_ids(mermaid_code)
        logger.info(f"Sanitized mermaid code (first 200 chars): {mermaid_code[:200]}")
        
        return {
            "mermaid": mermaid_code,
            "language": language
        }
    except Exception as e:
        logger.error(f"Flowchart generation failed: {str(e)}")
        return {
            "error": str(e),
            "mermaid": "flowchart TD\n    A[Error] --> B[Failed to generate flowchart]"
        }
