# -*- coding:utf-8 -*-
import sys
import time

from fake_useragent import UserAgent

# 五女山山城
# G9DtSzhWRl20oPXd

INIT_URL = 'http://www.dianping.com/shop/G9DtSzhWRl20oPXd/review_all/p{}?queryType=isPic&queryVal=true'

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

COOKIES = '_lxsdk_s=1798a329114-3d9-405-429%7C%7C67; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1621521318; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1621521240; s_ViewType=10; ctu=b78c9d73f1b6b57cab8dfd133095f2d2033523321a6168e151cc7d316b17ce4d; cy=60; cye=benxi; dper=a99c70e92a9bcc7fe065a6a657e7b2f24188626686f57fbf5680befbb42184bbe5286035a44848a9f6191138338b9c6df3e9b7d1b29d2fd8492e9318af1a6bf2dc495fe8fcefcefc2fa00f4dd3bc13796df67170bf68c91e0942b1fe1243df0c; dplet=0eea9ba2874a2025f2e7c5b766be0508; ll=7fd06e815b796be3df069dec7836c3df; ua=Hannah2021; _hc.v=150ac38f-055b-0f8e-fc5e-77abc50e9d6c.1621521240; _lxsdk=1798a329113c8-04d3fb9f0d2c6e8-3f62694b-13c680-1798a329113c8; _lxsdk_cuid=1798a329113c8-04d3fb9f0d2c6e8-3f62694b-13c680-1798a329113c8; fspop=test'
if len(COOKIES) > 0:
    COOKIES = {cookie.split('=')[0]: cookie.split('=')[1]
               for cookie in COOKIES.replace(' ', '').split(';')}

DEFAULT_NAME = 'Unnamed'

# redis cache key
CSS_CACHE_KEY = f"dian_ping-css_data-{time.strftime('%Y-%m-%d')}"
SVG_CACHE_KEY = f"dian_ping-svg_data-{time.strftime('%Y-%m-%d')}"

# MONGO_CLIENT = 'mongodb://root:123456@192.168.142.135:27017/admin?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
MONGO_CLIENT = 'mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb'

# MySQL Config
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PORT = 3306
MYSQL_PASSWORD = 'mysqlpwd'
MYSQL_DATABASE_NAME = 'Paul'

RES_PREFIX = sys.path[0] + '/tmp/' + time.strftime("%Y-%m-%d")
