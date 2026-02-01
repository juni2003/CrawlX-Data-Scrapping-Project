from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from models import ScrapedItem


def get_items(db: Session, skip: int = 0, limit: int = 50, tag: str = None):
    """Get items with optional tag filtering."""
    stmt = select(ScrapedItem)
    
    if tag:
        # Filter by tag using PostgreSQL JSONB contains operator
        stmt = stmt.where(ScrapedItem.tags.contains([tag]))
    
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def search_items(db: Session, q: str, skip: int = 0, limit: int = 50, tag: str = None):
    """
    Search items by query string with optional tag filtering.
    Searches in both title and summary fields.
    """
    stmt = select(ScrapedItem)
    
    # Search in title and summary
    search_filter = or_(
        ScrapedItem.title.ilike(f"%{q}%"),
        ScrapedItem.summary.ilike(f"%{q}%")
    )
    stmt = stmt.where(search_filter)
    
    # Add tag filter if provided
    if tag:
        stmt = stmt.where(ScrapedItem.tags.contains([tag]))
    
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def search_items_fuzzy(db: Session, q: str, skip: int = 0, limit: int = 50, tag: str = None):
    """
    Fuzzy search using PostgreSQL trigram similarity.
    Requires pg_trgm extension to be enabled in PostgreSQL.
    """
    stmt = select(ScrapedItem)
    
    # Use trigram similarity for fuzzy matching
    # similarity threshold of 0.3 (30% similar)
    similarity_threshold = 0.3
    search_filter = or_(
        func.similarity(ScrapedItem.title, q) > similarity_threshold,
        func.similarity(ScrapedItem.summary, q) > similarity_threshold
    )
    stmt = stmt.where(search_filter)
    
    # Add tag filter if provided
    if tag:
        stmt = stmt.where(ScrapedItem.tags.contains([tag]))
    
    # Order by similarity (most similar first)
    stmt = stmt.order_by(
        func.greatest(
            func.similarity(ScrapedItem.title, q),
            func.similarity(ScrapedItem.summary, q)
        ).desc()
    )
    
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()