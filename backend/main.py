from fastapi import FastAPI, Depends, Query, HTTPException
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

app = FastAPI(title="Scraper Backend API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()


@app.get("/")
def root():
    return {"status": "ok", "message": "Scraper API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/items", response_model=list[schemas.ScrapedItemOut])
def list_items(
    skip: int = 0,
    limit: int = Query(50, le=200),
    tag: str = Query(None, description="Filter by tag (e.g., 'news', 'tech')"),
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
    spiders: str = Query(None, description="Comma-separated list of spider names (e.g., 'news,jobs')")
):
    """
    Manually trigger scraping for specified spiders.
    
    Examples:
    - /scrape/run - Run all configured spiders
    - /scrape/run?spiders=news - Run only news spider
    - /scrape/run?spiders=news,jobs - Run news and jobs spiders
    """
    if spiders:
        selected = [s.strip() for s in spiders.split(",") if s.strip()]
    else:
        selected = DEFAULT_SPIDERS

    if not selected:
        raise HTTPException(status_code=400, detail="No spiders specified")

    await run_spiders_async(selected)
    return {"status": "ok", "spiders": selected, "message": f"Successfully triggered {len(selected)} spider(s)"}
