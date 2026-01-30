# CrawlX Data Scraping Project

A comprehensive data scraping platform with multi-source orchestration, NLP summarization, advanced search, and PDF export capabilities.

## 🚀 Quick Start

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide (5 minutes)
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Complete Windows setup instructions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues
- **[ENHANCED_FEATURES.md](ENHANCED_FEATURES.md)** - Complete feature documentation
- **[SECURITY.md](SECURITY.md)** - Security information and best practices

## ✨ Features

### 1. Multi-Source Scraping
- Orchestrate multiple scrapers (news, jobs, etc.)
- Scheduled automatic scraping
- Manual trigger via API endpoint

### 2. NLP Summarization
- Automatic text summarization using LSA algorithm
- Integrated in scraping pipeline
- Powered by Sumy library

### 3. Advanced Search & Filtering
- Tag-based filtering
- Full-text search across title and summary
- Fuzzy search using PostgreSQL trigrams
- Combined search with multiple filters

### 4. PDF Export
- Two professional formats: detailed report and simple table
- Tag-based filtering for exports
- Customizable item limits

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- PostgreSQL - Database with JSONB and trigram support
- Pydantic - Data validation

**Scraping:**
- Scrapy - Web scraping framework
- Sumy - NLP text summarization
- NLTK - Natural language processing

**Export:**
- ReportLab - PDF generation
- CSV export built-in

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/juni2003/CrawlX-Data-Scrapping-Project.git
cd CrawlX-Data-Scrapping-Project
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Setup Database
```bash
# Create database
createdb scraper_db

# Run migrations
psql -U postgres -d scraper_db -f migrations/001_enable_fuzzy_search.sql
```

### 4. Configure Environment
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/scraper_db
SCRAPER_SPIDERS=news,jobs
SCRAPE_INTERVAL_HOURS=6
```

### 5. Start the Application
```bash
uvicorn main:app --reload --port 8000
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status |
| `/health` | GET | Health check |
| `/items` | GET | List items (supports `?tag=`) |
| `/search` | GET | Search items (supports `?q=`, `?tag=`, `?fuzzy=`) |
| `/items/export/pdf` | GET | Export as PDF |
| `/items/export/csv` | GET | Export as CSV |
| `/scrape/run` | POST | Trigger manual scraping |

### Example Usage

```bash
# Check health
curl http://localhost:8000/health

# Get items by tag
curl "http://localhost:8000/items?tag=news&limit=10"

# Search with fuzzy matching
curl "http://localhost:8000/search?q=python&fuzzy=true"

# Export as PDF
curl "http://localhost:8000/items/export/pdf?tag=tech&limit=50" -o items.pdf

# Trigger scraping
curl -X POST "http://localhost:8000/scrape/run?spiders=news,jobs"
```

## 🐛 Troubleshooting

### Import Error (FIXED! ✅)
If you see `ImportError: attempted relative import with no known parent package`, this has been fixed in the latest version. Update your code from the repository.

### Database Connection
Ensure PostgreSQL is running:
```bash
# Check status
pg_isready

# Start PostgreSQL (Linux)
sudo systemctl start postgresql
```

### Missing Dependencies
```bash
pip install -r backend/requirements.txt
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 📁 Project Structure

```
CrawlX-Data-Scrapping-Project/
├── backend/                    # FastAPI application
│   ├── main.py                # Main application entry point
│   ├── crud.py                # Database operations
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── db.py                  # Database configuration
│   ├── scheduler.py           # Scraping scheduler
│   ├── pdf_export.py          # PDF generation utilities
│   ├── summarizer.py          # Text summarization
│   ├── requirements.txt       # Python dependencies
│   └── migrations/            # Database migrations
├── scraper/                   # Scrapy spiders
│   ├── scraper/
│   │   ├── spiders/           # Spider implementations
│   │   ├── items.py           # Scrapy items
│   │   ├── pipelines.py       # Data processing pipelines
│   │   └── settings.py        # Scrapy configuration
│   └── scrapy.cfg
└── documentation/             # Documentation files
```

## 🔒 Security

- NLTK vulnerability fixed (updated to >=3.9)
- Database credentials in environment variables
- Input validation with Pydantic
- See [SECURITY.md](SECURITY.md) for more details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**juni2003**

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Scrapy for web scraping capabilities
- PostgreSQL for robust database features
- All contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/juni2003/CrawlX-Data-Scrapping-Project/issues)
- **Documentation**: Check the docs in this repository
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

Made with ❤️ by juni2003
