#!/usr/bin/python3
import os

storage = None
redis_storage = None

storage_type = os.environ.get('STORAGE_TYPE')
storage_type2 = os.environ.get('STORAGE_TYPE2')

if storage_type == 'mysqlDB':
    from models.engine.DB_storage import DBstorage
    storage = DBstorage()
    storage.reload()
if storage_type2 == 'redisDB':
    from models.engine.RedisDB_storage import Cache
    redis_storage = Cache()
else:
    raise Exception("Invalid storage engine")
