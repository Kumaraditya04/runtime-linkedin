# LeadRadar AI Changelog

## [1.1.0] - 2026-08-01
### Added
- **Crawler Executions UI**: Added dedicated "Executions" tab to the frontend dashboard for viewing comprehensive crawler job histories.
- **Dynamic Extraction Progress**: Refactored the live extraction progress bar to calculate status dynamically based on the most recent job batch per keyword, rather than hardcoded global aggregates.
- **Render Deployment Support**: Created `docs/deployment/render.md` and verification script `scripts/check_playwright.py`.
- **Runtime Browser Detection**: Added `BrowserManager.check_environment()` diagnostic check and `DeploymentConfigurationError` exception handling.
- **Extended Health Check**: Updated `GET /api/v1/internal/health` to return `database`, `scheduler`, `playwright`, and `chromium` diagnostic metrics.
- **Graceful Error Recovery**: Updated `JobExecution` model with `JobErrorCategory.ENVIRONMENT` and non-blocking scheduler error resilience.
- **Stealth Crawler Upgrades**: Added Mac OS Desktop `User-Agent` headers, desktop viewport, and `navigator.webdriver` masking to `BrowserManager`.
- **IST Localization & Sorting**: Added universal `formatIST()` date helper and default descending lead sorting.
- **Mobile Responsiveness**: Added touch-optimized mobile lead cards view (`md:hidden`) and mobile navigation menu drawer.

## [1.0.0] - 2026-07-31
### Added
- Repository initialization and clean architecture scaffolding.
- AI Operating Manual (`AGENTS.md`, `CONVENTIONS.md`, `knowledge/`).
- Frontend Next.js scaffold with Tailwind and shadcn/ui.
- Backend FastAPI scaffold with SQLite and Alembic.
- Authentication module with JWT, password hashing, and RBAC-ready Admin model.
- Shared Backend Foundation: `BaseModel`, `TimestampMixin`, `AuditMixin`, `BaseRepository`, `BaseService`.
- `SystemSettings` table for dynamic global configuration.
- Internal APIs (`/health`, `/version`, `/ping`).
- Pagination utilities.
- Search and sorting utilities in `app.utils.query_builder`.
- Project bootstrap script (`scripts/bootstrap.py`).
- Updated API routes: `/api/v1/internal/version`, `/api/v1/internal/ping`.

### Sprint 3 (Frontend Framework)
- Updated backend auth to issue `HttpOnly` cookie.
- Configured TanStack React Query, Axios, Zod, React Hook Form, and `next-themes`.
- Installed shadcn/ui components for building the design system.
- Created robust API layer with Axios interceptors (`lib/http.ts`).
- Created reusable AppShell with Sidebar, TopBar, and theme toggling.
- Built reusable generic components (`DataTable`, `ChartCard`, `StatisticCard`).
- Centralized navigation config (`config/navigation.ts`).
- Scaffolded feature directories for scalable module development.
- Added Next.js middleware for route protection based on cookies.
- Added global `loading.tsx`, `error.tsx`, and `not-found.tsx` states.

### Sprint 4 (Keywords Module)
- Created `Keyword` database model with tracking fields and `KeywordStatus` Enum.
- Created `JobExecution` database model for future crawler runs.
- Configured Alembic to support Async migrations with `aiosqlite`.
- Built backend `KeywordRepository` and `KeywordService` with pagination.
- Built backend API routes under `/api/v1/admin/keywords` (CRUD, pause, resume, test).
- Built backend dashboard stats API under `/api/v1/admin/dashboard/stats`.
- Built frontend `features/keywords` module (schemas, types, hooks, API wrappers).
- Built frontend Keyword Form, DataTable columns, and pages (List, New, Edit).
- Integrated live backend statistics into the frontend Dashboard layout.

### Sprint 5 (Crawler Framework)
- Abstracted crawler architecture into `BaseCrawler`, `LeadParser`, and `BrowserManager` using Playwright.
- Implemented `LinkedInCrawler` skeleton.
- Created `Lead` database model with `raw_payload` retention for future AI extraction tuning.
- Expanded `JobExecution` model with `records_saved`, `records_skipped`, and `retry_count`.
- Wired `APScheduler` into FastAPI lifespan for background jobs.
- Implemented crawler, jobs, and leads APIs.
- Built frontend `features/leads` and `features/jobs` modules.
- Upgraded Dashboard UI to show active Jobs panel and Manual Crawl trigger.
