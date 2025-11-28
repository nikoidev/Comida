from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import time
from slowapi.errors import RateLimitExceeded

from .core.database import engine, Base
from .core.logging import app_logger, log_request
from .core.rate_limiting import limiter, rate_limit_exceeded_handler
from .core.exceptions import (
    BaseAPIException,
    base_api_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from .api.routes import auth, users, roles, permissions, audit_logs, profile
from .api.routes import restaurants, categories, menu_items, ingredients

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Comida - Food Business CMS API",
    description="Complete CMS for food businesses with menu management, user authentication, and RBAC",
    version="3.0.0"
)

# Add rate limiter state
app.state.limiter = limiter

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = (time.time() - start_time) * 1000  # Convert to milliseconds
    log_request(
        method=request.method,
        path=str(request.url.path),
        status_code=response.status_code,
        duration=duration
    )
    
    return response


# Exception handlers
app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Create uploads directory if it doesn't exist
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["Permissions"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])

# CMS routers
app.include_router(restaurants.router, prefix="/api/restaurants", tags=["Restaurants"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(menu_items.router, prefix="/api/menu-items", tags=["Menu Items"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["Ingredients"])


@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    app_logger.info("🚀 User Management System API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    app_logger.info("🛑 User Management System API shutting down")


@app.get("/")
def root():
    return {
        "message": "User Management System API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }

