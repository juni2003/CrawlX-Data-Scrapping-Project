# Free Deployment Plan (Recommended)

This project is best deployed as:

- Frontend: Vercel (free)
- Backend: Render Web Service (free)
- Database: Neon Postgres (free)

## 1. Push Your Repo to GitHub

From project root:

```bash
git add .
git commit -m "chore: prepare free deployment (Render backend + Vercel frontend)"
git push origin main
```

## 2. Create Free Postgres (Neon)

1. Go to https://neon.tech and create a free project.
2. Copy the connection string.
3. Use connection string in Render as `DATABASE_URL`.

## 3. Deploy Backend on Render (Free)

1. Go to https://render.com and connect GitHub.
2. Click New -> Blueprint.
3. Select this repository.
4. Render will detect `render.yaml`.
5. Set env vars when prompted:
   - `DATABASE_URL`: your Neon connection string
   - `CORS_ORIGINS`: `https://<your-vercel-app>.vercel.app`
6. Deploy.
7. After deploy, copy backend URL, e.g.:
   `https://crawlx-backend.onrender.com`

## 4. Deploy Frontend on Vercel (Free)

1. Go to https://vercel.com and import your GitHub repo.
2. Framework preset: Next.js.
3. Root Directory: `frontend`
4. Set env var:
   - `NEXT_PUBLIC_API_URL`: `https://crawlx-backend.onrender.com`
5. Deploy.

## 5. Verify End-to-End

- Backend health: `https://crawlx-backend.onrender.com/health`
- Frontend loads: `https://<your-vercel-app>.vercel.app`
- Try custom scraper from frontend UI.

## Notes

- Render free backend sleeps after inactivity and may take ~30-60s to wake up.
- That is normal for free tier.
- If your API is slow on first request, it is likely cold start.
