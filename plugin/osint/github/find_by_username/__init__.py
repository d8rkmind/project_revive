import re

from core.utils.query import Query
from core.utils.store import Store

__option__ = {}


def run(option: dict):
    q = Query()
    username = str(option["target"])
    data = q.get(f'https://api.github.com/users/{username}')
    table1 = {
        'header': ['Options', 'Value'],
        'value': []
    }

    if 'message' in data:  # user is wrong
        return
    for i in data:
        if i in ['login', 'id', 'avatar_url', 'name', 'blog', 'location', 'twitter_username',
                 'company', 'bio', 'public_gists', 'public_repos', 'followers', 'following',
                 'created_at', 'updated_at']:
            table1['value'].append([i.strip(), str(data[i])])
    response = q.get(f'https://api.github.com/users/{username}/repos?per_page=100&sort=pushed',
                     isText=True)
    repos = re.findall(
        r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)

    table2 = {
        'header': ['Public Repos', 'Forked'],
        'value': repos
    }

    response = q.get([
        f'https://github.com/{username}/{i[0]}/commits?author={username}' for i in repos if i[1] ==
        'false'], isText=True)
    commits = []
    for i in response:
        c = re.search(r'href="/%s/(.*?)/commit/(.*?)"' % username, i)
        commits.append([c.group(1), c.group(2)])

    response = q.get([
        f'https://github.com/{username}/{i[0]}/commit/{i[1]}.patch' for i in commits
    ], isText=True)
    emails = []
    for i in response:
        e = re.search(r'<(.*)>', i)
        emails.append(e.group(1))
    table3 = {
        'header': ['Emails collected from repositories'],
        'value': [[i] for i in set(emails)]
    }

    data = [table1, table2, table3]
    Store.write(option, data)
