
import scrapy


class WeiboItem(scrapy.Item):
    text = scrapy.Field()
    user = scrapy.Field()
    time = scrapy.Field()
