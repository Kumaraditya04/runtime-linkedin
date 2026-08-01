# Backend Overview

FastAPI backend providing REST APIs, Playwright automation, and background workers.

## Folder Structure

### app/api/v1
All route handlers. Grouped by access level (`admin/`, `internal/`, `public/`).
- `internal/health.py`: Diagnostics endpoint testing Database, APScheduler, Playwright, and Chromium executable status.

### app/crawler
Playwright-based crawler framework.
- `browser_manager.py`: Controls Chrome headless context, environment verification (`check_environment()`), and `DeploymentConfigurationError` exception handling.
- `base.py`: The `BaseCrawler` blueprint.
- `linkedin.py`: Specific LinkedIn extraction subclass with stealth User-Agent and navigator masks.
- `parser.py`: HTML to dictionary data normalizer.

### app/scheduler
Background jobs via APScheduler.
- `scheduler.py`: The `SchedulerService` running inside FastAPI lifespan, handling rate limits and graceful failure resilience.

### app/core/exceptions.py
Custom exception hierarchy including `DeploymentConfigurationError`.

### app/models
SQLAlchemy 2.0 ORM base classes and entities, including `JobErrorCategory.ENVIRONMENT`.

### app/repositories
Generic CRUD wrapper (`base.py`) utilizing async database sessions.

### app/schemas
Pydantic v2 schemas used for request/response validation.

### app/services
Business logic, mediating between APIs, the database, and the crawler.
