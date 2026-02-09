"""
PureAura AI - FastAPI Backend Main Application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

from backend.config import settings
from backend.api.endpoints import users, devices, readings, alerts, predictions, auth
from backend.utils.database import engine, Base, get_db

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Predictive Air Analytics API for Hong Kong Subdivided Units",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])
app.include_router(readings.router, prefix="/api/v1/readings", tags=["Sensor Readings"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["Predictions"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to PureAura AI API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "disabled in production",
        "health": "/health"
    }

@app.get("/health")
async def health_check(db=Depends(get_db)):
    """Health check endpoint"""
    try:
        # Check database connection
        db.execute("SELECT 1")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "healthy",
                "database": "connected",
                "service": "running"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )

@app.get("/api/v1/status")
async def api_status():
    """API status information"""
    return {
        "api": "running",
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=