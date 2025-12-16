from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.documentation import generate_documentation
from app.core.explain_code import explain_code
from app.core.unit_tests import generate_unit_tests
from app.core.optimize import optimize_code
from app.core.flowchart import generate_flowchart
from app.routes.auth_routes import get_current_user
from app.utils.code_cleaner import clean_code
from app.utils.rate_limiter import RateLimiter
from app.utils.streaming_client import generate_stream_with_fallback, stream_to_sse
from app.utils.prompt_builder import (
    build_doc_prompt,
    build_explain_prompt,
    build_test_prompt,
    build_optimize_prompt,
    build_flowchart_prompt
)

router = APIRouter(prefix="/ai", tags=["ai"])
rate_limiter = RateLimiter()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"
    file_name: str = "code"

# ============================================================================
# ORIGINAL ENDPOINTS (Backward Compatible)
# ============================================================================

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

# ============================================================================
# STREAMING ENDPOINTS (New - Real-time SSE)
# ============================================================================

@router.post("/documentation/stream")
async def stream_documentation(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Stream documentation generation in real-time"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    prompt = build_doc_prompt(
        code=cleaned_code,
        language=request.language,
        file_name=request.file_name
    )
    
    async def event_generator():
        generator = generate_stream_with_fallback(prompt)
        async for event in stream_to_sse(generator):
            yield event
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@router.post("/explain/stream")
async def stream_explain(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Stream code explanation in real-time"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    prompt = build_explain_prompt(code=cleaned_code, language=request.language)
    
    async def event_generator():
        generator = generate_stream_with_fallback(prompt)
        async for event in stream_to_sse(generator):
            yield event
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/tests/stream")
async def stream_tests(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Stream unit test generation in real-time"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    prompt = build_test_prompt(code=cleaned_code, language=request.language)
    
    async def event_generator():
        generator = generate_stream_with_fallback(prompt)
        async for event in stream_to_sse(generator):
            yield event
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/optimize/stream")
async def stream_optimize(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Stream code optimization in real-time"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    prompt = build_optimize_prompt(code=cleaned_code, language=request.language)
    
    async def event_generator():
        generator = generate_stream_with_fallback(prompt)
        async for event in stream_to_sse(generator):
            yield event
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/flowchart/stream")
async def stream_flowchart(
    request: CodeRequest,
    current_user = Depends(get_current_user)
):
    """Stream flowchart generation in real-time"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    prompt = build_flowchart_prompt(code=cleaned_code, language=request.language)
    
    async def event_generator():
        generator = generate_stream_with_fallback(prompt)
        async for event in stream_to_sse(generator):
            yield event
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
