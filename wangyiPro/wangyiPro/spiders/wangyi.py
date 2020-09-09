import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    models_dic = {}  # 存储五个板块详情页url和名字

    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='./chromedriver.exe')

    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [3, 4, 6, 7, 8]
        for index in alist:
            model_name = li_list[index].xpath('./a/text()').extract_first()
            model_url = li_list[index].xpath('./a/@href').extract_first()
            # print(model_name, model_url)
            self.models_dic.update({model_name: model_url})

        # print(self.models_dic.keys())
        #     print(self.models_dic)
        # # 依次对每一个板块对应的页面进行请求
        for url in self.models_dic.values():
            yield scrapy.Request(url, callback=self.parse_model)

    # 每一个板块对应的详情页信息都是动态加载的
    def parse_model(self, response):  # 解析每一个板块页面中对应的标题和新闻详情页的url
        # pass
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()

            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()

            print(title, new_detail_url)

            item = WangyiproItem()
            item['title'] = title

            # 对新闻详情页的url发起请求
            yield scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item': item})

    # 解析新闻内容
    def parse_detail(self, response):
        content = response.xpath('//*[@id="content"]//text()').extract()
        content = ''.join(content)
        content = content.strip()
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()
