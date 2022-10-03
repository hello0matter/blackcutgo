# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RepeatScanHtmlToolPipeline:
    def __init__(self):
        self.fp = None  #定义一个文件描述符属性
    def open_spider(self,spider):
        print('scan开始')
        self.fp = open('./data.txt', 'a+')



    def process_item(self, item, spider):
        if item['car']:
            if item['input'] == "销售单位已入库":
                self.fp.write(item['car'] + '\n')
                self.fp.flush()
        return item

    #结束爬虫时，执行一次
    def close_spider(self,spider):
        self.fp.close()
        print('爬虫结束')
