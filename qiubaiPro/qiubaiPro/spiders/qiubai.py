import scrapy
from qiubaiPro.items import QiubaiproItem


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    # def parse(self, response):
    #     # pass
    #     # 解析：作者的名称+段子
    #     div_list = response.xpath('//div[@class="col1 old-style-col1"]/div')
    #     # 存储所有解析到的数据
    #     all_data = []
    #     print(len(div_list))
    #     for div in div_list:
    #         # xpath返回的是列表，但是列表元素一定是selector类型的对象
    #         author = div.xpath('./div[1]/a[1]/img/@alt').extract()[0]
    #         # # author = div.xpath('./div[1]/a[2]/h2/test()')[0]
    #         # 列表调用了extract(),将列表中的每一个selector对象中data对应的字符串提取
    #         content = div.xpath('./a[1]/div/span//text()').extract()
    #         content = ''.join(content)
    #         # print(author)
    #         # print(author)
    #         # print(content)
    #         dic = {
    #             'author': author,
    #             'content': content
    #         }
    #         all_data.append(dic)
    #
    #     return all_data

    def parse(self, response):
        div_list = response.xpath('//div[@class="col1 old-style-col1"]/div')
        # 存储所有解析到的数据
        all_data = []
        for div in div_list:
            author = div.xpath('./div[1]/a[1]/img/@alt').extract()[0]
            content = div.xpath('./a[1]/div/span//text()').extract()
            content = ''.join(content)

            item = QiubaiproItem()
            item['author'] = author
            item['content'] = content
            # 将item提交给管道
            yield item
