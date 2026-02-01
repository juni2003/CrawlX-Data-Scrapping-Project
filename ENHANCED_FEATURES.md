# CrawlX Data Scraping Project - Enhanced Features

This document describes the enhanced features added to the CrawlX Data Scraping Project.

## Overview of Features

### 1. Multi-Source Scraping Orchestration ✅

The project now supports orchestrated scraping from multiple sources with flexible control.

#### Features:
- **Manual Trigger Endpoint**: `/scrape/run`
- **Selective Source Scraping**: Specify which spiders to run
- **Scheduled Scraping**: Automatic scraping at configurable intervals

#### Usage Examples:

```bash
# Run all configured spiders
POST http://localhost:8000/scrape/run

# Run specific spider(s)
POST http://localhost:8000/scrape/run?spiders=news
POST http://localhost:8000/scrape/run?spiders=news,jobs

# Response
{
  "status": "ok",
  "spiders": ["news", "jobs"],
  "message": "Successfully triggered 2 spider(s)"
}
```

#### Configuration:
Set spiders and interval in environment variables:
```env
SCRAPER_SPIDERS=news,jobs
SCRAPE_INTERVAL_HOURS=6
```

---

### 2. NLP Summarization ✅

Automatic text summarization for scraped content using the Sumy library.

#### Features:
- **Automatic Summary Generation**: Summaries created in the scraping pipeline
- **LSA Algorithm**: Uses Latent Semantic Analysis for intelligent summarization
- **Fallback Handling**: If summarization fails, uses title-based summary

#### Implementation:
- Pipeline: `SummarizerPipeline` in `scraper/pipelines.py`
- Utility: `backend/summarizer.py` for advanced summarization
- Currently generates basic summaries from title; can be extended to fetch and summarize full article content

---

### 3. Enhanced Search and Filtering ✅

Advanced search capabilities with tag filtering and fuzzy matching.

#### Tag Filtering

Filter items by tags using the JSONB containment operator:

```bash
# Get all items tagged with 'news'
GET http://localhost:8000/items?tag=news

# Get tech items
GET http://localhost:8000/items?tag=tech&limit=20
```

#### Enhanced Search

Search in both title and summary fields:

```bash
# Basic search
GET http://localhost:8000/search?q=python

# Search with tag filter
GET http://localhost:8000/search?q=ai&tag=tech

# Fuzzy search (requires pg_trgm extension)
GET http://localhost:8000/search?q=machine&fuzzy=true

# Fuzzy search with tag filter
GET http://localhost:8000/search?q=developer&tag=jobs&fuzzy=true
```

#### Database Setup for Fuzzy Search

Run the migration to enable pg_trgm extension:

```bash
psql -U postgres -d scraper_db -f backend/migrations/001_enable_fuzzy_search.sql
```

Or manually in PostgreSQL:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_scraped_items_title_trgm ON scraped_items USING gin (title gin_trgm_ops);
CREATE INDEX idx_scraped_items_summary_trgm ON scraped_items USING gin (summary gin_trgm_ops);
CREATE INDEX idx_scraped_items_tags ON scraped_items USING gin (tags);
```

---

### 4. PDF Export ✅

Export scraped items as formatted PDF documents.

#### Features:
- **Two Styles**: Detailed report or simple table format
- **Tag Filtering**: Export specific categories
- **Configurable Limit**: Control number of items
- **Professional Formatting**: Clean, readable PDF output

#### Usage Examples:

```bash
# Export all items in detailed format (default)
GET http://localhost:8000/items/export/pdf

# Export in simple table format
GET http://localhost:8000/items/export/pdf?style=simple

# Export with tag filter
GET http://localhost:8000/items/export/pdf?tag=news&limit=50

