from typing import List
from app.utils.ai_client import generate_with_fallback
from app.utils.prompt_builder import build_explain_prompt

async def explain_code(code_content: str, language: str) -> dict:
    """Generate line-by-line explanation of code"""
    
    prompt = build_explain_prompt(code=code_content, language=language)
    
    try:
        response_text = await generate_with_fallback(prompt)
        
        # Parse response into line explanations
        lines = code_content.split("\n")
        explanations = []
        
        for i, line in enumerate(lines, 1):
            if line.strip():
                explanations.append({
                    "line_no": i,
                    "code": line,
                    "explanation": "See full response for details"
                })
        
        return {
            "explanations": explanations,
            "full_explanation": response_text,
            "line_count": len(lines)
        }
    except Exception as e:
        return {"error": str(e), "explanations": []}
