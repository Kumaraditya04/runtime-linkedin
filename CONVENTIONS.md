# Project Conventions

This document dictates all naming conventions and structural rules for LeadRadar AI. AI agents must follow these strictly.

## 1. Naming Conventions

### Python (Backend)
- **Files/Folders**: `snake_case` (e.g., `user_service.py`)
- **Classes**: `PascalCase` (e.g., `UserService`)
- **Functions/Methods**: `snake_case` (e.g., `get_user_by_id`)
- **Variables**: `snake_case` (e.g., `user_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **SQLAlchemy Models**: Singular `PascalCase` (e.g., `User`, not `Users`)
- **Pydantic Schemas**: Suffix with intent (e.g., `UserCreate`, `UserResponse`)
- **Repositories**: Suffix with `Repository` (e.g., `UserRepository`)
- **Services**: Suffix with `Service` (e.g., `UserService`)

### TypeScript (Frontend)
- **Files/Folders**: `kebab-case` (e.g., `user-profile.tsx`)
- **React Components**: `PascalCase` (e.g., `UserProfile`)
- **Interfaces/Types**: `PascalCase` (e.g., `UserResponse`)
- **Functions/Variables**: `camelCase` (e.g., `fetchUser`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
- **Services**: Prefix with api (e.g., `api/users.ts`)

## 2. API Conventions
- **Base URL**: `/api/v1`
- **Paths**: Plural `kebab-case` nouns (e.g., `/api/v1/users`, `/api/v1/keywords`)
- **Standardized Response format**:
```json
{
  "success": true,
  "message": "Human readable message",
  "data": {},
  "meta": {}
}
```
- **Error Response format**:
```json
{
  "success": false,
  "message": "Error description",
  "errors": []
}
```

## 3. Environment Variables
- Centralized in `backend/app/config.py` using `pydantic-settings`.
- Do NOT access `os.getenv()` randomly in the codebase. Always inject config.

## 4. Logging Format
- Use structured JSON logging for major events.
- Minimum fields: `timestamp`, `level`, `module`, `message`.
- Add contextual fields where necessary (e.g., `keyword_id`, `run_time`).

## 5. Git Commit Style
Use Conventional Commits:
- `feat:` (New feature)
- `fix:` (Bug fix)
- `docs:` (Documentation changes)
- `style:` (Formatting, missing semi colons, etc; no code change)
- `refactor:` (Refactoring production code)
- `test:` (Adding tests, refactoring test; no production code change)
- `chore:` (Updating build tasks, package manager configs, etc; no production code change)
