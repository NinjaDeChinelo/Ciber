"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from config.settings import settings
from config.database import init_db

# Initialize database
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("✅ InstaVideo Studio Backend Starting...")
    yield
    print("❌ InstaVideo Studio Backend Shutting Down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Professional desktop application for video editing",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Routes (Placeholder) ============
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Routes will be imported and included here
# from api.routes import videos, projects, exports, downloads
# app.include_router(videos.router, prefix="/api", tags=["Videos"])
# app.include_router(projects.router, prefix="/api", tags=["Projects"])
# app.include_router(exports.router, prefix="/api", tags=["Exports"])
# app.include_router(downloads.router, prefix="/api", tags=["Downloads"])


def run():
    """Run the FastAPI application"""
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    run()