# Export specific number of items
GET http://localhost:8000/items/export/pdf?limit=100&style=detailed
```

#### PDF Styles:

1. **Detailed**: Full report with:
   - Title, source, URL
   - Summary and tags
   - Published and scraped dates
   - Professional formatting with sections

2. **Simple**: Table format with:
   - ID, Source, Title, Tags
   - Compact layout for quick reference

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status |
| `/health` | GET | Health check |
| `/items` | GET | List items (supports `?tag=`) |
| `/search` | GET | Search items (supports `?q=`, `?tag=`, `?fuzzy=`) |
| `/items/export` | GET | Export as JSON |
| `/items/export/csv` | GET | Export as CSV |
| `/items/export/pdf` | GET | Export as PDF (supports `?style=`, `?tag=`, `?limit=`) |
| `/scrape/run` | POST | Trigger manual scraping (supports `?spiders=`) |

---

## Installation

### 1. Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Scraper dependencies (if separate)
cd ../scraper
pip install scrapy python-dotenv psycopg2-binary
```

### 2. Setup Database

```bash
# Create database
createdb scraper_db

# Run migrations
psql -U postgres -d scraper_db -f backend/migrations/001_enable_fuzzy_search.sql
```

### 3. Configure Environment

Create `.env` file in both `backend/` and `scraper/` directories:

```env
# Database
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5433/scraper_db
PG_DB=scraper_db
PG_USER=postgres
PG_PASSWORD=yourpassword
PG_HOST=localhost
PG_PORT=5433

# Scraper
SCRAPER_SPIDERS=news,jobs
SCRAPE_INTERVAL_HOURS=6
```

### 4. Run the Application

```bash
# Start backend API
cd backend
uvicorn main:app --reload --port 8000

# Backend will automatically:
# - Create database tables
# - Start scheduled scraping
```

---

## Testing the Features

### Test Multi-Source Scraping

```bash
# Trigger scraping
curl -X POST "http://localhost:8000/scrape/run?spiders=news,jobs"

# Check if items were scraped
curl "http://localhost:8000/items?limit=10"
```

### Test Tag Filtering

```bash
# Get news items
curl "http://localhost:8000/items?tag=news"

# Get job items
curl "http://localhost:8000/items?tag=jobs"
```

### Test Search

```bash
# Basic search
curl "http://localhost:8000/search?q=python"

# Search with tag
curl "http://localhost:8000/search?q=developer&tag=jobs"

# Fuzzy search
curl "http://localhost:8000/search?q=machne&fuzzy=true"  # finds "machine"
```

### Test PDF Export

```bash
# Download PDF
curl "http://localhost:8000/items/export/pdf" -o items.pdf

# Download filtered PDF
curl "http://localhost:8000/items/export/pdf?tag=news&limit=20" -o news_items.pdf

# Download simple format
curl "http://localhost:8000/items/export/pdf?style=simple" -o items_table.pdf
```

---

## Development Notes

### Extending Summarization

To add full-text summarization from article URLs, modify the spiders:

```python
# In news_spider.py or jobs_spider.py
def parse_detail(self, response):
    # Extract full article text
    full_text = response.css('article p::text').getall()
    full_text = ' '.join(full_text)
    
    # Generate summary
    from backend.summarizer import summarize_text
    summary = summarize_text(full_text)
    
    item['summary'] = summary
    yield item
```

### Adding New Spiders

1. Create spider in `scraper/scraper/spiders/`
2. Add spider name to `SCRAPER_SPIDERS` environment variable
3. Spider will be included in automated and manual runs

### Performance Optimization

- GIN indexes are created for fast tag and fuzzy search queries
- Adjust `SENTENCES_COUNT` in `backend/summarizer.py` for longer/shorter summaries
- Configure `SCRAPE_INTERVAL_HOURS` based on content update frequency

---

## Dependencies

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- psycopg2-binary - PostgreSQL adapter
- sumy - Text summarization
- nltk - Natural language processing
- reportlab - PDF generation
- beautifulsoup4 - HTML parsing
- lxml - XML/HTML parser

### Scraper
- Scrapy - Web scraping framework
- psycopg2-binary - PostgreSQL adapter
- python-dotenv - Environment variables

---

## License

This project is part of the CrawlX Data Scraping Project.

---

## Support

For issues or questions, please refer to the main project repository.
