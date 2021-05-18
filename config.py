# -*- coding:utf-8 -*-
import sys
import time

from fake_useragent import UserAgent

INIT_URL = 'http://www.dianping.com/shop/k2CMKR7TLqey6YZX/review_all/p{}?queryType=isPic&queryVal=true'

ua = UserAgent()

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/beijing/',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': ua.random,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36 '
    # "Proxy-Tunnel": str(random.randint(1,10000))  # 使用代理时需设置
}

COOKIES = ''
COOKIES = {cookie.split('=')[0]: cookie.split('=')[1]
           for cookie in COOKIES.replace(' ', '').split(';')}

DEFAULT_NAME = 'Unnamed'

# redis cache key
CSS_CACHE_KEY = f"dian_ping-css_data-{time.strftime('%Y-%m-%d')}"
SVG_CACHE_KEY = f"dian_ping-svg_data-{time.strftime('%Y-%m-%d')}"

# MONGO_CLIENT = 'mongodb://root:123456@192.168.142.135:27017/admin?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
MONGO_CLIENT = 'mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb'

RES_PREFIX = sys.path[0] + '/tmp/' + time.strftime("%Y-%m-%d")

