from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import StructuredLoggingMiddleware
from app.scheduler.scheduler import scheduler_service

# This ensures logging is set up on import
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler_service.start()
    yield
    # Shutdown
    scheduler_service.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Middleware
app.add_middleware(StructuredLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.public import auth
from app.api.v1.internal import health, system_settings
from app.api.v1.admin import keywords, dashboard, crawler, leads, jobs

app.include_router(auth.router, prefix=settings.API_V1_STR + "/public/auth", tags=["auth"])
app.include_router(health.router, prefix=settings.API_V1_STR + "/internal", tags=["internal"])
app.include_router(system_settings.router, prefix=settings.API_V1_STR + "/internal/settings", tags=["internal", "settings"])
app.include_router(keywords.router, prefix=settings.API_V1_STR + "/admin/keywords", tags=["admin", "keywords"])
app.include_router(dashboard.router, prefix=settings.API_V1_STR + "/admin/dashboard", tags=["admin", "dashboard"])
app.include_router(crawler.router, prefix=settings.API_V1_STR + "/admin/crawler", tags=["admin", "crawler"])
app.include_router(leads.router, prefix=settings.API_V1_STR + "/admin/leads", tags=["admin", "leads"])
app.include_router(jobs.router, prefix=settings.API_V1_STR + "/admin/jobs", tags=["admin", "jobs"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
