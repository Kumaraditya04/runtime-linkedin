# Crawler Architecture

LeadRadar uses a generic Crawler Framework designed to easily scale across multiple social platforms.

## Core Components
- `BrowserManager`: Uses Playwright to manage a headless Chromium instance, verifies runtime environment (`check_environment()`), raises `DeploymentConfigurationError` if browser binaries are missing, and persists cookies/state to `storage/`.
- `BaseCrawler`: Abstract base class enforcing standard workflow (`login`, `search`, `extract`).
- `Parser`: Isolates DOM extraction logic from crawler logic. Returns standardized dictionaries with `raw_payload` retention for traceability.

## Current Implementations
- `LinkedInCrawler`: LinkedIn content search crawler featuring smooth scrolling, stealth User-Agent headers, `navigator.webdriver` masking, and exact post link copying via control menus.

## Scheduler & Environment Failure Resilience
The `SchedulerService` runs inside the FastAPI lifespan using `APScheduler`. If an environment error (`DeploymentConfigurationError`) occurs:
- The `JobExecution` is recorded as `FAILED` with `error_category = ENVIRONMENT`.
- The scheduler logs the error cleanly, preserves uptime, and continues with the next scheduled keyword without crashing.
