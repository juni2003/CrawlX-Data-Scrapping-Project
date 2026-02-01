import asyncio
import platform
import sys

# CRITICAL: Set Windows event loop policy BEFORE any other imports
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base
import crud
import schemas
from scheduler import start_scheduler, stop_scheduler, run_spiders_async, DEFAULT_SPIDERS
from pdf_export import generate_items_pdf, generate_simple_table_pdf
import io
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Scraper Backend API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"⚠ Database setup error: {e}")
    
    try:
        start_scheduler()
        print("✓ Scheduler started")
    except Exception as e:
        print(f"⚠ Scheduler error: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    """Cleanup on server shutdown."""
    from scraper_engine.browser_pool import close_browser
    
    try:
        stop_scheduler()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Scheduler shutdown error: {e}")
    
    try:
        await close_browser()
        logger.info("Browser closed")
    except Exception as e:
        logger.error(f"Browser shutdown error: {e}")


@app.get("/")
def root():
    return {"status": "ok", "message": "Scraper API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/items", response_model=list[schemas.ScrapedItemOut])
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, le=1000),
    tag: str = Query(default=None, description="Filter by tag (e.g., 'news', 'tech')"),
    db: Session = Depends(get_db),
):
    """
    List items with optional tag filtering.
    
    Examples:
    - /items - Get all items
    - /items?tag=news - Get only news items
    - /items?tag=tech&limit=10 - Get 10 tech items
    """
    return crud.get_items(db, skip=skip, limit=limit, tag=tag)


@app.get("/search", response_model=list[schemas.ScrapedItemOut])
def search_items(
    q: str = Query(..., description="Search query"),
    skip: int = 0,
    limit: int = Query(50, le=200),
    tag: str = Query(None, description="Filter by tag"),
    fuzzy: bool = Query(False, description="Enable fuzzy search (requires pg_trgm extension)"),
    db: Session = Depends(get_db),
):
    """
    Search items by query with optional tag filtering.
    
    Examples:
    - /search?q=python - Search for 'python' in title and summary
    - /search?q=ai&tag=tech - Search for 'ai' in tech items
    - /search?q=machine&fuzzy=true - Fuzzy search for 'machine'
    """
    if fuzzy:
        return crud.search_items_fuzzy(db, q=q, skip=skip, limit=limit, tag=tag)
    else:
        return crud.search_items(db, q=q, skip=skip, limit=limit, tag=tag)


@app.get("/items/export")
def export_items_json(db: Session = Depends(get_db)):
    """Export items as JSON."""
    items = crud.get_items(db, skip=0, limit=1000)
    data = [schemas.ScrapedItemOut.model_validate(i).model_dump(mode="json") for i in items]
    return JSONResponse(content=data)


@app.get("/items/export/csv")
def export_items_csv(db: Session = Depends(get_db)):
    """Export items as CSV."""
    items = crud.get_items(db, skip=0, limit=1000)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "source", "title", "url", "summary", "tags", "published_at", "scraped_at"])

    for i in items:
        writer.writerow([
            i.id, i.source, i.title, i.url, i.summary, i.tags, i.published_at, i.scraped_at
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scraped_items.csv"}
    )


@app.get("/items/export/pdf")
def export_items_pdf(
    style: str = Query("detailed", description="PDF style: 'detailed' or 'simple'"),
    limit: int = Query(100, le=500, description="Maximum number of items to export"),
    tag: str = Query(None, description="Filter by tag"),
    db: Session = Depends(get_db)
):
    """
    Export items as PDF.
    
    Parameters:
    - style: 'detailed' for full report or 'simple' for table format
    - limit: Maximum number of items (default: 100, max: 500)
    - tag: Optional tag filter
    
    Examples:
    - /items/export/pdf - Export all items in detailed format
    - /items/export/pdf?style=simple - Export in simple table format
    - /items/export/pdf?tag=news&limit=50 - Export 50 news items
    """
    items = crud.get_items(db, skip=0, limit=limit, tag=tag)
    
    if not items:
        raise HTTPException(status_code=404, detail="No items found to export")
    
    if style == "simple":
        pdf_buffer = generate_simple_table_pdf(items)
    else:
        pdf_buffer = generate_items_pdf(items)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=scraped_items.pdf"}
    )


@app.post("/scrape/run")
async def run_scrape(
    spiders: list[str] = Query(default=None, description="List of spider names")
):
    """
    Manually trigger scraping for specified spiders.
    
    Examples:
    - POST /scrape/run?spiders=news&spiders=jobs
    - POST /scrape/run (runs all default spiders)
    """
    if not spiders:
        spiders = DEFAULT_SPIDERS

    if not spiders:
        raise HTTPException(status_code=400, detail="No spiders specified")

    await run_spiders_async(spiders)
    return {"status": "ok", "spiders": spiders, "message": f"Successfully triggered {len(spiders)} spider(s)"}


@app.post("/scrape/url", response_model=schemas.UrlScrapeResponse)
async def scrape_custom_url(request: schemas.UrlScrapeRequest):
    """
    Scrape content from any custom URL using httpx (Windows compatible).
    
    This endpoint uses httpx with trafilatura for content extraction.
    Works on most websites without JavaScript dependencies.
    
    Features:
    - ✅ Fast HTTP-based scraping
    - ✅ Smart content extraction using trafilatura
    - ✅ Supports article, text, and structured data extraction
    - ✅ Windows compatible (no subprocess issues)
    - ✅ No external service costs
    
    Limitations:
    - ❌ Cannot handle JavaScript-heavy sites
    - ❌ Cannot bypass CAPTCHAs
    - ❌ No proxy rotation (may be rate-limited)
    
    Examples:
    ```json
    {
        "url": "https://news.ycombinator.com",
        "extract_type": "auto",
        "wait_seconds": 2
    }
    ```
    
    Args:
        request: UrlScrapeRequest with url, extract_type, and wait_for
        
    Returns:
        UrlScrapeResponse with extracted content
    """
    from scraper_engine.simple_scraper import scrape_with_httpx
    
    try:
        logger.info(f"Starting scrape for URL: {str(request.url)}")
        
        # Use simple httpx-based scraper (Windows compatible)
        result = await scrape_with_httpx(str(request.url), request.wait_for)
        
        # Build response according to schema
        from datetime import datetime
        
        return schemas.UrlScrapeResponse(
            success=True,
            url=str(request.url),
            title=result.get('title'),
            content=result['content'],
            author=result.get('author'),
            published_date=result.get('published_date'),
            tables=result.get('tables', []),
            lists=result.get('lists', []),
            extracted_at=datetime.now().isoformat(),
            extraction_method=request.extract_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scraping error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )
