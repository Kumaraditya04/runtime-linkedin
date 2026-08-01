import asyncio
import random
import logging
from typing import List, Dict, Any
from app.crawler.base import BaseCrawler
from app.crawler.parser import LeadParser
from app.models.keyword import Keyword
from app.crawler.selectors.linkedin import LinkedInSelectors
from app.models.system_settings import SystemSettings
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class LinkedInCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(source="linkedin")
        self.selectors = LinkedInSelectors()

    async def _random_delay(self, min_ms=1000, max_ms=3000):
        delay = random.uniform(min_ms, max_ms) / 1000.0
        await asyncio.sleep(delay)

    async def login(self):
        # We rely on the LI_AT cookie injected via BrowserManager
        pass

    async def _get_setting(self, db: AsyncSession, key: str, default: int) -> int:
        s = await db.get(SystemSettings, key)
        if s and s.value.isdigit():
            return int(s.value)
        return default

    async def search(self, keyword: Keyword, db: AsyncSession) -> List[Any]:
        page = self.page
        
        # Load configs
        max_posts = await self._get_setting(db, "linkedin_max_posts", 10)
        scroll_count = await self._get_setting(db, "linkedin_scroll_count", 3)
        min_delay = await self._get_setting(db, "linkedin_min_delay", 1000)
        max_delay = await self._get_setting(db, "linkedin_max_delay", 3000)
        timeout = await self._get_setting(db, "linkedin_timeout", 5000)
        
        # Format keyword for LinkedIn search
        kw_encoded = keyword.keyword.replace(" ", "%20")
        url = f"https://www.linkedin.com/search/results/content/?keywords={kw_encoded}"
        
        logger.info(f"Navigating to {url}")
        await page.goto(url, wait_until="domcontentloaded")
        await self._random_delay(min_delay, max_delay)
        
        # Check if we hit a login wall
        if "/login" in page.url or "/signup" in page.url:
            raise ValueError("Hit LinkedIn login wall! LI_AT cookie might be invalid or missing.")

        # Scroll to load full page of posts with human-like delays
        last_height = 0
        for i in range(scroll_count):
            # Random scroll distance between 600px and 1200px
            scroll_by = random.randint(600, 1200)
            await page.mouse.wheel(0, scroll_by)
            
            # Human jitter delay between scrolls (1.5s - 3.5s)
            await self._random_delay(min_delay, max_delay)
            
            # Check if we hit the bottom of the page
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height and i > 4:
                logger.info("Reached end of search results feed.")
                break
            last_height = new_height

        # Wait for posts to appear (try all selectors in the list)
        found_selector = None
        for sel in self.selectors.POST_CONTAINER:
            try:
                await page.wait_for_selector(sel, timeout=15000)
                found_selector = sel
                break
            except Exception:
                continue

        if not found_selector:
            raise ValueError("No posts found or all selector timeouts exceeded.")

        # Grant clipboard permissions for copying post links
        try:
            await page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
        except Exception:
            pass

        # Extract raw HTML, exact post URL, and timestamp for each post
        post_elements = await page.query_selector_all(found_selector)
        logger.info(f"Found {len(post_elements)} posts.")
        
        extracted_raw_items = []
        for idx, el in enumerate(post_elements[:max_posts]):
            # Scroll post item into view so control menu is clickable
            try:
                await el.scroll_into_view_if_needed()
                await asyncio.sleep(0.2)
            except Exception:
                pass

            html = await el.inner_html()
            
            # Extract timestamp
            ts_elem = await el.query_selector('span:has-text("•"), div:has-text("•"), p:has-text("•")')
            ts_text = await ts_elem.inner_text() if ts_elem else ""
            
            # Click control menu to copy exact post link
            exact_post_url = None
            try:
                menu_btn = await el.query_selector('button[aria-label*="Open control menu"]')
                if menu_btn:
                    await menu_btn.scroll_into_view_if_needed()
                    await menu_btn.click()
                    await asyncio.sleep(0.4)
                    copy_btn = await page.query_selector('div[role="menuitem"]:has-text("Copy link to post")')
                    if copy_btn:
                        await copy_btn.click()
                        await asyncio.sleep(0.4)
                        exact_post_url = await page.evaluate('navigator.clipboard.readText()')
                    else:
                        await page.keyboard.press('Escape')
            except Exception as copy_err:
                logger.debug(f"Failed to copy post link for item {idx}: {copy_err}")
                try:
                    await page.keyboard.press('Escape')
                except Exception:
                    pass
            
            extracted_raw_items.append({
                "html": html,
                "exact_post_url": exact_post_url,
                "timestamp_str": ts_text.strip()
            })
            
        return extracted_raw_items

    async def extract(self, raw_data: Any) -> Dict[str, Any]:
        if isinstance(raw_data, dict):
            return LeadParser.parse_linkedin_post(
                html_content=raw_data.get("html", ""),
                exact_post_url=raw_data.get("exact_post_url"),
                timestamp_str=raw_data.get("timestamp_str")
            )
        return LeadParser.parse_linkedin_post(raw_data)
