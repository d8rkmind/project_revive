from core.utils.request import request
from core.utils.store import Store
from plugin.osint.github.find_by_username import run as run2
import re


def run(option: dict):
    email = str(option["target"])
    response = request(
        [f'https://api.github.com/search/users?q={email}'], is_text=True)
    username = re.findall(r'"login":"(.*?)"', response[0])
    if not username:
        print("[-] No username found")
        return

    if len(username) > 1:
        Store.write(option, username)
    else:
        option['target'] = username[0]
        run2(option)
