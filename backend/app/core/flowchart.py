import google.generativeai as genai
import logging
from app.config import settings
from app.utils.prompt_builder import build_flowchart_prompt

logger = logging.getLogger(__name__)
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

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
        
        # Ensure it starts with flowchart or graph
        if not (mermaid_code.startswith("flowchart") or mermaid_code.startswith("graph")):
            # Try to extract flowchart definition from the response
            lines = mermaid_code.split("\n")
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if line_stripped.startswith("flowchart") or line_stripped.startswith("graph"):
                    mermaid_code = "\n".join(lines[i:])
                    break
        
        # Final validation - if still doesn't start correctly, wrap it
        if not (mermaid_code.startswith("flowchart") or mermaid_code.startswith("graph")):
            return {
                "error": "Invalid flowchart format generated",
                "mermaid": "flowchart TD\n    A[Error] --> B[Invalid flowchart format]"
            }
        
        return {
            "mermaid": mermaid_code,
            "language": language
        }
    except Exception as e:
        return {
            "error": str(e),
            "mermaid": "flowchart TD\n    A[Error] --> B[Failed to generate flowchart]"
        }
