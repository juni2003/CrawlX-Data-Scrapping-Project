from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


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