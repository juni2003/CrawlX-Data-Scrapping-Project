from datetime import datetime
from typing import Any, Optional, List
from pydantic import BaseModel, HttpUrl, Field


class ScrapedItemOut(BaseModel):
    id: int
    source: str
    title: str
    url: str
    summary: Optional[str]
    tags: Optional[Any]
    published_at: Optional[datetime]
    scraped_at: datetime

    class Config:
        from_attributes = True


# Custom URL Scraping Schemas

class UrlScrapeRequest(BaseModel):
    """Request schema for custom URL scraping."""
    url: HttpUrl = Field(..., description="URL to scrape")
    extract_type: str = Field(
        default="auto",
        description="Extraction type: 'auto', 'article', 'text', or 'structured'",
        pattern="^(auto|article|text|structured)$"
    )
    wait_for: Optional[int] = Field(
        default=2,
        description="Seconds to wait for page load (1-30)",
        ge=1,
        le=30
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "extract_type": "auto",
                "wait_for": 2
            }
        }


class UrlScrapeResponse(BaseModel):
    """Response schema for custom URL scraping."""
    success: bool
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    tables: Optional[List[List[List[str]]]] = None
    lists: Optional[List[List[str]]] = None
    extracted_at: str
    extraction_method: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "url": "https://example.com/article",
                "title": "Example Article Title",
                "content": "Full article content...",
                "author": "John Doe",
                "published_date": "2026-02-01",
                "description": "Article description",
                "tags": ["tech", "ai"],
                "extracted_at": "2026-02-01T12:00:00",
                "extraction_method": "article"
            }
        }
