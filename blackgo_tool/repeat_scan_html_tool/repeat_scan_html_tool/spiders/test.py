import scrapy

from blackgo_tool.repeat_scan_html_tool.repeat_scan_html_tool.items import RepeatScanHtmlToolItem


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.pzcode.cn']
    num = 14831610
    urltype = 'https://www.pzcode.cn/Manage/Basic/Battery/ScanView.aspx?type=1'
    start_urls = [urltype + '&id=' + str(num)]

    #根据合一码扫
    def parse(self, response):
        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        self.num = self.num + 1
        items = RepeatScanHtmlToolItem()
        items['input'] = inputs
        items['url'] = self.urltype + '&id=' + str(self.num)
        items['car'] = response.xpath('//*[@id="form1"]/div[4]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]')
        yield items
        # 下载后获得的response由parse_topic处理
        yield scrapy.Request(
            url=self.urltype + '&id=' + str(self.num),
            callback=self.parse
        )


class Test2Spider(scrapy.Spider):
    name = 'test2'
    # allowed_domains = ['www.pzcode.cn']
    num = 17
    urltype = 'http://pzcode.cn/pwb/MA2RJ6WHBBJCJB1DSM8012X059'
    start_urls = [urltype + str(num)]

    #根据电池码扫
    def parse(self, response):
        # 下载后获得的response由parse_topic处理

        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        if inputs:
            items = RepeatScanHtmlToolItem()
            items['input'] = inputs

            items['url'] = self.urltype + str(self.num)

            items['car'] = response.xpath('/html/body/form/div[2]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]').xpath('string(.)').extract_first()
        yield items
        self.num = self.num + 1

        yield scrapy.Request(
            url=self.urltype + str(self.num),
            callback=self.parse
        )
