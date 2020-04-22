# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json

from scrapy import signals, Request
from fake_useragent import UserAgent


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(ua=UserAgent())
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, ua):
        self.fua = ua

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.headers['User-Agent'] = self.fua.random

    def process_response(self, request: Request, response, spider):
        # todo 判断为何种类型的请求，如果为刷新cookies的请求，就重新请求，
        #  如果为请求的数据的请求，就先重新请求referer，然后重新请求之前的请求
        if response.status == 302:
            request.headers.pop('Cookie', None)  # 清空cookies
            if request.meta.get("is_get_cookie_url", False):  # 如果为请求cookies的请求，就直接重新请求
                spider.logger.debug(f'302 error get cookies url {response.url}')
                return request
            if request.meta.get('is_other_url', False):
                spider.logger.debug(f'302 error get other url {response.url}')
                return request

        if request.meta.get("is_get_data_url", False) and len(response.text) != 0:
            res_content = json.loads(response.text)
            is_success = res_content.get("success", False)
            if not is_success:
                spider.logger.debug(f'cookies out of date get data url {response.url}')
                refresh_referer_url = request.meta.get("referer_url")
                req = Request(
                    url=refresh_referer_url,
                    meta=request.meta,
                    priority=request.priority,
                    cb_kwargs=request.cb_kwargs,
                    callback=request.callback,
                    headers=request.headers,
                )
                req.meta['re_request_url'] = request  # 设置标志，回调时重新请求
                req.meta['is_get_cookie_url'] = True  # 补上标志
                req.meta['is_get_data_url'] = False  # 将标志取消
                req.headers.pop('Cookie', None)  # 清空cookies
                return req

        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
