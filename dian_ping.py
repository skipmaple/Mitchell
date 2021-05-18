# -*- coding:utf-8 -*-
import re
import urllib.error

import numpy as np
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy.selector import Selector

from config import *
from parse import parse
from proxy import xdaili_proxy
from utils.RedisUtil import RedisUtil
from utils.common import *


class DianPing(object):
    def __init__(self):
        self.headers = HEADERS
        self.proxies = xdaili_proxy()
        self.cookie = COOKIES
        self.client = MongoClient(MONGO_CLIENT)
        self.db = self.client.dianping
        self.collection = self.db.labagou_origin_forest_park
        self.redis_util = RedisUtil()
        self.max_pages = None

    def get_store_list_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies,
                                    cookies=self.cookie)
            print(f"url: {url}")
            if response.status_code == 200:
                # 本地存储 响应数据
                with open(RES_PREFIX + 'origin.html', 'w', encoding='UTF-8') as f:
                    f.write(response.text)
                return response
        except urllib.error.HTTPError as e:
            print(e.reason)

    # """
    # with open('./tmp/2021-05-18origin.html') as f:
    #     html = f.read()
    #
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(html, "html.parser")
    # """


    def parse_data(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        # 移除所有'收起评价'
        for node in soup.find_all(class_="less-words"):
            node.decompose()

        for node in soup.find_all('svgmtsi'):
            try:
                key_name = node['class'][0]
                cache_value = list(map(int, self.redis_util.hget(CSS_CACHE_KEY, key_name).split(',')))
                x = cache_value[0]
                y = cache_value[1]
                target_field = self.redis_util.hget(SVG_CACHE_KEY, x)[y]
                node.replace_with(target_field)
            except Exception as e:
                print(e)
                pass

        res = Selector(text=soup.prettify())
        location = res.css('.shop-info.clearfix .shop-name::text').get().strip()
        try:
            li_list = res.xpath('//*[contains(@class, "reviews-items")]/ul/li')
            if li_list:
                index = 0
                for li in li_list:
                    index = index + 1
                    print(index)
                    data = parse(li)
                    data['location'] = location
                    print(data)
                    self.save_to_db(data)
                    # break
        except Exception as e:
            print('Error: %s, Please Check it.' % e.args)

    def save_to_db(self, data):
        self.collection.insert_one(data)

    def cache_css_data(self, css_body):
        css_content_dict = {}
        css_content_arr = re.findall('.(.*?){background:-(\d+).0px -(\d+).0px;}', css_body)
        # ex: css_content_arr = [('vgbzu', '294', '1246'), ('vg9gj', '14', '694'), ('vg4kc', '406', '2222'), ('vg72m', '294', '1892'), ('vge7r', '490', '1798'), ('zlsfz', '134', '15'), ('vgjno', '126', '849')]
        for css_content in css_content_arr:
            css_content_dict[css_content[0]] = f'{css_content[2]},{int(int(css_content[1]) / 14)}'
        # ex: css_content_dict = {'vgbzu': '1246,21', 'vg9gj': '694,1', 'vg4kc': '2222,29', 'vg72m': '1892,21', 'vge7r': '1798,35', 'zlsfz': '15,9', 'vgjno': '849,9'}
        self.redis_util.mapped_hmset(CSS_CACHE_KEY, css_content_dict)

    def cache_svg_data(self, svg_body):
        res = Selector(text=svg_body)
        line_dict = {}
        if res.css('path').__len__() == 0:
            # <text></text>
            # method1
            #
            # ex: line_dict = {2287: '蚂订谜周快葛停贺粗溉肾域前蕉拆镇欲坚残察讲勺枯疑驻锣概嘉鲜头底贝墙舞坛碑巾该右端某旋', 2331: '任希钩桐钥峰觉侍闪虎艳彩定离凑匪秒喊象就劝婶有津阿州及着稿艰伙寸系村奔部严龄垂挪危飞', 2362: '恰堪闹仓运妹溪傻题沈喉括期雀炸藏方争谋细倘狗仍骤蛛洽谅防葵狂应咏戴惜废恒罐背树九望丰', 2412: '皆宅监惧蹈鸣垒屠欧敬帖惠慰闷芒碌销值荣蝴谢'}
            str_array = re.findall('<text x="0" y="(\d+)">(.*?)</text>', svg_body)
            for str_tuple in str_array:
                line_dict[int(str_tuple[0]) - 23] = str_tuple[1]
        else:
            # <textPath></textPath>
            # method2
            #
            # ex: map_array = [('1', '45'), ('2', '90'), ('3', '135'), ('4', '184'), ('5', '226'), ('6', '274'), ('7', '311'), ('8', '347'), ('9', '378'), ('10', '419'), ('11', '459'), ('12', '493'), ('13', '539'), ('14', '573'), ('15', '606'), ('16', '637'), ('17', '669'), ('18', '704'), ('19', '746'), ('20', '791'), ('21', '822'), ('22', '861'), ('23', '905'), ('24', '951'), ('25', '999'), ('26', '1049'), ('27', '1084'), ('28', '1117'), ('29', '1152'), ('30', '1201'), ('31', '1249'), ('32', '1297'), ('33', '1347'), ('34', '1381'), ('35', '1429'), ('36', '1470'), ('37', '1518'), ('38', '1554'), ('39', '1591'), ('40', '1637'), ('41', '1674'), ('42', '1705'), ('43', '1740'), ('44', '1787'), ('45', '1820'), ('46', '1864'), ('47', '1901'), ('48', '1947'), ('49', '1996'), ('50', '2039'), ('51', '2087'), ('52', '2118'), ('53', '2156'), ('54', '2197'), ('55', '2228'), ('56', '2278'), ('57', '2315'), ('58', '2353'), ('59', '2390'), ('60', '2424'), ('61', '2464'), ('62', '2514'), ('63', '2557'), ('64', '2595'), ('65', '2638'), ('66', '2686'), ('67', '2732'), ('68', '2778'), ('69', '2826'), ('70', '2869'), ('71', '2907'), ('72', '2940'), ('73', '2984'), ('74', '3028'), ('75', '3074'), ('76', '3119'), ('77', '3164'), ('78', '3206'), ('79', '3254'), ('80', '3292')]
            map_array = re.findall('<path id="(\d+)" d="M0 (\d+) H600"/>', svg_body)  # 得到字体的y坐标
            map_dict = {}
            # ex: map_dict = {1: 22, 2: 67, 3: 112, 4: 161, 5: 203, 6: 251, 7: 288, 8: 324, 9: 355, 10: 396, 11: 436, 12: 470, 13: 516, 14: 550, 15: 583, 16: 614, 17: 646, 18: 681, 19: 723, 20: 768, 21: 799, 22: 838, 23: 882, 24: 928, 25: 976, 26: 1026, 27: 1061, 28: 1094, 29: 1129, 30: 1178, 31: 1226, 32: 1274, 33: 1324, 34: 1358, 35: 1406, 36: 1447, 37: 1495, 38: 1531, 39: 1568, 40: 1614, 41: 1651, 42: 1682, 43: 1717, 44: 1764, 45: 1797, 46: 1841, 47: 1878, 48: 1924, 49: 1973, 50: 2016, 51: 2064, 52: 2095, 53: 2133, 54: 2174, 55: 2205, 56: 2255, 57: 2292, 58: 2330, 59: 2367, 60: 2401, 61: 2441, 62: 2491, 63: 2534, 64: 2572, 65: 2615, 66: 2663, 67: 2709, 68: 2755, 69: 2803, 70: 2846, 71: 2884, 72: 2917, 73: 2961, 74: 3005, 75: 3051, 76: 3096, 77: 3141, 78: 3183, 79: 3231, 80: 3269}
            for k, v in map_array:
                map_dict[int(k)] = int(v) - 23
            # ex: font_map_array= [('1', '448', '油欺民房乙口痛礼蜜偶朴境量颤猛西纵号吓裁暗迈鼓族烫兰洋泰轨绕壁谅'), ('2', '490', '劈低唱庄惰语墨插扶粘辆笔怕妙伤势聪蔬泳遗刑极重签熄本寄浮丹很哑碑罪邪居'), ('3', '406', '净代投脊鞋世涛够尤格苹喂费敏畅汪瓣迟石实娱阔牌胞下兴令肠拣'), ('4', '504', '傲餐侍项寒任垄盆君株遮摆篮抽棍录稿叠文建视横冤拉得仔如树铜堤夺软深其疗摩'),..]
            str_map_array = re.findall('<textPath xlink:href="#(\d+)" textLength="(\d+)">(.*?)</textPath>', svg_body)
            for line_num, _, str in str_map_array:
                line_dict[map_dict[int(line_num)]] = str
            # ex: line_dict = {13: '督胶还瓶衫里宜才尖林摘贵苗窝品扰怪豆一宁械策膜注屋杂公蚕板巷商薯烧评泥晓混锈冒魄泽践', 14: '姻煌盘背迈慢扎昂常亩米葬染斥寿察诗唇香亮轰纲宅梦径俩揭候煎观文力剂叮靠洪厘峡姨煮悄萝, ..., 3231: '篇慕察善嗽红刃止震在沿金铸准混掏社现滴驼怖胜罚桑冰要符同嘉哥慈业侮贵黄袋支', 3269: '赖吵匙磨估早顺惊旋拨旗弓幕鼠羊话鹊竞稍缺尝顶仁湿绸斤判洞飞突铺通作'}

        self.redis_util.mapped_hmset(SVG_CACHE_KEY, line_dict)

    def load_css(self, response):
        res = Selector(text=response.text)

        css_url = 'http:' + res.xpath('/html/head/link[4]/@href').get()
        resp = requests.get(css_url, proxies=self.proxies)
        check_http_resp(css_url, resp)

        css_body = resp.text
        with open(RES_PREFIX + f'.css', 'w', encoding='UTF-8') as f:
            f.write(css_body)
        self.cache_css_data(css_body)
        self.load_svg(css_body)

    def load_svg(self, css_body):
        svg_url = 'http:' + re.findall('-14px;background-image: url\((.*?)\)', css_body)[0]
        resp = requests.get(svg_url, proxies=self.proxies)
        check_http_resp(svg_url, resp)
        with open(RES_PREFIX + f'.svg', 'w', encoding='UTF-8') as f:
            f.write(resp.text)
        self.cache_svg_data(resp.text)

    def main(self):
        for i in range(0, 10000):
            i = i + 1
            if self.max_pages is not None and i > self.max_pages:
                break
            url = INIT_URL.format(str(i))
            # 请求页面列表
            response = self.get_store_list_page(url)
            if response.url.find('verify') > -1:
                print("第 %d 页反爬验证！" % i)
                break

            if self.max_pages is None:
                res = Selector(text=response.text)
                self.max_pages = int(res.xpath('//div[@class="reviews-pages"]/a/text()')[-2].get())
                # self.max_pages = 119
                print("共 %d 页" % self.max_pages)

            print("第%d页：" % i)

            self.load_css(response)
            self.parse_data(response)
            time.sleep(np.random.randint(1, 3))
            # 测试仅抓取第一页
            # break


if __name__ == '__main__':
    dian_ping = DianPing()
    dian_ping.main()
