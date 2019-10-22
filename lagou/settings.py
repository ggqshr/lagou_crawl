# -*- coding: utf-8 -*-

# Scrapy settings for lagou project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lagou'

SPIDER_MODULES = ['lagou.spiders']
NEWSPIDER_MODULE = 'lagou.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'lagou (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBIG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'lagou.middlewares.LagouSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'lagou.middlewares.LagouDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'lagou.pipelines.LagouPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

CITY_INFO = {"河池": 246, "洋浦市": 251, "宜春": 145, "张家界": 205, "辽阳": 52, "濮阳": 175, "阿拉善盟": 42, "邵阳": 202, "黑河": 67,
             "安庆": 118, "白银": 318, "湘潭": 200, "沧州": 16, "梧州": 238, "安顺": 276, "淄博": 150, "杭州": 6, "赤峰": 34, "铁岭": 54,
             "海北藏族自治州": 331, "福州": 128, "天水": 319, "舟山": 106, "龙岩": 136, "迪庆藏族自治州": 296, "吴忠": 339, "果洛藏族自治州": 334,
             "乐山": 261, "通化": 74, "日照": 158, "和田": 348, "湘西土家族苗族自治州": 211, "韶关": 214, "宝鸡": 300, "河源": 227, "大庆": 62,
             "日喀则地区": 311, "泉州": 132, "连云港": 89, "邯郸": 11, "攀枝花": 254, "潮州": 232, "石嘴山": 338, "黄山": 119, "保山": 285,
             "南京": 79, "克孜勒苏柯尔克孜自治州": 355, "徐州": 86, "湖州": 102, "株洲": 199, "安康": 306, "柳州": 236, "绍兴": 103, "金昌": 317,
             "重庆": 5, "阿里地区": 313, "营口": 50, "玉溪": 284, "伊春": 63, "巴彦淖尔": 41, "宁德": 137, "葫芦岛": 56, "庆阳": 324, "辽源": 73,
             "兰州": 315, "遵义": 275, "自贡": 253, "常熟": 82, "乌鲁木齐": 342, "周口": 182, "咸阳": 301, "呼和浩特": 31, "拉萨": 308,
             "常德": 204, "洛阳": 169, "信阳": 181, "莆田": 130, "清远": 229, "张掖": 321, "北京": 2, "佛山": 218, "齐齐哈尔": 58,
             "宣城": 127, "嘉兴": 101, "秦皇岛": 10, "阿坝藏族羌族自治州": 270, "恩施土家族苗族自治州": 196, "汕尾": 226, "楚雄彝族自治州": 287, "思茅": 290,
             "台湾": 358, "眉山": 263, "抚州": 146, "德宏傣族景颇族自治州": 292, "阿克苏地区": 349, "景德镇": 138, "铜川": 299, "长春": 70,
             "泰安": 156, "鞍山": 45, "海西蒙古族藏族自治州": 336, "澳门": 357, "阳江": 228, "商洛": 307,  "鹤岗": 60, "乌海": 33,
             "上海": 3, "吉林": 71, "沈阳": 44, "上饶": 147, "益阳": 206, "曲靖": 283, "博尔塔拉蒙古自治州": 347, "吉安": 144, "永州": 208,
             "常州": 87, "广元": 258, "巴中": 268, "昌都地区": 309, "克拉玛依": 343, "朝阳": 55, "新乡": 173, "海东地区": 330, "延边朝鲜族自治州": 78,
             "巢湖": 123, "临汾": 28, "蚌埠": 113, "南充": 262, "昆明": 282, "包头": 32, "临沂": 160, "渭南": 302, "赣州": 143, "聊城": 162,
             "巴音郭楞蒙古自治州": 353, "鹤壁": 172, "牡丹江": 66, "肇庆": 223, "泉港区": 133, "中卫": 341, "温州": 99, "山南地区": 310, "榆林": 305,
             "嘉峪关": 316, "绥化": 68, "成都": 252, "广安": 265, "太仓": 97, "泰州": 94, "阳泉": 21, "淮北": 116, "海宁": 100, "长沙": 198,
             "鹰潭": 142, "毕节地区": 279, "晋城": 23, "盐城": 91, "通辽": 35, "本溪": 47, "四平": 72, "惠州": 224, "铜仁地区": 277,
             "云浮": 234, "三门峡": 178, "来宾": 247, "焦作": 174, "玉环县": 109, "临沧": 297, "烟台": 153, "扬州": 92, "白城": 77,
             "苏州": 80, "塔城地区": 352, "南宁": 235, "十堰": 186, "吕梁": 29, "阜新": 51, "漳州": 134, "厦门": 129, "汉中": 304, "丹东": 48,
             "开封": 168, "铜陵": 117, "东莞": 230, "石家庄": 8, "德州": 161, "佳木斯": 64, "鄂州": 189, "黔南布依族苗族自治州": 281, "长治": 22,
             "永济市": 30, "昌吉回族自治州": 346, "承德": 15, "天津": 4, "娄底": 210, "莱芜": 159, "平顶山": 170, "荣成": 166, "怀化": 209,
             "甘南藏族自治州": 328, "菏泽": 164, "玉林": 243, "阿勒泰地区": 350, "淮南": 114, "昆山": 81, "七台河": 65, "张家港": 83, "芜湖": 112,
             "抚顺": 46, "三明": 131, "定西": 325, "滁州": 120, "驻马店": 183, "广州": 213, "临夏回族自治州": 327, "章丘": 165, "郑州": 167,
             "随州": 195, "伊犁哈萨克自治州": 354, "盘锦": 53, "海口": 249, "许昌": 176, "朔州": 24, "忻州": 27, "荆州": 192, "大兴安岭地区": 69,
             "北海": 239, "无锡": 84, "枣庄": 151, "晋中": 25, "德阳": 256, "哈尔滨": 57, "淮安": 90, "武威": 320, "保定": 13, "襄樊": 188,
             "黄冈": 193, "延安": 303, "大理白族自治州": 293, "喀什地区": 351, "茂名": 222, "锡林郭勒盟": 39, "江门": 220, "哈密地区": 345,
             "漯河": 177, "孝感": 191, "湛江": 221, "锦州": 49, "唐山": 9, "鸡西": 59, "遂宁": 259, "深圳": 215, "内江": 260,
             "红河哈尼族彝族自治州": 288, "荆门": 190, "汕头": 217, "池州": 126, "雅安": 267, "郴州": 207, "黔东南苗族侗族自治州": 280, "乌兰察布": 40,
             "南海区": 219, "林芝地区": 314, "张家口": 14, "方家山": 110, "襄阳": 197, "资阳": 269, "东营": 152, "昭通": 286, "亳州": 125,
             "海南藏族自治州": 333, "阜阳": 121, "宁波": 98, "贵港": 242, "金华": 104, "文山壮族苗族自治州": 289, "贵阳": 273, "潍坊": 154,
             "西双版纳傣族自治州": 291, "凉山彝族自治州": 272, "合肥": 111, "黔西南布依族苗族自治州": 278, "商丘": 180, "桂林": 237, "珠海": 216, "白山": 75,
             "青岛": 149, "大连": 43, "吐鲁番地区": 344, "威海": 157, "丽水": 108, "南昌": 7, "邢台": 12, "怒江傈僳族自治州": 295, "新余": 141,
             "酒泉": 323, "香港": 356, "马鞍山": 115, "南通": 88, "宜宾": 264, "九江": 140, "衢州": 105, "武汉": 184, "崇左": 248, "海晏": 1,
             "那曲地区": 312, "银川": 337, "六安": 124, "南阳": 179, "江阴": 85, "三亚": 250, "百色": 244, "黄南藏族自治州": 332, "黄石": 185,
             "平凉": 322, "太原": 19, "安阳": 171, "咸宁": 194, "济南": 148, "甘孜藏族自治州": 271, "六盘水": 274, "廊坊": 17, "丽江": 294,
             "玉树藏族自治州": 335, "大同": 20, "绵阳": 257, "兴安盟": 38, "靖江": 95, "陇南": 326, "衡水": 18, "呼伦贝尔": 37, "衡阳": 201,
             "台州": 107, "萍乡": 139, "鄂尔多斯": 36, "宿迁": 96, "镇江": 93, "揭阳": 233, "钦州": 241, "岳阳": 203, "泸州": 255, "松原": 76,
             "中山": 231, "防城港": 240, "运城": 26, "固原": 340, "达州": 266, "西宁": 329, "宿州": 122, "梅州": 225, "贺州": 245,
             "南平": 135, "新加坡": 359, "滨州": 163, "宜昌": 187, "西安": 298, "双鸭山": 61, "济宁": 155, "石河子": 212};