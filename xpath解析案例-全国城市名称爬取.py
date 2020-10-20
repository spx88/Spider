import requests
from lxml import etree

if __name__ == '__main__':
    # url = 'https://www.aqistudy.cn/historydata/'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    # }
    # page_text = requests.get(url=url, headers=headers).text
    #
    # tree = etree.HTML(page_text)
    #
    # hot_li_list = tree.xpath('//div[@class="bottom"]/ul/li')
    # hot_city_names = []
    # all_city_names = []
    # # 解析到了热门城市的名称
    # for li in hot_li_list:
    #     hot_city_name = li.xpath('./a/text()')[0]
    #     hot_city_names.append(hot_city_name)
    # all_city_list = tree.xpath('//div[@class="bottom"]/ul/div[2]/li')
    # # 解析全部城市的名称
    # for li in all_city_list:
    #     all_city_name = li.xpath('./a/text()')[0]
    #     all_city_names.append(all_city_name)
    #
    # print(hot_city_names, all_city_names, len(all_city_names))

    #  div/ul/li/a 热门城市a标签的层级关系
    #  div/ul/div[2]/li 全部城市a标签的层级关系

    url = 'https://www.aqistudy.cn/historydata/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    page_text = requests.get(url=url, headers=headers).text

    tree = etree.HTML(page_text)
    #  div/ul/li/a 热门城市a标签的层级关系
    #  div/ul/div[2]/li/a 全部城市a标签的层级关系

    a_list = tree.xpath('//div[@class="bottom"]/ul/li/a | //div[@class="bottom"]/ul/div[2]/li/a')
    all_city_names = []
    for a in a_list:
        city_name = a.xpath('./text()')[0]
        all_city_names.append(city_name)

    print(all_city_names)
    print(len(all_city_names))
