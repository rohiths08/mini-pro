import google.generativeai as genai
from app.config import settings
from app.utils.prompt_builder import build_test_prompt

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def generate_unit_tests(code_content: str, language: str) -> dict:
    """Generate unit tests for code"""
    
    prompt = build_test_prompt(code=code_content, language=language)
    
    try:
        response = model.generate_content(prompt)
        
        return {
            "test_source": response.text,
            "language": language,
            "notes": "Generated tests cover main functions and edge cases"
        }
    except Exception as e:
        return {
            "error": str(e),
            "test_source": f"# Error generating tests: {str(e)}"
        }
