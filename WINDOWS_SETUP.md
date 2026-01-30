# Windows Setup Guide

Quick guide for running CrawlX Data Scraping Project on Windows.

## Prerequisites

1. **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   
2. **PostgreSQL** - [Download from postgresql.org](https://www.postgresql.org/download/windows/)
   - Remember the password you set during installation
   - Default port is 5432

3. **Git** (optional) - [Download from git-scm.com](https://git-scm.com/download/win)

## Setup Steps

### 1. Install Python Dependencies

Open Command Prompt or PowerShell:

```cmd
cd C:\path\to\CrawlX-Data-Scrapping-Project\backend
pip install -r requirements.txt
```

If you get SSL errors:
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 2. Setup PostgreSQL Database

Open **pgAdmin 4** or **psql**:

**Using pgAdmin:**
1. Right-click "Databases" → "Create" → "Database"
2. Name: `scraper_db`
3. Click "Save"

**Using psql Command Line:**
```cmd
psql -U postgres
CREATE DATABASE scraper_db;
\q
```

### 3. Configure Database Connection

Create a file named `.env` in the `backend` folder:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/scraper_db
PG_DB=scraper_db
PG_USER=postgres
PG_PASSWORD=YOUR_PASSWORD
PG_HOST=localhost
PG_PORT=5432
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### 4. Run Database Migration

```cmd
cd C:\path\to\CrawlX-Data-Scrapping-Project\backend
psql -U postgres -d scraper_db -f migrations\001_enable_fuzzy_search.sql
```

Or using pgAdmin:
1. Select `scraper_db` database
2. Click "Query Tool"
3. Open `migrations\001_enable_fuzzy_search.sql`
4. Click "Execute"

### 5. Start the Application

```cmd
cd C:\path\to\CrawlX-Data-Scrapping-Project\backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 6. Test the Application

Open your browser and go to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

Or use curl/PowerShell:
```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health

# Or install curl for Windows and use:
curl http://localhost:8000/health
```

## Common Windows Issues

### Issue: "pip is not recognized"

**Solution:**
```cmd
python -m pip install -r requirements.txt
```

### Issue: "psql is not recognized"

**Solution:**
Add PostgreSQL to PATH:
1. Search "Environment Variables" in Windows
2. Edit "Path" in System Variables
3. Add: `C:\Program Files\PostgreSQL\15\bin` (adjust version number)
4. Restart Command Prompt

### Issue: Port 8000 is already in use

**Solution:**
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number from above)
taskkill /PID <PID_NUMBER> /F

# Or use a different port
uvicorn main:app --reload --port 8001
```

### Issue: PostgreSQL Service Not Running

**Solution:**
1. Press `Win + R`, type `services.msc`
2. Find "postgresql-x64-15" (or your version)
3. Right-click → Start

Or use Command Prompt (as Administrator):
```cmd
net start postgresql-x64-15
```

### Issue: Import Error with psycopg2

**Solution:**
```cmd
pip uninstall psycopg2
pip install psycopg2-binary
```

## Development Workflow

### Start Development Server
```cmd
cd backend
uvicorn main:app --reload --port 8000
```

### Run Scrapers Manually
```powershell
# PowerShell
Invoke-WebRequest -Method POST -Uri "http://localhost:8000/scrape/run?spiders=news"

# Or with curl
curl -X POST "http://localhost:8000/scrape/run?spiders=news,jobs"
```

### View Logs
Logs appear in the terminal where you started uvicorn.

### Stop the Server
Press `Ctrl + C` in the terminal

## Using Virtual Environment (Recommended)

### Create Virtual Environment
```cmd
cd C:\path\to\CrawlX-Data-Scrapping-Project\backend
python -m venv venv
```

### Activate Virtual Environment
```cmd
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

If PowerShell gives an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Dependencies in Virtual Environment
```cmd
pip install -r requirements.txt
```

### Deactivate Virtual Environment
```cmd
deactivate
```

## Useful Tools

### API Testing
- **Postman** - [Download](https://www.postman.com/downloads/)
- **Insomnia** - [Download](https://insomnia.rest/download)
- Browser: http://localhost:8000/docs (built-in FastAPI docs)

### Database Management
- **pgAdmin 4** - Comes with PostgreSQL
- **DBeaver** - [Download](https://dbeaver.io/download/)

### Code Editor
- **VS Code** - [Download](https://code.visualstudio.com/)
  - Install Python extension
  - Install PostgreSQL extension

## Project Structure

```
CrawlX-Data-Scrapping-Project/
├── backend/                    # FastAPI application
│   ├── main.py                # Main application file
│   ├── crud.py                # Database operations
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── db.py                  # Database configuration
│   ├── scheduler.py           # Scraping scheduler
│   ├── pdf_export.py          # PDF generation
│   ├── summarizer.py          # Text summarization
│   ├── requirements.txt       # Python dependencies
│   └── migrations/            # Database migrations
│       └── 001_enable_fuzzy_search.sql
├── scraper/                   # Scrapy spiders
│   ├── scraper/
│   │   ├── spiders/
│   │   │   ├── news_spider.py
│   │   │   └── jobs_spider.py
│   │   ├── items.py
│   │   ├── pipelines.py
│   │   └── settings.py
│   └── scrapy.cfg
└── documentation files...
```

## Next Steps

1. ✅ Application is running
2. Test the API endpoints: http://localhost:8000/docs
3. Trigger a scrape: POST to `/scrape/run`
4. Export data as PDF: GET `/items/export/pdf`
5. Build your frontend!

## Getting Help

If you encounter issues:
1. Check `TROUBLESHOOTING.md`
2. Review terminal logs
3. Verify PostgreSQL is running
4. Ensure all dependencies are installed

---

Happy coding! 🚀
