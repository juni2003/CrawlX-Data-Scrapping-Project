"""
Startup script for CrawlX backend with proper Windows support.

This script ensures the correct asyncio event loop policy is set
before uvicorn starts, which is required for Playwright on Windows.
"""

import asyncio
import os
import platform
import sys

# CRITICAL: Set event loop policy BEFORE importing anything else
if platform.system() == 'Windows':
    # Windows requires ProactorEventLoopPolicy for subprocess support
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    print("✓ Windows event loop policy set (ProactorEventLoopPolicy)")

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    print("Starting CrawlX Backend Server...")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    reload_enabled = os.getenv("UVICORN_RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload_enabled,
        log_level="info"
    )
