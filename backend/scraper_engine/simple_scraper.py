"""
Simple HTTP-based scraper for Windows compatibility.

This is a fallback scraper that uses httpx instead of Playwright
to avoid Windows subprocess issues.
"""

import httpx
from bs4 import BeautifulSoup
import trafilatura
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def scrape_with_httpx(url: str, wait_seconds: int = 2) -> Dict[str, Any]:
    """
    Scrape a URL using httpx (no browser automation).
    
    Args:
        url: URL to scrape
        wait_seconds: Not used, kept for compatibility
        
    Returns:
        Dictionary with scraped content
    """
    logger.info(f"Scraping with httpx: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
            logger.info(f"Got {len(html)} bytes from {url}")
        except Exception as e:
            logger.error(f"HTTP request failed: {e}")
            raise
    
    # Extract content using trafilatura
    try:
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_images=False,
        )
        
        if not extracted:
            # Fallback to BeautifulSoup
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            extracted = soup.get_text(separator='\n', strip=True)
        
    except Exception as e:
        logger.error(f"Content extraction failed: {e}")
        extracted = "Failed to extract content"
    
    # Extract metadata
    soup = BeautifulSoup(html, 'lxml')
    
    title = None
    if soup.title:
        title = soup.title.string
    elif soup.find('h1'):
        title = soup.find('h1').get_text(strip=True)
    
    author = None
    author_meta = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', attrs={'property': 'article:author'})
    if author_meta:
        author = author_meta.get('content')
    
    published_date = None
    date_meta = soup.find('meta', attrs={'property': 'article:published_time'}) or soup.find('meta', attrs={'name': 'date'})
    if date_meta:
        published_date = date_meta.get('content')
    
    # Extract tables
    tables = []
    for table in soup.find_all('table')[:5]:  # Limit to first 5 tables
        table_data = []
        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            if cells:
                table_data.append(cells)
        if table_data:
            tables.append(table_data)
    
    # Extract lists
    lists = []
    for ul in soup.find_all(['ul', 'ol'])[:10]:  # Limit to first 10 lists
        items = [li.get_text(strip=True) for li in ul.find_all('li')]
        if items:
            lists.append(items)
    
    return {
        'content': extracted or '',
        'title': title,
        'author': author,
        'published_date': published_date,
        'tables': tables,
        'lists': lists,
        'word_count': len(extracted.split()) if extracted else 0
    }
