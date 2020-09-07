# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# class ImgsproPipeline:
#     def process_item(self, item, spider):
#         return item

from scrapy.pipelines.images import ImagesPipeline
import scrapy


class imgsPileLine(ImagesPipeline):
    # 就是可以根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        print(item['src'])
        yield scrapy.Request(item['src'], meta={'item': item})  # 添加meta是为了下面使用

        # 指定图片存储的路径

    def file_path(self, request, response=None, info=None):
        # http: // pic1.sc.chinaz.com / Files / pic / pic9 / 202009 / apic27515_s.jpg
        # split切割成字符串数组然后切片操作取数组最后一个元素
        # stringObject.split(separator, howmany)
        # separator: 必需。字符串或正则表达式，从该参数指定的地方分割stringObject。
        # howmany 可选。该参数可指定返回的数组的最大长度。如果设置了该参数，返回的子串不会多于这个参数指定的数组。如果没有设置该参数，整个字符串都会被分割，不考虑它的长度。
        # imgName = request.url.split('/')[-1]
        item = request.meta['item']  # 通过上面的meta传递过来item
        imgName = item['img_name'] + '.jpg'
        print(imgName)
        return imgName

    # 下载完成后调用该方法
    def item_completed(self, results, item, info):
        return item  # 返回给下一个即将被执行的管道类
