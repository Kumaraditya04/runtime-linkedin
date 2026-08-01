import os
import logging
from pathlib import Path
from typing import Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Error as PlaywrightError

from dotenv import load_dotenv
from app.core.exceptions import DeploymentConfigurationError

load_dotenv()

logger = logging.getLogger(__name__)
STORAGE_DIR = Path("storage")
SNAPSHOT_DIR = STORAGE_DIR / "crawler"
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

    @classmethod
    async def check_environment(cls) -> Dict[str, Any]:
        """
        Verify Playwright installation, Chromium executable existence,
        writable storage directories, and return detailed environment diagnostics.
        """
        diagnostics = {
            "playwright_installed": False,
            "chromium_installed": False,
            "chromium_executable_path": None,
            "storage_writable": False,
            "snapshot_dir_exists": False,
            "environment": os.environ.get("RENDER_SERVICE_ID") and "render" or "local",
            "message": ""
        }

        # Check Playwright installation & Chromium executable
        try:
            pw = await async_playwright().start()
            diagnostics["playwright_installed"] = True
            exec_path = pw.chromium.executable_path
            diagnostics["chromium_executable_path"] = exec_path
            
            if exec_path and os.path.exists(exec_path):
                diagnostics["chromium_installed"] = True
            else:
                # Also try launching in headless mode to verify
                try:
                    b = await pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
                    await b.close()
                    diagnostics["chromium_installed"] = True
                except Exception as b_err:
                    diagnostics["chromium_installed"] = False
                    diagnostics["message"] = f"Chromium binary launch failed: {b_err}"
            await pw.stop()
        except Exception as pw_err:
            diagnostics["playwright_installed"] = False
            diagnostics["message"] = f"Playwright error: {pw_err}"

        # Check Storage Directory Writability
        try:
            STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            test_file = STORAGE_DIR / ".write_test"
            test_file.touch()
            test_file.unlink()
            diagnostics["storage_writable"] = True
        except Exception as st_err:
            diagnostics["storage_writable"] = False
            diagnostics["message"] += f" | Storage not writable: {st_err}"

        # Check Snapshot Directory
        try:
            SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
            diagnostics["snapshot_dir_exists"] = True
        except Exception as snap_err:
            diagnostics["snapshot_dir_exists"] = False

        if diagnostics["chromium_installed"] and diagnostics["storage_writable"]:
            diagnostics["message"] = "Environment operational and Chromium browser is ready."
        elif not diagnostics["chromium_installed"]:
            diagnostics["message"] = "Chromium browser is not installed. Run: playwright install chromium"

        return diagnostics

    async def initialize(self):
        if (
            self.playwright is not None 
            and self.browser is not None 
            and self.browser.is_connected() 
            and self.context is not None
        ):
            return # Already initialized and active

        self.storage_path.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

        if self.playwright is None:
            self.playwright = await async_playwright().start()

        # Check executable existence before launching
        exec_path = self.playwright.chromium.executable_path
        if exec_path and not os.path.exists(exec_path):
            logger.error(f"Chromium executable missing at path: {exec_path}")

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
            err_msg = str(launch_err)
            logger.error(f"Failed to launch Chromium browser: {err_msg}")
            if "Executable doesn't exist" in err_msg or "playwright install" in err_msg or not os.path.exists(exec_path or ""):
                raise DeploymentConfigurationError(
                    "Chromium browser is not installed. Run: playwright install chromium"
                ) from launch_err
            raise DeploymentConfigurationError(
                f"Chromium browser failed to launch: {err_msg}"
            ) from launch_err

        context_options = {}
        if self.state_file.exists():
            try:
                context_options["storage_state"] = str(self.state_file)
            except Exception:
                pass

        try:
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                device_scale_factor=1,
                locale="en-US",
                timezone_id="Asia/Kolkata",
                **context_options
            )
            
            # Stealth script to bypass headless detection
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.navigator.chrome = { runtime: {} };
            """)
            
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
        except Exception as ctx_err:
            logger.error(f"Failed to create browser context: {ctx_err}")
            raise DeploymentConfigurationError(f"Failed to initialize browser context: {ctx_err}") from ctx_err

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
