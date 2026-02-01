import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:juni071@localhost:5432/scraper_db"
)

# Configure connection pool to prevent hanging
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_size=10,           # Maximum number of connections to keep in pool
    max_overflow=20,        # Maximum overflow connections
    pool_pre_ping=True,     # Verify connections before using them
    pool_recycle=3600       # Recycle connections after 1 hour
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass