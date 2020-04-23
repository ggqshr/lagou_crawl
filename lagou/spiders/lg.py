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


def get_cookies_flag(*args):
    """
    用来生成统一的cookies标识的方法
    :param args:
    :return:
    """
    return "_".join([str(s) for s in args])


def get_page_job_number(response):
    """
    提取页面的工作数目
    :param response:
    :return:
    """
    return response.xpath("//a[@id='tab_pos']/span/text()").extract_first()


def append_key_word_to_url(url: str, args: dict) -> str:
    """
    在url后追加查询参数
    :param url:
    :param args:
    :return:
    """
    for k, v in quote_all_values_in_dict(args).items():
        url = url + f'&{k}={v}'
    return url


def quote_all_values_in_dict(args: dict) -> dict:
    """
    将字典的所有value使用quote函数进行编码
    :param args:
    :return:
    """
    return {k: quote(v) for k, v in args.items()}


class LgSpider(scrapy.Spider):
    handle_httpstatus_list = [301, 302]
    name = 'lg'
    allowed_domains = ['lagou.com', 'baidu.com']
    fill_city_url = "https://www.lagou.com/jobs/list_/p-city_{city}?px=default"
    fill_data_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'

    def start_requests(self):
        all_city = self.settings.get("CITY_INFO")
        for city, code in all_city.items():
            this_url = self.fill_city_url.format(city=code)
            self.logger.debug("process city %s url is %s" % (city, this_url))
            yield Request(
                url=this_url,
                meta={
                    'cookiejar': get_cookies_flag(city, code),
                    'referer_url': this_url,
                    'is_get_cookie_url': True,
                },
                cb_kwargs={
                    'area_args': {
                        'city': city,
                    },
                },
                priority=1,
                callback=self.parse_by_district,
                dont_filter=True,
            )

    def parse_by_district(self, response: Response, area_args):
        num = get_page_job_number(response)
        if num == '500+':
            all_district: list = response.xpath("//div[@data-type='district']//a/text()").extract()
            if len(all_district) == 0:
                all_district = response.xpath('//li[@data-toggle-type="district"]//a/text()').extract()
            if '不限' in all_district:
                all_district.remove("不限")
            for district in all_district:
                this_url = append_key_word_to_url(response.url, {'district': district})
                this_dict = dict(area_args)
                this_dict.update({'district': district})
                yield Request(
                    url=this_url,
                    meta={
                        'cookiejar': get_cookies_flag(response.meta.get('cookiejar'), district),
                        'referer_url': this_url,
                        'is_get_cookie_url': True,
                    },
                    cb_kwargs={'area_args': this_dict},
                    priority=2,
                    callback=self.parse_by_education,
                    dont_filter=True,
                )
        else:
            this_meta = dict(response.meta)  # 直接调用parse_first_level
            this_meta.update({'DONT_DOWNLOAD': True, 'origin_response': response, 'origin_request': response.request})
            yield Request(
                url="http://baidu.com",
                meta=this_meta,
                priority=3,
                cb_kwargs={'area_args': area_args},
                callback=self.parse_first_level,
            )

    def parse_by_education(self, response, area_args):
        num = get_page_job_number(response)
        if num == '500+':
            for edu in self.settings.get('EDUCATION_LEVEL'):
                this_url = append_key_word_to_url(response.url, {'xl': edu})  # 将参数拼接到url后
                this_dict = dict(area_args)
                this_dict.update({'xl': edu})  # 更新参数
                yield Request(
                    url=this_url,
                    meta={
                        'cookiejar': get_cookies_flag(response.meta.get('cookiejar'), edu),
                        'referer_url': this_url,
                        'is_get_cookie_url': True,
                    },
                    cb_kwargs={'area_args': this_dict},
                    priority=2,
                    callback=self.parse_first_level,
                    dont_filter=True,
                )
        else:
            this_meta = dict(response.meta)  # 直接调用parse_first_level
            this_meta.update({'DONT_DOWNLOAD': True, 'origin_response': response, 'origin_request': response.request})
            yield Request(
                url="http://baidu.com",
                meta=this_meta,
                priority=3,
                cb_kwargs={'area_args': area_args},
                callback=self.parse_first_level,
            )

    def parse_first_level(self, response: Response, area_args):
        re_req = self.process_re_request(response)
        if re_req is not None:
            yield re_req
            return

        this_req_url = append_key_word_to_url(self.fill_data_url, area_args)
        this_req_data = {
            "first": "true",
            "pn": str(1),
            'kd': "",
        }
        self.logger.debug(f'start to process {" ".join(area_args.values())}')
        yield FormRequest(
            url=this_req_url,
            meta={
                COOKIEJARSTR: response.meta.get(COOKIEJARSTR),
                'referer_url': response.meta.get('referer_url'),
                'is_get_data_url': True,
            },
            priority=5,
            formdata=this_req_data,
            cb_kwargs={'area_args': area_args, 'current_page': 1},
            callback=self.parse_second_level
        )

    def parse_second_level(self, response, area_args, current_page):
        re_req = self.process_re_request(response)
        if re_req is not None:
            yield re_req
            return
        this_req_url = response.url
        current_page += 1
        self.logger.debug(f'process {" ".join(area_args.values())} {current_page} pages')
        this_req_data = {
            "first": "false",
            "pn": str(current_page),
            'kd': "",
        }
        this_content = json.loads(response.text)
        this_position_data = this_content.get('content').get('positionResult')
        this_size = this_position_data.get('resultSize')
        if str(this_size) == '0':  # 如果当前页已经没有数据了，就停止请求下一页
            self.logger.debug(f'{" ".join(area_args.values())} {current_page} has null data, finish crawl')
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
            # yield Request(
            #     url=loader.get_output_value('link'),
            #     priority=7,
            #     headers={'Referer': response.meta.get('referer_url')},
            #     meta={'dont_merge_cookies': True, 'is_other_url': True},  # 不使用cookies
            #     cb_kwargs={'loader': loader},
            #     callback=self.parse_other,
            #     dont_filter=True,
            # )
            yield loader.load_item()
        yield FormRequest(
            url=this_req_url,
            formdata=this_req_data,
            headers={'Referer': response.meta.get('referer_url')},
            meta={
                COOKIEJARSTR: response.meta.get(COOKIEJARSTR),
                'referer_url': response.meta.get('referer_url'),
                'is_get_data_url': True,
            },
            cb_kwargs={'area_args': area_args, 'current_page': current_page},
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
