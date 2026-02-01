# CrawlX - Complete Setup Guide

## 🎯 What is CrawlX?

CrawlX is a powerful web scraping platform with:
- **Pre-configured scrapers** for Hacker News and RemoteOK jobs
- **Custom URL scraper** that can scrape ANY website with anti-bot detection
- **Smart content extraction** with multiple modes (auto, article, text, structured)
- **Modern Next.js frontend** with 3D effects and dark mode
- **PostgreSQL database** for data storage
- **Export functionality** (JSON, CSV, PDF)

## 📋 Prerequisites

Before running CrawlX, ensure you have:
- ✅ Python 3.11+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ Node.js 18+ and npm installed
- ✅ Git (optional, for version control)

## 🚀 Quick Start (5 Minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser (required for custom URL scraper)
python -m playwright install chromium

# Create .env file
# Copy this content into backend/.env:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/crawlx
```

**Important**: Replace `your_password` with your actual PostgreSQL password!

### Step 2: Database Setup

```bash
# Create database (run in PostgreSQL)
createdb crawlx

# OR use psql:
psql -U postgres -c "CREATE DATABASE crawlx;"
```

### Step 3: Start Backend

```bash
# In backend directory
uvicorn main:app --reload

# Should see:
# INFO: Uvicorn running on http://127.0.0.1:8000
```

Test it: Open http://localhost:8000/docs to see the interactive API documentation.

### Step 4: Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Should see:
# ▲ Next.js 14.x.x
# Local: http://localhost:3000
```

Open http://localhost:3000 in your browser!

## 🎨 Using CrawlX

### Dashboard (http://localhost:3000)
- View statistics (total items, today's scrapes, etc.)
- Click "Run Scrapers" to scrape Hacker News and RemoteOK
- Navigate to Custom Scraper or Data Explorer

### Custom URL Scraper (http://localhost:3000/scraper)
1. Enter any website URL (e.g., https://books.toscrape.com)
2. Choose extraction mode:
   - **Auto**: Smart detection
   - **Article**: For news/blogs
   - **Text**: All visible text
   - **Structured**: Tables & lists
3. Adjust wait time (1-10 seconds for slow sites)
4. Click "Scrape URL"
5. Copy or download results

### Data Explorer (http://localhost:3000/data)
- Search scraped content (with fuzzy search)
- Filter by tags (news, tech, jobs, remote)
- Export to CSV or PDF
- View full details with source links

## 🔧 Troubleshooting

### Backend Won't Start

**Error**: `FATAL: database "crawlx" does not exist`
```bash
createdb crawlx
```

**Error**: `connection to server at "localhost" (::1), port 5432 failed`
- PostgreSQL is not running
- Start it: `sudo systemctl start postgresql` (Linux) or `pg_ctl start` (Windows)

**Error**: `DETAIL: role "postgres" does not exist`
- Create PostgreSQL user:
```bash
psql -c "CREATE USER postgres WITH PASSWORD 'your_password' SUPERUSER;"
```

### Custom URL Scraper Not Working

**Error**: `Browser not installed`
```bash
python -m playwright install chromium
```

**Error**: `Scraping failed`
- Check if the website blocks bots
- Try increasing wait time to 5-10 seconds
- Some sites use aggressive anti-bot protection

### Frontend Won't Connect

**Error**: `Network Error` or `ERR_CONNECTION_REFUSED`
- Ensure backend is running on http://localhost:8000
- Check CORS settings in `backend/main.py`
- Verify firewall isn't blocking port 8000

### Database Connection Pool Exhausted

**Error**: `QueuePool limit exceeded`
- Restart backend server
- Check for hanging database connections:
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'crawlx';
```

## 📚 API Documentation

### Health Check
```bash
GET http://localhost:8000/
Response: {"message": "CrawlX API is running"}
```

### Get All Items
```bash
GET http://localhost:8000/items?limit=10&tag=news
```

### Search Items
```bash
GET http://localhost:8000/search?q=python&fuzzy=true
```

### Run Pre-configured Scrapers
```bash
POST http://localhost:8000/scrape
Body: ["news", "jobs"]
```

### Custom URL Scraper
```bash
POST http://localhost:8000/scrape/url
Body: {
  "url": "https://example.com",
  "extract_type": "auto",
  "wait_seconds": 2
}
```

### Export Data
```bash
GET http://localhost:8000/export/json
GET http://localhost:8000/export/csv
POST http://localhost:8000/export/pdf
```

Full interactive docs: http://localhost:8000/docs

## 📁 Project Structure

```
CrawlX-Data-Scrapping-Project/
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── models.py              # Database models
│   ├── crud.py                # Database operations
│   ├── scraper_engine/        # Custom URL scraper
│   │   ├── browser_pool.py
│   │   ├── stealth.py
│   │   └── extractors.py
│   ├── scraper/               # Scrapy project
│   │   └── spiders/
│   │       ├── news_spider.py
│   │       └── jobs_spider.py
│   ├── requirements.txt
│   └── .env                   # Database config
├── frontend/                   # Next.js frontend
│   ├── app/                   # Pages
│   │   ├── page.tsx          # Dashboard
│   │   ├── scraper/page.tsx  # Custom scraper
│   │   └── data/page.tsx     # Data explorer
│   ├── components/
│   │   ├── 3d/               # Three.js effects
│   │   ├── layout/           # Navbar, etc.
│   │   └── providers/        # Theme provider
│   ├── lib/api.ts            # API client
│   └── package.json
└── README.md                  # This file
```

## 🎯 Common Use Cases

### Scrape Hacker News
1. Go to Dashboard
2. Click "Run Scrapers"
3. Wait ~10 seconds
4. Go to Data Explorer
5. Filter by tag: "news"

### Scrape Custom Website
1. Go to Custom Scraper
2. Enter URL: `https://example.com`
3. Choose extraction mode
4. Click "Scrape URL"
5. View results

### Export All Data
1. Go to Data Explorer
2. Click "Export CSV" or "Export PDF"
3. File downloads automatically

### Search Scraped Content
1. Go to Data Explorer
2. Enter search term
3. Enable "Fuzzy search" for typo tolerance
4. Click "Search"

## 🔐 Security Notes

- **Database**: Change default PostgreSQL password
- **API**: Add authentication for production use
- **CORS**: Restrict allowed origins in production
- **Environment**: Never commit `.env` files
- **Rate Limiting**: Add rate limits for scraping endpoints

## 📊 Database Schema

### scraped_items table
- `id`: Primary key
- `url`: Source URL
- `title`: Item title
- `content`: Full content
- `summary`: AI-generated summary
- `tags`: Array of tags
- `source`: Scraper source
- `metadata`: JSON metadata
- `scraped_at`: Timestamp

## 🚀 Production Deployment

### Backend
```bash
# Use production ASGI server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build for production
npm run build

# Start production server
npm start
```

### Database
- Use PostgreSQL connection pooling
- Set up regular backups
- Configure proper indexes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

This project is for educational purposes.

## 🆘 Getting Help

- **Backend API Docs**: http://localhost:8000/docs
- **Frontend Errors**: Check browser console
- **Database Issues**: Check PostgreSQL logs
- **Scraper Issues**: Check `CUSTOM_URL_SCRAPER.md`

## 🎉 Success Checklist

✅ PostgreSQL running
✅ Backend starts without errors
✅ Frontend loads at http://localhost:3000
✅ Dashboard shows stats
✅ Custom URL scraper works
✅ Data explorer displays items
✅ Export functionality works

**Congratulations!** CrawlX is fully operational! 🎊
