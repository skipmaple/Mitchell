import sqlobject

from utils.mysql_util import conn


class DianPings(sqlobject.SQLObject):
    _connection = conn
    username = sqlobject.StringCol(unique=True, length=255)
    comment = sqlobject.StringCol()
    images = sqlobject.JSONCol()
    origin_images_urls = sqlobject.JSONCol()
    rank_level = sqlobject.IntCol()
    location = sqlobject.StringCol()
    comment_at = sqlobject.DateTimeCol(default=None)
    created_at = sqlobject.DateTimeCol(default=None)
    updated_at = sqlobject.DateTimeCol(default=None)


DianPings.createTable(ifNotExists=True)

if __name__ == '__main__':
    pass
