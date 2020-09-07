import scrapy
from bossPro.items import BossproItem
 

class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://s.yingjiesheng.com/search.php?area=&word=python&jobterm=']

    # 通用url的模板
    url = 'https://s.yingjiesheng.com/search.php?word=python&sort=score&start=%d'

    page_num = 10

    # 回调函数接收item
    def parse_detail(self, response):
        item = response.meta['item']

        job_desc = response.xpath('//*[@id="wordDiv"]/div/div[1]').xpath('string(.)').extract()
        job_desc = "".join(job_desc)
        job_desc = ("".join([s for s in job_desc.splitlines(True) if s.strip()]))
        # print(job_desc)
        item['job_desc'] = job_desc

        yield item

    # 解析首页中的岗位名称
    def parse(self, response):
        li_list = response.xpath('//*[@id="container"]/div[1]/ul/li')
        for li in li_list:
            job_name = li.xpath('./div/h3/a/text()').extract()
            job_name = ''.join(job_name)
            print(job_name)

            item = BossproItem()
            item['job_name'] = job_name
            detail_url = li.xpath('./div/h3/a/@href').extract_first()

            # 对详情页发请求，获取详情页的页面源码数据
            # 请求传参：meta={}，可以将meta字典传递给请求对应的回调函数
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})

        # 分页操作
        if self.page_num <= 100:
            new_url = format(self.url % self.page_num)
            self.page_num += 10

            yield scrapy.Request(new_url, callback=self.parse)
