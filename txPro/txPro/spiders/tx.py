import scrapy
import json


class TxSpider(scrapy.Spider):
    name = 'tx'
    # allowed_domains = ['https://careers.tencent.com/']
    allowed_domains = ['careers.tencent.com']
    start_urls = []
    for page in range(1, 62):
        url = 'https://careers.tencent.com/tencentcareer/api/post/Query?keyword=python&pageIndex=%s&pageSize=10' % page
        start_urls.append(url)

    def parse(self, response):
        content = response.body.decode('utf-8')
        data = json.loads(content)
        job_list = data['Data']['Posts']
        for job in job_list:
            name = job['RecruitPostName']
            country = job['CountryName']
            duty = job['Responsibility']
            # info=name+country+duty+'\n'
            info = {
                "name": name,
                "country": country,
                "duty": duty,
            }
            with open('job.txt', 'a', encoding='utf-8') as fp:
                fp.write(str(info) + '\n')
