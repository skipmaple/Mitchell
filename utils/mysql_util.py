# -*- coding: utf-8 -*-

from sqlobject.mysql import builder

from config import *

conn = builder()(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, db=MYSQL_DATABASE_NAME, port=MYSQL_PORT, driver='pymysql')
