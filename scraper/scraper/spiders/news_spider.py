import scrapy
from scraper.items import ScrapedItem


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/"]

    def parse(self, response):
        for row in response.css("tr.athing"):
            title = row.css("span.titleline a::text").get()
            url = row.css("span.titleline a::attr(href)").get()
            if title and url:
                item = ScrapedItem()
                item["source"] = "Hacker News"
                item["title"] = title
                item["url"] = url
                item["summary"] = None
                item["tags"] = ["news", "tech"]
                item["published_at"] = None
                yield item