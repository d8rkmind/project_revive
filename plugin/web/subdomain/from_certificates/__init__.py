import re
from core.utils.query import Query
from core.settings import Api
from core.utils.store import Store


q = Query()
subdomains = set()


def censys(domain: str):
    data = {
        'query': f'parsed.names: {domain}',
        'page': 1,
        'fields': ['parsed.subject_dn', 'parsed.names'],
        'flatten': True}
    res = q.post('https://search.censys.io/api/v1/search/certificates', isText=True,
                 json=data, auth=(Api.censys_api_id, Api.censys_api_secret))
    subdomain = re.findall(
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+" + domain, res)
    subdomains.update(set(subdomain))


def certsporter(domain: str):
    params = {'domain': domain,
              'include_subdomains': 'true',
              'expand': 'dns_names'}
    res = q.get('https://api.certspotter.com/v1/issuances',
                isText=True, params=params)
    subdomain = re.findall(
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+" + domain, res)
    subdomains.update(set(subdomain))


def crtsh(domain: str):
    params = {'q': f'%.{domain}', 'output': 'json'}
    res = q.get('https://crt.sh/',
                isText=True, params=params)
    subdomain = re.findall(
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+" + domain, res)
    subdomains.update(set(subdomain))


def run(options: dict):
    url = options['target']
    censys(url)
    certsporter(url)
    crtsh(url)
    table: dict = {
        'header': ["Subdomains"],
        'value': [[i] for i in subdomains]
    }
    Store.write(options, [table])
