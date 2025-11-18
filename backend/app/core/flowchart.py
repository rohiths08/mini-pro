import google.generativeai as genai
from app.config import settings
from app.utils.prompt_builder import build_flowchart_prompt

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def generate_flowchart(code_content: str, language: str) -> dict:
    """Generate Mermaid flowchart from code"""
    
    prompt = build_flowchart_prompt(code=code_content, language=language)
    
    try:
        response = model.generate_content(prompt)
        
        return {
            "mermaid": response.text,
            "language": language
        }
    except Exception as e:
        return {
            "error": str(e),
            "mermaid": "graph TD\n  A[Error]\n  B[Failed to generate flowchart]\n  A --> B"
        }
