from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.config import connect_to_mongo, close_mongo, settings
from app.routes import auth_routes, github_routes, ai_routes, export_routes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown"""
    # Startup
    try:
        await connect_to_mongo()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
    
    yield
    
    # Shutdown
    await close_mongo()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="AI CodeDoc Studio API",
    description="Backend API for AI-powered code documentation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response

# Include routers
app.include_router(auth_routes.router)
app.include_router(github_routes.router)
app.include_router(ai_routes.router)
app.include_router(export_routes.router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI CodeDoc Studio API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
