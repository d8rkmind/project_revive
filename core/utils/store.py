from datetime import datetime

from sqlitedict import SqliteDict

from core.settings import Server
from core.utils.table import table_print


class Store:
    def write(option: dict, data: list):
        try:
            with SqliteDict(Server.storage, autocommit=True) as i:
                i[f'{option["plugin"]}&{option["target"]}&{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'] = data
        except Exception as e:
            print(e.with_traceback)

    def result():
        mydict = SqliteDict(Server.storage)
        table_print({
            'header': ['Si', 'Plugin', 'Target', 'Stored at'],
            'value': [[str(index + 1), *str(i).strip().split("&")] for index, i in
                      enumerate(mydict)]
        })

    def result_value(index: int):
        mydict = SqliteDict(Server.storage)
        try:
            results = mydict[list(mydict)[index - 1]]
            for result in results:
                if isinstance(result, dict):
                    table_print(result)
                else:
                    print(results)
        except IndexError:
            print("[-] There is no such element in the result")
