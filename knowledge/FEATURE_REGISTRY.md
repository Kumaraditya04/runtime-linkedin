# LeadRadar AI Feature Registry

This registry tracks the status and dependencies of all major features.

## Authentication
- **Status**: Completed
- **Version**: 1.1
- **Depends On**: None

---

## Shared Foundations
- **Status**: Completed
- **Version**: 1.1
- **Depends On**: Authentication

---

## Keywords Module
- **Status**: Completed
- **Version**: 1.1
- **Depends On**: Shared Foundations

---

## Crawler & Deployment
- **Status**: Completed
- **Version**: 1.1
- **Depends On**: Keywords
- **Features**: Playwright Chromium automation, `BrowserManager.check_environment()`, `DeploymentConfigurationError`, `GET /api/v1/internal/health` extended diagnostics, `scripts/check_playwright.py` verification, Render build support (`docs/deployment/render.md`).

---

## AI Analysis
- **Status**: Planned
- **Version**: 1.0
- **Depends On**: Crawler

---

## Dashboard
- **Status**: Completed
- **Version**: 1.1
- **Depends On**: Crawler, Keywords
