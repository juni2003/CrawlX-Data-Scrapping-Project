import os
import asyncio
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Default spiders to run if not specified
DEFAULT_SPIDERS = [
    name.strip()
    for name in os.getenv("SCRAPER_SPIDERS", "news,jobs").split(",")
    if name.strip()
]

# Path to Scrapy project
SCRAPER_PROJECT_PATH = os.path.abspath(
    os.getenv(
        "SCRAPER_PROJECT_PATH",
        os.path.join(os.path.dirname(__file__), "..", "scraper"),
    )
)

scheduler = BackgroundScheduler()


def run_spiders(spiders: list[str]) -> None:
    for spider in spiders:
        cmd = ["scrapy", "crawl", spider]
        subprocess.run(cmd, cwd=SCRAPER_PROJECT_PATH, check=True)


async def run_spiders_async(spiders: list[str]) -> None:
    await asyncio.to_thread(run_spiders, spiders)


def start_scheduler() -> None:
    if scheduler.running:
        return

    interval_hours = int(os.getenv("SCRAPE_INTERVAL_HOURS", "6"))
    scheduler.add_job(
        run_spiders,
        trigger=IntervalTrigger(hours=interval_hours),
        args=[DEFAULT_SPIDERS],
        id="scrape_job",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
