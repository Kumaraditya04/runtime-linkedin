# Crawler Architecture

LeadRadar uses a generic Crawler Framework designed to easily scale across multiple social platforms.

## Core Components
- `BrowserManager`: Uses Playwright to manage a headless Chromium instance and persists cookies/state per source to `storage/`.
- `BaseCrawler`: Abstract base class enforcing standard workflow (`login`, `search`, `extract`).
- `Parser`: Isolates DOM extraction logic from crawler logic. Returns standardized dictionaries with `raw_payload` retention for traceability.

## Current Implementations
- `LinkedInCrawler`: Basic skeleton for LinkedIn. 

## Scheduler
The `SchedulerService` runs inside the FastAPI lifespan using `APScheduler`. It can be triggered manually via POST to `/api/v1/admin/crawler/run`.
