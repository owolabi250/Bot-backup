#!/usr/bin/python3

storage_t = 'db'

if storage_t == 'db':
    from models.engine.DB_storage import DBstorage
    storage = DBstorage()
    storage.reload()
else:
    print("unknown db")

