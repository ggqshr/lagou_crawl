# -*- coding: utf-8 -*-
import json
import uuid
from typing import Union

import scrapy
from scrapy import Request, FormRequest, Selector
from scrapy.http import Response
from scrapy.http.cookies import CookieJar
from urllib.parse import quote

from lagou.items import LagouItemLoader, LagouItem
from scrapy.loader.processors import SelectJmes, Compose, MapCompose

COOKIEJARSTR = 'cookiejar'
COOKIEFLAG = "{flag}_{number}"


class LgSpider(scrapy.Spider):
    handle_httpstatus_list = [301, 302]
    name = 'lg'
    allowed_domains = ['lagou.com']
    fill_city_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=default"
    fill_data_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={city}&needAddtionalResult=false'

    def start_requests(self):
        all_city = self.settings.get("CITY_INFO")
        for city, code in all_city.items():
            this_url = self.fill_city_url.format(city=code)
            self.logger.debug("process city %s url is %s" % (city, this_url))
            yield Request(
                url=this_url,
                meta={
                    'cookiejar': COOKIEFLAG.format(flag=city, number=code),
                    'referer_url': this_url,
                    'is_get_cookie_url': True,
                },
                cb_kwargs={'city': city},
                priority=1,
                callback=self.parse_first_level,
                dont_filter=True,
            )

    def parse_first_level(self, response: Response, city):
        re_req = self.process_re_request(response)
        if re_req is not None:
            yield re_req
            return
        this_req_url = self.fill_data_url.format(city=quote(city))
        this_req_data = {
            "first": "true",
            "pn": str(1),
            'kd': "",
        }
        yield FormRequest(
            url=this_req_url,
            meta={
                COOKIEJARSTR: response.meta.get(COOKIEJARSTR),
                'referer_url': response.meta.get('referer_url'),
                'is_get_data_url': True,
            },
            priority=5,
            formdata=this_req_data,
            cb_kwargs={'city': city, 'current_page': 1},
            callback=self.parse_second_level
        )

    def parse_second_level(self, response, city, current_page):
        re_req = self.process_re_request(response)
        if re_req is not None:
            yield re_req
            return
        this_req_url = response.url
        current_page += 1
        self.logger.debug(f'process {city} {current_page} pages')
        this_req_data = {
            "first": "false",
            "pn": str(current_page),
            'kd': "",
        }
        this_content = json.loads(response.text)
        this_position_data = this_content.get('content').get('positionResult')
        this_size = this_position_data.get('resultSize')
        if str(this_size) == '0':  # 如果当前页已经没有数据了，就停止请求下一页
            self.logger.debug(f'{city} {current_page} has null data, finish crawl')
            return
        this_result: list = this_position_data.get('result')
        for position_info in this_result:
            loader = LagouItemLoader(item=LagouItem())
            loader.add_value('link', position_info)
            loader.add_value('id', position_info)
            loader.add_value('post_time', position_info)
            loader.add_value('job_name', position_info)
            loader.add_value('salary', position_info)
            loader.add_value('place', position_info)
            loader.add_value('job_nature', position_info)
            loader.add_value('experience', position_info)
            loader.add_value('education', position_info)
            loader.add_value('job_kind', position_info)
            loader.add_value('advantage', position_info)
            loader.add_value('company_name', position_info)
            loader.add_value('company_size', position_info)
            loader.add_value('company_industry', position_info)
            yield Request(
                url=loader.get_output_value('link'),
                priority=7,
                headers={'Referer': response.meta.get('referer_url')},
                meta={'dont_merge_cookies': True, 'is_other_url': True},  # 不使用cookies
                cb_kwargs={'loader': loader},
                callback=self.parse_other,
                dont_filter=True,
            )
            # yield loader.load_item()
        yield FormRequest(
            url=this_req_url,
            formdata=this_req_data,
            headers={'Referer': response.meta.get('referer_url')},
            meta={
                COOKIEJARSTR: response.meta.get(COOKIEJARSTR),
                'referer_url': response.meta.get('referer_url'),
                'is_get_data_url': True,
            },
            cb_kwargs={'city': city, 'current_page': current_page},
            priority=6,
            callback=self.parse_second_level,
        )

    def parse_other(self, response, loader: LagouItemLoader):
        loader.selector = Selector(response)
        loader.add_xpath('job_content', 'string(//div[@class="job-detail"])')
        loader.add_xpath('job_place', 'string(//div[@class="work_addr"])')
        yield loader.load_item()

    def process_re_request(self, response) -> Union[Request, None]:
        re_request = response.meta.pop("re_request_url", None)
        if re_request is not None:
            self.logger.debug(f"re-request url {re_request} because of cookies out of date")
            return re_request
        return
