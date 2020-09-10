import scrapy


class MiddleSpider(scrapy.Spider):
    name = 'middle'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.baidu.com/s?wd=ip']

    def parse(self, response):
        page_text = response.text
        print('开始保存..')
        with open('./ip.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)
            print('保存完毕')
