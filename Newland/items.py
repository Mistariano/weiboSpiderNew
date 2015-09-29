
import scrapy


class WeiboItem(scrapy.Item):
    index = scrapy.Field()
    text = scrapy.Field()
    user = scrapy.Field()
    time = scrapy.Field()
    uid = scrapy.Field()
