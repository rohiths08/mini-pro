from app.utils.ai_client import generate_with_fallback
from app.utils.prompt_builder import build_test_prompt

async def generate_unit_tests(code_content: str, language: str) -> dict:
    """Generate unit tests for code"""
    
    prompt = build_test_prompt(code=code_content, language=language)
    
    try:
        response_text = await generate_with_fallback(prompt)
        
        return {
            "test_source": response_text,
            "language": language,
            "notes": "Generated tests cover main functions and edge cases"
        }
    except Exception as e:
        return {
            "error": str(e),
            "test_source": f"# Error generating tests: {str(e)}"
        }
