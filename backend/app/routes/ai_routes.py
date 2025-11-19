from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.documentation import generate_documentation
from app.core.explain_code import explain_code
from app.core.unit_tests import generate_unit_tests
from app.core.optimize import optimize_code
from app.core.flowchart import generate_flowchart
from app.routes.auth_routes import get_current_user
from app.utils.code_cleaner import clean_code
from app.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/ai", tags=["ai"])
rate_limiter = RateLimiter()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"
    file_name: str = "code"

@router.post("/documentation")
async def get_documentation(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Generate code documentation"""
    
    # Check rate limit
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    result = await generate_documentation(
        cleaned_code,
        request.language,
        request.file_name
    )
    return result

@router.post("/explain")
async def explain(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Explain code line by line"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    result = await explain_code(cleaned_code, request.language)
    return result

@router.post("/tests")
async def generate_tests(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Generate unit tests"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    result = await generate_unit_tests(cleaned_code, request.language)
    return result

@router.post("/optimize")
async def optimize(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Optimize code"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    result = await optimize_code(cleaned_code, request.language)
    return result

@router.post("/flowchart")
async def flowchart(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Generate flowchart"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    result = await generate_flowchart(cleaned_code, request.language)
    return result
