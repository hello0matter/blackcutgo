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
        self.fp1 = open('./data1.txt', 'a+')
        self.fp2 = open('./data2.txt', 'a+')



    def process_item(self, item, spider):
        if spider.name == "testtype0":
            self.fp.write(str(dict(item)) + '\n')
            self.fp.flush()
        if spider.name == "testtype1":
            self.fp1.write(str(dict(item)) + '\n')
            self.fp1.flush()
        if spider.name == "testtype2":
            self.fp2.write(str(dict(item)) + '\n')
            self.fp2.flush()
        return item

    #结束爬虫时，执行一次
    def close_spider(self,spider):
        self.fp.close()
        self.fp1.close()
        self.fp2.close()
        print('爬虫结束')
