# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RepeatScanHtmlToolItem(scrapy.Item):

    input = scrapy.Field()
    url = scrapy.Field()
    car = scrapy.Field()
    type = scrapy.Field()
    type2 = scrapy.Field()
    hp = scrapy.Field()
    data = scrapy.Field()
    data2 = scrapy.Field()
    dc = scrapy.Field()
    qy = scrapy.Field()
    qy2 = scrapy.Field()