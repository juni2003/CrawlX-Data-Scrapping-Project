from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import ScrapedItem


def get_items(db: Session, skip: int = 0, limit: int = 50):
    stmt = select(ScrapedItem).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def search_items(db: Session, q: str, skip: int = 0, limit: int = 50):
    stmt = (
        select(ScrapedItem)
        .where(ScrapedItem.title.ilike(f"%{q}%"))
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()