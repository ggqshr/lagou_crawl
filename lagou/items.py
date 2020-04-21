# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes, Compose, MapCompose, TakeFirst
import json


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


link_format_url = "https://www.lagou.com/jobs/{}.html"


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field(
        input_processor=MapCompose(SelectJmes('positionId'), lambda x: link_format_url.format(x))
    )  # url
    id = scrapy.Field(
        input_processor=Compose(TakeFirst(), SelectJmes('positionId')),
    )  # rloc
    post_time = scrapy.Field(
        input_processor=MapCompose(SelectJmes("createTime"), lambda x: x.split(" ")[0])
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
        input_processor=Compose(TakeFirst(), SelectJmes("positionAdvantage")),
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
    company_address = scrapy.Field()  # companyaddress
    company_nature = scrapy.Field()  # employertype
    job_content = scrapy.Field()
    job_place = scrapy.Field()
    # company_homepage = scrapy.Field()  # official
