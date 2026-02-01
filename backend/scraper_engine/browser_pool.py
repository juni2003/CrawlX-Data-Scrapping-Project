"""
Browser Pool Manager for Playwright

Manages Playwright browser instances with proper lifecycle management.
Uses a single browser instance to save resources (minimal implementation).
"""

import asyncio
import platform
import sys
from playwright.async_api import async_playwright, Browser, Page
import logging

logger = logging.getLogger(__name__)

# Global browser instance
_browser: Browser = None
_playwright = None

# Ensure Windows compatibility
if platform.system() == 'Windows':
    # Set the event loop policy for Windows
    if sys.version_info >= (3, 8) and isinstance(
        asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy
    ) is False:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def get_browser() -> Browser:
    """
    Get or create a Playwright browser instance.
    
    Returns:
        Browser: Playwright browser instance
    """
    global _browser, _playwright
    
    if _browser is None or not _browser.is_connected():
        logger.info("Launching new Playwright browser...")
        
        try:
            _playwright = await async_playwright().start()
            
            # Launch browser with stealth settings
            _browser = await _playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            logger.info("Browser launched successfully")
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            raise
    
    return _browser
    
    return _browser


async def close_browser():
    """Close the browser and cleanup resources."""
    global _browser, _playwright
    
    if _browser:
        await _browser.close()
        _browser = None
        logger.info("Browser closed")
    
    if _playwright:
        await _playwright.stop()
        _playwright = None
        logger.info("Playwright stopped")


async def create_stealth_page(browser: Browser) -> Page:
    """
    Create a new page with stealth settings.
    
    Args:
        browser: Playwright browser instance
        
    Returns:
        Page: Configured page with stealth settings
    """
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    )
    
    page = await context.new_page()
    
    # Add stealth scripts
    await page.add_init_script("""
        // Overwrite the `navigator.webdriver` property to undefined
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Overwrite the `plugins` property to a fake PluginArray
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Overwrite the `languages` property
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Remove automation indicators
        delete navigator.__proto__.webdriver;
    """)
    
    return page
