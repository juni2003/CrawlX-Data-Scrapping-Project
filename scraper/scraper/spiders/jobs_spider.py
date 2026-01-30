import scrapy
from scraper.items import ScrapedItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["remoteok.com"]
    start_urls = ["https://remoteok.com/remote-dev-jobs"]

    def parse(self, response):
        jobs = response.css("tr.job")
        for job in jobs:
            title = job.css("h2::text").get()
            company = job.css("h3::text").get()
            url = job.css("a.preventLink::attr(href)").get()
            if url and url.startswith("/"):
                url = "https://remoteok.com" + url

            if title and url:
                item = ScrapedItem()
                item["source"] = "RemoteOK"
                item["title"] = f"{title} - {company}" if company else title
                item["url"] = url
                item["summary"] = None
                item["tags"] = ["jobs", "remote"]
                item["published_at"] = None
                yield item