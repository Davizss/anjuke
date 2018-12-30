# -*- coding: utf-8 -*-
import sys
import os
import scrapy
import re
from scrapy import Request
from lxml import etree
import hashlib
from selenium import webdriver
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from feixiaohao.items import FeixiaohaoExchangeItem, FeixiaohaoConcept


class FeixiaohaoSpider(scrapy.Spider):
    name = 'feixiaohao'
    allowed_domains = ['feixiaohao.com']
    exchange_url = 'https://www.feixiaohao.com/exchange/list_%d.html'
    concept_url = 'https://www.feixiaohao.com/concept/'

    def __init__(self, executable_path='phantomjs'):
        """
        添加了executable_path参数，phantomjs的路径，默认路径是phantomjs
        :param executable_path: phantomjs的路径
        """
        super(FeixiaohaoSpider).__init__()
        # 初始化模拟浏览器
        self.browser = webdriver.PhantomJS(executable_path=executable_path,)
        self.browser.set_page_load_timeout(2)

    def closed(self, spider):
        # 关闭并退出模拟浏览器
        self.browser.close()
        self.browser.quit()

    def start_requests(self):
        for base_url in self.start_urls:
            yield Request(url=base_url, callback=self.parse)

    def parse(self, response):
        """
        把exchange_url和concept_url的URL传入到回调函数进行解析
        :param response:首页的响应
        :return:无
        执行contracts测试
        @url https://www.feixiaohao.com
        @returns items 0 0
        @returns requests 0 8
        """
        for i in range(6):
            exchange_url = self.exchange_url % (i+1)
            yield Request(url=exchange_url, callback=self.parse_exchange)
        yield Request(url=self.concept_url, callback=self.parse_concept)

    def parse_exchange(self, response):
        """
        解析exchange_url,抓取想要的数据
        :param response: exchange_url 的响应数据
        :return:
        执行contracts测试
        @url https://www.feixiaohao.com/exchange
        @returns items 0 200
        @returns requests 0 0
        @scrapes unique_id  exchange_name volume_cny pairs_amount transaction_type country stars
        """
        response = etree.HTML(response.text)
        exchange_list = response.xpath("//table[@class='table exchange-table']/tbody/tr")
        for exchange in exchange_list:
            item = FeixiaohaoExchangeItem()
            item['exchange_name'] = exchange.xpath(".//td[2]/a/text()")[1].strip()
            volume_cny = exchange.xpath(".//td[3]/a/text()")[0]
            item['volume_cny'] = self.get_volume_cny(volume_cny)
            item['pairs_amount'] = int(exchange.xpath(".//td[4]/a/text()")[0])
            item['country'] = exchange.xpath(".//td[5]//text()")[0]
            transaction_type = exchange.xpath(".//td[6]/a/i/@class")
            item['transaction_type'] = self.get_transaction_type(transaction_type)
            item['stars'] = exchange.xpath(".//td[7]/div/@class")[0][5:]
            unique_id = '%s%s' % (item['exchange_name'], item['country'])
            item['unique_id'] = self.get_md5(unique_id)
            item['last_updated_timestamp'] = str(int(time.time() * 1000))
            followers_number = int(exchange.xpath(".//td[8]//text()")[0])
            meta = {
                'followers_number': followers_number,
            }
            item['meta'] = meta
            yield item

    def parse_concept(self, response):
        """
        解析concept_url,抓取想要的数据
        :param response: concept_url 的响应数据
        :return:
        执行contracts测试
        @url https://www.feixiaohao.com/concept
        @returns items 0 200
        @returns requests 0 0
        @scrapes concept  average_change volume_cny pairs_amount best worst rise_fall
        """
        response = etree.HTML(response.text)
        concept_list = response.xpath("//table[@id='table']/tbody/tr")
        for concept in concept_list:
            item = FeixiaohaoConcept()
            item['concept'] = concept.xpath(".//td[1]/a/text()")[0].strip()
            volume_cny = concept.xpath(".//td[2]/text()")[0].strip()
            item['volume_cny'] = self.get_volume_cny(volume_cny)
            item['average_change'] = concept.xpath(".//td[3]/text()")[0].strip()
            best = dict()
            best['pair_name'] = concept.xpath(".//td[4]/a/text()")[0].strip()
            best['pair_change'] = concept.xpath(".//td[4]/span/text()")[0].strip()
            worst = dict()
            worst['pair_name'] = concept.xpath(".//td[5]/a/text()")[0].strip()
            worst['pair_change'] = concept.xpath(".//td[5]/span/text()")[0].strip()

            item['pairs_amount'] = int(concept.xpath(".//td[6]/text()")[0].strip())
            rise = concept.xpath(".//td[7]//text()")[0]
            fall = concept.xpath(".//td[7]//text()")[2]

            item['best'] = best
            item['worst'] = worst
            item['rise_fall'] = {
                'rise': int(rise),
                'fall': int(fall)
            }
            item['unique_id'] = self.get_md5(item['concept'])
            item['last_updated_timestamp'] = str(int(time.time() * 1000))

            yield item

    def get_transaction_type(self, value):
        """
        得到交易类型列表（list）
        :param value: 交易类型列表
        :return: 交易类型列表（list）
        """
        res = []
        for t_type in value:
            t = t_type.replace('fxh-login fxh-xianhuo', '现货交易').replace('fxh-login fxh-qihuo', '期货交易').replace('fxh-login fxh-fabi', '法币交易').replace('fxh-login fxh-share-deep', '共享深度').replace('fxh-login fxh-wakuang', '交易挖矿')
            res.append(t)
        return res

    def get_volume_cny(self, value):
        """
        得到交易金额（int）
        :param value: 交易额字符串
        :return: 交易金额（int）
        """
        if value:
            if value == '?':
                return -1
            num = re.sub("\D", "", value)
            if '万' in value:
                return int(num) * 10000
            return int(num)
        else:
            return -1

    def get_md5(self, value):
        """
        md5加密
        :param value: 字符串
        :return: md5值
        """
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()