import requests
from lxml import etree
import os

if __name__ == '__main__':

    page = input("请输入需要爬取第几页的简历模板")
    if page == '1':
        url = 'http://sc.chinaz.com/jianli/free.html'
    else:
        url = 'http://sc.chinaz.com/jianli/free_' + page + '.html'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    page_text = requests.get(url=url, headers=headers).text

    tree = etree.HTML(page_text)
    # 首页div获取
    div_list = tree.xpath('//div[@id="main"]/div/div')
    # 存储详情模板href的列表
    detail_hrefs = []
    # 批量获取div中的a标签中的href
    for div in div_list:
        detail_hrefs.append(div.xpath('./a/@href')[0])
    print('模板详情地址', detail_hrefs)
    print('模板个数：', len(detail_hrefs))
    # 存储下载模板链接的字典，用来存储模板名字以及下载地址
    down_hrefs = {}
    # 对每个简历模板对应的详情页批量发送请求
    for detail_href in detail_hrefs:
        detail_page_text = requests.get(url=detail_href, headers=headers).text
        # 实例化模板详情页的etree对象
        detail_tree = etree.HTML(detail_page_text)
        # 获取模板名字
        resume_name = detail_tree.xpath('//div[@class="ppt_tit clearfix"]/h1/text()')[0]
        resume_name = resume_name.encode('iso-8859-1').decode('utf-8')
        # 对具体模板详情页进行分析，下载地址分层为：//div[@class="down_wrap"]/div/ul/li/a，所以获取第一个li标签列表的a标签
        down_href = detail_tree.xpath('//div[@class="down_wrap"]//ul/li[1]/a/@href')[0]
        down_hrefs[resume_name] = down_href
    print(down_hrefs)
    # 创建一个存取简历模板的文件夹
    if not os.path.exists('./resume_templates'):
        os.mkdir('./resume_templates')
    # 遍历下载地址的字典
    for resume_name, down_href in down_hrefs.items():
        # 模板下载好的存储路径
        resume_path = 'resume_templates/' + resume_name
        # 下载请求并返回content
        resume_down = requests.get(url=down_href, headers=headers).content
        with open(resume_path, 'wb') as fb:
            fb.write(resume_down)
        print(resume_name, '下载成功')
