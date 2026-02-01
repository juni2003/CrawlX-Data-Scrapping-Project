# ✅ CrawlX Testing Guide

Complete testing checklist to verify everything works correctly.

## 🚀 Pre-Testing Setup

### 1. Ensure Backend is Running
```bash
# In backend directory
uvicorn main:app --reload

# Should see:
# INFO: Uvicorn running on http://127.0.0.1:8000
```

### 2. Ensure Frontend is Running
```bash
# In frontend directory
npm run dev

# Should see:
# ▲ Next.js 14.x.x
# Local: http://localhost:3000
```

### 3. Verify Database is Ready
```bash
# Check PostgreSQL is running
pg_isready

# Verify database exists
psql -U postgres -l | grep crawlx
```

---

## 🧪 Backend API Testing

### Test 1: Health Check
```bash
# Request
curl http://localhost:8000/

# Expected Response
{"message": "CrawlX API is running"}

# ✅ Pass: Returns message
# ❌ Fail: Connection refused or error
```

### Test 2: API Documentation
```bash
# Open in browser
http://localhost:8000/docs

# ✅ Pass: Shows Swagger UI with all endpoints
# ❌ Fail: 404 or doesn't load
```

### Test 3: Get Items (Empty Database)
```bash
# Request
curl http://localhost:8000/items

# Expected Response
[]

# ✅ Pass: Returns empty array
# ❌ Fail: Error or null
```

### Test 4: Run News Scraper
```bash
# Request
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '["news"]'

# Expected Response
{"message": "Scraping started for spiders: ['news']"}

# Wait 10 seconds, then check items
curl http://localhost:8000/items?limit=5

# ✅ Pass: Returns array with news items
# ❌ Fail: Empty array or error
```

### Test 5: Custom URL Scraper
```bash
# Request
curl -X POST "http://localhost:8000/scrape/url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://books.toscrape.com",
    "extract_type": "auto",
    "wait_seconds": 2
  }'

# Expected Response (partial)
{
  "url": "https://books.toscrape.com",
  "success": true,
  "content": "...",
  "metadata": {...}
}

# ✅ Pass: success=true with content
# ❌ Fail: success=false or error
```

### Test 6: Search Items
```bash
# First, ensure you have some items (run scrapers)

# Request (exact search)
curl "http://localhost:8000/search?q=python&limit=5"

# Request (fuzzy search)
curl "http://localhost:8000/search?q=pythn&fuzzy=true&limit=5"

# ✅ Pass: Returns matching items
# ❌ Fail: Empty or error
```

### Test 7: Export JSON
```bash
# Request
curl http://localhost:8000/export/json -o data.json

# Check file
cat data.json

# ✅ Pass: Valid JSON file created
# ❌ Fail: Empty or invalid JSON
```

### Test 8: Export CSV
```bash
# Request
curl http://localhost:8000/export/csv -o data.csv

# Check file
head data.csv

# ✅ Pass: CSV with headers and data
# ❌ Fail: Empty or malformed CSV
```

### Test 9: Export PDF
```bash
# Request
curl -X POST "http://localhost:8000/export/pdf" \
  -H "Content-Type: application/json" \
  -d '{"style": "detailed", "limit": 10}' \
  -o data.pdf

# Check file
file data.pdf

# ✅ Pass: Valid PDF file (shows "PDF document")
# ❌ Fail: Not a PDF or error
```

---

## 🎨 Frontend UI Testing

### Test 10: Home Page Loads
1. Open http://localhost:3000
2. Check:
   - ✅ Page loads without errors
   - ✅ 3D particle background animates
   - ✅ Navbar shows with logo and links
   - ✅ Dashboard content visible
   - ❌ Any console errors

### Test 11: Dashboard Stats
1. Go to Dashboard (/)
2. Check:
   - ✅ Four stat cards display (Total, Today, News, Jobs)
   - ✅ Numbers show correctly (may be 0 initially)
   - ✅ Icons display properly
   - ✅ Cards have float animation
   - ❌ Missing cards or broken layout

### Test 12: Run Scrapers Button
1. Click "Run Scrapers" button
2. Check:
   - ✅ Button shows loading state
   - ✅ Success message appears
   - ✅ Stats update after ~10 seconds (refresh page)
   - ❌ Error message or no response

### Test 13: Dark Mode Toggle
1. Click sun/moon icon in navbar
2. Check:
   - ✅ Theme switches instantly
   - ✅ All text remains readable
   - ✅ Particle background adjusts opacity
   - ✅ Preference persists on page reload
   - ❌ Broken colors or unreadable text

### Test 14: Navigation Links
1. Click each navbar link
2. Check:
   - ✅ Dashboard (/) loads
   - ✅ Custom Scraper (/scraper) loads
   - ✅ Data Explorer (/data) loads
   - ✅ URL changes correctly
   - ❌ 404 or broken links

