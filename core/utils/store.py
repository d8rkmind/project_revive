from sqlitedict import SqliteDict
from core.settings import Server
from datetime import datetime


class Store:
    def write(option: dict, data):
        try:
            with SqliteDict(Server.storage, autocommit=True) as i:
                i[f'{option["plugin"]}&{option["target"]}&{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'] = data
        except Exception as e:
            print(e.with_traceback)
