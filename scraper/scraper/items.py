import scrapy


class ScrapedItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()
    published_at = scrapy.Field()