# Backend Overview

FastAPI backend providing REST APIs and background workers.

## Folder Structure

### app/api/v1
All route handlers. Grouped by access level (`admin/`, `internal/`, `public/`).

### app/crawler
Playwright-based crawler framework.
- `browser_manager.py`: Controls Chrome headless context and `storage/` persistence.
- `base.py`: The `BaseCrawler` blueprint.
- `linkedin.py`: Specific LinkedIn extraction subclass.
- `parser.py`: HTML to dictionary data normalizer.

### app/scheduler
Background jobs via APScheduler.
- `scheduler.py`: The `SchedulerService` running inside FastAPI lifespan.

### app/models
SQLAlchemy 2.0 ORM base classes and entities.

### app/repositories
Generic CRUD wrapper (`base.py`) utilizing async database sessions.

### app/schemas
Pydantic v2 schemas used for request/response validation.

### app/services
Business logic, mediating between APIs, the database, and the crawler.
