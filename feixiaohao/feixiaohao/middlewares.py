# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import time
import hashlib


class MaYiProxyMiddleware(object):
    """
    To use class:
        from mayi_proxy import MaYiProxyMiddleware
        my_p = MaYiProxyMiddleware()
    """

    def get_proxy(self):
        """
        获取得到蚂蚁代理
        :return: 身份验证及代理
        """
        appkey = "249349693"
        secret = "c57955ade91fe9b3f8b78f0d49fa6c7b"
        mayi_url = "s5.proxy.mayidaili.com"
        mayi_port = "8123"
        mayi_proxy = '{}:{}'.format(mayi_url, mayi_port)
        proxy = {'http': mayi_proxy}
        paramMap = {
            "app_key": appkey,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        keys = sorted(paramMap)
        codes = "%s%s%s" % (secret, str().join('%s%s' % (key, paramMap[key]) for key in keys), secret)
        sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()
        paramMap["sign"] = sign
        keys = paramMap.keys()
        auth = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)
        return {
            'auth': auth,
            'proxy': proxy
        }


class ProxyMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.my_p = MaYiProxyMiddleware()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        try:
            kv_ = self.my_p.get_proxy()
            request.meta['proxy'] = kv_['proxy']
            request.headers['Proxy-Authorization'] = kv_['auth']
        except Exception as e:
            logging.critical(e)
