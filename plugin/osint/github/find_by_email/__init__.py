
from core.utils.query import Query
from core.utils.store import Store
from plugin.osint.github.find_by_username import run as run2
import re


def run(option: dict):
    q = Query()
    email = str(option["target"])
    response = q.get(f'https://api.github.com/search/users?q={email}', isText=True)
    username = re.findall(r'"login":"(.*?)"', response[0])
    if not username:
        print("[-] No username found")
        return

    if len(username) > 1:
        Store.write(option, username)
    else:
        option['target'] = username[0]
        run2(option)
