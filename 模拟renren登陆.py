import requests
from lxml import etree
from chaojiying import Chaojiying_Client
import os


class Login():

    def __init__(self):
        self.url = 'http://www.renren.com/SysHome.do'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        self.login_url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=202083133788'

    def get_code(self):
        directory = './code_imgs'
        if not os.path.exists(directory):
            os.mkdir(directory)
        page_text = requests.get(url=self.url, headers=self.headers).text
        tree = etree.HTML(page_text)
        code_img_href = tree.xpath('//*[@id="verifyPic_login"]/@src')[0]
        # 传入下载验证码图片地址，以及保存文件夹路径，调用下载函数
        self.download(code_img_href, directory)

    # 验证码图片的下载函数
    def download(self, href, directory):
        code_img_name = 'code2.jpg'
        code_img_path = directory + '/' + code_img_name
        code_img_data = requests.get(url=href, headers=self.headers).content
        with open(code_img_path, 'wb') as fp:
            fp.write(code_img_data)
            print(code_img_name, '下载成功')
        # 传入下载验证码图片路径，调用识别函数进行识别
        self.distinguish_code(code_img_path)

    # 超级鹰对验证码图片进行识别
    def distinguish_code(self, code_img_path):
        chaojiying = Chaojiying_Client('spx888', 'spx2622196135', '907630')  # 用户中心>>软件ID 生成一个替换 96001
        im = open(code_img_path, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        # 输出是字典类型
        verification_dic = chaojiying.PostPic(im, 1902)  # 1902 验证码类型
        print(verification_dic)
        result = verification_dic['pic_str']
        print('识别验证码为：' + result)
        # 传入result，调用登录函数
        self.login(result)

    def login(self, result):
        data = {
            ' email': ' 15234405680',
            ' icode': result,
            ' origURL': ' http: // www.renren.com / home',
            ' domain': ' renren.com',
            'key_id': ' 1',
            'captcha_type': ' web_login',
            ' password': ' afe79d89e8084b73175b913a1878c9ecc4edf20b1788c2720d81a6ed99f3cb7b',
            ' rkey': ' 663b464e765f525c76e3f8081672a8cf',
            ' f': ' http%3A%2F%2Fwww.renren.com%2F975042080%2Fnewsfeed%2Fphoto',
        }
        session = requests.Session()
        response = session.post(url=self.login_url, headers=self.headers, data=data)
        # 输出响应状态码，检查模拟登陆是否成功，输出200即一切正常
        print(response.status_code)
        # login_page_text = response.text
        # # 将登陆成功的页面保存
        # with open('renren.html', 'w', encoding='utf-8') as fp:
        #     fp.write(login_page_text)
        # 爬取登录后用户页面详情信息
        detail_url = 'http://www.renren.com/975042080/profile'
        # 手动Cookie处理
        # Login.headers = {
        #     'Cookie':    ''
        # }
        detail_page_text = session.get(url=detail_url, headers=self.headers).text
        with open('spx.html', 'w', encoding='utf-8') as fp:
            fp.write(detail_page_text)
            print('用户详情页爬取成功！')


if __name__ == '__main__':
    spider = Login()
    spider.get_code()
