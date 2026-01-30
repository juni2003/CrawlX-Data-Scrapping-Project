import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scraper.pipelines.SummarizerPipeline": 200,
    "scraper.pipelines.PostgresPipeline": 300,
}

LOG_LEVEL = "INFO"