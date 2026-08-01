import os
import subprocess
import logging
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
STORAGE_DIR = Path("storage")
_managers = {}

def get_browser_manager(source: str) -> 'BrowserManager':
    if source not in _managers:
        _managers[source] = BrowserManager(source)
    return _managers[source]

class BrowserManager:
    def __init__(self, source: str):
        self.source = source
        self.storage_path = STORAGE_DIR / source
        self.state_file = self.storage_path / "state.json"
        
        self.playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None

    async def initialize(self):
        if (
            self.playwright is not None 
            and self.browser is not None 
            and self.browser.is_connected() 
            and self.context is not None
        ):
            return # Already initialized and active

        self.storage_path.mkdir(parents=True, exist_ok=True)
        if self.playwright is None:
            self.playwright = await async_playwright().start()

        launch_args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-zygote"
        ]

        try:
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=launch_args
            )
        except Exception as launch_err:
            logger.warning(f"Initial Chromium launch failed ({launch_err}). Auto-installing Playwright Chromium...")
            try:
                subprocess.run(["playwright", "install", "chromium"], check=False)
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=launch_args
                )
            except Exception as retry_err:
                logger.error(f"Failed auto-installing Chromium: {retry_err}")
                raise retry_err

        context_options = {}
        if self.state_file.exists():
            try:
                context_options["storage_state"] = str(self.state_file)
            except Exception:
                pass

        self.context = await self.browser.new_context(**context_options)
        
        # Inject LINKEDIN_LI_AT cookie if present in environment
        li_at_cookie = os.environ.get("LINKEDIN_LI_AT")
        if li_at_cookie and self.source == "linkedin":
            await self.context.add_cookies([{
                "name": "li_at",
                "value": li_at_cookie.strip('"\''),
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "httpOnly": True
            }])
            await self.save_state()

    async def get_page(self):
        if not self.context or not self.browser or not self.browser.is_connected():
            self.playwright = None
            self.browser = None
            self.context = None
            await self.initialize()
        return await self.context.new_page()

    async def save_state(self):
        if self.context:
            try:
                await self.context.storage_state(path=str(self.state_file))
            except Exception as e:
                logger.debug(f"Failed to save storage state: {e}")

    async def cleanup(self):
        pass
