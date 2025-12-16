"""
Streaming AI client for real-time response generation.
Supports Server-Sent Events (SSE) streaming.
"""
import logging
import json
from typing import AsyncGenerator, Optional
import google.generativeai as genai
from huggingface_hub import InferenceClient
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize clients
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

huggingface_client = InferenceClient(
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    token=settings.HUGGINGFACE_API_KEY
)


async def generate_stream_with_fallback(
    prompt: str,
    max_tokens: int = 2000
) -> AsyncGenerator[str, None]:
    """
    Stream AI responses chunk by chunk with fallback support.
    
    Args:
        prompt: The prompt to send to the AI
        max_tokens: Maximum tokens in response
        
    Yields:
        Text chunks as they are generated
        
    Raises:
        Exception: If both providers fail
    """
    
    # Try Gemini first (supports streaming natively)
    if settings.GEMINI_API_KEY:
        try:
            logger.info("🌊 Starting streaming with Gemini...")
            response = gemini_model.generate_content(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                )
            )
            
            for chunk in response:
                if chunk.text:
                    logger.debug(f"📦 Chunk: {len(chunk.text)} chars")
                    yield chunk.text
            
            logger.info("✅ Streaming completed with Gemini")
            return
            
        except Exception as e:
            logger.warning(f"⚠️ Gemini streaming failed: {str(e)}")
            logger.info("Falling back to Hugging Face (non-streaming)...")
    
    # Fallback to Hugging Face (non-streaming, but yield in chunks)
    if settings.HUGGINGFACE_API_KEY:
        try:
            logger.info("Attempting generation with Hugging Face...")
            messages = [{"role": "user", "content": prompt}]
            response = huggingface_client.chat_completion(messages, max_tokens=max_tokens)
            result = response.choices[0].message.content.strip()
            
            # Simulate streaming by yielding in chunks
            chunk_size = 50  # Characters per chunk
            for i in range(0, len(result), chunk_size):
                chunk = result[i:i + chunk_size]
                yield chunk
            
            logger.info("✅ Completed with Hugging Face (simulated streaming)")
            return
            
        except Exception as e:
            logger.error(f"❌ Hugging Face also failed: {str(e)}")
            raise Exception(f"Both AI providers failed. Last error: {str(e)}")
    
    raise Exception("No AI provider configured. Please set GEMINI_API_KEY or HUGGINGFACE_API_KEY")


async def stream_to_sse(
    generator: AsyncGenerator[str, None],
    include_metadata: bool = True
) -> AsyncGenerator[str, None]:
    """
    Convert async generator to Server-Sent Events format.
    
    Args:
        generator: Async generator yielding text chunks
        include_metadata: Whether to include metadata events
        
    Yields:
        SSE-formatted strings
    """
    try:
        if include_metadata:
            # Send start event
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
        
        # Stream chunks
        async for chunk in generator:
            # Escape newlines and special characters for JSON
            event_data = json.dumps({'type': 'chunk', 'content': chunk})
            yield f"data: {event_data}\n\n"
        
        # Send completion event
        if include_metadata:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
    except Exception as e:
        # Send error event
        error_data = json.dumps({'type': 'error', 'message': str(e)})
        yield f"data: {error_data}\n\n"
        logger.error(f"❌ Streaming error: {str(e)}")
