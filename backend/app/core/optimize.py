from app.utils.ai_client import generate_with_fallback
from app.utils.prompt_builder import build_optimize_prompt

async def optimize_code(code_content: str, language: str) -> dict:
    """Generate optimization suggestions for code"""
    
    prompt = build_optimize_prompt(code=code_content, language=language)
    
    try:
        response_text = await generate_with_fallback(prompt)
        
        return {
            "refactored_code": response_text,
            "language": language,
            "notes": "Review suggestions and apply selectively"
        }
    except Exception as e:
        return {
            "error": str(e),
            "refactored_code": code_content,
            "suggestions": []
        }
