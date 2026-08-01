#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Starting build process for Render..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
# PLAYWRIGHT_BROWSERS_PATH=0 installs the browser inside the site-packages
# directory, which ensures it is preserved in the Render runtime environment.
export PLAYWRIGHT_BROWSERS_PATH=0
playwright install chromium

echo "Build complete."
