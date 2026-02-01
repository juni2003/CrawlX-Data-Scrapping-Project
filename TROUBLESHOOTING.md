# Troubleshooting Guide

This guide helps you resolve common issues when running the CrawlX Data Scraping Project.

## Issue 1: Import Error When Starting Uvicorn ✅ FIXED

### Symptoms
When running `uvicorn main:app --reload --port 8000`, you see:
```
ImportError: attempted relative import with no known parent package
```

### Root Cause
The backend files were using relative imports (e.g., `from .db import ...`) but the directory was not set up as a Python package.

### Solution
**This has been fixed in the latest commit!** The imports have been converted from relative to absolute.

**What was changed:**
- `from .db import SessionLocal` → `from db import SessionLocal`
- `from .models import Base` → `from models import Base`
- `from . import crud, schemas` → `import crud, schemas`
- And similar changes in all backend files

**Verification:**
```bash
cd backend
python3 -c "import main; print('✓ Import successful')"
```

---

## Issue 2: Database Connection Error

### Symptoms
After fixing imports, you see:
```
psycopg2.OperationalError: connection to server at "localhost", port 5433 failed
```

### Root Cause
PostgreSQL database is not running or not accessible on the specified port.

### Solution

#### Option 1: Start PostgreSQL (Recommended)
```bash
# On Windows
# Make sure PostgreSQL service is running in Services

# On Linux/Mac
sudo systemctl start postgresql
# or
sudo service postgresql start
```

#### Option 2: Update Database Configuration
Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql+psycopg2://USERNAME:PASSWORD@localhost:PORT/DATABASE_NAME

# Example:
# DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/scraper_db
```

Replace:
- `USERNAME` - Your PostgreSQL username (default: `postgres`)
- `PASSWORD` - Your PostgreSQL password
- `PORT` - PostgreSQL port (default: `5432`, not `5433`)
- `DATABASE_NAME` - Database name (default: `scraper_db`)

#### Option 3: Create the Database
```bash
# Using psql command line
createdb scraper_db

# Or connect to PostgreSQL and run:
psql -U postgres
CREATE DATABASE scraper_db;
\q
```

---

## Issue 3: Missing Dependencies

### Symptoms
```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'apscheduler'
```

### Solution
Install all required dependencies:

```bash
cd backend
pip install -r requirements.txt

# If requirements.txt is incomplete, install these manually:
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
pip install sumy nltk reportlab beautifulsoup4 lxml numpy
pip install apscheduler

# For the scraper:
pip install scrapy
```

---

## Issue 4: Port Already in Use

### Symptoms
```
OSError: [WinError 10048] Only one usage of each socket address
```

### Solution

#### Option 1: Use a Different Port
```bash
uvicorn main:app --reload --port 8001
```

#### Option 2: Kill the Process Using Port 8000
**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Issue 5: Scrapy Not Finding Spiders

### Symptoms
When triggering `/scrape/run`, spiders don't execute or error occurs.

### Solution
Make sure you're in the correct directory structure:
```
CrawlX-Data-Scrapping-Project/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
└── scraper/
    ├── scraper/
    │   ├── spiders/
    │   │   ├── news_spider.py
    │   │   └── jobs_spider.py
    │   └── ...
    └── scrapy.cfg
```

Update `backend/scheduler.py` if needed:
```python
SCRAPER_PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "scraper")
)
```

---

## Quick Start Checklist

Before running the application:

- [ ] PostgreSQL is installed and running
- [ ] Database `scraper_db` exists
- [ ] All Python dependencies are installed (`pip install -r requirements.txt`)
- [ ] `.env` file is configured (if using custom database settings)
- [ ] Port 8000 is available

**Start the application:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Verify it's working:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## Common Commands

### Start Development Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Start Production Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Run Database Migration
```bash
psql -U postgres -d scraper_db -f backend/migrations/001_enable_fuzzy_search.sql
```

### Test Imports
```bash
cd backend
python3 -c "import main; print('Success!')"
```

### Trigger Manual Scraping
```bash
curl -X POST "http://localhost:8000/scrape/run?spiders=news,jobs"
```

---

## Getting Help

If you encounter issues not covered here:

1. Check the FastAPI interactive docs: `http://localhost:8000/docs`
2. Review the logs in the terminal where uvicorn is running
3. Ensure all dependencies are installed: `pip list`
4. Check PostgreSQL is running: `pg_isready` (Linux/Mac) or Services (Windows)

---

## System Requirements

- Python 3.8 or higher
- PostgreSQL 12 or higher
- 2GB+ RAM
- Windows 10/11, Linux, or macOS

---

Last Updated: 2026-01-30
