#!/usr/bin/env python3
"""
Playwright Environment Verification Script for LeadRadar AI.
Verifies Playwright installation, Chromium executable availability, and browser launch capability.
Returns exit code 0 on success, 1 on failure.
"""

import sys
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def verify_playwright():
    logging.info("Checking Playwright environment...")
    
    # 1. Check Playwright Module
    try:
        from playwright.async_api import async_playwright
        logging.info("✓ Playwright Python package installed.")
    except ImportError:
        logging.error("❌ Playwright package not installed! Run: pip install playwright")
        return False

    # 2. Check Chromium Executable & Launch
    try:
        pw = await async_playwright().start()
        exec_path = pw.chromium.executable_path
        logging.info(f"Chromium executable path: {exec_path}")
        
        if not exec_path or not os.path.exists(exec_path):
            logging.warning("⚠️ Chromium executable path does not exist on disk.")

        logging.info("Attempting Chromium launch in headless mode...")
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        logging.info("✓ Chromium browser launched successfully.")

        page = await browser.new_page()
        await page.goto("about:blank")
        logging.info("✓ Browser page created and navigated.")

        await browser.close()
        await pw.stop()
        logging.info("✓ Browser closed cleanly.")
        return True

    except Exception as e:
        logging.error(f"❌ Playwright Chromium verification failed: {e}")
        logging.error("Chromium browser is not installed or dependencies missing.")
        logging.error("Run: playwright install chromium")
        return False

def main():
    success = asyncio.run(verify_playwright())
    if success:
        logging.info("=== PLAYWRIGHT VERIFICATION PASSED ===")
        sys.exit(0)
    else:
        logging.error("=== PLAYWRIGHT VERIFICATION FAILED ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
