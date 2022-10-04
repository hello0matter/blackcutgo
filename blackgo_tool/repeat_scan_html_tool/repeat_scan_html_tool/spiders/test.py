import scrapy

from blackgo_tool.repeat_scan_html_tool.repeat_scan_html_tool.items import RepeatScanHtmlToolItem


class TestSpidertype2(scrapy.Spider):
    name = 'testtype2'
    # allowed_domains = ['www.pzcode.cn']
    num = 8707443
    urltype = 'https://www.pzcode.cn/Manage/Basic/Battery/ScanView.aspx?type=2'
    start_urls = [urltype + '&id=' + str(num)]

    # 根据合一码扫
    def parse(self, response):
        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        self.num = self.num + 1
        items = RepeatScanHtmlToolItem()
        items['input'] = inputs
        items['url'] = self.urltype + '&id=' + str(self.num)
        items['car'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]').xpath(
            'string(.)').extract_first()
        items['hp'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[4]/div/div/div[1]/span[2]').xpath(
            'string(.)').extract_first()
        items['type'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[6]/span[2]').xpath(
            'string(.)').extract_first()
        items['type2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[10]/span[2]').xpath(
            'string(.)').extract_first()
        items['data'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        items['data2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[15]/span[2]').xpath(
            'string(.)').extract_first()
        first = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[2]/span[2]').xpath(
            'string(.)').extract_first()
        if first:
            items['dc'] = first.strip()

        items['qy'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[4]/span[2]').xpath(
            'string(.)').extract_first()
        items['qy2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        yield items
        # 下载后获得的response由parse_topic处理
        yield scrapy.Request(
            url=self.urltype + '&id=' + str(self.num),
            callback=self.parse
        )


class TestSpidertype1(scrapy.Spider):
    name = 'testtype1'
    # allowed_domains = ['www.pzcode.cn']
    num = 8703101
    urltype = 'https://www.pzcode.cn/Manage/Basic/Battery/ScanView.aspx?type=1'
    start_urls = [urltype + '&id=' + str(num)]

    # 根据合一码扫
    def parse(self, response):
        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        self.num = self.num + 1
        items = RepeatScanHtmlToolItem()
        items['input'] = inputs
        items['url'] = self.urltype + '&id=' + str(self.num)
        items['car'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]').xpath(
            'string(.)').extract_first()
        items['hp'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[4]/div/div/div[1]/span[2]').xpath(
            'string(.)').extract_first()
        items['type'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[6]/span[2]').xpath(
            'string(.)').extract_first()
        items['type2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[10]/span[2]').xpath(
            'string(.)').extract_first()
        items['data'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        items['data2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[15]/span[2]').xpath(
            'string(.)').extract_first()
        first = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[2]/span[2]').xpath(
            'string(.)').extract_first()
        if first:
            items['dc'] = first.strip()

        items['qy'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[4]/span[2]').xpath(
            'string(.)').extract_first()
        items['qy2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        yield items
        # 下载后获得的response由parse_topic处理
        yield scrapy.Request(
            url=self.urltype + '&id=' + str(self.num),
            callback=self.parse
        )


# 往上都是扫车码绑定关系所有信息或者码牌号码关联绑定信息
class TestSpidertype0(scrapy.Spider):
    name = 'testtype0'
    # allowed_domains = ['www.pzcode.cn']
    num = 8703101
    urltype = 'https://www.pzcode.cn/Manage/Basic/Battery/ScanView.aspx?type=0'
    start_urls = [urltype + '&id=' + str(num)]

    # 根据合一码扫
    def parse(self, response):
        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        self.num = self.num + 1
        items = RepeatScanHtmlToolItem()
        items['input'] = inputs
        items['url'] = self.urltype + '&id=' + str(self.num)
        items['car'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]').xpath(
            'string(.)').extract_first()
        items['hp'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[4]/div/div/div[1]/span[2]').xpath(
            'string(.)').extract_first()
        items['type'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[6]/span[2]').xpath(
            'string(.)').extract_first()
        items['type2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[10]/span[2]').xpath(
            'string(.)').extract_first()
        items['data'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        items['data2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[15]/span[2]').xpath(
            'string(.)').extract_first()
        first = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[2]/span[2]').xpath(
            'string(.)').extract_first()
        if first:
            items['dc'] = first.strip()

        items['qy'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[3]/div/div/div[4]/span[2]').xpath(
            'string(.)').extract_first()
        items['qy2'] = response.xpath('//*[@id="form1"]/div[2]/div[1]/div[2]/div[2]/div/div/div[8]/span[2]').xpath(
            'string(.)').extract_first()
        yield items
        # 下载后获得的response由parse_topic处理
        yield scrapy.Request(
            url=self.urltype + '&id=' + str(self.num),
            callback=self.parse
        )


# 扫电池码中有车型的
class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.pzcode.cn']
    num = 17
    urltype = 'http://pzcode.cn/pwb/MA2RJ6WHBBJCJB1DSM8012X059'
    start_urls = [urltype + str(num)]

    # 根据电池码扫
    def parse(self, response):
        # 下载后获得的response由parse_topic处理

        inputs = response.xpath('//*[@id="btnDc"]').xpath('string(.)').extract_first()
        if inputs:
            items = RepeatScanHtmlToolItem()
            items['input'] = inputs

            items['url'] = self.urltype + str(self.num)

            items['car'] = response.xpath('/html/body/form/div[2]/div[1]/div[2]/div[2]/div/div/div[13]/span[2]').xpath(
                'string(.)').extract_first()
        yield items
        self.num = self.num + 1

        yield scrapy.Request(
            url=self.urltype + str(self.num),
            callback=self.parse
        )
