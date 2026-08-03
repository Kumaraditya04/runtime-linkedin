import os
import json
import asyncio
import random
import logging
from typing import List, Dict, Any, Optional
from curl_cffi.requests import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession as DBSession

from app.models.keyword import Keyword
from app.models.system_settings import SystemSettings

logger = logging.getLogger(__name__)


class LinkedInVoyagerCrawler:
    """
    Browser-free LinkedIn crawler using the internal Voyager REST API.
    Uses curl_cffi to impersonate Chrome's TLS fingerprint, bypassing LinkedIn's
    bot detection without needing Playwright or Chromium.
    """

    BASE_URL = "https://www.linkedin.com"
    VOYAGER = "https://www.linkedin.com/voyager/api"

    def __init__(self):
        self.source = "linkedin"
        self._session: Optional[AsyncSession] = None
        self._csrf_token: Optional[str] = None

    async def _random_delay(self, min_ms: int = 800, max_ms: int = 2000):
        await asyncio.sleep(random.uniform(min_ms, max_ms) / 1000.0)

    async def _get_setting(self, db: DBSession, key: str, default: int) -> int:
        s = await db.get(SystemSettings, key)
        if s and s.value.isdigit():
            return int(s.value)
        return default

    def _load_saved_cookies(self) -> Dict[str, str]:
        """Read cookies saved by Playwright's last successful run from state.json."""
        state_file = os.path.join("storage", "linkedin", "state.json")
        if not os.path.exists(state_file):
            return {}
        try:
            with open(state_file) as f:
                data = json.load(f)
            return {c["name"]: c["value"] for c in data.get("cookies", [])}
        except Exception:
            return {}

    async def login(self):
        li_at = os.environ.get("LINKEDIN_LI_AT", "").strip("\"'")
        if not li_at:
            raise ValueError("LINKEDIN_LI_AT environment variable is not set.")

        saved = self._load_saved_cookies()
        li_at = li_at or saved.get("li_at", "")

        self._cookies: Dict[str, str] = {k: v for k, v in saved.items()}
        self._cookies["li_at"] = li_at

        jsessionid_env = os.environ.get("LINKEDIN_JSESSIONID", "").strip("\"'")
        if jsessionid_env:
            self._cookies["JSESSIONID"] = jsessionid_env

        self._csrf_token = self._cookies.get("JSESSIONID", "").strip('"')

        # impersonate="chrome120" gives Chrome's exact TLS/H2 fingerprint
        self._session = AsyncSession(impersonate="chrome120")

        if self._csrf_token:
            # Full session available — skip any page load, go straight to API
            logger.info("LinkedIn Voyager: session ready (using saved JSESSIONID).")
            return

        # No JSESSIONID — try loading feed to obtain one
        try:
            resp = await self._session.get(
                f"{self.BASE_URL}/feed/",
                cookies=self._cookies,
                headers={"Accept-Language": "en-US,en;q=0.9"},
                allow_redirects=True,
                max_redirects=10,
            )
        except Exception as e:
            raise ValueError(
                f"LinkedIn session init failed: {e}. "
                "Add LINKEDIN_JSESSIONID to your .env (copy from browser DevTools → Cookies)."
            )

        if "/login" in str(resp.url) or resp.status_code in (401, 403):
            raise ValueError(
                "LinkedIn authentication failed — li_at cookie may be expired or invalid."
            )

        jsessionid = resp.cookies.get("JSESSIONID", "")
        self._csrf_token = jsessionid.strip('"') or "ajax:0"
        if jsessionid:
            self._cookies["JSESSIONID"] = self._csrf_token

        logger.info(f"LinkedIn Voyager: session ready (status={resp.status_code}).")

    def _api_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/vnd.linkedin.normalized+json+2.1",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Li-Lang": "en_US",
            "X-RestLi-Protocol-Version": "2.0.0",
            "X-Li-Track": json.dumps({
                "clientVersion": "1.13.18390",
                "mpVersion": "1.13.18390",
                "osName": "web",
                "timezoneOffset": 5.5,
                "timezone": "Asia/Calcutta",
                "deviceFormFactor": "DESKTOP",
                "mpName": "voyager-web",
                "displayDensity": 2.0,
                "displayWidth": 1280,
                "displayHeight": 800,
            }),
            "Csrf-Token": self._csrf_token,
            "Referer": "https://www.linkedin.com/search/results/content/",
        }

    async def search(self, keyword: Keyword, db: DBSession) -> List[Any]:
        max_posts = await self._get_setting(db, "linkedin_max_posts", 20)
        await self._random_delay()

        params = {
            "q": "content",
            "keywords": keyword.keyword,
            "count": min(max_posts, 50),
            "start": 0,
            "origin": "FACETED_SEARCH",
            "filters": "List(resultType->CONTENT)",
        }

        logger.info(f"Voyager: searching '{keyword.keyword}'")

        resp = await self._session.get(
            f"{self.VOYAGER}/search/blended",
            params=params,
            headers=self._api_headers(),
            cookies=self._cookies,
        )

        if resp.status_code == 401:
            raise ValueError("LinkedIn auth error (401) — li_at cookie may be expired.")
        if resp.status_code in (429, 999):
            raise ValueError("LinkedIn rate-limited. Slow down requests.")
        if resp.status_code != 200:
            raise ValueError(f"LinkedIn Voyager API returned HTTP {resp.status_code}.")

        data = resp.json()
        results = self._parse_response(data)
        logger.info(f"Voyager: extracted {len(results)} posts for '{keyword.keyword}'")
        return results

    def _parse_response(self, data: dict) -> List[Dict[str, Any]]:
        # Build URN → object lookup from the normalized 'included' array
        included: Dict[str, dict] = {}
        for item in data.get("included", []):
            urn = item.get("entityUrn") or item.get("urn", "")
            if urn:
                included[urn] = item

        results = []

        for urn, obj in included.items():
            obj_type = obj.get("$type", "")

            # Only process post/update objects
            if "UpdateV2" not in obj_type and "FeedUpdate" not in obj_type:
                continue

            actor = obj.get("actor", {}) or {}
            name_obj = actor.get("name", {})
            author_name = (
                name_obj.get("text", "") if isinstance(name_obj, dict) else ""
            ).strip()

            if not author_name:
                continue

            nav = actor.get("navigationUrl") or actor.get("url", "")
            author_url = (
                nav if str(nav).startswith("http") else f"https://www.linkedin.com{nav}"
            )

            desc = actor.get("description", {})
            author_title = (
                desc.get("text", "") if isinstance(desc, dict) else ""
            ).strip()

            commentary = obj.get("commentary", {}) or {}
            text_obj = commentary.get("text", {})
            post_text = (
                text_obj.get("text", "") if isinstance(text_obj, dict) else str(text_obj)
            ).strip()

            if not post_text:
                continue

            results.append({
                "author_name": author_name,
                "author_url": author_url or "https://linkedin.com",
                "author_title": author_title,
                "post_url": f"https://www.linkedin.com/feed/update/{urn}/",
                "post_text": post_text,
                "published_at": None,
                "normalized_data": {
                    "author": author_name,
                    "title": author_title,
                    "text": post_text,
                    "urn": urn,
                },
                "raw_payload": {"urn": urn, "type": obj_type},
            })

        return results

    async def extract(self, raw_data: Any) -> Dict[str, Any]:
        # Data is already structured in search(); passthrough for interface compat
        return raw_data

    async def crawl(self, keyword: Keyword, db: DBSession) -> List[Dict[str, Any]]:
        try:
            await self.login()
            return await self.search(keyword, db)
        except Exception as e:
            logger.error(f"Voyager crawl failed for '{keyword.keyword}': {e}")
            raise
        finally:
            await self.cleanup()

    async def cleanup(self):
        if self._session:
            await self._session.close()
            self._session = None
