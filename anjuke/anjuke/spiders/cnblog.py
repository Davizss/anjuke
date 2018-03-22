# -*- coding: utf-8 -*-
import scrapy
import re
from day14.items import CnblogItem

class CnblogSpider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://www.cnblogs.com']
    base_url = 'https://www.cnblogs.com/pick/%d/'

    def parse(self, response):
        for i in range(3,0,-1):
            fullurl = self.base_url % i
            yield scrapy.Request(url=fullurl,callback=self.parseList)

    def parseList(self,response):
        article_div  = response.xpath('//div[@id="post_list"]/div')
        for article in article_div:
            item = CnblogItem()

            title = article.xpath('.//a[@class="titlelnk"]/text()').extract()[0].strip()
            # 详情页链接
            link = article.xpath('.//a[@class="titlelnk"]/@href').extract()[0].strip()

            # 获取文章id
            id_pat = re.compile(r'(\d+).html')
            res = id_pat.search(link)
            if res is not None:
                aid = res.group(1)


                industry = article.xpath('.//p[@class="post_item_summary"]/text()').extract()
                industry = ''.join(industry).strip()

                recommend = article.xpath('.//span[@class="diggnum"]/text()').extract()[0].strip()
                nick = article.xpath('.//div[@class="post_item_foot"]/a/text()').extract()[0].strip()
                date_pub = article.xpath('.//div[@class="post_item_foot"]/text()').extract()[1].strip().strip('发布于')
                comment = article.xpath('.//span[@class="article_comment"]/a/text()').extract()[0].strip()
                comment = self.getNum(comment)
                read_num = article.xpath('.//span[@class="article_view"]/a/text()').extract()[0].strip()
                read_num = self.getNum(read_num)

                item["aid"] = aid
                item["title"] = title

                item["industry"] = industry
                item["recommend"] = recommend
                item["nick"] = nick
                item["date_pub"] = date_pub
                item["comment"] = comment
                item["read_num"] = read_num

                yield scrapy.Request(url=link, callback=self.parseDetail, meta={'data':item})

    def parseDetail(self,response):
        item = response.meta['data']
        # 获取详情
        pass


    def getNum(self,value):
        pat = re.compile(r'\d+')
        res = pat.search(value)
        if res is not None:
            res = int(res.group())
        else:
            res = 0
        return res