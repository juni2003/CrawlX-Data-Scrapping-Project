"""
Stealth Configuration for Browser Pages

Additional stealth techniques to avoid bot detection.
"""

from playwright.async_api import Page
from fake_useragent import UserAgent


async def setup_stealth_page(page: Page) -> Page:
    """
    Apply advanced stealth techniques to a Playwright page.
    
    Args:
        page: Playwright page instance
        
    Returns:
        Page: Page with stealth configurations applied
    """
    
    # Add extra stealth scripts
    await page.add_init_script("""
        // Pass the Chrome Test
        window.chrome = {
            runtime: {},
        };
        
        // Pass the Permissions Test
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Pass the Plugins Length Test
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Pass the iframe Test
        Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
            get: function() {
                return window;
            }
        });
        
        // Pass toString test
        window.navigator.chrome = {
            runtime: {},
        };
    """)
    
    return page


def get_random_user_agent() -> str:
    """
    Get a random realistic user agent string.
    
    Returns:
        str: Random user agent
    """
    ua = UserAgent()
    return ua.random
