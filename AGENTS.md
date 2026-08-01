# LeadRadar AI - AI Agent Operating Manual

Welcome to the LeadRadar AI repository. You are an AI agent contributing to this project. This file is your strict operating manual.

## 1. Core Mandate
LeadRadar AI is an AI-powered Sales Intelligence Platform. This codebase must remain modular, clean, and highly maintainable.
You must prioritize long-term maintainability over speed of implementation.

## 2. Before Writing Any Code
You MUST perform the following steps before modifying any code:
1. Read `knowledge/index.md`
2. Read the relevant feature specification in `knowledge/features/`
3. Read this file (`AGENTS.md`)
4. Read `CONVENTIONS.md`
5. Read any applicable rules in the `rules/` directory
6. Never read unrelated files. Only read what is necessary.

## 3. Strict Rules (What NOT to do)
- **NEVER** rewrite unrelated files.
- **NEVER** rename public APIs without explicit user approval.
- **NEVER** duplicate business logic.
- **NEVER** create utility functions that already exist.
- **NEVER** delete code unless explicitly instructed.
- **NEVER** change the database schema without updating documentation (`knowledge/database.md`) and generating Alembic migrations.
- **NEVER** introduce a new dependency unless necessary. Check if functionality exists internally first.
- **PREFER** extending existing modules over creating new ones.

## 4. Feature Implementation Workflow
1. Requirement identified.
2. Knowledge Update (`knowledge/features/`).
3. Database (`models/`).
4. Repository.
5. Service.
6. API.
7. Frontend Service.
8. UI.
9. Verification.
10. Knowledge Update (Progress, TODOs).
11. Changelog (`knowledge/changelog.md`).

## 5. Standard Completion Response
After finishing a feature, output this EXACT format:

```text
Completed

✓ Models
✓ Repository
✓ Service
✓ API
✓ Frontend
✓ Knowledge Base Updated
✓ Changelog Updated

Files Modified
...

Next Suggested Task
...
```

Follow these instructions at all times.
