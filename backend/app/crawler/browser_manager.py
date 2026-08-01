import os
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext

from dotenv import load_dotenv
load_dotenv()

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
        if self.playwright is not None:
            return # Already initialized

        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(headless=True)

        context_options = {}
        if self.state_file.exists():
            context_options["storage_state"] = str(self.state_file)

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
            # Save it so it persists in state.json
            await self.save_state()

    async def get_page(self):
        if not self.context:
            await self.initialize()
        return await self.context.new_page()

    async def save_state(self):
        if self.context:
            await self.context.storage_state(path=str(self.state_file))

    async def cleanup(self):
        # We don't close the browser here anymore so it can be reused across jobs.
        # The OS will clean up the process when the FastAPI server exits.
        pass
