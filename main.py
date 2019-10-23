from scrapy import cmdline
from lagou.settings import ip_pool
ip_pool.start()
cmdline.execute(['scrapy', 'crawl', 'lg'])