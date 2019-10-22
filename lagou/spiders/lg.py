# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from scrapy.http import Response
from scrapy.http.cookies import CookieJar


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['lagou.com']
    origin_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    header_dict = {
        "Accept": r'application/json, text/javascript, */*; q=0.01',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }
    cookie_jar = CookieJar()

    def start_requests(self):
        get_cookies_url = "https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput="
        yield Request(url=get_cookies_url, callback=self.pass_cookies_to_post, meta={"cookiejar": 11},
                      headers=self.header_dict)

    def pass_cookies_to_post(self, response:Response):
        self.cookie_jar.extract_cookies(response,response.request)
        this_req = FormRequest(
            url=self.origin_url,
            formdata={"first": "true", "pn": "1"},
            callback=self.parse,
        )
        yield this_req

    def parse(self, response):
        a = response
        yield a
