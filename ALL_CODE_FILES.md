# All Code Files - Ready to Copy

This document contains all the code files you need for the enhanced features. You can copy these directly into your project.

---

## 1. backend/requirements.txt

```
fastapi==0.115.8
uvicorn==0.30.6
SQLAlchemy==2.0.37
psycopg2-binary==2.9.9
pydantic==2.10.6
python-dotenv==1.0.1
sumy==0.11.0
nltk>=3.9
reportlab==4.0.9
beautifulsoup4==4.12.3
lxml==5.1.0
numpy>=1.24.0
```

---

## 2. backend/summarizer.py

```python
"""
Text summarization utility using sumy library.
"""
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os

# Download required NLTK data on first import
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

LANGUAGE = "english"
SENTENCES_COUNT = 3  # Number of sentences in summary


def summarize_text(text: str, sentences_count: int = SENTENCES_COUNT) -> str:
    """
    Summarize text using LSA (Latent Semantic Analysis) algorithm.
    
    Args:
        text: The text to summarize
        sentences_count: Number of sentences to include in summary
        
    Returns:
        Summarized text as a string
    """
    if not text or len(text.strip()) < 50:
        return text  # Return original if too short
    
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        summary_sentences = summarizer(parser.document, sentences_count)
        summary = " ".join(str(sentence) for sentence in summary_sentences)
        
        return summary if summary else text
    except Exception as e:
        # If summarization fails, return original text
        print(f"Summarization error: {e}")
        return text


def generate_summary_from_url(url: str, title: str = "") -> str:
    """
    Generate a basic summary from URL and title.
    This is a fallback when full text is not available.
    
    Args:
        url: The URL of the content
        title: The title of the content
        
    Returns:
        A simple summary string
    """
    if title:
        return f"Article: {title}"
    return f"Content from: {url}"
```

---

## 3. backend/pdf_export.py

```python
"""
PDF export utility using ReportLab.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from datetime import datetime
from typing import List


def generate_items_pdf(items: List, title: str = "Scraped Items Report") -> BytesIO:
    """
    Generate a PDF report from scraped items.
    
    Args:
        items: List of ScrapedItem objects
        title: Title for the PDF report
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#444444')
    )
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary statistics
    elements.append(Paragraph(f"Total Items: {len(items)}", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Process each item
    for idx, item in enumerate(items, 1):
        # Item header
        item_title = f"{idx}. {item.title[:100]}..." if len(item.title) > 100 else f"{idx}. {item.title}"
        elements.append(Paragraph(item_title, heading_style))
        
        # Item details
        data = [
            ["Source:", str(item.source)],
            ["URL:", Paragraph(str(item.url)[:80] + "..." if len(str(item.url)) > 80 else str(item.url), normal_style)],
        ]
        
        if item.summary:
            summary_text = str(item.summary)[:200] + "..." if len(str(item.summary)) > 200 else str(item.summary)
            data.append(["Summary:", Paragraph(summary_text, normal_style)])
        
        if item.tags:
            tags_str = ", ".join(item.tags) if isinstance(item.tags, list) else str(item.tags)
            data.append(["Tags:", tags_str])
        
        if item.published_at:
            data.append(["Published:", str(item.published_at.strftime('%Y-%m-%d %H:%M'))])
        
        data.append(["Scraped:", str(item.scraped_at.strftime('%Y-%m-%d %H:%M'))])
        
        # Create table for item details
        t = Table(data, colWidths=[1.2*inch, 5.8*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add page break every 3 items to avoid overflow
        if idx % 3 == 0 and idx < len(items):
            elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    buffer.seek(0)
    return buffer


def generate_simple_table_pdf(items: List) -> BytesIO:
    """
    Generate a simple table-based PDF report.
    
    Args:
        items: List of ScrapedItem objects
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("Scraped Items Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Prepare table data
    data = [['ID', 'Source', 'Title', 'Tags']]
    
    for item in items:
        tags_str = ", ".join(item.tags[:2]) if item.tags and isinstance(item.tags, list) else ""
        title_short = item.title[:50] + "..." if len(item.title) > 50 else item.title
        data.append([
            str(item.id),
            str(item.source),
            title_short,
            tags_str
        ])
    
    # Create table
    t = Table(data, colWidths=[0.5*inch, 1.5*inch, 3.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
```

---

## 4. backend/crud.py (Complete Updated File)

```python
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
```

---

## 5. backend/main.py (Complete Updated File)

```python
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
```

---

## 6. scraper/scraper/pipelines.py (Complete Updated File)

```python
import os
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()


class SummarizerPipeline:
    """Pipeline to generate summaries for items."""
    
    def process_item(self, item, spider):
        # Generate a basic summary from title if summary is not present
        if not item.get("summary"):
            title = item.get("title", "")
            source = item.get("source", "")
            if title:
                item["summary"] = f"{source}: {title}"
        return item


class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname=os.getenv("PG_DB", "scraper_db"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "yourpassword"),
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5433"),
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """
                INSERT INTO scraped_items (source, title, url, summary, tags, published_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
                """,
                (
                    item.get("source"),
                    item.get("title"),
                    item.get("url"),
                    item.get("summary"),
                    Json(item.get("tags") or []),  # ✅ proper JSON
                    item.get("published_at"),
                ),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return item
```

---

## 7. scraper/scraper/settings.py (Complete Updated File)

```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scraper.pipelines.SummarizerPipeline": 200,
    "scraper.pipelines.PostgresPipeline": 300,
}

LOG_LEVEL = "INFO"
```

---

## 8. backend/migrations/001_enable_fuzzy_search.sql

```sql
-- Enable PostgreSQL pg_trgm extension for fuzzy text search
-- This extension provides functions and operators for determining the similarity of text based on trigram matching

-- Create the extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create GIN index on title for faster fuzzy search
CREATE INDEX IF NOT EXISTS idx_scraped_items_title_trgm ON scraped_items USING gin (title gin_trgm_ops);

-- Create GIN index on summary for faster fuzzy search
CREATE INDEX IF NOT EXISTS idx_scraped_items_summary_trgm ON scraped_items USING gin (summary gin_trgm_ops);

-- Create GIN index on tags for faster tag filtering
CREATE INDEX IF NOT EXISTS idx_scraped_items_tags ON scraped_items USING gin (tags);
```

---

## Installation Instructions

1. **Copy all the files above** to your project in the correct locations

2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run database migration**:
   ```bash
   psql -U postgres -d scraper_db -f backend/migrations/001_enable_fuzzy_search.sql
   ```

4. **Start the API**:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

5. **Test the features**:
   ```bash
   # Check health
   curl http://localhost:8000/health
   
   # Trigger scraping
   curl -X POST "http://localhost:8000/scrape/run"
   
   # Get items by tag
   curl "http://localhost:8000/items?tag=news"
   
   # Search
   curl "http://localhost:8000/search?q=python"
   
   # Export PDF
   curl "http://localhost:8000/items/export/pdf" -o items.pdf
   ```

---

## Additional Documentation

See these files for more details:
- `ENHANCED_FEATURES.md` - Complete feature documentation
- `QUICKSTART.md` - Quick start guide
- `IMPLEMENTATION_SUMMARY.md` - Implementation details

All files are available in the `feature/enhanced-features` branch!
