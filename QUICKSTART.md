# Quick Start Guide - Enhanced Features

This guide will help you quickly set up and test the new enhanced features.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Setup Steps

### 1. Install Dependencies

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install Scrapy for the scraper
cd ../scraper
pip install scrapy python-dotenv psycopg2-binary
```

### 2. Setup Database

```bash
# Create the database
createdb scraper_db

# Enable pg_trgm extension for fuzzy search
psql -U postgres -d scraper_db -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# Run the migration script
psql -U postgres -d scraper_db -f backend/migrations/001_enable_fuzzy_search.sql
```

### 3. Configure Environment

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/scraper_db
PG_DB=scraper_db
PG_USER=postgres
PG_PASSWORD=yourpassword
PG_HOST=localhost
PG_PORT=5432
SCRAPER_SPIDERS=news,jobs
SCRAPE_INTERVAL_HOURS=6
```

Create a `.env` file in the `scraper` directory with the same database settings.

### 4. Start the API Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Testing the Features

### Test 1: Check API Health

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{"status": "healthy"}
```

### Test 2: Trigger Manual Scraping

```bash
# Run all spiders
curl -X POST "http://localhost:8000/scrape/run"

# Run specific spider
curl -X POST "http://localhost:8000/scrape/run?spiders=news"
```

Expected output:
```json
{
  "status": "ok",
  "spiders": ["news"],
  "message": "Successfully triggered 1 spider(s)"
}
```

### Test 3: List Items

```bash
# Get all items
curl "http://localhost:8000/items?limit=5"

# Get items by tag
curl "http://localhost:8000/items?tag=news&limit=5"
```

### Test 4: Search Items

```bash
# Basic search
curl "http://localhost:8000/search?q=python&limit=5"

# Search with tag filter
curl "http://localhost:8000/search?q=developer&tag=jobs"

# Fuzzy search
curl "http://localhost:8000/search?q=machne&fuzzy=true"
```

### Test 5: Export as PDF

```bash
# Export detailed PDF
curl "http://localhost:8000/items/export/pdf?limit=10" -o items.pdf

# Export simple table
curl "http://localhost:8000/items/export/pdf?style=simple&limit=20" -o items_table.pdf

# Export filtered by tag
curl "http://localhost:8000/items/export/pdf?tag=news&limit=15" -o news.pdf
```

### Test 6: Check Summaries

```bash
# Get items and check if they have summaries
curl "http://localhost:8000/items?limit=5" | jq '.[].summary'
```

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly in your browser.

## Common Issues

### Issue: "pg_trgm extension not found"

**Solution**: Enable the extension manually:
```bash
psql -U postgres -d scraper_db -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
```

### Issue: "No items found"

**Solution**: Trigger scraping first:
```bash
curl -X POST "http://localhost:8000/scrape/run"
```
Wait a few minutes for the spiders to complete, then check again.

### Issue: "Database connection failed"

**Solution**: Verify your `.env` file settings match your PostgreSQL configuration.

### Issue: "Module not found"

**Solution**: Make sure all dependencies are installed:
```bash
pip install -r backend/requirements.txt
```

## Next Steps

1. **Customize Spiders**: Add more spiders in `scraper/scraper/spiders/`
2. **Extend Summarization**: Modify spiders to fetch full article text for better summaries
3. **Add Frontend**: Build a frontend to visualize the data
4. **Schedule Scraping**: The scheduler runs automatically every 6 hours (configurable)

## Using the Python Example Script

```bash
# Run the example script
cd examples
python3 api_usage.py
```

This will show all available endpoints and test basic connectivity.

## API Endpoints Reference

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/health` | GET | - | Health check |
| `/items` | GET | `tag`, `limit`, `skip` | List items with optional tag filter |
| `/search` | GET | `q`, `tag`, `fuzzy`, `limit` | Search with query and optional filters |
| `/items/export/pdf` | GET | `style`, `tag`, `limit` | Export as PDF |
| `/items/export/csv` | GET | - | Export as CSV |
| `/items/export` | GET | - | Export as JSON |
| `/scrape/run` | POST | `spiders` | Trigger manual scraping |

For detailed documentation, see `ENHANCED_FEATURES.md`.

## Support

For more information, refer to:
- `ENHANCED_FEATURES.md` - Complete feature documentation
- `http://localhost:8000/docs` - Interactive API documentation
