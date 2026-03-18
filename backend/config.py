import os
from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(raw_url: str) -> str:
    """Normalize provider URLs for SQLAlchemy psycopg2 engine."""
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
    if raw_url.startswith("postgresql://") and "+psycopg2" not in raw_url:
        return raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return raw_url

DATABASE_URL = normalize_database_url(os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:juni071@localhost:5432/scraper_db"
))