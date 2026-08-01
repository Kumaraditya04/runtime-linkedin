# Render Deployment Guide - LeadRadar AI

This guide documents how to deploy LeadRadar AI to **Render Free Tier** with persistent Playwright Chromium browser support.

---

## 1. Required Build Command

We have provided a dedicated build script that ensures the Playwright browser is installed inside your project environment so that it persists to the Render runtime.

In your Render Dashboard Web Service settings:

- **Build Command**:
  ```bash
  ./render-build.sh
  ```

*(If you prefer to enter the command manually, it is: `pip install -r requirements.txt && export PLAYWRIGHT_BROWSERS_PATH=0 && playwright install chromium`)*

---

## 2. Required Start Command

- **Start Command**:
  ```bash
  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

---

## 3. Environment Variables

Set the following environment variables in **Render Dashboard $\rightarrow$ Environment**:

| Variable | Recommended Value / Description |
| :--- | :--- |
| `LINKEDIN_LI_AT` | `AQED...` *(LinkedIn Session Cookie)* |
| `SECRET_KEY` | `your_secure_jwt_secret_key` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./leadradar.db` *(or PostgreSQL)* |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `43200` *(30 Days)* |

---

## 4. Render Free Tier Considerations

- **Ephemeral Storage**: Render free tier instances use ephemeral storage. Storage state and HTML snapshots are saved in `./storage/`.
- **Pre-Installed Chromium**: Playwright Chromium browsers must be installed during the **Build Command** phase so browser binaries exist before Uvicorn starts.
- **Stealth & Headless Flags**: The browser manager automatically uses `--no-sandbox`, `--disable-dev-shm-usage`, and desktop `User-Agent` headers to operate cleanly within Linux container memory limits.

---

## 5. Environment Health Verification

To verify that Playwright and Chromium are operational on your live service:

```bash
GET /api/v1/internal/health
```

Expected Response:
```json
{
  "success": true,
  "message": "Service is operational",
  "data": {
    "database": true,
    "scheduler": true,
    "playwright": true,
    "chromium": true,
    "version": "1.0.0",
    "environment": "render",
    "diagnostics": "Environment operational and Chromium browser is ready."
  }
}
```
