import scrapy
from imgsPro.items import ImgsproItem

class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            img_name = div.xpath('./div/a/@alt').extract_first()
            # print(img_name)
            # 这是一种软加载的模式，只有当前查看的img的属性是src，其它是src2，而这里没有可视化界面，也就是全部都是src2
            src = div.xpath('./div/a/img/@src2').extract_first()
            # print(src)

            item = ImgsproItem()
            item['src'] = src
            item['img_name'] = img_name

            yield item
