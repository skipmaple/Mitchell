# -*- coding: utf-8 -*-
from datetime import timedelta

import redis


class RedisUtil:

    def __init__(self, redis_host='127.0.0.1', redis_port=6379, redis_pass=None):
        """
        redis 默认链接本机
        :param redis_host: redis 链接地址
        :param redis_port: redis 端口号
        :param redis_pass: redis 密码
        """
        if redis_pass:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def hset(self, big_key, key, value):
        res = self.r.hset(big_key, key, value)
        self.r.expire(big_key, timedelta(days=1))
        return res

    def hget(self, big_key, key):
        return self.r.hget(big_key, key)

    def hexist(self, big_key, key):
        return self.r.hexists(big_key, key)

    def mapped_hmset(self, big_key, dict_data):
        """新增mapped_hash
        ex: hash_data = { a:1, b:2, c:3 }
        """
        res = self.r.hmset(big_key, dict_data)
        self.r.expire(big_key, timedelta(days=1))
        return res
