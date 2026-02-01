from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from db import Base


class ScrapedItem(Base):
    __tablename__ = "scraped_items"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    summary = Column(Text, nullable=True)
    tags = Column(JSONB, nullable=True)  # list of tags or keywords
    published_at = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, server_default=func.now(), nullable=False)