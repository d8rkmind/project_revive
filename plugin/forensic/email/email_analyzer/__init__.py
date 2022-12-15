import re
import quopri
from core.utils.store import Store
import hashlib
from zipfile import ZipFile
from io import BytesIO
from email.parser import HeaderParser
from email import policy, message_from_file

# from core.utils.table import table_print

store = []


def attachements(filename: str):
    table = {
        'header': ['Attachment names', "Hash mode", "Hash value"],
        'value': []
    }
    with open(filename, "r") as f:
        msg = message_from_file(f, policy=policy.default)
    if msg.iter_attachments():
        archive = BytesIO()
        with ZipFile(archive, 'w') as zip_archive:
            for attachment in msg.iter_attachments():
                out_file = attachment.get_filename()
                payload = attachment.get_payload(decode=True)
                with zip_archive.open(out_file, 'w') as f:
                    f.write(payload)
                table['value'] += [[out_file, k, v] for k, v in {
                    "MD5": hashlib.md5(payload).hexdigest(),
                    "SHA1": hashlib.sha1(payload).hexdigest(),
                    "SHA256": hashlib.sha256(payload).hexdigest(),
                }.items()]

        with open(f'{filename.split("/")[-1]}_attachements.zip', 'wb') as f:
            f.write(archive.getbuffer())
        archive.close()
        print(
            f'[+] a file named {filename.split("/")[-1]}_attachements.zip is created with all the \
attachements')
    store.append(table)


def links(data: str):
    if "Content-Transfer-Encoding" in data:
        data = str(quopri.decodestring(data))
    links = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    links = set(links)
    if links:
        store.append({
            'header': ['Links collected from eml file'],
            'value': [[i] for i in links]
        })


def header(data: str):
    header = HeaderParser().parsestr(data, headersonly=True)
    store.append({
        'header': ['Headers', 'Value'],
        'value': [[str(k), str(v)] for k, v in header.items()]
    })


def run(options: dict):
    try:
        filename = options['target']
        if not str(filename).endswith('.eml'):
            print("[-] '.eml' file is required")
            return
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()

        header(data)
        links(data)
        store.append({
            'header': ['Hashes', 'Content Hash Value'],
            'value': [
                ["MD5", hashlib.md5(data.encode("utf-8")).hexdigest()],
                ["SHA1", hashlib.sha1(data.encode("utf-8")).hexdigest()],
                ["SHA256", hashlib.sha256(
                    data.encode("utf-8")).hexdigest()],
            ]
        })
        attachements(filename)
        Store.write(options, store)
    except FileNotFoundError:
        print("[-] the target file is not found")
