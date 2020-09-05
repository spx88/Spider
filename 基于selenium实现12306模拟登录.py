from chaojiying import Chaojiying_Client
import time
from selenium import webdriver
from PIL import Image
from selenium.webdriver import ActionChains

bro = webdriver.Chrome(executable_path='./chromedriver1.exe')

bro.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(1)

# 将打开的浏览器最大化
bro.maximize_window()
time.sleep(1)
account_login_url = bro.find_element_by_css_selector(
    'body > div.login-panel > div.login-box > ul > li.login-hd-account > a')
account_login_url.click()
# 整张页面截图且保存
bro.save_screenshot('aa.png')

# 确定验证码对应的左上和右下的坐标
code_img_ele = bro.find_element_by_xpath('//*[@id="J-loginImg"]')
location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
size = code_img_ele.size  # 验证码标签对应的长和宽
# 左上角和右下角坐标
rangle = (
    int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height'])
)

i = Image.open('./aa.png')
code_img_name = './code.png'
# crop根据指定区域进行图片裁剪
frame = i.crop(rangle)
# 保存
frame.save(code_img_name)

# 将验证码图片提交给超级鹰进行识别
chaojiying = Chaojiying_Client('xxx', 'xxx', 'xxx')  # 用户中心>>软件ID 生成一个替换 96001
im = open('./code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
# 输出是字典,取值
result = chaojiying.PostPic(im, 9004)['pic_str']
print(result)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

# 处理超级鹰返回的数据
all_list = []  # 存储即将要点击的点的坐标，存储在列表
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
print(all_list)
# 遍历列表，使用动作链对每一个元素对应的x,y指定的位置进行点击操作
for l in all_list:
    x = l[0]
    y = l[1]
    ActionChains(bro).move_to_element_with_offset(code_img_ele, x, y).click().perform()
    time.sleep(0.5)

bro.find_element_by_id('J-userName').send_keys('xxx')
time.sleep(1)
bro.find_element_by_id('J-password').send_keys('xxx')
time.sleep(1)
bro.find_element_by_id('J-login').click()
time.sleep(1)
bro.quit()
