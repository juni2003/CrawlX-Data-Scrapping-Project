# 🚀 CrawlX - Advanced Web Scraping Platform

<div align="center">

![CrawlX Logo](https://img.shields.io/badge/CrawlX-Data%20Scraping-6366f1?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791?style=flat-square&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)

**Scrape any website with AI-powered extraction, beautiful UI, and 3D effects**

[Features](#-features) • [Quick Start](#-quick-start-2-minutes) • [Documentation](#-documentation) • [Screenshots](#-screenshots)

</div>

---

## 🎯 What is CrawlX?

CrawlX is a **modern, full-stack web scraping platform** that combines powerful backend scraping capabilities with a stunning Next.js frontend featuring 3D effects and dark mode.

### Why CrawlX?

- ✅ **Scrape ANY website** - Custom URL scraper with anti-bot detection
- ✅ **Smart extraction** - Auto-detect best method for each site
- ✅ **Pre-configured scrapers** - Built-in support for Hacker News & RemoteOK
- ✅ **Beautiful UI** - Modern Next.js 14 with Three.js 3D effects
- ✅ **Dark mode** - Seamless theme switching
- ✅ **Export data** - JSON, CSV, or PDF formats
- ✅ **Fuzzy search** - Find content even with typos
- ✅ **Real-time stats** - Live dashboard with metrics

---

## ✨ Features

### 🌐 Backend (FastAPI + Scrapy)
- **Custom URL Scraper**
  - Playwright-based browser automation
  - Anti-bot detection bypass
  - Multiple extraction modes (auto, article, text, structured)
  - Handles dynamic content & JavaScript
  
- **Pre-configured Scrapers**
  - Hacker News (latest tech news)
  - RemoteOK (remote job listings)
  
- **Advanced Search**
  - PostgreSQL full-text search
  - Fuzzy matching with trigram similarity
  - Tag-based filtering
  
- **Export Options**
  - JSON (raw data)
  - CSV (spreadsheet)
  - PDF (styled reports)

### 🎨 Frontend (Next.js 14)
- **3D Effects**
  - Animated particle background (Three.js)
  - Floating cards with glow effects
  - Glassmorphism design
  
- **Three Main Pages**
  1. **Dashboard** - Stats, quick actions, navigation
  2. **Custom Scraper** - Enter any URL and scrape it
  3. **Data Explorer** - Browse, search, export data
  
- **Modern UX**
  - Dark/Light mode with persistence
  - Responsive design (mobile, tablet, desktop)
  - Smooth animations (Framer Motion)
  - Copy/download functionality
  - Real-time loading states

---

## 🚀 Quick Start (2 Minutes)

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Node.js 18+
- npm

### 1️⃣ Clone & Setup Backend
```bash
# Clone repository
cd backend

# Install dependencies
pip install -r requirements.txt

# Install browser for scraping
python -m playwright install chromium

# Create .env file
echo DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/crawlx > .env

# Create database
createdb crawlx
```

### 2️⃣ Setup Frontend
```bash
cd frontend

# Install dependencies (takes 1-2 minutes)
npm install
```

### 3️⃣ Run Everything
**Option A: Using Scripts (Windows)**
```bash
# Double-click start-all.bat
# OR run from command line:
start-all.bat
```

**Option B: Manual Start**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4️⃣ Open in Browser
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000

---

## 📚 Documentation

### Complete Guides
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Detailed setup with troubleshooting
- **[FRONTEND_IMPLEMENTATION.md](FRONTEND_IMPLEMENTATION.md)** - Frontend architecture & features
- **[CUSTOM_URL_SCRAPER.md](CUSTOM_URL_SCRAPER.md)** - Custom scraper usage guide
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation

### Quick References
- **API Documentation**: http://localhost:8000/docs (interactive Swagger UI)
- **Database Schema**: See `backend/models.py`
- **TypeScript Types**: See `frontend/types/index.ts`

---

## 📸 Screenshots

### Dashboard
Modern dashboard with real-time statistics and quick actions.

```
┌─────────────────────────────────────────┐
│  ⚡ Total Items        📊 Today's Scrapes│
│     1,234 items            45 today     │
│                                         │
│  📰 News Articles      💼 Job Listings  │
│     856 articles          378 jobs      │
│                                         │
│  [Run Scrapers Now]                     │
└─────────────────────────────────────────┘
```

### Custom URL Scraper
Scrape any website with smart content extraction.

```
┌─────────────────────────────────────────┐
│  Enter URL: [https://example.com    ]  │
│  Mode: [Auto ▼]   Wait: ●──────── 2s   │
│  [Scrape URL]                           │
│                                         │
│  ✓ Scraped successfully!                │
│  Title: Example Page                    │
│  Content: Lorem ipsum...                │
│  [Copy] [Download]                      │
└─────────────────────────────────────────┘
```

### Data Explorer
Browse and export your scraped data.

```
┌─────────────────────────────────────────┐
│  [🔍 Search] [Tags ▼] [Export ▼]        │
│  ☑ Fuzzy search                         │
│  ┌───────────────────────────────────┐ │
│  │ Title    │ Source │ Tags │ Time   │ │
│  │ Item 1   │ News   │ tech │ 2h ago │ │
│  │ Item 2   │ Jobs   │ dev  │ 5h ago │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.115.8 | REST API framework |
| PostgreSQL | 12+ | Data storage |
| Scrapy | 2.12.0 | Scraping framework |
| Playwright | 1.40.0 | Browser automation |
| Trafilatura | 1.12.2 | Content extraction |
| SQLAlchemy | 2.0.37 | ORM |
| NLTK + Sumy | Latest | Summarization |
| ReportLab | 4.2.5 | PDF generation |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.2.0 | React framework |
| TypeScript | 5.3.0 | Type safety |
| Tailwind CSS | 3.4.0 | Styling |
| Three.js | 0.160.0 | 3D graphics |
| @react-three/fiber | 8.15.0 | React Three.js |
| Framer Motion | 11.0.0 | Animations |
| Axios | 1.6.0 | HTTP client |
| Zustand | 4.5.0 | State management |
| date-fns | 3.0.0 | Date formatting |

---

## 📁 Project Structure

```
CrawlX-Data-Scrapping-Project/
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── models.py              # Database models
│   ├── crud.py                # Database operations
│   ├── schemas.py             # Pydantic schemas
│   ├── scraper_engine/        # Custom URL scraper
│   │   ├── browser_pool.py   # Playwright browser manager
│   │   ├── stealth.py        # Anti-bot detection
│   │   └── extractors.py     # Content extraction logic
│   ├── scraper/              # Scrapy project
│   │   └── spiders/
│   │       ├── news_spider.py
│   │       └── jobs_spider.py
│   └── requirements.txt
├── frontend/                  # Next.js frontend
│   ├── app/                  # Pages (App Router)
│   │   ├── page.tsx         # Dashboard
│   │   ├── scraper/         # Custom scraper page
│   │   └── data/            # Data explorer page
│   ├── components/
│   │   ├── 3d/              # Three.js components
│   │   ├── layout/          # Navbar, etc.
│   │   └── providers/       # Theme provider
│   ├── lib/
│   │   └── api.ts           # API client
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   └── package.json
├── start-all.bat             # Quick start script (Windows)
├── start-backend.bat         # Backend only
├── start-frontend.bat        # Frontend only
└── README.md                 # This file
```

---

## 🎯 Usage Examples

### Scrape Hacker News
```bash
# Using API
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '["news"]'

# OR use the UI
# 1. Go to Dashboard
# 2. Click "Run Scrapers"
# 3. View results in Data Explorer
```

### Scrape Custom URL
```bash
# Using API
curl -X POST "http://localhost:8000/scrape/url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "extract_type": "auto",
    "wait_seconds": 2
  }'

# OR use the UI
# 1. Go to Custom Scraper page
# 2. Enter URL
# 3. Select extraction mode
# 4. Click "Scrape URL"
```

### Search Data
```bash
# Fuzzy search via API
curl "http://localhost:8000/search?q=pythn&fuzzy=true&limit=10"

# OR use the UI
# 1. Go to Data Explorer
# 2. Enter search term
# 3. Enable "Fuzzy search"
# 4. Click "Search"
```

### Export Data
```bash
# Export to CSV
curl "http://localhost:8000/export/csv" -o data.csv

# Export to PDF
curl -X POST "http://localhost:8000/export/pdf" \
  -H "Content-Type: application/json" \
  -d '{"style": "detailed", "limit": 100}' \
  -o data.pdf

# OR use the UI
# 1. Go to Data Explorer
# 2. Click "Export CSV" or "Export PDF"
```

---

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/crawlx
```

### Database Connection Pool
```python
# backend/db.py
pool_size=10          # Concurrent connections
max_overflow=20       # Additional connections
pool_pre_ping=True    # Check connection health
pool_recycle=3600     # Recycle after 1 hour
```

### Frontend (lib/api.ts)
```typescript
const API_BASE = 'http://localhost:8000';
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Test health endpoint
curl http://localhost:8000/

# Test custom scraper
curl -X POST http://localhost:8000/scrape/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://books.toscrape.com", "extract_type": "auto", "wait_seconds": 2}'

# Test pre-configured scrapers
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '["news", "jobs"]'
```

### Frontend Tests
```bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

### Manual Testing Checklist
- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Dashboard displays stats
- [ ] Custom URL scraper works
- [ ] Pre-configured scrapers work
- [ ] Search functionality works
- [ ] Fuzzy search finds typos
- [ ] Export CSV/PDF works
- [ ] Dark/light mode switches
- [ ] 3D background animates
- [ ] Mobile responsive

---

## 🐛 Troubleshooting

### Backend Issues

**Database connection failed**
```bash
# Check if PostgreSQL is running
pg_isready

# Create database
createdb crawlx

# Verify connection string in .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/crawlx
```

**Playwright browser not found**
```bash
# Install Chromium
python -m playwright install chromium
```

**Port already in use**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**npm install fails**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**3D background not rendering**
- Check browser console for WebGL errors
- Ensure browser supports WebGL
- Try disabling hardware acceleration

**API connection refused**
- Ensure backend is running on http://localhost:8000
- Check CORS settings in `backend/main.py`
- Verify firewall isn't blocking port

### Database Issues

**Connection pool exhausted**
```bash
# Restart backend server
# Check for hanging connections in PostgreSQL
```

**Fuzzy search not working**
```bash
# Run migration to enable trigram extension
psql -U postgres -d crawlx -f backend/migrations/001_enable_fuzzy_search.sql
```

---

## 🚀 Deployment

### Backend (Production)
```bash
# Install production server
pip install gunicorn

# Run with multiple workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Production)
```bash
# Build for production
npm run build

# Start production server
npm start

# OR export static files
npm run build && npx next export
```

### Environment Variables (Production)
```env
# Backend
DATABASE_URL=postgresql://user:password@db-server:5432/crawlx
ALLOWED_ORIGINS=https://yourdomain.com

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## 📊 Database Schema

### scraped_items
```sql
CREATE TABLE scraped_items (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    content TEXT,
    summary TEXT,
    tags TEXT[],
    source VARCHAR(50),
    metadata JSONB,
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tags ON scraped_items USING GIN(tags);
CREATE INDEX idx_source ON scraped_items(source);
CREATE INDEX idx_scraped_at ON scraped_items(scraped_at);
```

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

This project is for educational purposes. Feel free to use and modify!

---

## 🆘 Support

Having issues? Check these resources:

1. **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Comprehensive setup guide
2. **[API Documentation](http://localhost:8000/docs)** - Interactive API explorer
3. **Browser Console** - Check for frontend errors
4. **Backend Logs** - Check terminal output for errors

---

## 🎉 Success Checklist

Before considering setup complete, verify:

✅ PostgreSQL is running  
✅ Database `crawlx` exists  
✅ Backend starts without errors at http://localhost:8000  
✅ `/docs` endpoint shows API documentation  
✅ Frontend loads at http://localhost:3000  
✅ Dashboard displays stats  
✅ Custom URL scraper works (test with https://books.toscrape.com)  
✅ Pre-configured scrapers work  
✅ Data Explorer shows items  
✅ Search functionality works  
✅ Export CSV/PDF works  
✅ Dark/light mode switches correctly  
✅ 3D particle background animates  

**All checked?** Congratulations! 🎊 CrawlX is fully operational!

---

## 📈 Roadmap

Future improvements:

- [ ] User authentication & authorization
- [ ] Scheduled scraping (cron jobs)
- [ ] Webhook notifications
- [ ] More pre-configured scrapers
- [ ] Proxy support for scraping
- [ ] API rate limiting
- [ ] Pagination for large datasets
- [ ] Advanced filters in Data Explorer
- [ ] Real-time scraping status (WebSockets)
- [ ] Docker containerization
- [ ] Kubernetes deployment configs

---

<div align="center">

**Made with ❤️ for web scraping enthusiasts**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/yourusername/crawlx/issues) • [Request Feature](https://github.com/yourusername/crawlx/issues)

</div>
