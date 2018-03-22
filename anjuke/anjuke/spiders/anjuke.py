# -*- coding: utf-8 -*-
import scrapy
from day14 import settings
import os
import re
from day14.items import HouseItem
from urllib import request
import uuid

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    # start_urls = ['https://www.baidu.com/']
    base_url = 'https://bj.zu.anjuke.com/fangyuan/p%d/'

    headers = {
        "Host": "bj.zu.anjuke.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://beijing.anjuke.com/?pi=PZ-baidu-pc-all-biaoti",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # 全局请求头，
    custom_settings = {
        'CONCURRENT_REQUESTS' : 1,
        # 'DEFAULT_REQUEST_HEADERS' : {
        #     "Host": "bj.zu.anjuke.com",
        #     "Connection": "keep-alive",
        #     "Pragma": "no-cache",
        #     "Cache-Control": "no-cache",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Referer": "https://beijing.anjuke.com/?pi=PZ-baidu-pc-all-biaoti",
        #     # "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        # },
        'COOKIES_ENABLED' : False,
        'DOWNLOAD_DELAY' : 1,
        'IMAGES_URLS_FIELD' : 'image_path',
        'IMAGES_STORE' : os.path.join(settings.Base_dir,'images'),

        'ITEM_PIPELINES' : {
            'day14.pipelines.HouseImagePipeline' : 1,
        }
    }

    # 构建首次请求
    def start_requests(self):
        base_url = 'https://bj.zu.anjuke.com/'
        yield scrapy.Request(url=base_url,headers=self.headers)

    # 解析首次请求
    def parse(self, response):
        for i in range(50,0,-1):
            fullurl = self.base_url % i
            yield scrapy.Request(url=fullurl,callback=self.parsePage,headers=self.headers)

    # 解析列表页
    def parsePage(self,response):
        detail_url = response.xpath('//div[@class="zu-itemmod  "]/@link').extract()
        for url in detail_url:
            yield scrapy.Request(url=url,callback=self.parseDetail,headers=self.headers)

    # 解析详情页
    def parseDetail(self,response):
        hid_pat = re.compile(r'fangyuan/(\d+)')
        res = hid_pat.search(response.url)
        if res is not None:
            item = HouseItem()

            hid = res.group(1)

            # 获取详情页信息
            title = response.xpath('//div[@class="wrapper"]//h3/text()').extract()[0].strip()
            money = response.xpath('//span[@class="f26"]/text()').extract()[0].strip()
            rent_type = response.xpath('//div[@class="litem fl"]/dl[2]/dd[1]/text()').extract()[0].strip()
            house_type = response.xpath('//div[@class="litem fl"]/dl[3]/dd/text()').extract()[0].strip()
            area = response.xpath('//div[@class="ritem fr"]/dl[3]/dd/text()').extract()[0].strip()
            location = response.xpath('//div[@class="litem fl"]/dl[5]/dd/a/text()').extract()[0].strip()
            level = response.xpath('//div[@class="ritem fr"]/dl[5]/dd/text()').extract()[0].strip()

            images = response.xpath('//div[@class="picCon"]/ul[@class="picMove cf"]/li/a/img/@src').extract()
            image_path = [image for image in images if '600x450' in image]

            item["hid"] = hid
            item["title"] = title
            item["money"] = money
            item["rent_type"] = rent_type
            item["house_type"] = house_type
            item["area"] = area
            item["location"] = location
            item["level"] = level
            item['image_path'] = image_path

            # 下载图片
            fname_list = []
            for url in image_path:
                fname = str(uuid.uuid4()) + '.jpg'
                request.urlretrieve(url,os.path.join(settings.Base_dir,'images/') + fname)
                fname_list.append(fname)
            
            item['image_path'] = '|'.join(fname_list)

            yield item
            #print(title,money,rent_type,house_type,area,location,level)



