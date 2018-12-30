from scrapy.http import HtmlResponse
import logging
import time


class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'feixiaohao':
            try:
                spider.browser.get(request.url)
            except Exception as e:
                logging.critical(e)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding="utf-8", request=request, headers={'referer': 'https://www.feixiaohao.com'})