### Test 15: Custom URL Scraper Form
1. Go to /scraper
2. Enter URL: `https://books.toscrape.com`
3. Select mode: "Auto"
4. Set wait time: 2 seconds
5. Click "Scrape URL"
6. Check:
   - ✅ Loading spinner shows
   - ✅ Results display after ~3-5 seconds
   - ✅ Title and metadata shown
   - ✅ Content preview visible
   - ✅ Copy and Download buttons work
   - ❌ Error or no results

### Test 16: Extraction Modes
1. Go to /scraper
2. Test each mode with https://example.com:
   - ✅ Auto mode extracts content
   - ✅ Article mode extracts article
   - ✅ Text mode extracts text
   - ✅ Structured mode extracts tables/lists
   - ❌ Any mode fails

### Test 17: Copy Button
1. Scrape any URL
2. Click "Copy Content" button
3. Paste into notepad
4. Check:
   - ✅ Content copies to clipboard
   - ✅ Tooltip shows "Copied!"
   - ❌ Nothing copies or error

### Test 18: Download Button
1. Scrape any URL
2. Click "Download" button
3. Check:
   - ✅ File downloads automatically
   - ✅ Filename includes domain and date
   - ✅ File contains scraped content
   - ❌ No download or empty file

### Test 19: Data Explorer - Initial Load
1. Go to /data
2. Check:
   - ✅ Items table loads
   - ✅ All columns visible (Title, Source, Tags, Time, Link)
   - ✅ Items display with correct formatting
   - ✅ Relative timestamps (e.g., "2 hours ago")
   - ❌ Empty table or errors

### Test 20: Data Explorer - Search
1. Enter search term (e.g., "python")
2. Click "Search"
3. Check:
   - ✅ Results filter to matching items
   - ✅ Highlights relevant content
   - ✅ Item count updates
   - ❌ No results or error

### Test 21: Data Explorer - Fuzzy Search
1. Enter misspelled term (e.g., "pythn")
2. Enable "Fuzzy search" checkbox
3. Click "Search"
4. Check:
   - ✅ Still finds "python" items
   - ✅ Tolerates typos
   - ❌ No results

### Test 22: Data Explorer - Tag Filter
1. Select a tag (e.g., "news")
2. Check:
   - ✅ Table filters to selected tag
   - ✅ Only shows items with that tag
   - ❌ Shows all items or error

### Test 23: Data Explorer - Reset Button
1. Search for something
2. Select a tag
3. Click "Reset"
4. Check:
   - ✅ Search query clears
   - ✅ Tag filter resets to "All Tags"
   - ✅ All items show again
   - ❌ Filters don't clear

### Test 24: Data Explorer - Export CSV
1. Click "Export CSV" button
2. Check:
   - ✅ File downloads
   - ✅ Contains all visible items
   - ✅ Headers match table columns
   - ✅ Opens in Excel/Sheets correctly
   - ❌ Empty or malformed CSV

### Test 25: Data Explorer - Export PDF
1. Click "Export PDF" button
2. Check:
   - ✅ File downloads
   - ✅ PDF renders correctly
   - ✅ Contains item details
   - ✅ Formatted nicely
   - ❌ Blank or broken PDF

### Test 26: External Links
1. In Data Explorer, click 🔗 icon
2. Check:
   - ✅ Opens source URL in new tab
   - ✅ Correct website loads
   - ❌ Broken link or 404

### Test 27: Responsive Design - Mobile
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select "iPhone 12 Pro" or similar
4. Check:
   - ✅ Navbar collapses to mobile menu
   - ✅ Stats stack vertically
   - ✅ Tables scroll horizontally
   - ✅ Buttons remain clickable
   - ❌ Broken layout or overflow

### Test 28: Responsive Design - Tablet
1. Select "iPad" in DevTools
2. Check:
   - ✅ Two-column layouts
   - ✅ Readable font sizes
   - ✅ Touch-friendly buttons
   - ❌ Squished or broken layout

### Test 29: 3D Background Performance
1. Open Performance tab in DevTools
2. Record for 10 seconds
3. Check:
   - ✅ Maintains 60 FPS (or close)
   - ✅ No frame drops during interaction
   - ✅ CPU usage < 30%
   - ❌ Laggy or stuttering animation

### Test 30: Browser Console
1. Open Console tab (F12)
2. Navigate all pages
3. Check:
   - ✅ No errors (red messages)
   - ✅ No warnings (yellow messages)
   - ❌ Any errors logged

---

## 🔄 Integration Testing

### Test 31: End-to-End Scraping Flow
1. Go to Dashboard
2. Click "Run Scrapers"
3. Wait 15 seconds
4. Go to Data Explorer
5. Check:
   - ✅ New items appear in table
   - ✅ Tags include "news" or "jobs"
   - ✅ Timestamps are recent
   - ❌ No new items

