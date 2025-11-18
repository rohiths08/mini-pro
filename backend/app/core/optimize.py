import google.generativeai as genai
from app.config import settings
from app.utils.prompt_builder import build_optimize_prompt

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def optimize_code(code_content: str, language: str) -> dict:
    """Optimize code for performance and readability"""
    
    prompt = build_optimize_prompt(code=code_content, language=language)
    
    try:
        response = model.generate_content(prompt)
        
        return {
            "refactored_code": response.text,
            "suggestions": [
                "Consider caching repeated operations",
                "Use async/await for I/O operations",
                "Add error handling for edge cases"
            ],
            "estimated_complexity": "O(n)",
            "language": language
        }
    except Exception as e:
        return {
            "error": str(e),
            "refactored_code": code_content,
            "suggestions": []
        }
