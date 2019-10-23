# -*- coding: utf-8 -*-
import uuid

import scrapy
from scrapy import Request, FormRequest
from scrapy.http import Response
from scrapy.http.cookies import CookieJar
from urllib.parse import quote


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['lagou.com']
    fill_city_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&gx=&isSchoolJob=1#filterBox"
    fill_district_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&gx=&isSchoolJob=1&district={district}#filterBox"
    fill_bizArea_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&district={district}&bizArea={bizArea}#filterBox"
    origin_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    get_cookies_url = "https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput="
    header_dict = {
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }

    def __init__(self, city_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_info = city_list

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(city_list=crawler.settings.get("CITY_INFO"), *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        yield Request(url=self.get_cookies_url, callback=self.parse_by_city, meta={"cookiejar": "lagou"},
                      headers=self.header_dict, priority=4, dont_filter=True)

    def parse_by_city(self, response):
        """
        按照城市进行遍历
        :param response:
        :return:
        """
        num = response.xpath("//a[@id='tab_pos']/span/text()").extract_first()
        if num == '500+':
            # 遍历所有的城市
            for city, code in self.city_info.items():
                yield Request(
                    url=self.fill_city_url.format(city=code),
                    meta={"city": city, "city_code": code, "cookiejar": "lagou1"},
                    headers=self.header_dict,
                    callback=self.parse_by_district,
                    dont_filter=True
                )
        else:
            # 直接抓取
            for pageNum in range(1, 31):
                yield Request(url=self.get_cookies_url, callback=self.parse_by_city, meta={"cookiejar": "lagou"},
                              headers=self.header_dict, priority=4, dont_filter=True)
                yield FormRequest(
                    url=self.origin_url,
                    formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                    callback=self.parse,
                    meta={"cookiejar": "lagou"},
                    method="POST",
                    headers=self.header_dict,
                    priority=3,
                    dont_filter=True
                )

    def parse_by_district(self, response):
        """
        按照城市划分还是太多，按照城市的区域划分
        :param response:
        :return:
        """
        num = response.xpath("//a[@id='tab_pos']/span/text()").extract_first()
        this_city = response.meta['city']
        this_city_code = response.meta['city_code']
        if num == '500+':
            # 遍历该城市所有的区
            all_district: list = response.xpath("//div[@data-type='district']//a/text()").extract()
            if len(all_district) == 0:
                all_district = response.xpath('//li[@data-toggle-type="district"]//a/text()').extract()
            if len(all_district) == 0:
                return
            all_district.remove("不限")
            for district in all_district:
                yield Request(
                    url=self.fill_district_url.format(city=this_city_code, district=district),
                    meta={"district": district, "city": this_city, "city_code": this_city_code, "cookiejar": "lagou1"},
                    headers=self.header_dict,
                    callback=self.parse_by_bizArea,
                    dont_filter=True
                )
        else:
            # 直接抓取
            total_page_num = response.xpath("//span[@class='span totalNum']/text()").extract_first()
            if not total_page_num:
                pass
            else:
                for pageNum in range(1, int(total_page_num) + 1):
                    yield Request(url=self.get_cookies_url, callback=self.parse_by_city, meta={"cookiejar": "lagou"},
                                  headers=self.header_dict, priority=4, dont_filter=True)
                    yield FormRequest(
                        url=self.origin_url + f"&city={quote(this_city)}",
                        formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                        callback=self.parse,
                        meta={"cookiejar": "lagou"},
                        method="POST",
                        headers=self.header_dict,
                        priority=3,
                        dont_filter=True
                    )

    def parse_by_bizArea(self, response):
        """
        如果分区的结果还是很多，就按照商圈进行分类
        :param response:
        :return:
        """
        num = response.xpath("//a[@id='tab_pos']/span/text()").extract_first()
        this_city = response.meta['city']
        this_city_code = response.meta['city_code']
        this_district = response.meta['district']
        if num == '500+':
            # 遍历该区的所有商圈
            all_bizArea: list = response.xpath("//li[@data-toggle-type='bizArea']/div//a/text()").extract()
            all_bizArea.remove("不限")
            for bizArea in all_bizArea:
                yield Request(
                    url=self.fill_bizArea_url.format(city=this_city_code, district=this_district, bizArea=bizArea),
                    meta={"bizArea": bizArea, "district": this_district, "city": this_city, "city_code": this_city_code,
                          "cookiejar": "lagou1"},
                    headers=self.header_dict,
                    callback=self.parse_bizArea,
                    dont_filter=True
                )
        else:
            # 直接抓取
            total_page_num = response.xpath("//span[@class='span totalNum']/text()").extract_first()
            if not total_page_num or total_page_num=="0":
                pass
            else:
                for pageNum in range(1, int(total_page_num) + 1):
                    yield Request(url=self.get_cookies_url, callback=self.parse_by_city, meta={"cookiejar": "lagou"},
                                  headers=self.header_dict, priority=4, dont_filter=True)
                    yield FormRequest(
                        url=self.origin_url + f"&city={quote(this_city)}&district={this_district}",
                        formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                        callback=self.parse,
                        meta={"cookiejar": "lagou"},
                        method="POST",
                        headers=self.header_dict,
                        priority=3,
                        dont_filter=True
                    )

    def parse_bizArea(self, response):
        this_city = response.meta['city']
        this_city_code = response.meta['city_code']
        this_district = response.meta['district']
        this_biz_area = response.meta['bizArea']
        total_page_num = response.xpath("//span[@class='span totalNum']/text()").extract_first()
        if not total_page_num:
            pass
        else:
            for pageNum in range(1, int(total_page_num) + 1):
                yield Request(url=self.get_cookies_url, callback=self.parse_by_city, meta={"cookiejar": "lagou"},
                              headers=self.header_dict, priority=4, dont_filter=True)
                yield FormRequest(
                    url=self.origin_url + f"&city={quote(this_city)}&district={this_district}&bizArea={this_biz_area}",
                    formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                    callback=self.parse,
                    meta={"cookiejar": "lagou"},
                    method="POST",
                    headers=self.header_dict,
                    priority=3,
                    dont_filter=True
                )

    def parse(self, response):
        """
        解析并填充item
        :param response:
        :return:
        """
        a = response
        yield a
