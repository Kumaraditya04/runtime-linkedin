import os
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database.database import get_db
from app.core.responses import StandardResponse, success_response
from app.crawler.browser_manager import BrowserManager
from app.scheduler.scheduler import scheduler

router = APIRouter()

@router.get("/health", response_model=StandardResponse[dict])
async def health_check(db: AsyncSession = Depends(get_db)):
    # 1. Database Check
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    # 2. Scheduler Check
    scheduler_ok = scheduler.running if scheduler else False

    # 3. Playwright & Chromium Environment Check
    env_diag = await BrowserManager.check_environment()
    playwright_ok = env_diag.get("playwright_installed", False)
    chromium_ok = env_diag.get("chromium_installed", False)

    health_status = {
        "database": db_ok,
        "scheduler": scheduler_ok,
        "playwright": playwright_ok,
        "chromium": chromium_ok,
        "version": "1.0.0",
        "environment": os.environ.get("RENDER_SERVICE_ID") and "render" or "local",
        "diagnostics": env_diag.get("message", "All systems operational")
    }

    message = "Service is operational" if (db_ok and chromium_ok) else "Service health degraded: missing dependencies"
    return success_response(message=message, data=health_status)

@router.get("/version", response_model=StandardResponse[dict])
async def get_version():
    return success_response(
        message="Version information", 
        data={"version": "1.0.0"}
    )

@router.get("/ping", response_model=StandardResponse[dict])
async def ping():
    return success_response(
        message="Pong", 
        data={"ping": "pong"}
    )
