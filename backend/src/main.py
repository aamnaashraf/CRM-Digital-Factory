"""
FastAPI Application
Main application setup with routes and middleware
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
try:
    from prometheus_client import make_asgi_app
except ImportError:
    # Prometheus client not available in simplified version
    make_asgi_app = None
import logging
import time
import asyncio
from typing import Optional

# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings
from src.database.connection import init_database, get_db_manager
from src.api import webhooks, support, health, dashboard, settings as settings_router
from src.api.reports import router as reports_router
from src.tasks.email_polling_task import GmailPollingTask
from src.scheduler.report_scheduler import daily_report_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


# Global variables to hold tasks
gmail_polling_task: Optional[GmailPollingTask] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    global gmail_polling_task
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")

    # Initialize database
    init_database(
        settings.database_url,
        settings.database_pool_size,
        settings.database_max_overflow
    )

    # Create tables if in development
    if settings.is_development:
        db = get_db_manager()
        await db.create_tables()
        logger.info("Database tables created")

    # Health check
    db = get_db_manager()
    if await db.health_check():
        logger.info("Database connection verified")
    else:
        logger.error("Database connection failed!")

    # Start Gmail polling if enabled
    if settings.enable_email_polling:
        logger.info("Starting Gmail polling task...")
        gmail_polling_task = GmailPollingTask()

        # Start the polling task in the background
        asyncio.create_task(gmail_polling_task.start_polling())
        logger.info(f"Gmail polling started with interval: {gmail_polling_task.poll_interval}s")

    # Start daily report scheduler
    try:
        logger.info("Starting daily report scheduler...")
        await daily_report_scheduler.start()
        logger.info("Daily report scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start daily report scheduler: {e}", exc_info=True)

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down application")

    # Stop the polling task if it exists
    if gmail_polling_task:
        logger.info("Stopping Gmail polling task...")
        await gmail_polling_task.stop_polling()

    # Stop the daily report scheduler
    try:
        logger.info("Stopping daily report scheduler...")
        await daily_report_scheduler.stop()
        logger.info("Daily report scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping daily report scheduler: {e}", exc_info=True)

    db = get_db_manager()
    await db.close()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="24/7 AI Customer Success Agent for TaskFlow",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)


# Middleware
# Allow frontend origins
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://frontend-rust-gamma-56.vercel.app",
    "https://frontend-lt98wd90v-aamna-ashraf-rajputs-projects.vercel.app",
    "https://frontend-ky8woqwrh-aamna-ashraf-rajputs-projects.vercel.app",
]

# In development, allow all origins
if settings.is_development:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.is_development else "An error occurred"
        }
    )


# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(support.router, prefix="/api/support", tags=["Support"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(settings_router.router, prefix="/api/settings", tags=["Settings"])
app.include_router(reports_router, prefix="/api", tags=["Reports"])


# Prometheus metrics endpoint
if settings.enable_metrics and make_asgi_app is not None:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers if settings.is_production else 1,
        reload=settings.is_development,
        log_level=settings.log_level.lower()
    )
