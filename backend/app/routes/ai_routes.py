import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import get_db
from app.core.documentation import generate_documentation
from app.core.explain_code import explain_code
from app.core.unit_tests import generate_unit_tests
from app.core.optimize import optimize_code
from app.core.flowchart import generate_flowchart
from app.routes.auth_routes import get_current_user
from app.utils.code_cleaner import clean_code
from app.utils.rate_limiter import RateLimiter
from app.utils.ai_cache import AICache
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
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Generate code documentation"""
    
    # Check rate limit
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, "documentation")
    if cached:
        return cached
        
    result = await generate_documentation(
        cleaned_code,
        request.language,
        request.file_name
    )
    
    # Cache result if successful
    if result and "error" not in result:
        await ai_cache.set_cached_response(cleaned_code, request.language, "documentation", result)
        
    return result

@router.post("/explain")
async def explain(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Explain code line by line"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, "explain")
    if cached:
        return cached
        
    result = await explain_code(cleaned_code, request.language)
    
    # Cache result if successful
    if result and "error" not in result:
        await ai_cache.set_cached_response(cleaned_code, request.language, "explain", result)
        
    return result

@router.post("/tests")
async def generate_tests(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Generate unit tests"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, "tests")
    if cached:
        return cached
        
    result = await generate_unit_tests(cleaned_code, request.language)
    
    # Cache result if successful
    if result and "error" not in result:
        await ai_cache.set_cached_response(cleaned_code, request.language, "tests", result)
        
    return result

@router.post("/optimize")
async def optimize(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Optimize code"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, "optimize")
    if cached:
        return cached
        
    result = await optimize_code(cleaned_code, request.language)
    
    # Cache result if successful
    if result and "error" not in result:
        await ai_cache.set_cached_response(cleaned_code, request.language, "optimize", result)
        
    return result

@router.post("/flowchart")
async def flowchart(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Generate flowchart"""
    
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, "flowchart")
    if cached:
        return cached
        
    result = await generate_flowchart(cleaned_code, request.language)
    
    # Cache result if successful
    if result and "error" not in result:
        await ai_cache.set_cached_response(cleaned_code, request.language, "flowchart", result)
        
    return result

# ============================================================================
# STREAMING HELPER & ENDPOINTS
# ============================================================================

async def handle_streaming_endpoint(
    request: CodeRequest,
    current_user,
    db: AsyncIOMotorDatabase,
    prompt: str,
    analysis_type: str,
    response_key: str
):
    # Check rate limit
    if not await rate_limiter.check_limit(current_user["user_id"]):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    cleaned_code = clean_code(request.code)
    ai_cache = AICache(db)
    
    # Check cache
    cached = await ai_cache.get_cached_response(cleaned_code, request.language, analysis_type)
    if cached:
        text = cached.get(response_key, "")
        async def cached_generator():
            # Yield text in chunks to simulate streaming
            chunk_size = 50
            for i in range(0, len(text), chunk_size):
                yield text[i:i + chunk_size]
                
        return StreamingResponse(
            stream_to_sse(cached_generator()),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    # Cache miss: run generator, collect stream, then write to cache
    full_text = []
    async def intercepting_generator():
        generator = generate_stream_with_fallback(prompt)
        async for chunk in generator:
            full_text.append(chunk)
            yield chunk
            
    async def event_generator():
        try:
            async for event in stream_to_sse(intercepting_generator()):
                yield event
                
            # Stream completed successfully, aggregate and cache
            combined_text = "".join(full_text)
            if combined_text:
                if analysis_type == "documentation":
                    result_data = {
                        "markdown": combined_text,
                        "tokens_used": len(combined_text) // 4,
                        "duration_seconds": 0.0,
                        "language": request.language
                    }
                elif analysis_type == "explain":
                    lines = cleaned_code.split("\n")
                    explanations = [{"line_no": i, "code": line, "explanation": "See full response for details"} for i, line in enumerate(lines, 1) if line.strip()]
                    result_data = {
                        "full_explanation": combined_text,
                        "explanations": explanations,
                        "line_count": len(lines),
                        "language": request.language
                    }
                elif analysis_type == "tests":
                    result_data = {
                        "test_source": combined_text,
                        "language": request.language,
                        "notes": "Generated tests cover main functions and edge cases"
                    }
                elif analysis_type == "optimize":
                    result_data = {
                        "refactored_code": combined_text,
                        "language": request.language,
                        "notes": "Review suggestions and apply selectively"
                    }
                elif analysis_type == "flowchart":
                    import re
                    mermaid_code = re.sub(r'^```\s*mermaid\s*\n?', '', combined_text, flags=re.IGNORECASE | re.MULTILINE)
                    mermaid_code = re.sub(r'\n?```\s*$', '', mermaid_code, flags=re.MULTILINE)
                    mermaid_code = re.sub(r'^```\s*$', '', mermaid_code, flags=re.MULTILINE)
                    mermaid_code = re.sub(r'^`+|`+$', '', mermaid_code, flags=re.MULTILINE).strip()
                    result_data = {
                        "mermaid": mermaid_code,
                        "language": request.language
                    }
                else:
                    result_data = {
                        response_key: combined_text,
                        "language": request.language
                    }
                    
                await ai_cache.set_cached_response(cleaned_code, request.language, analysis_type, result_data)
        except Exception as e:
            pass
            
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# ============================================================================
# STREAMING ENDPOINTS (New - Real-time SSE)
# ============================================================================

@router.post("/documentation/stream")
async def stream_documentation(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Stream documentation generation in real-time"""
    cleaned_code = clean_code(request.code)
    prompt = build_doc_prompt(
        code=cleaned_code,
        language=request.language,
        file_name=request.file_name
    )
    return await handle_streaming_endpoint(
        request=request,
        current_user=current_user,
        db=db,
        prompt=prompt,
        analysis_type="documentation",
        response_key="markdown"
    )

@router.post("/explain/stream")
async def stream_explain(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Stream code explanation in real-time"""
    cleaned_code = clean_code(request.code)
    prompt = build_explain_prompt(code=cleaned_code, language=request.language)
    return await handle_streaming_endpoint(
        request=request,
        current_user=current_user,
        db=db,
        prompt=prompt,
        analysis_type="explain",
        response_key="full_explanation"
    )

@router.post("/tests/stream")
async def stream_tests(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Stream unit test generation in real-time"""
    cleaned_code = clean_code(request.code)
    prompt = build_test_prompt(code=cleaned_code, language=request.language)
    return await handle_streaming_endpoint(
        request=request,
        current_user=current_user,
        db=db,
        prompt=prompt,
        analysis_type="tests",
        response_key="test_source"
    )

@router.post("/optimize/stream")
async def stream_optimize(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Stream code optimization in real-time"""
    cleaned_code = clean_code(request.code)
    prompt = build_optimize_prompt(code=cleaned_code, language=request.language)
    return await handle_streaming_endpoint(
        request=request,
        current_user=current_user,
        db=db,
        prompt=prompt,
        analysis_type="optimize",
        response_key="refactored_code"
    )

@router.post("/flowchart/stream")
async def stream_flowchart(
    request: CodeRequest,
    current_user = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Stream flowchart generation in real-time"""
    cleaned_code = clean_code(request.code)
    prompt = build_flowchart_prompt(code=cleaned_code, language=request.language)
    return await handle_streaming_endpoint(
        request=request,
        current_user=current_user,
        db=db,
        prompt=prompt,
        analysis_type="flowchart",
        response_key="mermaid"
    )
