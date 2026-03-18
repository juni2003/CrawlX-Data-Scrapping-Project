# PythonAnywhere Deployment Guide (Free - No Card Needed)

**PythonAnywhere is completely FREE.** No card required. No hidden charges.

## Overview

- **Frontend**: Vercel (free)
- **Backend**: PythonAnywhere (free)
- **Database**: Neon Postgres (free)

---

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Click **Sign Up** → **Create a Beginner account**
3. Fill in email, username, password
4. **NO CARD REQUIRED** ✅
5. Verify email and log in

---

## Step 2: Upload Your Code to PythonAnywhere

### Option A: From GitHub (Recommended)

1. Login to PythonAnywhere dashboard
2. Click **Files** (left sidebar)
3. Click **Upload a file** OR use **Bash console**
4. In **Bash console**, run:

```bash
cd ~
git clone https://github.com/juni2003/CrawlX-Data-Scrapping-Project.git
cd CrawlX-Data-Scrapping-Project
```

### Option B: Upload ZIP (If GitHub fails)

1. Go to your GitHub repo: https://github.com/juni2003/CrawlX-Data-Scrapping-Project
2. Click **Code** → **Download ZIP**
3. Extract locally
4. In PythonAnywhere Files → drag ZIP file
5. Unzip it

---

## Step 3: Set Up Virtual Environment

In PythonAnywhere **Bash console**:

```bash
cd ~/CrawlX-Data-Scrapping-Project/backend
mkvirtualenv --python=/usr/bin/python3.10 crawlx
pip install -r requirements.txt
```

---

## Step 4: Configure WSGI Application

1. Click **Web** (left sidebar in PythonAnywhere)
2. Click **Add a new web app**
3. Choose **Manual configuration** (not pre-made frameworks)
4. Select **Python 3.10**
5. This creates a **WSGI config file**

Now click the **WSGI configuration file** link and replace contents with:

```python
import sys
from pathlib import Path

# Add your project to path
project_path = str(Path.home() / 'CrawlX-Data-Scrapping-Project' / 'backend')
sys.path.insert(0, project_path)

# Set environment variables
import os
os.environ['DATABASE_URL'] = 'postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require'
os.environ['CORS_ORIGINS'] = 'https://your-vercel-app.vercel.app'
os.environ['HOST'] = '0.0.0.0'
os.environ['PORT'] = '5000'
os.environ['UVICORN_RELOAD'] = 'false'

# Import and create FastAPI app
from main import app

# Create WSGI application
application = app
```

---

## Step 5: Configure Virtual Environment in Web App

1. Back in PythonAnywhere **Web** tab
2. Scroll down to **Virtualenv**
3. Click the folder icon next to **Virtualenv**
4. Type: `/home/your-username/.virtualenvs/crawlx`
   - Replace `your-username` with your PythonAnywhere username
5. Click **Save**

---

## Step 6: Set Up Static/Media Files (If Needed)

1. In **Web** tab, look for **Static files:**
2. Click **+ Enter URL** and add:
   - URL: `/static/`
   - Directory: (leave empty for now)

---

## Step 7: Restart Web App

1. At the top of **Web** tab, click the **green Reload button**
2. Wait ~5 seconds
3. Your app URL will appear at the top, like:
   ```
   https://your-username.pythonanywhere.com
   ```

---

## Step 8: Test Backend

Open in browser:
```
https://your-username.pythonanywhere.com/health
```

Should return: `{"message": "healthy"}`

---

## Step 9: Deploy Frontend on Vercel

1. Go to https://vercel.com → **Add New** → **Project**
2. Import GitHub repo: `CrawlX-Data-Scrapping-Project`
3. Settings:
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
4. Environment Variables:
   - `NEXT_PUBLIC_API_URL`: `https://your-username.pythonanywhere.com`
5. Click **Deploy**

---

## Step 10: Update Backend CORS

Go back to PythonAnywhere **WSGI config**, update:

```python
os.environ['CORS_ORIGINS'] = 'https://your-vercel-username.vercel.app'
```

Then reload the web app.

---

## Step 11: Test Everything

1. Open Vercel app: `https://your-vercel-app.vercel.app`
2. Go to **Scraper** page
3. Try scraping: `https://books.toscrape.com/`
4. If it works → **YOU'RE LIVE!** 🎉

---

## Troubleshooting

**App shows error on PythonAnywhere:**
- Click **Web** → **Error log** at bottom
- Check **Server log** for errors
- Common issues:
  - `DATABASE_URL` not set properly
  - Virtual environment path wrong
  - Missing dependencies in `requirements.txt`

**Frontend can't reach backend:**
- Check CORS_ORIGINS in WSGI config
- Make sure Vercel URL is exact: `https://...vercel.app` (no trailing slash)

**Database connection error:**
- Copy Neon connection string exactly
- Make sure it includes: `?sslmode=require`

---

## Important Notes

- **Free tier limits:**
  - 100 CPU seconds/day (your app sleeps after that)
  - That's ~100 requests of 1 second each
  - Plenty for testing

- **Database:**
  - Your Neon database stays separate (free tier)
  - PythonAnywhere doesn't host it

- **Cold starts:**
  - First request might take 3-5 seconds
  - That's normal on free tier

---

## Next Steps

1. Create PythonAnywhere account (5 min)
2. Upload code via GitHub (2 min)
3. Set up virtualenv (3 min)
4. Configure WSGI (5 min)
5. Deploy frontend on Vercel (5 min)
6. Test end-to-end (2 min)

**Total time: ~20 minutes**

Any questions during setup, just ask!
