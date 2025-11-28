"""
Unified AI client with Hugging Face primary and Gemini fallback.
"""
import logging
from typing import Optional
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


async def generate_with_fallback(prompt: str, max_tokens: int = 2000) -> str:
    """
    Generate AI response with Hugging Face primary and Gemini fallback.
    
    Args:
        prompt: The prompt to send to the AI
        max_tokens: Maximum tokens in response
        
    Returns:
        Generated text response
        
    Raises:
        Exception: If both providers fail
    """
    # Try Hugging Face first
    if settings.HUGGINGFACE_API_KEY:
        try:
            logger.info("Attempting generation with Hugging Face...")
            messages = [{"role": "user", "content": prompt}]
            response = huggingface_client.chat_completion(messages, max_tokens=max_tokens)
            result = response.choices[0].message.content.strip()
            logger.info("✅ Successfully generated with Hugging Face")
            return result
        except Exception as e:
            logger.warning(f"⚠️ Hugging Face failed: {str(e)}")
            logger.info("Falling back to Gemini...")
    
    # Fallback to Gemini
    if settings.GEMINI_API_KEY:
        try:
            logger.info("Attempting generation with Gemini...")
            response = gemini_model.generate_content(prompt)
            result = response.text.strip()
            logger.info("✅ Successfully generated with Gemini (fallback)")
            return result
        except Exception as e:
            logger.error(f"❌ Gemini also failed: {str(e)}")
            raise Exception(f"Both AI providers failed. HF: {str(e)}")
    
    raise Exception("No AI provider configured. Please set HUGGINGFACE_API_KEY or GEMINI_API_KEY")
