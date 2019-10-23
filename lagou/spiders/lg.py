# -*- coding: utf-8 -*-
import json
import uuid

import scrapy
from scrapy import Request, FormRequest
from scrapy.http import Response
from scrapy.http.cookies import CookieJar
from urllib.parse import quote

from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes, Compose

from lagou.items import LagouItemLoader, LagouItem


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['lagou.com']
    fill_city_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&gx=#filterBox"
    fill_district_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&gx=&district={district}#filterBox"
    fill_bizArea_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=new&district={district}&bizArea={bizArea}#filterBox"
    origin_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    get_cookies_url = "https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput="
    job_detail_url = "https://www.lagou.com/jobs/{id}.html"
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
                    meta={"city": city, "city_code": code, "cookiejar": code},
                    headers=self.header_dict,
                    callback=self.parse_by_district,
                    dont_filter=True
                )
        else:
            # 直接抓取
            for pageNum in range(1, 31):
                yield FormRequest(
                    url=self.origin_url,
                    formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                    callback=self.parse,
                    meta={"cookiejar": response.meta['cookiejar'], "page": pageNum},
                    method="POST",
                    headers=self.header_dict,
                    priority=4,
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
                    meta={"district": district, "city": this_city, "city_code": this_city_code, "cookiejar": district},
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
                    yield FormRequest(
                        url=self.origin_url + f"&city={quote(this_city)}",
                        formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                        callback=self.parse,
                        meta={"cookiejar": response.meta['cookiejar'], "page": pageNum},
                        method="POST",
                        headers=self.header_dict,
                        priority=4,
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
                          "cookiejar": bizArea},
                    headers=self.header_dict,
                    callback=self.parse_bizArea,
                    dont_filter=True
                )
        else:
            # 直接抓取
            total_page_num = response.xpath("//span[@class='span totalNum']/text()").extract_first()
            if not total_page_num or total_page_num == "0":
                pass
            else:
                for pageNum in range(1, int(total_page_num) + 1):
                    yield FormRequest(
                        url=self.origin_url + f"&city={quote(this_city)}&district={this_district}",
                        formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                        callback=self.parse,
                        meta={"cookiejar": response.meta['cookiejar'], "page": pageNum},
                        method="POST",
                        headers=self.header_dict,
                        priority=4,
                        dont_filter=True
                    )

    def parse_bizArea(self, response):
        """
        经过前面的过滤，按照城市，分区，以及商圈爬取
        :param response:
        :return:
        """
        this_city = response.meta['city']
        this_city_code = response.meta['city_code']
        this_district = response.meta['district']
        this_biz_area = response.meta['bizArea']
        total_page_num = response.xpath("//span[@class='span totalNum']/text()").extract_first()
        if not total_page_num:
            pass
        else:
            for pageNum in range(1, int(total_page_num) + 1):
                yield FormRequest(
                    url=self.origin_url + f"&city={quote(this_city)}&district={this_district}&bizArea={this_biz_area}",
                    formdata={"first": "true", "pn": str(pageNum), 'kd': ""},
                    callback=self.parse,
                    meta={"cookiejar": response.meta['cookiejar'], "page": pageNum},
                    method="POST",
                    headers=self.header_dict,
                    priority=4,
                    dont_filter=True
                )

    def parse(self, response: Response):
        """
        解析并填充item
        :param response:
        :return:
        """
        res_json = response.text
        extract_status = Compose(json.loads, SelectJmes("status"))
        status = extract_status(res_json)
        if status is None:
            # 成功的情况
            extract_result = Compose(json.loads, SelectJmes("content"), SelectJmes("positionResult"),
                                     SelectJmes("result"))
            result_list = extract_result(response.text)
            for res in result_list:
                loader = LagouItemLoader(item=LagouItem())
                loader.add_value("post_time", res)
                loader.add_value("job_name", res)
                loader.add_value("salary", res)
                loader.add_value("place", res)
                loader.add_value("job_nature", res)
                loader.add_value("experience", res)
                loader.add_value("education", res)
                loader.add_value("job_kind", res)
                loader.add_value("advantage", res)
                loader.add_value("company_name", res)
                loader.add_value("company_size", res)
                loader.add_value("company_industry", res)
                loader.add_value("id", res)
                loader.add_value("link", self.job_detail_url.format(id=loader.get_output_value("id")))
                this_item = loader.load_item()
                yield this_item
                # yield Request(
                #     url=this_item.get("link"),
                #     headers=self.header_dict,
                #     meta={"cookiejar": uuid.uuid4(), "item": this_item},
                #     callback=self.parse_other,
                #     priority=5,
                # )
        else:
            # 若请求失败，则重新请求一个主页，获得cookies，然后再次发起请求
            key = uuid.uuid4()
            yield Request(url=self.get_cookies_url, callback=self.empty, meta={"cookiejar": key},
                          headers=self.header_dict, priority=5, dont_filter=True)
            yield FormRequest(
                url=response.url,
                formdata={"first": "true", "pn": str(response.meta['page']), 'kd': ""},
                callback=self.parse,
                meta={"cookiejar": key, "page": response.meta['page']},
                method="POST",
                headers=self.header_dict,
                priority=4,
                dont_filter=True
            )

    def parse_other(self, response):
        """
        进入到工作对应的页面，爬取剩下的内容
        :param response:
        :return:
        """
        loader = LagouItemLoader(response=response, item=response.meta["item"])
        loader.add_xpath("job_content", "string(//div[@class='job-detail'])")
        loader.add_xpath("job_place", "string(//div[@class='work_addr'])")
        loader.add_xpath("company_homepage", "(//h4[@class='c_feature_name'])[4]/../@href")
        yield loader.load_item()

    def empty(self, response):
        pass
