"""
Generic URL Scraper Engine (Option C - Minimal Implementation)

This module provides basic web scraping capabilities for any URL
with stealth mode and smart content extraction.
"""

from .browser_pool import get_browser, close_browser
from .extractors import extract_content
from .stealth import setup_stealth_page

__all__ = ['get_browser', 'close_browser', 'extract_content', 'setup_stealth_page']
