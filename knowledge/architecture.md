# Architecture Overview

LeadRadar AI is a monolithic application designed with a clear separation of concerns, built using a modern Python/Next.js stack.

## Tech Stack
### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite (Async via `aiosqlite`), SQLAlchemy 2.0 ORM, Alembic for migrations
- **Scheduler**: APScheduler (AsyncIOScheduler) running in the FastAPI lifespan
- **Crawler**: Playwright for headless browser automation
- **Parsing**: BeautifulSoup4/lxml

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **State Management**: React Query
- **Styling**: Tailwind CSS + Shadcn UI
- **Routing**: Protected routes via Next.js middleware using HttpOnly cookies

## Core Modules
### 1. Crawler Framework
- **BrowserManager**: Headless Playwright orchestration (Cookie persistence via `storage/`).
- **SchedulerService**: Uses APScheduler wired to the FastAPI lifespan.
- **BaseCrawler**: Abstract layer orchestrating (`login`, `search`, `extract`).
- **Parser**: Isolates scraping logic.

### 2. Lead Management
- Retains `raw_payload` from crawlers to enable future AI re-processing.
- Status workflow: `NEW` -> `REVIEWED` -> `CONTACTED`.

### 3. Keyword Tracking
- Defines what the crawlers search for. Includes pause/resume mechanics and live stats.
