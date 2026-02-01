"""
Smart Content Extraction

Automatically extracts meaningful content from web pages.
Handles articles, blog posts, and general text content.
"""

import trafilatura
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def extract_content(html: str, url: str, extract_type: str = "auto") -> Dict:
    """
    Extract content from HTML using multiple strategies.
    
    Args:
        html: Raw HTML content
        url: Source URL
        extract_type: Type of extraction (auto, article, text, structured)
        
    Returns:
        Dict with extracted content
    """
    
    if extract_type == "auto":
        # Try article extraction first (best for news/blogs)
        result = extract_article(html, url)
        if result.get("content"):
            return result
        
        # Fallback to general text extraction
        return extract_text(html, url)
    
    elif extract_type == "article":
        return extract_article(html, url)
    
    elif extract_type == "text":
        return extract_text(html, url)
    
    elif extract_type == "structured":
        return extract_structured_data(html, url)
    
    else:
        return extract_text(html, url)


def extract_article(html: str, url: str) -> Dict:
    """
    Extract article content using trafilatura (specialized for news/blogs).
    
    Args:
        html: Raw HTML content
        url: Source URL
        
    Returns:
        Dict with article data
    """
    try:
        # Use trafilatura for smart article extraction
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            no_fallback=False,
            favor_precision=True,
            url=url
        )
        
        # Extract metadata
        metadata = trafilatura.extract_metadata(html)
        
        result = {
            "success": True,
            "url": url,
            "title": metadata.title if metadata and metadata.title else extract_title(html),
            "content": extracted or "",
            "author": metadata.author if metadata and metadata.author else None,
            "published_date": metadata.date if metadata and metadata.date else None,
            "description": metadata.description if metadata and metadata.description else None,
            "tags": metadata.tags if metadata and metadata.tags else [],
            "extracted_at": datetime.now().isoformat(),
            "extraction_method": "article"
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Article extraction failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


def extract_text(html: str, url: str) -> Dict:
    """
    Extract general text content from any webpage.
    
    Args:
        html: Raw HTML content
        url: Source URL
        
    Returns:
        Dict with text data
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        # Get title
        title = extract_title(html)
        
        # Get main content
        # Try to find main content areas
        main_content = None
        for selector in ['main', 'article', '[role="main"]', '.content', '#content']:
            element = soup.select_one(selector)
            if element:
                main_content = element.get_text(separator='\n', strip=True)
                break
        
        # Fallback to body text
        if not main_content:
            main_content = soup.body.get_text(separator='\n', strip=True) if soup.body else ""
        
        # Clean up text
        lines = (line.strip() for line in main_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Extract meta description
        description = None
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content')
        
        return {
            "success": True,
            "url": url,
            "title": title,
            "content": text[:10000],  # Limit to 10k chars
            "description": description,
            "extracted_at": datetime.now().isoformat(),
            "extraction_method": "text"
        }
        
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


def extract_structured_data(html: str, url: str) -> Dict:
    """
    Extract structured data like tables, lists, etc.
    
    Args:
        html: Raw HTML content
        url: Source URL
        
    Returns:
        Dict with structured data
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract tables
        tables = []
        for table in soup.find_all('table')[:5]:  # Limit to 5 tables
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)
        
        # Extract lists
        lists = []
        for ul in soup.find_all(['ul', 'ol'])[:10]:  # Limit to 10 lists
            items = [li.get_text(strip=True) for li in ul.find_all('li', recursive=False)]
            if items:
                lists.append(items)
        
        return {
            "success": True,
            "url": url,
            "title": extract_title(html),
            "tables": tables,
            "lists": lists,
            "extracted_at": datetime.now().isoformat(),
            "extraction_method": "structured"
        }
        
    except Exception as e:
        logger.error(f"Structured extraction failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


def extract_title(html: str) -> Optional[str]:
    """
    Extract page title from HTML.
    
    Args:
        html: Raw HTML content
        
    Returns:
        Page title or None
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Try multiple methods
        # 1. <title> tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        # 2. og:title meta tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        
        # 3. h1 tag
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return "Untitled"
        
    except:
        return "Untitled"


def extract_links(html: str, base_url: str) -> List[str]:
    """
    Extract all links from a webpage.
    
    Args:
        html: Raw HTML content
        base_url: Base URL for resolving relative links
        
    Returns:
        List of URLs
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Make absolute URLs
            if href.startswith('/'):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)
            if href.startswith('http'):
                links.append(href)
        
        return list(set(links))  # Remove duplicates
        
    except Exception as e:
        logger.error(f"Link extraction failed: {e}")
        return []