### Test 32: Custom Scrape → Data Explorer
1. Go to Custom Scraper
2. Scrape https://books.toscrape.com
3. Wait for results
4. Go to Data Explorer
5. Search for "books"
6. Check:
   - ✅ Scraped item appears
   - ✅ Correct URL and content
   - ❌ Item not found

### Test 33: Search After Scraping
1. Run news scraper
2. Wait for completion
3. Go to Data Explorer
4. Search for "tech" or "python"
5. Check:
   - ✅ Finds relevant news items
   - ✅ Fuzzy search works
   - ❌ No results

### Test 34: Export After Filtering
1. Go to Data Explorer
2. Filter by tag "news"
3. Export to CSV
4. Open CSV file
5. Check:
   - ✅ Only contains news items
   - ✅ No jobs or other tags
   - ❌ Contains all items

### Test 35: Theme Persistence
1. Switch to dark mode
2. Close browser tab
3. Open http://localhost:3000 again
4. Check:
   - ✅ Still in dark mode
   - ✅ Preference saved
   - ❌ Reverts to light mode

---

## 🐛 Error Handling Testing

### Test 36: Invalid URL in Custom Scraper
1. Enter invalid URL: "not-a-url"
2. Click "Scrape URL"
3. Check:
   - ✅ Shows validation error
   - ✅ Button remains clickable
   - ❌ Crashes or freezes

### Test 37: Offline Backend
1. Stop backend server
2. Try to load Dashboard stats
3. Check:
   - ✅ Shows error message
   - ✅ Doesn't crash frontend
   - ✅ Retry option available
   - ❌ Infinite loading

### Test 38: Scraping Protected Site
1. Go to Custom Scraper
2. Enter: https://www.google.com
3. Click "Scrape URL"
4. Check:
   - ✅ Shows "scraping failed" or similar
   - ✅ Error message is clear
   - ❌ Crashes or hangs

### Test 39: Empty Search
1. Go to Data Explorer
2. Leave search empty
3. Click "Search"
4. Check:
   - ✅ Shows all items (or loads normally)
   - ✅ Doesn't error
   - ❌ Breaks or errors

### Test 40: Export with No Data
1. Delete all items from database
2. Go to Data Explorer
3. Click "Export CSV"
4. Check:
   - ✅ Shows "no data" message OR
   - ✅ Creates empty CSV with headers
   - ❌ Crashes or errors

---

## 📊 Final Checklist

### Backend Health
- [ ] All API endpoints respond correctly
- [ ] Database connection stable
- [ ] No errors in terminal logs
- [ ] Playwright browser installed
- [ ] Scrapers work (news, jobs, custom)
- [ ] Search functionality works
- [ ] Exports work (JSON, CSV, PDF)

### Frontend Functionality
- [ ] All pages load without errors
- [ ] Navigation works correctly
- [ ] Dark mode toggles properly
- [ ] 3D background animates smoothly
- [ ] Forms validate input
- [ ] API calls succeed
- [ ] Error messages display clearly
- [ ] Loading states show correctly

### User Experience
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Fast page loads (< 3s)
- [ ] Smooth animations (60 FPS)
- [ ] Readable in both themes
- [ ] Accessible (keyboard navigation)
- [ ] Tooltips and help text present

### Data Integrity
- [ ] Scraped data saves correctly
- [ ] Search returns accurate results
- [ ] Fuzzy search works
- [ ] Exports contain correct data
- [ ] Timestamps are accurate
- [ ] Tags apply correctly
- [ ] No data loss on page refresh

---

## 🎉 Success Criteria

**All tests pass?** Congratulations! 🎊

Your CrawlX installation is **100% functional** and ready for use!

**Some tests fail?** Check:
1. Backend logs for errors
2. Frontend console for errors
3. Database connection
4. PostgreSQL is running
5. All dependencies installed
6. Correct .env configuration

---

## 📝 Testing Notes

### Record Issues Here
```
Test #: ___
Issue: _______________________________________________
Expected: ______________________________________________
Actual: ________________________________________________
Error Message: _________________________________________
Solution: ______________________________________________
```

### Performance Metrics
```
Page Load Time:
- Dashboard: _____ ms
- Custom Scraper: _____ ms
- Data Explorer: _____ ms

API Response Time:
- Get Items: _____ ms
- Search: _____ ms
- Custom Scrape: _____ s

Bundle Size:
- Main: _____ KB
- Three.js: _____ KB
- Total: _____ KB
```

---

## 🔧 Debugging Tips

### Backend Issues
```bash
# Check logs
cd backend
uvicorn main:app --reload --log-level debug

# Test database
psql -U postgres -d crawlx -c "SELECT COUNT(*) FROM scraped_items;"

# Verify Playwright
python -m playwright install --with-deps chromium
```

### Frontend Issues
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run dev

# Check build errors
npm run build
```

### Database Issues
```bash
# Check connections
psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE datname = 'crawlx';"

# Reset database
dropdb crawlx
createdb crawlx
```

Happy Testing! 🚀
