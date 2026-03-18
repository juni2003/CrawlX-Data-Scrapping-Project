"""
Simple HTTP-based scraper for Windows compatibility.

This scraper avoids browser subprocesses and adds retry/error handling,
better metadata extraction, and cleaner output for higher data accuracy.
"""

import asyncio
import logging
import re
from typing import Any, Dict, List

import httpx
import trafilatura
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ScrapeRequestError(Exception):
    """Structured scrape error with HTTP status mapping."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _normalize_text(text: str) -> str:
    """Normalize whitespace and remove noisy empty lines."""
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def _is_noise_line(line: str) -> bool:
    """Detect low-information lines that commonly pollute scraped output."""
    if not line:
        return True

    normalized = line.replace("\xa0", " ").strip().lower()
    compact = re.sub(r"\s+", "", normalized)
    alpha_count = len(re.findall(r"[a-z]", normalized))

    # Common storefront/status noise.
    if normalized in {
        "in stock",
        "out of stock",
        "add to basket",
        "add to cart",
        "read more",
    }:
        return True

    # Currency, numeric-only, and common catalog stock lines.
    if re.fullmatch(r"[£$€]\s?\d+(?:\.\d{1,2})?", normalized):
        return True
    if re.fullmatch(r"[£$€]\s?\d+(?:\.\d{1,2})?\s+(in stock|out of stock)", normalized):
        return True
    if re.fullmatch(r"\d+(?:\.\d+)?", normalized):
        return True

    # Encoding-agnostic fallback for catalog stock lines and symbol-heavy snippets.
    if "in stock" in normalized or "out of stock" in normalized:
        if len(normalized) <= 24:
            return True

    if alpha_count == 0 and len(compact) <= 24:
        return True

    if len(compact) > 0 and (alpha_count / len(compact)) < 0.2 and len(compact) <= 24:
        return True

    # Very short lines with no letters are usually UI noise.
    if len(normalized) <= 3 and not re.search(r"[a-z]", normalized):
        return True

    return False


def _refine_content(text: str) -> str:
    """Clean extracted content by removing low-information and duplicate lines."""
    normalized = _normalize_text(text)
    if not normalized:
        return ""

    seen = set()
    refined_lines: List[str] = []
    for line in normalized.split("\n"):
        if _is_noise_line(line):
            continue

        key = line.strip().lower()
        if key in seen:
            continue

        seen.add(key)
        refined_lines.append(line)

    if not refined_lines:
        return ""

    return "\n".join(refined_lines)


def _build_semantic_fallback(soup: BeautifulSoup) -> str:
    """Build readable fallback content from meaningful headings/paragraphs."""
    chunks: List[str] = []

    for node in soup.select("main h1, main h2, main h3, article h1, article h2, article h3, main p, article p, h1, h2, h3, p"):
        text = _normalize_text(node.get_text(" ", strip=True))
        if not text:
            continue

        # Keep text-like chunks and skip very short/noisy snippets.
        if len(text) < 8:
            continue
        if _is_noise_line(text):
            continue

        chunks.append(text)

    # De-duplicate while preserving order.
    unique_chunks = list(dict.fromkeys(chunks))
    return "\n".join(unique_chunks[:120])


def _extract_meta_content(soup: BeautifulSoup, selectors: List[Dict[str, str]]) -> str | None:
    """Return the first non-empty meta content from candidate selectors."""
    for attrs in selectors:
        meta = soup.find("meta", attrs=attrs)
        if meta and meta.get("content"):
            value = meta.get("content", "").strip()
            if value:
                return value
    return None


def _extract_tags(soup: BeautifulSoup) -> List[str]:
    """Extract and normalize tags from common metadata fields."""
    tags: List[str] = []

    keyword_content = _extract_meta_content(
        soup,
        [
            {"name": "keywords"},
            {"property": "article:tag"},
            {"name": "news_keywords"},
        ],
    )

    if keyword_content:
        for tag in re.split(r"[,;|]", keyword_content):
            cleaned = tag.strip().lower()
            if cleaned:
                tags.append(cleaned)

    # De-duplicate while keeping order.
    unique_tags = list(dict.fromkeys(tags))
    return unique_tags[:20]


def _extract_tables(soup: BeautifulSoup, limit: int = 5) -> List[List[List[str]]]:
    tables: List[List[List[str]]] = []
    for table in soup.find_all("table")[:limit]:
        table_data: List[List[str]] = []
        for row in table.find_all("tr"):
            cells = [_normalize_text(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
            cells = [cell for cell in cells if cell]
            if cells:
                table_data.append(cells)
        if table_data:
            tables.append(table_data)
    return tables


def _extract_lists(soup: BeautifulSoup, limit: int = 10) -> List[List[str]]:
    lists: List[List[str]] = []
    for node in soup.find_all(["ul", "ol"])[:limit]:
        items = [_normalize_text(li.get_text(" ", strip=True)) for li in node.find_all("li", recursive=False)]
        items = [item for item in items if item and len(item) > 1]
        # Keep lists with meaningful content only.
        if len(items) >= 2:
            lists.append(items[:50])
    return lists


async def scrape_with_httpx(url: str, wait_seconds: int = 2, extract_type: str = "auto") -> Dict[str, Any]:
    """
    Scrape a URL using httpx (no browser automation).
    
    Args:
        url: URL to scrape
        wait_seconds: Kept for compatibility; influences timeout/retry pacing
        extract_type: 'auto', 'article', 'text', or 'structured'
        
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
    
    timeout_seconds = min(60.0, max(20.0, 20.0 + float(wait_seconds)))
    retries = 3
    response: httpx.Response | None = None

    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds) as client:
        for attempt in range(1, retries + 1):
            try:
                response = await client.get(url, headers=headers)

                # Retry transient upstream failures.
                if response.status_code in {429, 500, 502, 503, 504}:
                    if attempt < retries:
                        delay = attempt * max(1, wait_seconds)
                        logger.warning(
                            "Transient status %s for %s (attempt %s/%s). Retrying in %ss.",
                            response.status_code,
                            url,
                            attempt,
                            retries,
                            delay,
                        )
                        await asyncio.sleep(delay)
                        continue

                    raise ScrapeRequestError(
                        status_code=response.status_code,
                        detail=f"Target site returned {response.status_code}. Please retry later.",
                    )

                if response.status_code == 403:
                    raise ScrapeRequestError(
                        status_code=403,
                        detail="Access blocked by target site (HTTP 403).",
                    )

                response.raise_for_status()
                break

            except ScrapeRequestError:
                raise
            except httpx.TimeoutException as exc:
                if attempt < retries:
                    delay = attempt * max(1, wait_seconds)
                    logger.warning("Timeout scraping %s (attempt %s/%s). Retrying in %ss.", url, attempt, retries, delay)
                    await asyncio.sleep(delay)
                    continue
                raise ScrapeRequestError(status_code=504, detail=f"Request timed out: {exc}") from exc
            except httpx.TransportError as exc:
                if attempt < retries:
                    delay = attempt * max(1, wait_seconds)
                    logger.warning("Transport error scraping %s (attempt %s/%s). Retrying in %ss.", url, attempt, retries, delay)
                    await asyncio.sleep(delay)
                    continue
                raise ScrapeRequestError(status_code=502, detail=f"Transport error: {exc}") from exc

    if response is None:
        raise ScrapeRequestError(status_code=500, detail="Unknown error: no response received")

    html = response.text or ""
    if not html.strip():
        raise ScrapeRequestError(status_code=502, detail="Target site returned an empty response")

    logger.info("Got %s bytes from %s", len(html), response.url)
    
    # Extract content using trafilatura
    try:
        if extract_type == "article":
            extracted = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                include_images=False,
                favor_precision=True,
                no_fallback=False,
                url=str(response.url),
            )
            extraction_method = "article"
        elif extract_type == "text":
            extracted = None
            extraction_method = "text"
        elif extract_type == "structured":
            extracted = None
            extraction_method = "structured"
        else:
            extracted = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                include_images=False,
                favor_precision=True,
                no_fallback=False,
                url=str(response.url),
            )
            extraction_method = "article" if extracted else "text"

        soup = BeautifulSoup(html, "lxml")

        if not extracted:
            for noisy in soup(["script", "style", "noscript", "svg"]):
                noisy.decompose()

            main_node = (
                soup.select_one("main")
                or soup.select_one("article")
                or soup.select_one("[role='main']")
                or soup.body
                or soup
            )
            extracted = main_node.get_text(separator="\n", strip=True)

        # In auto mode, recover from low-density article extraction.
        if extract_type == "auto" and extracted:
            normalized_article = _normalize_text(extracted)
            article_word_count = len(normalized_article.split())

            if article_word_count < 80:
                for noisy in soup(["script", "style", "noscript", "svg"]):
                    noisy.decompose()

                main_node = (
                    soup.select_one("main")
                    or soup.select_one("article")
                    or soup.select_one("[role='main']")
                    or soup.body
                    or soup
                )
                fallback_text = _normalize_text(main_node.get_text(separator="\n", strip=True))

                if len(fallback_text.split()) > article_word_count:
                    extracted = fallback_text
                    extraction_method = "text"

        extracted = _refine_content(extracted)
        if not extracted:
            extracted = _build_semantic_fallback(soup)
    except ScrapeRequestError:
        raise
    except Exception as e:
        logger.error("Content extraction failed: %s", e)
        raise ScrapeRequestError(status_code=500, detail=f"Content extraction failed: {e}") from e
    
    # Extract metadata
    title = (
        _extract_meta_content(soup, [{"property": "og:title"}, {"name": "twitter:title"}])
        or (_normalize_text(soup.title.string) if soup.title and soup.title.string else None)
        or (_normalize_text(soup.find("h1").get_text(" ", strip=True)) if soup.find("h1") else None)
    )

    author = _extract_meta_content(
        soup,
        [
            {"name": "author"},
            {"property": "article:author"},
        ],
    )

    published_date = _extract_meta_content(
        soup,
        [
            {"property": "article:published_time"},
            {"name": "date"},
            {"name": "pubdate"},
        ],
    )

    description = _extract_meta_content(
        soup,
        [
            {"name": "description"},
            {"property": "og:description"},
            {"name": "twitter:description"},
        ],
    )

    tags = _extract_tags(soup)
    tables = _extract_tables(soup)
    lists = _extract_lists(soup)

    return {
        "content": extracted or "",
        "title": title,
        "author": author,
        "published_date": published_date,
        "description": description,
        "tags": tags,
        "tables": tables,
        "lists": lists,
        "word_count": len(extracted.split()) if extracted else 0,
        "final_url": str(response.url),
        "http_status": response.status_code,
        "extraction_method": extraction_method,
    }
