@echo off
echo ========================================
echo   CrawlX - Starting Frontend Server
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Checking if node_modules exists...
if not exist "node_modules" (
    echo Installing dependencies (this may take a few minutes)...
    call npm install
) else (
    echo Dependencies already installed.
)

echo.
echo Starting Next.js development server on http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
