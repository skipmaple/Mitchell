# -*- coding:utf-8 -*-
import re
from datetime import datetime

from bs4 import BeautifulSoup

from config import *


def parse(li):
    """
    解析一条数据
    """
    data = dict()
    # 评论者昵称
    data['username'] = li.css('.main-review .dper-info > a::text').extract_first(DEFAULT_NAME).strip()
    # print(f"username: {data['user_name']}")

    # 评论星级
    rank_span_str = li.css('.main-review .review-rank .sml-rank-stars').get()
    rank_span = BeautifulSoup(rank_span_str, features="lxml")
    rank_class_attr = rank_span.find('span')['class'][1]
    if ('50' in rank_class_attr) or ('40' in rank_class_attr):
        # 好评
        rank_level = 1
    elif '30' in rank_class_attr:
        # 中评
        rank_level = 2
    elif ('20' in rank_class_attr) or ('10' in rank_class_attr):
        # 差评
        rank_level = 3
    else:
        # NOT FOUND
        rank_level = 404
    data['rank_level'] = rank_level
    # print(f"rank_level: {data['rank_level']}")

    # 评论时间
    create_at_str = li.css('.main-review .misc-info.clearfix .time::text').get().strip()
    create_at_match = re.search('(\d+)-(\d+)-(\d+) (\d+):(\d+)', create_at_str)
    if create_at_match:
        datetime_object = datetime.strptime(create_at_match[0], '%Y-%m-%d %H:%M')
        # data['created_at'] = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_at'] = datetime_object
    else:
        data['comment_at'] = None
    # print(f"created_at: {data['created_at']}")

    # 评论内容
    comment_content = li.css('.main-review .review-words.Hide')
    if not comment_content:
        comment_content = li.css('.main-review .review-words')

    comment_content = comment_content.xpath('string()').get().strip()
    comment_content = re.sub("\n", " ", comment_content)
    comment_content = re.sub("\s+", "", comment_content)
    data['comment'] = comment_content
    # print(f"content: {data['comment_content']}")

    # 评论图片
    data['origin_images_urls'] = li.css('.main-review .review-pictures > ul > li > a > img::attr(data-big)').getall()

    return data


if __name__ == '__main__':
    pass
