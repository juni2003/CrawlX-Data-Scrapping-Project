@echo off
echo ========================================
echo   CrawlX - Quick Start
echo ========================================
echo.
echo This will start both backend and frontend servers.
echo.
echo Make sure PostgreSQL is running!
echo.
pause

start "CrawlX Backend" cmd /k "%~dp0start-backend.bat"
timeout /t 5 /nobreak > nul
start "CrawlX Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Both servers will open in new windows.
echo Close this window or press any key to exit.
pause > nul
