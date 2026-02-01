import os
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()


class SummarizerPipeline:
    """Pipeline to generate summaries for items."""
    
    def process_item(self, item, spider):
        # Generate a basic summary from title if summary is not present
        if not item.get("summary"):
            title = item.get("title", "")
            source = item.get("source", "")
            if title:
                item["summary"] = f"{source}: {title}"
        return item


class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname=os.getenv("PG_DB", "scraper_db"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "yourpassword"),
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432"),
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """
                INSERT INTO scraped_items (source, title, url, summary, tags, published_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
                """,
                (
                    item.get("source"),
                    item.get("title"),
                    item.get("url"),
                    item.get("summary"),
                    Json(item.get("tags") or []),  # ✅ proper JSON
                    item.get("published_at"),
                ),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return item