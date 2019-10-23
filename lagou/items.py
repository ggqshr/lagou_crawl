# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes, Compose, MapCompose, Identity, TakeFirst
import json

regSpace = re.compile(r'([\s\r\n\t])+')


def replace_all_n(text):
    # 以防止提取不到
    try:
        if type(text) == str:
            rel = re.sub(regSpace, "", text)
            return rel
        elif type(text) == list:
            return "".join([re.sub(regSpace, "", t) for t in text])
    except TypeError as e:
        return "空"


def process_job_place(text):
    """
    将工作地点中的查看地图去掉
    :param text:
    :return:
    """
    if text:
        return text.replace("查看地图", "")


def process_post_time(text):
    """
    按照空格分割发布时间，只保留日期
    :param text:
    :return:
    """
    if text:
        return text.split(" ")[0]


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = Identity()


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()  # url
    id = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("positionId")),
        output_processor=TakeFirst(),
    )  # rloc
    post_time = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("createTime"), process_post_time),
    )  # lastmod
    job_name = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("positionName")),
    )  # title
    salary = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("salary")),
    )  # salary
    place = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("city")),
    )  # city
    job_nature = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("jobNature")),
    )  # type
    experience = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("workYear")),
    )  # experience
    education = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("education")),
    )  # education
    # job_number = scrapy.Field()  # number
    job_kind = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("firstType")),
    )  # jobsecondclass
    advantage = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("positionAdvantage"), replace_all_n),
    )  # ori_welfare
    company_name = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("companyFullName")),
    )  # officialname
    company_size = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("companySize")),
    )  # size
    company_industry = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes("industryField")),
    )  # industry
    job_content = scrapy.Field(
        input_processor=Compose(TakeFirst(), replace_all_n),
    )
    job_place = scrapy.Field(
        input_processor=Compose(TakeFirst(), replace_all_n, process_job_place),
    )
    company_homepage = scrapy.Field(
        input_processor=Compose(TakeFirst(), replace_all_n),
    )  # official
    # company_address = scrapy.Field()  # companyaddress
    # company_nature = scrapy.Field()  # employertype
