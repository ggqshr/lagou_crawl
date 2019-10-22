# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes, Compose, MapCompose
import json


class LagouItemLoader(ItemLoader):
    pass


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()  # url
    id = scrapy.Field()  # rloc
    post_time = scrapy.Field(
        input_processor=SelectJmes("createTime"),
    )  # lastmod
    job_name = scrapy.Field(
        input_processor=SelectJmes("positionName"),
    )  # title
    salary = scrapy.Field(
        input_processor=SelectJmes("salary"),
    )  # salary
    place = scrapy.Field(
        input_processor=SelectJmes("city"),
    )  # city
    job_nature = scrapy.Field(
        input_processor=SelectJmes("jobNature"),
    )  # type
    experience = scrapy.Field(
        input_processor=SelectJmes("workYear"),
    )  # experience
    education = scrapy.Field(
        input_processor=SelectJmes("education"),
    )  # education
    # job_number = scrapy.Field()  # number
    job_kind = scrapy.Field(
        input_processor=SelectJmes("firstType"),
    )  # jobsecondclass
    advantage = scrapy.Field(
        input_processor=SelectJmes("positionAdvantage"),
    )  # ori_welfare
    company_name = scrapy.Field(
        input_processor=SelectJmes("companyFullName"),
    )  # officialname
    company_size = scrapy.Field(
        input_processor=SelectJmes("companySize"),
    )  # size
    company_industry = scrapy.Field(
        input_processor=SelectJmes("industryField"),
    )  # industry
    company_address = scrapy.Field()  # companyaddress
    company_nature = scrapy.Field()  # employertype
    job_content = scrapy.Field()
    job_place = scrapy.Field()
    # company_homepage = scrapy.Field()  # official
    hot_score = scrapy.Field()  # 百度对于本条招聘信息的热度评分  hot_score
    job_safety_score = scrapy.Field()  # 百度对于招聘信息的安全评分  job_safety_score
    company_reputation_score = scrapy.Field()  # 百度对于招聘公司的声誉评分 company_reputation_score
    salary_level_score = scrapy.Field()  # 对于薪水评分  salary_level_score
