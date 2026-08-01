from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
from datetime import datetime, timezone
import os
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession

from app.crawler.browser_manager import get_browser_manager
from app.models.keyword import Keyword

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    def __init__(self, source: str):
        self.source = source
        self.browser_manager = get_browser_manager(source)
        self.page = None

    async def initialize(self):
        await self.browser_manager.initialize()
        self.page = await self.browser_manager.get_page()

    @abstractmethod
    async def login(self):
        """Perform login if required and save state."""
        pass

    @abstractmethod
    async def search(self, keyword: Keyword, db: AsyncSession) -> List[Any]:
        """Search the source for the keyword and return raw elements/data."""
        pass

    @abstractmethod
    async def extract(self, raw_data: Any) -> Dict[str, Any]:
        """Extract data from a raw element into a standardized dictionary."""
        pass

    async def crawl(self, keyword: Keyword, db: AsyncSession) -> List[Dict[str, Any]]:
        """Main orchestrator."""
        try:
            await self.initialize()
            await self.login()
            raw_results = await self.search(keyword, db)
            
            extracted_leads = []
            for raw in raw_results:
                try:
                    lead_data = await self.extract(raw)
                    if lead_data:
                        extracted_leads.append(lead_data)
                except Exception as e:
                    logger.error(f"Error extracting lead from {self.source}: {e}")
            
            if not extracted_leads and raw_results:
                logger.warning("No leads extracted despite having raw results. Saving snapshot.")
                await self._save_snapshot(keyword, "extraction_failed")
                
            return extracted_leads
        except Exception as e:
            logger.error(f"Crawl failed: {e}")
            await self._save_snapshot(keyword, "crawl_failed")
            raise e
        finally:
            await self.cleanup()

    async def _save_snapshot(self, keyword: Keyword, reason: str):
        try:
            if not self.page:
                logger.error("No page available to take snapshot.")
                return
            html = await self.page.content()
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            ts = datetime.now(timezone.utc).strftime("%H%M%S")
            path_dir = f"storage/crawler/{self.source}/{date_str}"
            os.makedirs(path_dir, exist_ok=True)
            filepath = f"{path_dir}/{keyword.id}_{reason}_{ts}.html"
            with open(filepath, "w") as f:
                f.write(html)
            logger.info(f"Saved HTML snapshot to {filepath}")
        except Exception as snap_e:
            logger.error(f"Failed to save snapshot: {snap_e}")

    async def cleanup(self):
        if self.page:
            await self.page.close()
        # We don't call browser_manager.cleanup() here so the context is reused
