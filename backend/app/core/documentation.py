import google.generativeai as genai
from typing import Optional
from app.config import settings
from app.utils.prompt_builder import build_doc_prompt
import time

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def generate_documentation(
    code_content: str,
    language: str,
    file_name: str = "code",
    options: dict = None
) -> dict:
    """Generate comprehensive documentation for code"""
    
    if options is None:
        options = {}
    
    include_examples = options.get("include_examples", True)
    include_api = options.get("include_api", True)
    
    start_time = time.time()
    
    prompt = build_doc_prompt(
        code=code_content,
        language=language,
        file_name=file_name,
        include_examples=include_examples,
        include_api=include_api
    )
    
    try:
        response = model.generate_content(prompt)
        duration = time.time() - start_time
        
        return {
            "markdown": response.text,
            "tokens_used": len(response.text) // 4,  # Rough estimate
            "duration_seconds": round(duration, 2),
            "language": language
        }
    except Exception as e:
        return {
            "error": str(e),
            "markdown": f"# Documentation Generation Failed\n\nError: {str(e)}"
        }
